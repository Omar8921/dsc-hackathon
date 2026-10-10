"""Measure queues under ordinary demand and freeze the congestion-alert reference."""

import argparse
import json
import statistics
import sys
import tempfile
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "alerts.json"
INTERSECTIONS_PATH = PROJECT_ROOT / "configs" / "intersections.json"
CONTROLLER_CONFIG_PATH = PROJECT_ROOT / "configs" / "controller.json"
DEFAULT_SCENARIOS = [
    PROJECT_ROOT / "simulation" / "scenarios" / "balanced.sumocfg",
    PROJECT_ROOT / "simulation" / "scenarios" / "ew_heavy.sumocfg",
]

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

from src.congestion_detector import worst_approach_queue  # noqa: E402
from src.runner import BASELINES, run_episode  # noqa: E402


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Calibrate the congestion-alert reference.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Alert settings JSON to update. Default: configs/alerts.json in the project root.",
    )
    parser.add_argument(
        "--controller",
        choices=BASELINES,
        default="actuated",
        help="Controller running during calibration. Default: actuated.",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        type=Path,
        help="Ordinary-demand scenarios. Default: the balanced and ew_heavy development scenarios.",
    )

    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    arguments = parse_arguments()
    config_path = arguments.config.resolve()
    config = load_json(config_path)
    scenarios = [path.resolve() for path in arguments.scenarios] if arguments.scenarios else DEFAULT_SCENARIOS
    intersections = load_json(INTERSECTIONS_PATH)
    controller_config = load_json(CONTROLLER_CONFIG_PATH)
    samples = {node_id: [] for node_id in intersections["intersections"]}

    def collect(adapter, control, states, alerts, status) -> None:
        for node_id, state in states.items():
            samples[node_id].append(worst_approach_queue(state))

    for scenario_path in scenarios:
        run = {"run_id": "calibration", "scenario": scenario_path.stem, "controller": arguments.controller}

        with tempfile.TemporaryDirectory() as folder:
            run_episode(
                scenario_path, run, intersections, controller_config, Path(folder), quiet=True, on_step=collect
            )

        print(f"Measured {scenario_path.stem} with {arguments.controller}", flush=True)

    config["reference_p95"] = {
        node_id: statistics.quantiles(values, n=100, method="inclusive")[94]
        for node_id, values in samples.items()
    }
    config["calibration"] = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "controller": arguments.controller,
        "scenarios": [path.stem for path in scenarios],
        "statistic": "95th percentile of the worst approach's queue / storage, per simulated second",
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    for node_id, value in config["reference_p95"].items():
        print(f"{node_id}: reference 95th percentile {value:.3f}")

    print(f"Saved {config_path}")


if __name__ == "__main__":
    main()
