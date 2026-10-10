"""Run a SUMO scenario live and serve it to the browser viewer."""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO_PATH = PROJECT_ROOT / "simulation" / "scenarios" / "balanced.sumocfg"
VIEWER_PAGE = PROJECT_ROOT / "viewer" / "index.html"

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

from src.simulation_adapter import SimulationAdapter  # noqa: E402
from src.telemetry import TelemetryServer, build_snapshot  # noqa: E402


# Signals follow the program stored in the network until our controllers exist.
CONTROLLER_LABEL = "SUMO default fixed-time program"


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Run a SUMO scenario live and serve it to the browser viewer."
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
        "--speed",
        type=float,
        default=5.0,
        help="Simulated seconds per real second. Default: 5.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Address the viewer is served on. Default: 127.0.0.1 (this computer only).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port the viewer is served on. Default: 8000.",
    )

    return parser.parse_args()


def run_scenario(
    adapter: SimulationAdapter, server: TelemetryServer, run: dict, speed: float
) -> None:
    """Step SUMO at a watchable pace and publish a snapshot after each step."""

    seconds_per_step = adapter.step_length_s / speed
    server.publish(build_snapshot(adapter, run, "running", seconds_per_step))
    next_tick = time.perf_counter()

    while not adapter.finished():
        adapter.step()
        server.publish(build_snapshot(adapter, run, "running", seconds_per_step))

        next_tick += seconds_per_step
        delay = next_tick - time.perf_counter()

        if delay > 0:
            time.sleep(delay)
        else:
            # Running behind; continue from now instead of catching up in a burst.
            next_tick = time.perf_counter()

    server.publish(build_snapshot(adapter, run, "finished", seconds_per_step))


def main() -> None:
    """Run the selected scenario and serve it until stopped."""

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
        "controller": CONTROLLER_LABEL,
    }

    server = TelemetryServer(arguments.host, arguments.port, VIEWER_PAGE)
    adapter = SimulationAdapter(scenario_path)

    try:
        adapter.start()
        server.set_network(adapter.read_network())
        server.start()

        print(f"Scenario: {scenario_path}", flush=True)
        print(f"Viewer: {server.url}  (open it in your browser)", flush=True)

        run_scenario(adapter, server, run, arguments.speed)
        adapter.close()

        print(
            "Scenario finished. The viewer keeps the final state; "
            "press Ctrl+C to stop.",
            flush=True,
        )

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        adapter.close()
        server.stop()


if __name__ == "__main__":
    main()
