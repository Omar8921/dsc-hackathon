"""Check configs/intersections.json against the generated SUMO network."""

import json
import math
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERSECTIONS_PATH = PROJECT_ROOT / "configs" / "intersections.json"
SCENARIOS_PATH = PROJECT_ROOT / "configs" / "scenarios.json"

APPROACHES = ("N", "E", "S", "W")
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_network(path: Path) -> dict:
    """Read the parts of a .net.xml file that the mapping refers to."""

    root = ET.parse(path).getroot()
    edges = {}
    lanes = {}

    for edge in root.findall("edge"):
        if edge.get("function") == "internal":
            continue

        edges[edge.get("id")] = (edge.get("from"), edge.get("to"))

        for lane in edge.findall("lane"):
            lanes[lane.get("id")] = {
                "edge": edge.get("id"),
                "length": float(lane.get("length")),
            }

    junctions = {
        junction.get("id"): (float(junction.get("x")), float(junction.get("y")))
        for junction in root.findall("junction")
        if junction.get("type") != "internal"
    }

    programs = {
        program.get("id"): [phase.get("state") for phase in program.findall("phase")]
        for program in root.findall("tlLogic")
    }

    # Signal-controlled movements, grouped by signal.
    links = {}

    for connection in root.findall("connection"):
        if connection.get("tl") is None:
            continue

        links.setdefault(connection.get("tl"), []).append(
            {
                "index": int(connection.get("linkIndex")),
                "from_lane": f"{connection.get('from')}_{connection.get('fromLane')}",
                "to_lane": f"{connection.get('to')}_{connection.get('toLane')}",
                "direction": connection.get("dir"),
            }
        )

    return {
        "edges": edges,
        "lanes": lanes,
        "junctions": junctions,
        "programs": programs,
        "links": links,
    }


def side_of(center: tuple[float, float], point: tuple[float, float]) -> str:
    """Return which side (N, E, S, W) of center the point lies on."""

    dx = point[0] - center[0]
    dy = point[1] - center[1]

    if abs(dx) > abs(dy):
        return "E" if dx > 0 else "W"

    return "N" if dy > 0 else "S"


class IntersectionMappingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_json(INTERSECTIONS_PATH)
        cls.network = load_network(PROJECT_ROOT / cls.config["network_file"])
        cls.intersections = cls.config["intersections"]

    def test_signals_and_slots_exist(self) -> None:
        for node_id, node in self.intersections.items():
            with self.subTest(intersection=node_id):
                self.assertIn(node["junction_id"], self.network["junctions"])
                self.assertIn(node["signal_id"], self.network["programs"])
                self.assertEqual(sorted(node["approaches"]), sorted(APPROACHES))

    def test_lanes_enter_and_leave_on_configured_sides(self) -> None:
        edges = self.network["edges"]
        lanes = self.network["lanes"]
        junctions = self.network["junctions"]

        for node_id, node in self.intersections.items():
            junction_id = node["junction_id"]
            center = junctions[junction_id]

            for slot, approach in node["approaches"].items():
                with self.subTest(intersection=node_id, approach=slot):
                    for lane_id in approach["incoming_lanes"]:
                        start, end = edges[lanes[lane_id]["edge"]]
                        self.assertEqual(end, junction_id)
                        self.assertEqual(side_of(center, junctions[start]), slot)

                    # Straight-through traffic leaves on the opposite side.
                    for lane_id in approach["receiving_lanes"]:
                        start, end = edges[lanes[lane_id]["edge"]]
                        self.assertEqual(start, junction_id)
                        self.assertEqual(side_of(center, junctions[end]), OPPOSITE[slot])

    def test_receiving_lanes_are_straight_movements(self) -> None:
        for node_id, node in self.intersections.items():
            straight = {
                (link["from_lane"], link["to_lane"])
                for link in self.network["links"][node["signal_id"]]
                if link["direction"] == "s"
            }

            for slot, approach in node["approaches"].items():
                with self.subTest(intersection=node_id, approach=slot):
                    for incoming in approach["incoming_lanes"]:
                        self.assertTrue(
                            any(
                                (incoming, receiving) in straight
                                for receiving in approach["receiving_lanes"]
                            )
                        )

    def test_every_controlled_lane_is_mapped(self) -> None:
        for node_id, node in self.intersections.items():
            with self.subTest(intersection=node_id):
                controlled = {
                    link["from_lane"] for link in self.network["links"][node["signal_id"]]
                }
                mapped = {
                    lane_id
                    for approach in node["approaches"].values()
                    for lane_id in approach["incoming_lanes"]
                }
                self.assertEqual(controlled, mapped)

    def test_neighbors_match_connecting_roads(self) -> None:
        edges = self.network["edges"]
        lanes = self.network["lanes"]
        junction_to_node = {
            node["junction_id"]: node_id for node_id, node in self.intersections.items()
        }

        for node_id, node in self.intersections.items():
            for slot, approach in node["approaches"].items():
                with self.subTest(intersection=node_id, approach=slot):
                    for lane_id in approach["incoming_lanes"]:
                        start, _end = edges[lanes[lane_id]["edge"]]
                        self.assertEqual(approach["neighbor"], junction_to_node.get(start))

    def test_storage_capacity_matches_lane_length(self) -> None:
        spacing = self.config["vehicle_spacing_m"]
        lanes = self.network["lanes"]

        for node_id, node in self.intersections.items():
            for slot, approach in node["approaches"].items():
                with self.subTest(intersection=node_id, approach=slot):
                    length = sum(lanes[lane_id]["length"] for lane_id in approach["incoming_lanes"])
                    self.assertEqual(approach["storage_capacity"], math.floor(length / spacing))

    def test_vehicle_spacing_matches_demand_vehicle(self) -> None:
        vehicle = load_json(SCENARIOS_PATH)["vehicle_type"]
        self.assertAlmostEqual(
            self.config["vehicle_spacing_m"], vehicle["length"] + vehicle["minGap"]
        )

    def test_actions_select_matching_phases(self) -> None:
        for node_id, node in self.intersections.items():
            actions = node["actions"]
            states = self.network["programs"][node["signal_id"]]
            links = self.network["links"][node["signal_id"]]
            lane_slot = {
                lane_id: slot
                for slot, approach in node["approaches"].items()
                for lane_id in approach["incoming_lanes"]
            }

            with self.subTest(intersection=node_id):
                self.assertEqual(
                    [action["action"] for action in actions], list(range(len(actions)))
                )

                # Every approach is served by exactly one action.
                served = [slot for action in actions for slot in action["served_approaches"]]
                self.assertEqual(sorted(served), sorted(APPROACHES))

            for action in actions:
                served_slots = set(action["served_approaches"])
                green = states[action["green_phase"]]
                yellow = states[action["yellow_phase"]]
                all_red = states[action["all_red_phase"]]

                for link in links:
                    served_link = lane_slot[link["from_lane"]] in served_slots
                    index = link["index"]

                    with self.subTest(
                        intersection=node_id, action=action["name"], link=index
                    ):
                        self.assertIn(green[index], "Gg" if served_link else "rR")
                        self.assertIn(yellow[index], "yY" if served_link else "rR")
                        self.assertIn(all_red[index], "rR")


if __name__ == "__main__":
    unittest.main()
