"""Run one full training episode in SUMO and one PPO update.

This test starts SUMO, so it takes a few seconds.
"""

import json
import math
import unittest
from pathlib import Path

import torch

from src.observations import OBSERVATION_SIZE
from src.policy import ActorCritic, collect_episode, ppo_update
from src.rl_environment import TrafficSignalEnv
from src.safety_controller import audit_phase_timeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class TrainingEpisodeTest(unittest.TestCase):
    def test_one_episode_and_one_update(self) -> None:
        controller = load_json(PROJECT_ROOT / "configs" / "controller.json")
        training = load_json(PROJECT_ROOT / "configs" / "training.json")
        intersections = load_json(PROJECT_ROOT / "configs" / "intersections.json")
        ppo = training["ppo"]

        torch.manual_seed(0)
        model = ActorCritic(OBSERVATION_SIZE, 2, ppo["hidden_size"])
        env = TrafficSignalEnv(controller, training["reward"], quiet=True)

        try:
            pooled, stats = collect_episode(
                env, model, PROJECT_ROOT / "simulation" / "scenarios" / "ew_heavy.sumocfg", intersections, ppo
            )
        finally:
            env.close()

        agents = len(intersections["intersections"])
        decisions = 900 // controller["policy"]["decision_interval_s"]

        self.assertEqual(stats["decisions"], decisions)
        self.assertEqual(len(pooled["actions"]), decisions * agents)
        self.assertTrue(all(len(observation) == OBSERVATION_SIZE for observation in pooled["observations"]))
        self.assertLessEqual(stats["mean_reward"], 0.0)
        self.assertTrue(all(math.isfinite(value) for value in pooled["returns"]))

        # A random policy's requests still produce only legal transitions.
        for node_id, node in intersections["intersections"].items():
            with self.subTest(intersection=node_id):
                violations = audit_phase_timeline(
                    env.phase_log[node["signal_id"]], node["actions"], controller["safety"], 1.0
                )
                self.assertEqual(violations, [])

        before = [parameter.clone() for parameter in model.parameters()]
        optimizer = torch.optim.Adam(model.parameters(), lr=ppo["learning_rate"])
        losses = ppo_update(model, optimizer, pooled, ppo, torch.Generator().manual_seed(0))

        self.assertTrue(all(math.isfinite(value) for value in losses.values()))
        self.assertTrue(any(not torch.equal(a, b) for a, b in zip(before, model.parameters())))


if __name__ == "__main__":
    unittest.main()
