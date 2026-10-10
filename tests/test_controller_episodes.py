"""Run full SUMO episodes with each baseline and check safety and metrics.

This test starts SUMO four times, so it takes several seconds.
"""

import json
import tempfile
import unittest
from pathlib import Path

from src.runner import BASELINES, run_episode


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("balanced", "ew_heavy")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class ControllerEpisodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.intersections = load_json(PROJECT_ROOT / "configs" / "intersections.json")
        cls.controller_config = load_json(PROJECT_ROOT / "configs" / "controller.json")

    def test_baselines_complete_scenarios_with_legal_transitions(self) -> None:
        for controller in BASELINES:
            for scenario in SCENARIOS:
                with self.subTest(controller=controller, scenario=scenario):
                    with tempfile.TemporaryDirectory() as folder:
                        output_dir = Path(folder)
                        summary = run_episode(
                            PROJECT_ROOT / "simulation" / "scenarios" / f"{scenario}.sumocfg",
                            {"run_id": "test", "scenario": scenario, "controller": controller},
                            self.intersections,
                            self.controller_config,
                            output_dir,
                            quiet=True,
                        )
                        self.assertTrue((output_dir / "metrics.json").is_file())

                    trips = summary["trips"]
                    safety = summary["safety"]

                    self.assertEqual(safety["illegal_transitions"], 0, safety["violations"])
                    self.assertEqual(trips["teleports"], 0)
                    self.assertGreater(trips["completed"], 0)
                    # Every vehicle that departed either finished or is still driving.
                    self.assertEqual(trips["departed"], trips["completed"] + trips["still_running"])
                    self.assertIsNotNone(summary["completed_trips"]["waiting_s"])
                    self.assertEqual(set(summary["queues"]), set(self.intersections["intersections"]))


if __name__ == "__main__":
    unittest.main()
