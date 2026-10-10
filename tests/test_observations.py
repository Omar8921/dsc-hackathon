"""Check the 44-value observation layout and normalization."""

import unittest

from src.observations import OBSERVATION_FIELDS, OBSERVATION_SIZE, build_observation
from src.state import (
    APPROACH_ORDER,
    ApproachState,
    IntersectionState,
    NeighborState,
    SignalState,
)


SETTINGS = {"arrival_reference_vps": 0.5, "wait_reference_s": 120, "max_green_s": 60}


def approach(**overrides) -> ApproachState:
    values = {
        "vehicle_count": 0,
        "queue_count": 0,
        "occupancy": 0.0,
        "arrival_rate_vps": 0.0,
        "mean_wait_s": 0.0,
        "mean_speed_mps": 13.89,
        "downstream_occupancy": 0.0,
        "storage_capacity": 25,
        "speed_limit_mps": 13.89,
    }
    values.update(overrides)
    return ApproachState(**values)


def absent_neighbor() -> NeighborState:
    return NeighborState(present=False, intersection_id=None, normalized_queue=0.0, mean_occupancy=0.0)


def make_state(approaches=None, neighbors=None, signal=None) -> IntersectionState:
    approaches = approaches or {}
    neighbors = neighbors or {}
    return IntersectionState(
        sim_time_s=0.0,
        intersection_id="X",
        signal=signal or SignalState(active_green_phase=0, transition_state="green", elapsed_green_s=0.0),
        approaches={slot: approaches.get(slot, approach()) for slot in APPROACH_ORDER},
        neighbors={slot: neighbors.get(slot, absent_neighbor()) for slot in APPROACH_ORDER},
    )


def field(observation: list[float], name: str) -> float:
    return observation[OBSERVATION_FIELDS.index(name)]


class ObservationTest(unittest.TestCase):
    def test_layout_has_44_named_values(self) -> None:
        self.assertEqual(OBSERVATION_SIZE, 44)
        self.assertEqual(len(set(OBSERVATION_FIELDS)), 44)
        self.assertEqual(len(build_observation(make_state(), SETTINGS)), 44)

    def test_approach_values_are_normalized(self) -> None:
        east = approach(
            queue_count=10,
            vehicle_count=15,
            occupancy=0.3,
            arrival_rate_vps=0.25,
            mean_wait_s=60.0,
            mean_speed_mps=6.945,
            downstream_occupancy=0.8,
        )
        observation = build_observation(make_state({"E": east}), SETTINGS)
        expected = {
            "E.queue": 10 / 25,
            "E.vehicles": 15 / 25,
            "E.occupancy": 0.3,
            "E.arrival_rate": 0.25 / 0.5,
            "E.mean_wait": 60 / 120,
            "E.mean_speed": 0.5,
            "E.downstream_occupancy": 0.8,
        }

        for name, value in expected.items():
            with self.subTest(field=name):
                self.assertAlmostEqual(field(observation, name), value)

    def test_values_are_clipped_but_raw_state_is_kept(self) -> None:
        raw = make_state({"N": approach(queue_count=40, vehicle_count=40, mean_wait_s=300.0)})
        observation = build_observation(raw, SETTINGS)

        self.assertEqual(field(observation, "N.queue"), 1.0)
        self.assertEqual(field(observation, "N.mean_wait"), 1.0)
        self.assertEqual(raw.approaches["N"].queue_count, 40)
        self.assertTrue(all(0.0 <= value <= 1.0 for value in observation))

    def test_absent_neighbor_is_three_zeros(self) -> None:
        observation = build_observation(make_state(), SETTINGS)

        for slot in APPROACH_ORDER:
            for name in ("present", "queue", "occupancy"):
                self.assertEqual(field(observation, f"neighbor_{slot}.{name}"), 0.0)

    def test_empty_neighbor_differs_from_absent_neighbor(self) -> None:
        neighbors = {
            "E": NeighborState(present=True, intersection_id="B0", normalized_queue=0.0, mean_occupancy=0.0),
            "W": NeighborState(present=True, intersection_id="A0", normalized_queue=0.25, mean_occupancy=0.3),
        }
        observation = build_observation(make_state(neighbors=neighbors), SETTINGS)

        def block(slot):
            return [field(observation, f"neighbor_{slot}.{name}") for name in ("present", "queue", "occupancy")]

        self.assertEqual(block("E"), [1.0, 0.0, 0.0])
        self.assertEqual(block("W"), [1.0, 0.25, 0.3])
        self.assertEqual(block("N"), [0.0, 0.0, 0.0])

    def test_signal_block(self) -> None:
        cases = [
            (SignalState(0, "green", 30.0), [1.0, 0.0, 0.5, 0.0]),
            (SignalState(1, "green", 90.0), [0.0, 1.0, 1.0, 0.0]),
            (SignalState(1, "yellow", 0.0), [0.0, 1.0, 0.0, 1.0]),
            (SignalState(0, "all_red", 0.0), [1.0, 0.0, 0.0, 1.0]),
        ]

        for signal, expected in cases:
            with self.subTest(signal=signal):
                self.assertEqual(build_observation(make_state(signal=signal), SETTINGS)[-4:], expected)

    def test_non_finite_measurement_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_observation(make_state({"S": approach(mean_wait_s=float("nan"))}), SETTINGS)


if __name__ == "__main__":
    unittest.main()
