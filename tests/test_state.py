"""Check StateBuilder measurements using hand-made SUMO readings."""

import json
import unittest
from pathlib import Path

from src.state import APPROACH_ORDER, StateBuilder


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERSECTIONS = json.loads(
    (PROJECT_ROOT / "configs" / "intersections.json").read_text(encoding="utf-8-sig")
)

LANE_IDS = sorted(
    {
        lane_id
        for node in INTERSECTIONS["intersections"].values()
        for approach in node["approaches"].values()
        for lane_id in approach["incoming_lanes"] + approach["receiving_lanes"]
    }
)
# Equal lengths keep the expected occupancy values simple.
GEOMETRY = {lane_id: {"length_m": 100.0, "speed_limit_mps": 13.89} for lane_id in LANE_IDS}


def empty_lanes() -> dict:
    return {lane_id: {"occupancy": 0.0} for lane_id in LANE_IDS}


def vehicle(vehicle_id: str, lane: str, speed: float = 10.0, waiting: float = 0.0) -> dict:
    return {"id": vehicle_id, "lane": lane, "speed_mps": speed, "waiting_s": waiting}


class StateBuilderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = StateBuilder(INTERSECTIONS, arrival_window_s=30, lane_geometry=GEOMETRY)

    def update(self, time_s, vehicles=(), lanes=None, phase=0):
        signals = [{"id": node_id, "phase": phase} for node_id in INTERSECTIONS["intersections"]]
        return self.builder.update(time_s, lanes or empty_lanes(), list(vehicles), signals)

    def test_counts_queue_wait_and_speed(self) -> None:
        states = self.update(
            0,
            [
                vehicle("stopped", "top0A0_0", speed=0.0, waiting=12.0),
                vehicle("moving", "top0A0_0", speed=10.0),
            ],
        )
        north = states["A0"].approaches["N"]

        self.assertEqual(north.vehicle_count, 2)
        self.assertEqual(north.queue_count, 1)
        self.assertAlmostEqual(north.mean_wait_s, 6.0)
        self.assertAlmostEqual(north.mean_speed_mps, 5.0)

    def test_empty_approach_reports_free_flow_speed(self) -> None:
        east = self.update(0)["A0"].approaches["E"]

        self.assertEqual((east.vehicle_count, east.queue_count, east.mean_wait_s), (0, 0, 0.0))
        self.assertAlmostEqual(east.mean_speed_mps, 13.89)

    def test_vehicles_inside_the_junction_are_not_counted(self) -> None:
        states = self.update(0, [vehicle("crossing", ":A0_1_0")])

        self.assertTrue(
            all(approach.vehicle_count == 0 for approach in states["A0"].approaches.values())
        )

    def test_arrival_rate_uses_a_rolling_window(self) -> None:
        lane = "left0A0_0"

        def west_rate(time_s, ids):
            states = self.update(time_s, [vehicle(vehicle_id, lane) for vehicle_id in ids])
            return states["A0"].approaches["W"].arrival_rate_vps

        west_rate(1, ["a"])
        self.assertAlmostEqual(west_rate(2, ["a", "b"]), 2 / 30)

        # Vehicles that stay on the approach are not counted again.
        for time_s in range(3, 31):
            self.assertAlmostEqual(west_rate(time_s, ["a", "b"]), 2 / 30)

        # Arrivals older than the 30 s window drop out.
        self.assertAlmostEqual(west_rate(31, ["a", "b"]), 1 / 30)
        self.assertAlmostEqual(west_rate(32, ["a", "b"]), 0.0)

    def test_occupancy_and_downstream_occupancy(self) -> None:
        lanes = empty_lanes()
        lanes["top0A0_0"]["occupancy"] = 0.4
        lanes["A0bottom0_0"]["occupancy"] = 0.7
        north = self.update(0, lanes=lanes)["A0"].approaches["N"]

        self.assertAlmostEqual(north.occupancy, 0.4)
        self.assertAlmostEqual(north.downstream_occupancy, 0.7)

    def test_neighbor_summary_reads_the_connected_intersection(self) -> None:
        lanes = empty_lanes()
        lanes["top0A0_0"]["occupancy"] = 0.4
        queued = [vehicle(f"q{i}", "top0A0_0", speed=0.0) for i in range(3)]
        states = self.update(0, queued, lanes)

        a0_storage = sum(
            approach["storage_capacity"]
            for approach in INTERSECTIONS["intersections"]["A0"]["approaches"].values()
        )
        west_of_b0 = states["B0"].neighbors["W"]

        self.assertTrue(west_of_b0.present)
        self.assertEqual(west_of_b0.intersection_id, "A0")
        self.assertAlmostEqual(west_of_b0.normalized_queue, 3 / a0_storage)
        self.assertAlmostEqual(west_of_b0.mean_occupancy, 0.4 / 4)

        north_of_a0 = states["A0"].neighbors["N"]
        self.assertFalse(north_of_a0.present)
        self.assertEqual((north_of_a0.normalized_queue, north_of_a0.mean_occupancy), (0.0, 0.0))

    def test_signal_state_follows_phase_changes(self) -> None:
        # (time, SUMO phase) -> (active green, transition state, elapsed green)
        timeline = [
            (0, 0, (0, "green", 0)),
            (20, 0, (0, "green", 20)),
            (41, 1, (0, "yellow", 0)),
            (44, 2, (0, "all_red", 0)),
            (45, 3, (1, "green", 0)),
            (50, 3, (1, "green", 5)),
        ]

        for time_s, phase, (active, transition, elapsed) in timeline:
            with self.subTest(time=time_s):
                signal = self.update(time_s, phase=phase)["A0"].signal
                self.assertEqual(signal.active_green_phase, active)
                self.assertEqual(signal.transition_state, transition)
                self.assertAlmostEqual(signal.elapsed_green_s, elapsed)

    def test_unmapped_phase_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.update(0, phase=7)

    def test_state_dict_has_every_slot(self) -> None:
        state = self.update(0)["B0"].to_dict()

        self.assertEqual(state["intersection_id"], "B0")
        self.assertEqual(state["source"], "sumo")
        self.assertEqual(list(state["approaches"]), list(APPROACH_ORDER))
        self.assertEqual(list(state["neighbors"]), list(APPROACH_ORDER))


if __name__ == "__main__":
    unittest.main()
