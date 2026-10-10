"""Run scenarios with a selected controller, live in the viewer or headless.

In the viewer, a different scenario, controller, or speed can be chosen while
the server runs; choosing a new run stops the current one and starts it.
"""

import argparse
import json
import re
import sys
import threading
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_DIR = PROJECT_ROOT / "simulation" / "scenarios"
DEFAULT_SCENARIO_PATH = SCENARIOS_DIR / "balanced.sumocfg"
TRAINING_CONFIG_PATH = PROJECT_ROOT / "configs" / "training.json"
CONTROLLER_CONFIG_PATH = PROJECT_ROOT / "configs" / "controller.json"
ALERTS_CONFIG_PATH = PROJECT_ROOT / "configs" / "alerts.json"
VIEWER_PAGE = PROJECT_ROOT / "viewer" / "index.html"

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

from src.metrics import LiveTripTracker  # noqa: E402
from src.runner import CONTROLLERS, run_episode  # noqa: E402
from src.telemetry import SCHEMA_VERSION, TelemetryServer, build_snapshot  # noqa: E402


CONTROLLER_LABELS = {
    "fixed-time": "Fixed-time timer",
    "actuated": "Actuated (sensor-based)",
    "ppo": "AI controller (PPO)",
}
# Scenario groups by file-name prefix, and the order they are listed in.
GROUP_PREFIXES = {"demo_": "Demonstrations", "test_": "Held-out tests, never seen in training"}
GROUP_ORDER = ["Demonstrations", "Development", "Held-out tests, never seen in training"]
SPEEDS = [1, 2, 5, 10, 20]


class RunCancelled(Exception):
    """Raised inside a live run when the viewer chooses another run."""


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Run a scenario with a selected controller and save its metrics."
    )
    parser.add_argument(
        "--scenario",
        type=Path,
        default=DEFAULT_SCENARIO_PATH,
        help=(
            "SUMO .sumocfg file to start with. A relative path resolves from the current "
            "directory. Default: simulation/scenarios/balanced.sumocfg in the project root."
        ),
    )
    parser.add_argument(
        "--controller",
        choices=CONTROLLERS,
        default="fixed-time",
        help="Signal controller to start with. Default: fixed-time.",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        help=(
            "Trained policy checkpoint (.pt) for the ppo controller. "
            "Default: selected_checkpoint in configs/training.json."
        ),
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run once at full speed without the viewer.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "Headless only: folder for metrics.json and tripinfo.xml. "
            "Default: results/<run id>_<scenario>_<controller> in the project root."
        ),
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=5.0,
        help="Viewer only: simulated seconds per real second at start. Default: 5.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Viewer only: address to serve on. Default: 127.0.0.1 (this computer only).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Viewer only: port to serve on. Default: 8000.",
    )

    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_networks() -> list[dict]:
    """Networks listed in configs/training.json, with their mappings and scenarios."""

    networks = []

    for entry in load_json(TRAINING_CONFIG_PATH)["networks"]:
        scenarios = load_json(PROJECT_ROOT / entry["scenarios"])
        networks.append(
            {
                "name": entry["name"],
                "intersections": load_json(PROJECT_ROOT / entry["intersections"]),
                "scenarios": scenarios,
                "network_path": (PROJECT_ROOT / scenarios["network_file"]).resolve(),
            }
        )

    return networks


def network_of(sumocfg_path: Path, networks: list[dict]) -> dict | None:
    """Return the listed network that a .sumocfg file runs on, if any."""

    net_file = ET.parse(sumocfg_path).getroot().find("input/net-file").get("value")
    path = (sumocfg_path.parent / net_file).resolve()
    return next((network for network in networks if network["network_path"] == path), None)


def describe_scenario(path: Path, network: dict) -> dict:
    """Readable name and group for one scenario file."""

    scenarios = network["scenarios"]["scenarios"]
    match = re.fullmatch(r"(.+)_s(\d+)", path.stem)
    base, seed = (match.group(1), match.group(2)) if match and match.group(1) in scenarios else (path.stem, None)
    settings = scenarios.get(base, {})
    label = settings.get("label", path.stem.replace("_", " "))
    group = next(
        (name for prefix, name in GROUP_PREFIXES.items() if path.stem.startswith(prefix)), "Development"
    )

    return {
        "id": path.stem,
        "label": f"{label}, seed {seed}" if seed else label,
        "description": settings.get("description", ""),
        "group": group,
        "network": network["name"],
        "path": path,
        "intersections": network["intersections"],
    }


def build_catalog(networks: list[dict]) -> dict[str, dict]:
    """Every scenario file whose network is listed, in display order."""

    entries = [
        describe_scenario(path, network)
        for path in sorted(SCENARIOS_DIR.glob("*.sumocfg"))
        if (network := network_of(path, networks)) is not None
    ]
    entries.sort(key=lambda entry: (GROUP_ORDER.index(entry["group"]), entry["id"]))
    return {entry["id"]: entry for entry in entries}


def alerts_for(intersections: dict, alerts_config: dict | None) -> dict | None:
    """Use the congestion detector only where every intersection has a reference."""

    if not alerts_config or not alerts_config.get("reference_p95"):
        return None

    return alerts_config if set(intersections["intersections"]) <= set(alerts_config["reference_p95"]) else None


def print_summary(summary: dict, output_dir: Path) -> None:
    trips = summary["trips"]
    waiting = summary["completed_trips"]["waiting_s"]
    time_loss = summary["completed_trips"]["time_loss_s"]
    safety = summary["safety"]

    print(f"Controller: {summary['controller']}   Scenario: {summary['scenario']}")
    print(
        f"Trips: {trips['completed']} completed, {trips['still_running']} still running, "
        f"{trips['waiting_to_insert']} waiting to enter, {trips['teleports']} teleports"
    )

    if waiting:
        print(
            f"Completed trips: mean waiting {waiting['mean']:.1f} s "
            f"(95th percentile {waiting['p95']:.1f} s), "
            f"mean time loss {time_loss['mean']:.1f} s"
        )

    print(
        f"Safety: {safety['illegal_transitions']} illegal transitions, "
        f"overrides {safety['overrides'] or 'none'}"
    )

    for event in summary.get("alerts", []):
        print(
            f"Congestion alert {event['event_id']}: {event['intersection_id']} from "
            f"{event['started_s']:.0f} s for {event['duration_s']:.0f} s, {event['status']}"
        )

    print(f"Metrics: {output_dir / 'metrics.json'}")


def main() -> None:
    """Run the selected scenario and controller."""

    arguments = parse_arguments()

    if arguments.speed <= 0:
        raise ValueError("--speed must be positive.")

    controller_config = load_json(CONTROLLER_CONFIG_PATH)
    # Congestion alerts run only once a reference has been calibrated.
    alerts_config = load_json(ALERTS_CONFIG_PATH) if ALERTS_CONFIG_PATH.is_file() else None
    networks = load_networks()

    selected = load_json(TRAINING_CONFIG_PATH).get("selected_checkpoint")
    checkpoint = arguments.checkpoint or (PROJECT_ROOT / selected if selected else None)
    checkpoint = checkpoint.resolve() if checkpoint and checkpoint.is_file() else None

    if arguments.controller == "ppo" and checkpoint is None:
        raise FileNotFoundError("--controller ppo needs --checkpoint pointing to a .pt file.")

    scenario_path = arguments.scenario.resolve()

    if not scenario_path.is_file():
        raise FileNotFoundError(f"Cannot find {scenario_path}. Run scripts/generate_demand.py first.")

    network = network_of(scenario_path, networks)

    if network is None:
        raise ValueError(f"{scenario_path.name} runs on a network not listed in configs/training.json.")

    catalog = build_catalog(networks)
    first = catalog.get(scenario_path.stem)

    if first is None or first["path"] != scenario_path:
        first = describe_scenario(scenario_path, network)

    def make_run(entry: dict, controller: str) -> dict:
        run = {
            "run_id": datetime.now().strftime("%Y%m%d-%H%M%S-%f"),
            "scenario": entry["id"],
            "scenario_label": entry["label"],
            "network": entry["network"],
            "controller": controller,
            "controller_label": CONTROLLER_LABELS[controller],
        }

        if controller == "ppo":
            run["checkpoint"] = str(checkpoint)

        return run

    def results_dir(run: dict) -> Path:
        return PROJECT_ROOT / "results" / f"{run['run_id']}_{run['scenario']}_{run['controller']}"

    if arguments.headless:
        run = make_run(first, arguments.controller)
        output_dir = arguments.output_dir.resolve() if arguments.output_dir else results_dir(run)
        print(f"Scenario: {scenario_path}", flush=True)
        summary = run_episode(
            scenario_path,
            run,
            first["intersections"],
            controller_config,
            output_dir,
            quiet=True,
            alerts_config=alerts_for(first["intersections"], alerts_config),
        )
        print_summary(summary, output_dir)
        return

    server = TelemetryServer(arguments.host, arguments.port, VIEWER_PAGE)
    server.set_catalog(
        {
            "scenarios": [
                {key: entry[key] for key in ("id", "label", "description", "group", "network")}
                for entry in catalog.values()
            ],
            "controllers": [
                {"id": name, "label": CONTROLLER_LABELS[name], "available": name != "ppo" or checkpoint is not None}
                for name in CONTROLLERS
            ],
            "speeds": SPEEDS,
        }
    )

    # Shared between the HTTP thread (commands) and the main thread (runs).
    session = {"pending": None, "speed": arguments.speed, "serving": False}
    changed = threading.Event()
    lock = threading.Lock()

    def command(path: str, payload: dict) -> dict:
        if path == "/api/speed":
            speed = float(payload.get("speed"))

            if not 0 < speed <= 100:
                raise ValueError("Speed must be between 0 and 100.")

            session["speed"] = speed
            return {"ok": True, "speed": speed}

        entry = catalog.get(payload.get("scenario"))
        controller = payload.get("controller")

        if entry is None:
            raise ValueError("Unknown scenario.")

        if controller not in CONTROLLERS or (controller == "ppo" and checkpoint is None):
            raise ValueError("Unknown or unavailable controller.")

        with lock:
            session["pending"] = (entry, controller)

        changed.set()
        return {"ok": True}

    server.on_command = command
    selection = (first, arguments.controller)

    try:
        while True:
            entry, controller = selection
            run = make_run(entry, controller)
            tracker = LiveTripTracker(1.0)
            progress = {"network_sent": False, "next_tick": None}
            changed.clear()
            server.publish({"schema_version": SCHEMA_VERSION, "status": "starting"})
            print(f"Running: {entry['label']} with {CONTROLLER_LABELS[controller]}", flush=True)

            def publish(adapter, control, states, alerts, status) -> None:
                if changed.is_set():
                    raise RunCancelled()

                # Each run may use a different network; send it before the first snapshot.
                if not progress["network_sent"]:
                    server.set_network(adapter.read_network())
                    progress["network_sent"] = True
                    progress["next_tick"] = time.perf_counter()
                    tracker.step_length_s = adapter.step_length_s

                    if not session["serving"]:
                        server.start()
                        session["serving"] = True
                        print(f"Viewer: {server.url}  (open it in your browser)", flush=True)

                tracker.update(adapter.read_vehicles())
                seconds_per_step = adapter.step_length_s / session["speed"]
                server.publish(
                    build_snapshot(
                        adapter,
                        {**run, "speed": session["speed"]},
                        status,
                        seconds_per_step,
                        control,
                        states,
                        alerts,
                        tracker.summary(),
                    )
                )

                progress["next_tick"] += seconds_per_step
                delay = progress["next_tick"] - time.perf_counter()

                if delay > 0:
                    time.sleep(delay)
                else:
                    # Running behind; continue from now instead of catching up in a burst.
                    progress["next_tick"] = time.perf_counter()

            try:
                output_dir = results_dir(run)
                summary = run_episode(
                    entry["path"],
                    run,
                    entry["intersections"],
                    controller_config,
                    output_dir,
                    on_step=publish,
                    alerts_config=alerts_for(entry["intersections"], alerts_config),
                )
                print_summary(summary, output_dir)
                print("Finished. Choose another run in the viewer, or press Ctrl+C to stop.", flush=True)

                while not changed.wait(0.5):
                    pass
            except RunCancelled:
                print("Switching to the newly selected run.", flush=True)

            with lock:
                selection = session["pending"]
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        server.stop()


if __name__ == "__main__":
    main()
