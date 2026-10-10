"""Generate vehicle routes and SUMO scenario files from configs/scenarios.json."""

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "scenarios.json"

# Scripts run directly, so make the project's src package importable.
sys.path.insert(0, str(PROJECT_ROOT))

from src.demand import validate_scenario, write_routes, write_sumocfg  # noqa: E402


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Generate vehicle routes and SUMO scenario files."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=(
            "Scenario settings JSON. A relative path resolves from the current "
            "directory. Default: configs/scenarios.json in the project root."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Generate route and scenario files for every configured scenario."""

    config_path = parse_arguments().config.resolve()

    # Load the selected scenario settings.
    print(f"Using config: {config_path}", flush=True)
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))

    # Resolve paths relative to the project, rather than the current terminal.
    network_path = PROJECT_ROOT / config["network_file"]

    if not network_path.is_file():
        raise FileNotFoundError(
            f"Cannot find {network_path}. Run scripts/generate_network.py first."
        )

    routes_dir = PROJECT_ROOT / config["routes_dir"]
    scenarios_dir = PROJECT_ROOT / config["scenarios_dir"]
    routes_dir.mkdir(parents=True, exist_ok=True)
    scenarios_dir.mkdir(parents=True, exist_ok=True)

    for name, scenario in config["scenarios"].items():
        validate_scenario(name, scenario, set(config["routes"]))

        # A scenario with "seeds" gets one file per seed, named <name>_s<seed>.
        if "seeds" in scenario:
            variants = [(f"{name}_s{seed}", seed) for seed in scenario["seeds"]]
        else:
            variants = [(name, scenario["seed"])]

        for file_name, seed in variants:
            seeded = {**scenario, "seed": seed}
            routes_path = routes_dir / f"{file_name}.rou.xml"
            scenario_path = scenarios_dir / f"{file_name}.sumocfg"

            counts = write_routes(routes_path, config, seeded)
            write_sumocfg(
                scenario_path,
                network_path,
                routes_path,
                seeded,
                config["step_length_s"],
            )

            print(f"{file_name}: {sum(counts.values())} vehicles, seed {seed}")

            for route_id, count in counts.items():
                print(f"  {route_id}: {count}")

            print(f"  Routes: {routes_path}")
            print(f"  Scenario: {scenario_path}")

    print("Demand generation complete.")


if __name__ == "__main__":
    main()
