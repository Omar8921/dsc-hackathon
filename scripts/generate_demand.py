"""Generate vehicle routes and SUMO scenario files from configs/scenarios.json."""

import argparse
import json
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "scenarios.json"


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


def validate_scenario(name: str, scenario: dict, route_ids: set[str]) -> None:
    """Check interval timing and flow values for one scenario."""

    previous_end_s = 0

    for interval in sorted(scenario["intervals"], key=lambda item: item["begin_s"]):
        begin_s = interval["begin_s"]
        end_s = interval["end_s"]

        if not previous_end_s <= begin_s < end_s <= scenario["end_s"]:
            raise ValueError(
                f"{name}: intervals must not overlap and must lie within "
                f"0..{scenario['end_s']} s."
            )

        unknown_routes = set(interval["flows_vph"]) - route_ids

        if unknown_routes:
            raise ValueError(f"{name}: unknown routes {sorted(unknown_routes)}.")

        if any(flow < 0 for flow in interval["flows_vph"].values()):
            raise ValueError(f"{name}: flows must be non-negative.")

        previous_end_s = end_s


def sample_departures(route_id: str, seed: int, intervals: list[dict]) -> list[float]:
    """Sample Poisson departure times for one route across all intervals."""

    # A separate stream per route keeps one route's departures unchanged
    # when another route's flow is edited.
    rng = random.Random(f"{seed}:{route_id}")
    departures = []

    for interval in sorted(intervals, key=lambda item: item["begin_s"]):
        rate_vps = interval["flows_vph"].get(route_id, 0) / 3600.0

        if rate_vps == 0:
            continue

        time_s = interval["begin_s"]

        while True:
            time_s += rng.expovariate(rate_vps)

            if time_s >= interval["end_s"]:
                break

            departures.append(time_s)

    return departures


def write_routes(path: Path, config: dict, scenario: dict) -> dict[str, int]:
    """Write the route file and return the vehicle count per route."""

    root = ET.Element("routes")
    vehicle_type = config["vehicle_type"]

    ET.SubElement(
        root, "vType", {key: str(value) for key, value in vehicle_type.items()}
    )

    for route_id, edges in config["routes"].items():
        ET.SubElement(root, "route", id=route_id, edges=" ".join(edges))

    vehicles = []
    counts = {}

    for route_id in config["routes"]:
        departures = sample_departures(
            route_id, scenario["seed"], scenario["intervals"]
        )
        counts[route_id] = len(departures)

        for index, depart_s in enumerate(departures):
            vehicles.append((depart_s, f"{route_id}.{index}", route_id))

    # SUMO expects vehicles sorted by departure time.
    for depart_s, vehicle_id, route_id in sorted(vehicles):
        ET.SubElement(
            root,
            "vehicle",
            id=vehicle_id,
            type=vehicle_type["id"],
            route=route_id,
            depart=f"{depart_s:.2f}",
            departSpeed="max",
        )

    ET.indent(root)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

    return counts


def write_sumocfg(
    path: Path,
    network_path: Path,
    routes_path: Path,
    scenario: dict,
    step_length_s: float,
) -> None:
    """Write a SUMO configuration that references the network and routes."""

    # SUMO resolves paths inside a .sumocfg relative to the file itself.
    def relative(target: Path) -> str:
        return Path(os.path.relpath(target, path.parent)).as_posix()

    root = ET.Element("configuration")

    inputs = ET.SubElement(root, "input")
    ET.SubElement(inputs, "net-file", value=relative(network_path))
    ET.SubElement(inputs, "route-files", value=relative(routes_path))

    time = ET.SubElement(root, "time")
    ET.SubElement(time, "begin", value="0")
    ET.SubElement(time, "end", value=str(scenario["end_s"]))
    ET.SubElement(time, "step-length", value=str(step_length_s))

    random_number = ET.SubElement(root, "random_number")
    ET.SubElement(random_number, "seed", value=str(scenario["seed"]))

    ET.indent(root)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


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

        routes_path = routes_dir / f"{name}.rou.xml"
        scenario_path = scenarios_dir / f"{name}.sumocfg"

        counts = write_routes(routes_path, config, scenario)
        write_sumocfg(
            scenario_path,
            network_path,
            routes_path,
            scenario,
            config["step_length_s"],
        )

        print(f"{name}: {sum(counts.values())} vehicles, seed {scenario['seed']}")

        for route_id, count in counts.items():
            print(f"  {route_id}: {count}")

        print(f"  Routes: {routes_path}")
        print(f"  Scenario: {scenario_path}")

    print("Demand generation complete.")


if __name__ == "__main__":
    main()
