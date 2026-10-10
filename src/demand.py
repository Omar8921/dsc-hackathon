"""Vehicle demand: seeded departures, route files, and SUMO scenario files."""

import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path


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

    for incident in scenario.get("incidents", []):
        if incident["route"] not in route_ids:
            raise ValueError(f"{name}: incident uses unknown route {incident['route']!r}.")


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
            vehicles.append((depart_s, f"{route_id}.{index}", route_id, None))

    # An incident is one extra vehicle that stops on a lane, blocking it.
    for index, incident in enumerate(scenario.get("incidents", [])):
        vehicles.append((incident["depart_s"], f"incident.{index}", incident["route"], incident))

    # SUMO expects vehicles sorted by departure time.
    for depart_s, vehicle_id, route_id, incident in sorted(vehicles, key=lambda item: item[:3]):
        element = ET.SubElement(
            root,
            "vehicle",
            id=vehicle_id,
            type=vehicle_type["id"],
            route=route_id,
            depart=f"{depart_s:.2f}",
            departSpeed="max",
        )

        if incident is not None:
            ET.SubElement(
                element,
                "stop",
                lane=incident["lane"],
                endPos=str(incident["position_m"]),
                duration=str(incident["duration_s"]),
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


def sample_training_scenario(
    rng: random.Random, demand: dict, route_groups: dict[str, list[str]]
) -> dict:
    """Draw one random demand scenario for a training episode.

    Profiles: "balanced" (similar flows everywhere), "ew_heavy" and "ns_heavy"
    (one group of routes busier), and "shift" (the busy group changes mid-run).
    """

    end_s = demand["episode_length_s"]
    jitter = demand["route_jitter"]

    def flows(heavy_group: str | None) -> dict[str, int]:
        result = {}

        for group, route_ids in route_groups.items():
            if heavy_group is None:
                low, high = demand["balanced_vph"]
            elif group == heavy_group:
                low, high = demand["major_vph"]
            else:
                low, high = demand["minor_vph"]

            # One level per group, then a small per-route variation.
            level = rng.uniform(low, high)

            for route_id in route_ids:
                result[route_id] = round(level * rng.uniform(1 - jitter, 1 + jitter))

        return result

    profile = rng.choice(demand["profiles"])
    heavy = {"ew_heavy": "east_west", "ns_heavy": "north_south"}

    if profile == "balanced":
        intervals = [{"begin_s": 0, "end_s": end_s, "flows_vph": flows(None)}]
    elif profile in heavy:
        intervals = [{"begin_s": 0, "end_s": end_s, "flows_vph": flows(heavy[profile])}]
    elif profile == "shift":
        first, second = rng.sample(["east_west", "north_south"], 2)
        switch_s = round(end_s * rng.uniform(0.35, 0.65))
        intervals = [
            {"begin_s": 0, "end_s": switch_s, "flows_vph": flows(first)},
            {"begin_s": switch_s, "end_s": end_s, "flows_vph": flows(second)},
        ]
    else:
        raise ValueError(f"Unknown demand profile {profile!r}.")

    return {
        "profile": profile,
        "seed": rng.randrange(2**31),
        "end_s": end_s,
        "intervals": intervals,
    }
