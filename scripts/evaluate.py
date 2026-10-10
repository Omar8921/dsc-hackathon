"""Compare controllers on held-out scenarios and write a results table."""

import argparse
import json
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERSECTIONS_PATH = PROJECT_ROOT / "configs" / "intersections.json"
CONTROLLER_CONFIG_PATH = PROJECT_ROOT / "configs" / "controller.json"
SCENARIOS_DIR = PROJECT_ROOT / "simulation" / "scenarios"

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

from src.runner import BASELINES, CONTROLLERS, run_episode  # noqa: E402


# (key, column title, value from a run summary). Lower is better except "completed".
METRICS = [
    ("mean_wait_s", "Mean wait (s)", lambda s: s["completed_trips"]["waiting_s"]["mean"]),
    ("p95_wait_s", "95th pct wait (s)", lambda s: s["completed_trips"]["waiting_s"]["p95"]),
    ("mean_time_loss_s", "Mean time loss (s)", lambda s: s["completed_trips"]["time_loss_s"]["mean"]),
    ("completed", "Completed trips", lambda s: s["trips"]["completed"]),
    ("unfinished", "Unfinished", lambda s: s["trips"]["still_running"] + s["trips"]["waiting_to_insert"]),
    ("overrides", "Safety overrides", lambda s: sum(s["safety"]["overrides"].values())),
    ("illegal", "Illegal transitions", lambda s: s["safety"]["illegal_transitions"]),
]
COMPARED = [("mean_wait_s", "mean wait"), ("mean_time_loss_s", "time loss")]


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Compare controllers on held-out scenarios.")
    parser.add_argument("--checkpoint", type=Path, help="Trained policy checkpoint for the ppo controller.")
    parser.add_argument(
        "--controllers",
        nargs="+",
        choices=CONTROLLERS,
        default=list(CONTROLLERS),
        help="Controllers to compare. Default: all.",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        type=Path,
        help="Scenario .sumocfg files. Default: simulation/scenarios/test_*.sumocfg.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Folder for results. Default: results/eval_<run id> in the project root.",
    )

    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def spread(values: list[float]) -> dict:
    return {
        "mean": statistics.fmean(values),
        "sd": statistics.stdev(values) if len(values) > 1 else 0.0,
        "n": len(values),
    }


def cell(value: dict) -> str:
    text = f"{value['mean']:.1f}"
    return f"{text} ± {value['sd']:.1f}" if value["n"] > 1 else text


def main() -> None:
    """Run every controller on every scenario and summarize."""

    arguments = parse_arguments()

    if "ppo" in arguments.controllers and (arguments.checkpoint is None or not arguments.checkpoint.is_file()):
        raise FileNotFoundError("Evaluating ppo needs --checkpoint pointing to a .pt file.")

    scenarios = [path.resolve() for path in arguments.scenarios] if arguments.scenarios else sorted(
        SCENARIOS_DIR.glob("test_*.sumocfg")
    )

    if not scenarios:
        raise FileNotFoundError("No scenarios found. Run scripts/generate_demand.py first.")

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = arguments.output_dir.resolve() if arguments.output_dir else PROJECT_ROOT / "results" / f"eval_{run_id}"
    intersections = load_json(INTERSECTIONS_PATH)
    controller_config = load_json(CONTROLLER_CONFIG_PATH)
    runs = []

    for scenario_path in scenarios:
        for controller in arguments.controllers:
            run = {"run_id": f"eval_{run_id}", "scenario": scenario_path.stem, "controller": controller}

            if controller == "ppo":
                run["checkpoint"] = str(arguments.checkpoint.resolve())

            summary = run_episode(
                scenario_path,
                run,
                intersections,
                controller_config,
                output_dir / scenario_path.stem / controller,
                quiet=True,
            )
            values = {key: read(summary) for key, _, read in METRICS}
            runs.append({"scenario": scenario_path.stem, "controller": controller, **values})
            print(
                f"{scenario_path.stem:24s} {controller:11s} "
                f"wait {values['mean_wait_s']:6.1f} s | time loss {values['mean_time_loss_s']:6.1f} s | "
                f"completed {values['completed']:4d} | illegal {values['illegal']}",
                flush=True,
            )

    # Group seeds of the same scenario: test_balanced_s9001 -> test_balanced.
    families = list(dict.fromkeys(re.sub(r"_s\d+$", "", run["scenario"]) for run in runs))
    table = {}

    for family in families:
        for controller in arguments.controllers:
            matching = [
                run for run in runs
                if run["controller"] == controller and re.sub(r"_s\d+$", "", run["scenario"]) == family
            ]
            table[(family, controller)] = {key: spread([run[key] for run in matching]) for key, _, _ in METRICS}

    # Positive means PPO is lower (better) than the baseline.
    improvements = {}

    if "ppo" in arguments.controllers:
        for family in families:
            for baseline in [name for name in BASELINES if name in arguments.controllers]:
                for key, _ in COMPARED:
                    base = table[(family, baseline)][key]["mean"]
                    ppo = table[(family, "ppo")][key]["mean"]
                    improvements[(family, baseline, key)] = 100 * (base - ppo) / base if base > 0 else None

    lines = [
        "# Held-out evaluation",
        "",
        f"Checkpoint: `{arguments.checkpoint}`" if arguments.checkpoint else "Checkpoint: none",
        "",
        "Values are mean ± standard deviation over seeds. Lower is better, except completed trips. "
        "Waiting and time loss cover completed trips; unfinished vehicles are counted separately.",
        "",
        "| Scenario | Controller | " + " | ".join(title for _, title, _ in METRICS) + " |",
        "| --- | --- | " + " | ".join("---" for _ in METRICS) + " |",
    ]

    for family in families:
        for controller in arguments.controllers:
            row = table[(family, controller)]
            lines.append(f"| {family} | {controller} | " + " | ".join(cell(row[key]) for key, _, _ in METRICS) + " |")

    if improvements:
        baselines = [name for name in BASELINES if name in arguments.controllers]
        lines += [
            "",
            "## PPO compared with baselines",
            "",
            "Percent change of the mean; positive means PPO is better, negative means worse.",
            "",
            "| Scenario | " + " | ".join(f"vs {name}: {label}" for name in baselines for _, label in COMPARED) + " |",
            "| --- | " + " | ".join("---" for _ in baselines for _ in COMPARED) + " |",
        ]

        for family in families:
            values = []

            for name in baselines:
                for key, _ in COMPARED:
                    change = improvements[(family, name, key)]
                    values.append("n/a" if change is None else f"{change:+.1f}%")

            lines.append(f"| {family} | " + " | ".join(values) + " |")

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "summary.json").write_text(
        json.dumps(
            {
                "checkpoint": str(arguments.checkpoint) if arguments.checkpoint else None,
                "runs": runs,
                "table": [{"scenario": f, "controller": c, **values} for (f, c), values in table.items()],
                "improvement_percent": [
                    {"scenario": f, "baseline": b, "metric": k, "value": v} for (f, b, k), v in improvements.items()
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("\n".join(lines))
    print(f"\nSaved {output_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
