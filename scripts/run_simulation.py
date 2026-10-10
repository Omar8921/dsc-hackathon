"""Run a scenario with a selected controller, live in the viewer or headless."""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO_PATH = PROJECT_ROOT / "simulation" / "scenarios" / "balanced.sumocfg"
INTERSECTIONS_PATH = PROJECT_ROOT / "configs" / "intersections.json"
CONTROLLER_CONFIG_PATH = PROJECT_ROOT / "configs" / "controller.json"
VIEWER_PAGE = PROJECT_ROOT / "viewer" / "index.html"

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

from src.runner import CONTROLLERS, run_episode  # noqa: E402
from src.telemetry import TelemetryServer, build_snapshot  # noqa: E402


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
            "SUMO .sumocfg file to run. A relative path resolves from the current "
            "directory. Default: simulation/scenarios/balanced.sumocfg in the "
            "project root."
        ),
    )
    parser.add_argument(
        "--controller",
        choices=CONTROLLERS,
        default="fixed-time",
        help="Signal controller. Default: fixed-time.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run at full speed without the viewer.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "Folder for metrics.json and tripinfo.xml. "
            "Default: results/<run id>_<scenario>_<controller> in the project root."
        ),
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=5.0,
        help="Viewer only: simulated seconds per real second. Default: 5.",
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
    print(f"Metrics: {output_dir / 'metrics.json'}")


def main() -> None:
    """Run the selected scenario and controller."""

    arguments = parse_arguments()

    if arguments.speed <= 0:
        raise ValueError("--speed must be positive.")

    scenario_path = arguments.scenario.resolve()

    if not scenario_path.is_file():
        raise FileNotFoundError(
            f"Cannot find {scenario_path}. Run scripts/generate_demand.py first."
        )

    run = {
        "run_id": datetime.now().strftime("%Y%m%d-%H%M%S"),
        "scenario": scenario_path.stem,
        "controller": arguments.controller,
    }
    output_dir = (
        arguments.output_dir.resolve()
        if arguments.output_dir
        else PROJECT_ROOT
        / "results"
        / f"{run['run_id']}_{run['scenario']}_{run['controller']}"
    )
    intersections = load_json(INTERSECTIONS_PATH)
    controller_config = load_json(CONTROLLER_CONFIG_PATH)

    print(f"Scenario: {scenario_path}", flush=True)

    if arguments.headless:
        summary = run_episode(
            scenario_path, run, intersections, controller_config, output_dir, quiet=True
        )
        print_summary(summary, output_dir)
        return

    server = TelemetryServer(arguments.host, arguments.port, VIEWER_PAGE)
    pacing = {"next_tick": None}

    def publish(adapter, control, status) -> None:
        # The network is only known once SUMO has started.
        if pacing["next_tick"] is None:
            server.set_network(adapter.read_network())
            server.start()
            print(f"Viewer: {server.url}  (open it in your browser)", flush=True)
            pacing["next_tick"] = time.perf_counter()

        seconds_per_step = adapter.step_length_s / arguments.speed
        server.publish(build_snapshot(adapter, run, status, seconds_per_step, control))

        pacing["next_tick"] += seconds_per_step
        delay = pacing["next_tick"] - time.perf_counter()

        if delay > 0:
            time.sleep(delay)
        else:
            # Running behind; continue from now instead of catching up in a burst.
            pacing["next_tick"] = time.perf_counter()

    try:
        summary = run_episode(
            scenario_path, run, intersections, controller_config, output_dir, on_step=publish
        )
        print_summary(summary, output_dir)
        print(
            "Scenario finished. The viewer keeps the final state; press Ctrl+C to stop.",
            flush=True,
        )

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        server.stop()


if __name__ == "__main__":
    main()
