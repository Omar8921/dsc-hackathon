"""Check the shared policy network, GAE, PPO updates, and checkpoints."""

import tempfile
import unittest
from pathlib import Path

import torch

from src.policy import ActorCritic, compute_gae, load_policy, ppo_update, save_checkpoint


PPO = {
    "hidden_size": 64,
    "learning_rate": 0.001,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "entropy_coef": 0.0,
    "value_coef": 0.5,
    "epochs": 10,
    "minibatch_size": 64,
    "max_grad_norm": 0.5,
}


class PolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(0)
        self.model = ActorCritic(44, 2, 64)

    def test_act_returns_valid_actions(self) -> None:
        observations = torch.rand(5, 44)
        actions, log_probs, values = self.model.act(observations)

        self.assertEqual(actions.shape, (5,))
        self.assertTrue(set(actions.tolist()) <= {0, 1})
        self.assertTrue(bool((log_probs <= 0).all()))
        self.assertEqual(values.shape, (5,))

    def test_evaluate_matches_act(self) -> None:
        observations = torch.rand(8, 44)
        actions, log_probs, _ = self.model.act(observations)
        evaluated, entropy, _ = self.model.evaluate(observations, actions)

        self.assertTrue(torch.allclose(evaluated, log_probs))
        self.assertTrue(bool((entropy > 0).all()))

    def test_initial_policy_is_close_to_uniform(self) -> None:
        probs = self.model.distribution(torch.rand(16, 44)).probs
        self.assertTrue(torch.allclose(probs, torch.full_like(probs, 0.5), atol=0.05))

    def test_gae_bootstraps_truncation_but_not_termination(self) -> None:
        # Hand-computed with gamma 0.9 and lambda 0.5.
        advantages, returns = compute_gae([1.0, 1.0], [0.5, 0.5], 2.0, 0.9, 0.5)
        self.assertEqual([round(a, 6) for a in advantages], [1.985, 2.3])
        self.assertEqual([round(r, 6) for r in returns], [2.485, 2.8])

        advantages, _ = compute_gae([1.0, 1.0], [0.5, 0.5], 2.0, 0.9, 0.5, terminated=True)
        self.assertEqual([round(a, 6) for a in advantages], [1.175, 0.5])

    def test_ppo_learns_an_observation_dependent_choice(self) -> None:
        # Action 1 is good when feature 0 is 1, action 0 when it is 0.
        optimizer = torch.optim.Adam(self.model.parameters(), lr=PPO["learning_rate"])
        generator = torch.Generator().manual_seed(0)

        for _ in range(15):
            observations = torch.rand(256, 44)
            observations[:, 0] = torch.randint(0, 2, (256,)).float()
            actions, log_probs, values = self.model.act(observations)
            advantages = torch.where(actions == observations[:, 0].long(), 1.0, -1.0)
            pooled = {
                "observations": observations.tolist(),
                "actions": actions.tolist(),
                "log_probs": log_probs.tolist(),
                "values": values.tolist(),
                "advantages": advantages.tolist(),
                "returns": advantages.tolist(),
            }
            losses = ppo_update(self.model, optimizer, pooled, PPO, generator)
            self.assertTrue(all(torch.isfinite(torch.tensor(v)) for v in losses.values()))

        probe = torch.rand(200, 44)
        probe[:100, 0] = 1.0
        probe[100:, 0] = 0.0
        probs = self.model.distribution(probe).probs

        self.assertGreater(probs[:100, 1].mean().item(), 0.8)
        self.assertGreater(probs[100:, 0].mean().item(), 0.8)

    def test_checkpoint_round_trip(self) -> None:
        optimizer = torch.optim.Adam(self.model.parameters())
        observations = torch.rand(10, 44)

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "checkpoint.pt"
            save_checkpoint(path, self.model, optimizer, {"observation_size": 44, "action_count": 2, "hidden_size": 64})
            loaded, metadata = load_policy(path)

        self.assertEqual(metadata["action_count"], 2)
        self.assertTrue(torch.allclose(loaded.distribution(observations).probs, self.model.distribution(observations).probs))
        self.assertTrue(torch.allclose(loaded.value(observations), self.model.value(observations)))


if __name__ == "__main__":
    unittest.main()
