"""Train the shared PPO policy on randomized demand."""

import argparse
import json
import platform
import random
import sys
from datetime import datetime
from importlib.metadata import version
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "training.json"
CONTROLLER_CONFIG_PATH = PROJECT_ROOT / "configs" / "controller.json"

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

import torch  # noqa: E402

from src.demand import sample_training_scenario, write_routes, write_sumocfg  # noqa: E402
from src.observations import OBSERVATION_SIZE  # noqa: E402
from src.policy import ActorCritic, collect_episode, ppo_update, save_checkpoint  # noqa: E402
from src.rl_environment import TrafficSignalEnv  # noqa: E402


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Train the shared PPO traffic-signal policy.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=(
            "Training settings JSON. A relative path resolves from the current "
            "directory. Default: configs/training.json in the project root."
        ),
    )
    parser.add_argument(
        "--updates",
        type=int,
        help="Override the number of PPO updates, e.g. for a short trial run.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Folder for checkpoints and logs. Default: models/ppo_<run id> in the project root.",
    )

    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_networks(training: dict) -> list[dict]:
    """Load each training network's intersection mapping and route settings."""

    networks = []

    for entry in training["networks"]:
        scenarios = load_json(PROJECT_ROOT / entry["scenarios"])
        networks.append(
            {
                "name": entry["name"],
                "intersections": load_json(PROJECT_ROOT / entry["intersections"]),
                "scenarios": scenarios,
                "network_path": PROJECT_ROOT / scenarios["network_file"],
            }
        )

    return networks


def main() -> None:
    """Collect episodes, update the shared policy, and save checkpoints."""

    arguments = parse_arguments()
    config_path = arguments.config.resolve()
    training = load_json(config_path)
    controller = load_json(CONTROLLER_CONFIG_PATH)
    updates = arguments.updates or training["updates"]
    networks = load_networks(training)
    ppo = training["ppo"]

    action_counts = {
        len(node["actions"])
        for network in networks
        for node in network["intersections"]["intersections"].values()
    }

    if len(action_counts) != 1:
        raise ValueError("Every intersection must offer the same number of actions.")

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = (
        arguments.output_dir.resolve()
        if arguments.output_dir
        else PROJECT_ROOT / "models" / f"ppo_{run_id}"
    )
    # The current episode's route and scenario files are rewritten here.
    episode_dir = output_dir / "episode"
    episode_dir.mkdir(parents=True, exist_ok=True)

    seed = training["seed"]
    rng = random.Random(seed)
    torch.manual_seed(seed)
    generator = torch.Generator().manual_seed(seed)

    model = ActorCritic(OBSERVATION_SIZE, action_counts.pop(), ppo["hidden_size"])
    optimizer = torch.optim.Adam(model.parameters(), lr=ppo["learning_rate"])
    env = TrafficSignalEnv(controller, training["reward"], quiet=True)

    metadata = {
        "run_id": run_id,
        "seed": seed,
        "observation_size": OBSERVATION_SIZE,
        "action_count": model.actor[-1].out_features,
        "hidden_size": ppo["hidden_size"],
        "training_config": training,
        "controller_config": controller,
        "networks": {network["name"]: network["intersections"] for network in networks},
        "versions": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "sumo": version("eclipse-sumo"),
        },
    }
    (output_dir / "run_config.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Using config: {config_path}", flush=True)
    print(f"Output: {output_dir}", flush=True)
    print(
        f"{updates} updates x {training['episodes_per_update']} episodes, "
        f"networks: {', '.join(network['name'] for network in networks)}",
        flush=True,
    )

    try:
        with (output_dir / "training_log.jsonl").open("a", encoding="utf-8") as log:
            for update in range(1, updates + 1):
                pooled = {key: [] for key in ("observations", "actions", "log_probs", "values", "advantages", "returns")}
                episodes = []

                for _ in range(training["episodes_per_update"]):
                    network = rng.choice(networks)
                    scenario = sample_training_scenario(
                        rng, training["demand"], network["scenarios"]["route_groups"]
                    )
                    routes_path = episode_dir / "episode.rou.xml"
                    sumocfg_path = episode_dir / "episode.sumocfg"
                    write_routes(routes_path, network["scenarios"], scenario)
                    write_sumocfg(
                        sumocfg_path,
                        network["network_path"],
                        routes_path,
                        scenario,
                        network["scenarios"]["step_length_s"],
                    )

                    transitions, stats = collect_episode(
                        env, model, sumocfg_path, network["intersections"], ppo
                    )

                    for key, values in transitions.items():
                        pooled[key].extend(values)

                    episodes.append(
                        {"network": network["name"], "profile": scenario["profile"], "seed": scenario["seed"], **stats}
                    )

                losses = ppo_update(model, optimizer, pooled, ppo, generator)
                log.write(json.dumps({"update": update, "episodes": episodes, **losses}) + "\n")
                log.flush()

                count = len(episodes)
                wall = sum(episode["wall_seconds"] for episode in episodes)
                sim = sum(episode["sim_seconds"] for episode in episodes)
                print(
                    f"update {update:4d}/{updates}"
                    f" | reward {sum(e['mean_reward'] for e in episodes) / count:7.3f}"
                    f" | queue {sum(e['mean_normalized_queue'] for e in episodes) / count:.3f}"
                    f" | switch requests {sum(e['switch_request_rate'] for e in episodes) / count:.2f}"
                    f" | overrides {sum(e['overrides'] for e in episodes):4d}"
                    f" | entropy {losses['entropy']:.3f}"
                    f" | kl {losses['approx_kl']:.4f}"
                    f" | {wall:.1f} s ({sim / wall:.0f} sim-s/s)",
                    flush=True,
                )

                if update % training["checkpoint_every_updates"] == 0 or update == updates:
                    path = output_dir / f"checkpoint_{update:04d}.pt"
                    save_checkpoint(path, model, optimizer, {**metadata, "update": update})
                    print(f"Saved {path}", flush=True)
    finally:
        env.close()

    print("Training complete. Performance is unproven until evaluated on held-out scenarios.")


if __name__ == "__main__":
    main()
