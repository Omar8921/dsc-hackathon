"""Check the fixed-time and actuated baseline decisions without SUMO."""

import json
import unittest
from pathlib import Path

from src.baselines import ActuatedController, FixedTimeController
from src.state import SignalState


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERSECTIONS = json.loads(
    (PROJECT_ROOT / "configs" / "intersections.json").read_text(encoding="utf-8-sig")
)
GEOMETRY = {
    lane_id: {"length_m": 200.0, "speed_limit_mps": 13.89}
    for lane_id in ("top0A0_0", "bottom0A0_0", "left0A0_0", "B0A0_0")
}


def green(action: int, elapsed: float) -> dict:
    return {"A0": SignalState(action, "green", elapsed)}


def car(lane: str, distance_to_stop_line: float) -> dict:
    return {"id": f"{lane}-{distance_to_stop_line}", "lane": lane, "lane_position_m": 200.0 - distance_to_stop_line}


class FixedTimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = FixedTimeController(INTERSECTIONS, green_s=30)

    def test_switches_after_green_s(self) -> None:
        self.assertEqual(self.controller.requests(0, green(0, 29), []), {})
        self.assertEqual(self.controller.requests(0, green(0, 30), []), {"A0": 1})
        self.assertEqual(self.controller.requests(0, green(1, 30), []), {"A0": 0})

    def test_no_requests_during_a_transition(self) -> None:
        states = {"A0": SignalState(0, "yellow", 0.0)}
        self.assertEqual(self.controller.requests(0, states, []), {})


class ActuatedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = ActuatedController(
            INTERSECTIONS, GEOMETRY, min_green_s=10, detector_distance_m=40
        )

    def test_waits_for_minimum_green(self) -> None:
        cars = [car("left0A0_0", 5)]
        self.assertEqual(self.controller.requests(0, green(0, 9), cars), {})

    def test_switches_when_served_approaches_gap_out(self) -> None:
        # North-south green, nobody near its stop lines, a car waiting on the west.
        cars = [car("left0A0_0", 5), car("top0A0_0", 150)]
        self.assertEqual(self.controller.requests(0, green(0, 12), cars), {"A0": 1})

    def test_extends_while_served_traffic_is_detected(self) -> None:
        cars = [car("left0A0_0", 5), car("top0A0_0", 20)]
        self.assertEqual(self.controller.requests(0, green(0, 12), cars), {})

    def test_holds_without_conflicting_demand(self) -> None:
        self.assertEqual(self.controller.requests(0, green(0, 12), [car("left0A0_0", 100)]), {})

    def test_ignores_vehicles_inside_the_junction(self) -> None:
        cars = [{"id": "x", "lane": ":A0_4_0", "lane_position_m": 1.0}]
        self.assertEqual(self.controller.requests(0, green(0, 12), cars), {})


if __name__ == "__main__":
    unittest.main()
