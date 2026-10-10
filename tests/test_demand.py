"""Check demand generation and the training scenario sampler."""

import json
import random
import tempfile
import unittest
from pathlib import Path

from src.demand import sample_training_scenario, validate_scenario, write_routes


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


SCENARIOS = load_json(PROJECT_ROOT / "configs" / "scenarios.json")
TRAINING = load_json(PROJECT_ROOT / "configs" / "training.json")


class DemandTest(unittest.TestCase):
    def test_committed_route_files_are_reproduced(self) -> None:
        # Moving the demand code into src/ must not change any generated file.
        for name in ("balanced", "ew_heavy"):
            with self.subTest(scenario=name), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "routes.rou.xml"
                write_routes(path, SCENARIOS, SCENARIOS["scenarios"][name])
                committed = PROJECT_ROOT / "simulation" / "routes" / f"{name}.rou.xml"
                self.assertEqual(
                    path.read_bytes().replace(b"\r\n", b"\n"),
                    committed.read_bytes().replace(b"\r\n", b"\n"),
                )

    def test_route_groups_cover_every_route_once(self) -> None:
        grouped = [route for routes in SCENARIOS["route_groups"].values() for route in routes]
        self.assertEqual(sorted(grouped), sorted(SCENARIOS["routes"]))

    def test_test_scenarios_have_their_own_seeds(self) -> None:
        dev_seeds = {s["seed"] for s in SCENARIOS["scenarios"].values() if "seed" in s}

        for name, scenario in SCENARIOS["scenarios"].items():
            if name.startswith("test_"):
                with self.subTest(scenario=name):
                    self.assertGreaterEqual(len(scenario["seeds"]), 3)
                    self.assertFalse(dev_seeds & set(scenario["seeds"]))

    def test_training_scenarios_are_valid_and_reproducible(self) -> None:
        demand = TRAINING["demand"]
        groups = SCENARIOS["route_groups"]
        draws_a = [sample_training_scenario(rng, demand, groups) for rng in [random.Random(3)] for _ in range(60)]
        draws_b = [sample_training_scenario(rng, demand, groups) for rng in [random.Random(3)] for _ in range(60)]

        self.assertEqual(draws_a, draws_b)
        self.assertEqual({draw["profile"] for draw in draws_a}, set(demand["profiles"]))

        for draw in draws_a:
            with self.subTest(profile=draw["profile"], seed=draw["seed"]):
                validate_scenario("draw", draw, set(SCENARIOS["routes"]))
                intervals = draw["intervals"]

                # Intervals cover the whole episode without gaps.
                self.assertEqual(intervals[0]["begin_s"], 0)
                self.assertEqual(intervals[-1]["end_s"], demand["episode_length_s"])
                for before, after in zip(intervals, intervals[1:]):
                    self.assertEqual(before["end_s"], after["begin_s"])

                for interval in intervals:
                    self.assertEqual(set(interval["flows_vph"]), set(SCENARIOS["routes"]))

                if draw["profile"] in ("ew_heavy", "ns_heavy", "shift"):
                    busy = [self._busier_group(interval["flows_vph"], groups) for interval in intervals]
                    if draw["profile"] == "shift":
                        self.assertEqual(len(intervals), 2)
                        self.assertNotEqual(busy[0], busy[1])
                    else:
                        expected = "east_west" if draw["profile"] == "ew_heavy" else "north_south"
                        self.assertEqual(busy, [expected])

    @staticmethod
    def _busier_group(flows: dict, groups: dict) -> str:
        # Heavy routes are always busier than light ones, even after jitter.
        lowest = {group: min(flows[route] for route in routes) for group, routes in groups.items()}
        highest = {group: max(flows[route] for route in routes) for group, routes in groups.items()}
        for group in groups:
            if all(lowest[group] > highest[other] for other in groups if other != group):
                return group
        return "none"


if __name__ == "__main__":
    unittest.main()
