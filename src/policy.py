"""Shared actor-critic network and parameter-sharing independent PPO.

Every intersection uses the same network but gets its own observation and
samples its own action. Each intersection keeps its own trajectory; advantages
are computed along it, then all trajectories are pooled into one update.
"""

import math
import time
from pathlib import Path

import torch
from torch import nn
from torch.distributions import Categorical

from src.observations import OBSERVATION_FIELDS


GREEN_PHASE_FIELDS = [OBSERVATION_FIELDS.index("signal.green_phase_0"), OBSERVATION_FIELDS.index("signal.green_phase_1")]


class ActorCritic(nn.Module):
    """Categorical actor and value head, each a two-layer MLP."""

    def __init__(self, observation_size: int, action_count: int, hidden_size: int = 64) -> None:
        super().__init__()

        def mlp(output_size: int, output_gain: float) -> nn.Sequential:
            layers = [
                nn.Linear(observation_size, hidden_size),
                nn.Tanh(),
                nn.Linear(hidden_size, hidden_size),
                nn.Tanh(),
                nn.Linear(hidden_size, output_size),
            ]

            # Orthogonal initialization; a small actor output gain starts
            # the policy close to uniform.
            for layer in layers:
                if isinstance(layer, nn.Linear):
                    gain = output_gain if layer is layers[-1] else math.sqrt(2)
                    nn.init.orthogonal_(layer.weight, gain)
                    nn.init.zeros_(layer.bias)

            return nn.Sequential(*layers)

        self.actor = mlp(action_count, 0.01)
        self.critic = mlp(1, 1.0)

    def distribution(self, observations: torch.Tensor) -> Categorical:
        return Categorical(logits=self.actor(observations))

    def value(self, observations: torch.Tensor) -> torch.Tensor:
        return self.critic(observations).squeeze(-1)

    @torch.no_grad()
    def act(self, observations: torch.Tensor, deterministic: bool = False):
        """Return actions, their log probabilities, and state values."""

        dist = self.distribution(observations)
        actions = dist.probs.argmax(-1) if deterministic else dist.sample()
        return actions, dist.log_prob(actions), self.value(observations)

    def evaluate(self, observations: torch.Tensor, actions: torch.Tensor):
        """Return log probabilities, entropy, and values for stored actions."""

        dist = self.distribution(observations)
        return dist.log_prob(actions), dist.entropy(), self.value(observations)


def compute_gae(
    rewards: list[float],
    values: list[float],
    last_value: float,
    gamma: float,
    gae_lambda: float,
    terminated: bool = False,
) -> tuple[list[float], list[float]]:
    """Return advantages and returns for one agent's trajectory.

    A time-limit truncation bootstraps from last_value, the value of the
    final observation; a real termination does not.
    """

    advantages = [0.0] * len(rewards)
    next_value = 0.0 if terminated else last_value
    running = 0.0

    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * next_value - values[t]
        running = delta + gamma * gae_lambda * running
        advantages[t] = running
        next_value = values[t]

    returns = [advantage + value for advantage, value in zip(advantages, values)]
    return advantages, returns


def collect_episode(env, model: ActorCritic, sumocfg_path: Path, intersections_config: dict, ppo: dict):
    """Run one episode with the current policy.

    Returns the pooled transitions of every agent and episode statistics. The
    stored action is the one the policy sampled, even when the safety
    controller did not apply it.
    """

    started = time.perf_counter()
    observations = env.reset(sumocfg_path, intersections_config)
    agent_ids = env.agent_ids
    trajectories = {
        agent_id: {"observations": [], "actions": [], "log_probs": [], "values": [], "rewards": []}
        for agent_id in agent_ids
    }
    infos = []
    switch_requests = 0

    while True:
        batch = torch.tensor([observations[agent_id] for agent_id in agent_ids], dtype=torch.float32)
        actions, log_probs, values = model.act(batch)
        result = env.step({agent_id: int(actions[i]) for i, agent_id in enumerate(agent_ids)})

        for i, agent_id in enumerate(agent_ids):
            trajectory = trajectories[agent_id]
            trajectory["observations"].append(observations[agent_id])
            trajectory["actions"].append(int(actions[i]))
            trajectory["log_probs"].append(float(log_probs[i]))
            trajectory["values"].append(float(values[i]))
            # Every agent receives the same team reward.
            trajectory["rewards"].append(result.reward)

            current_green = max(GREEN_PHASE_FIELDS, key=lambda field: observations[agent_id][field])
            if int(actions[i]) != GREEN_PHASE_FIELDS.index(current_green):
                switch_requests += 1

        infos.append(result.info)
        observations = result.observations

        if result.truncated:
            break

    # The episode ended at its time limit, so bootstrap from the final state.
    final = torch.tensor([observations[agent_id] for agent_id in agent_ids], dtype=torch.float32)

    with torch.no_grad():
        last_values = model.value(final).tolist()

    pooled = {"observations": [], "actions": [], "log_probs": [], "values": [], "advantages": [], "returns": []}

    for i, agent_id in enumerate(agent_ids):
        trajectory = trajectories[agent_id]
        advantages, returns = compute_gae(
            trajectory["rewards"], trajectory["values"], last_values[i], ppo["gamma"], ppo["gae_lambda"]
        )

        for key in ("observations", "actions", "log_probs", "values"):
            pooled[key].extend(trajectory[key])

        pooled["advantages"].extend(advantages)
        pooled["returns"].extend(returns)

    decisions = len(infos)
    rewards = trajectories[agent_ids[0]]["rewards"]
    stats = {
        "decisions": decisions,
        "mean_reward": sum(rewards) / decisions,
        "mean_normalized_queue": sum(info["mean_normalized_queue"] for info in infos) / decisions,
        "congested_receiving_fraction": sum(info["congested_receiving_fraction"] for info in infos) / decisions,
        "switch_request_rate": switch_requests / (decisions * len(agent_ids)),
        "overrides": sum(info["overrides"] for info in infos),
        "sim_seconds": infos[-1]["time_s"],
        "wall_seconds": time.perf_counter() - started,
    }

    return pooled, stats


def ppo_update(
    model: ActorCritic,
    optimizer: torch.optim.Optimizer,
    pooled: dict,
    ppo: dict,
    generator: torch.Generator,
) -> dict:
    """Run clipped PPO epochs over the pooled transitions of every agent."""

    observations = torch.tensor(pooled["observations"], dtype=torch.float32)
    actions = torch.tensor(pooled["actions"], dtype=torch.long)
    old_log_probs = torch.tensor(pooled["log_probs"], dtype=torch.float32)
    returns = torch.tensor(pooled["returns"], dtype=torch.float32)
    advantages = torch.tensor(pooled["advantages"], dtype=torch.float32)
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    count = len(actions)
    clip = ppo["clip_range"]
    totals = {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0, "approx_kl": 0.0, "clip_fraction": 0.0}
    batches = 0

    for _ in range(ppo["epochs"]):
        order = torch.randperm(count, generator=generator)

        for start in range(0, count, ppo["minibatch_size"]):
            index = order[start:start + ppo["minibatch_size"]]
            log_probs, entropy, values = model.evaluate(observations[index], actions[index])

            log_ratio = log_probs - old_log_probs[index]
            ratio = log_ratio.exp()
            advantage = advantages[index]

            policy_loss = -torch.min(ratio * advantage, ratio.clamp(1 - clip, 1 + clip) * advantage).mean()
            value_loss = (returns[index] - values).pow(2).mean()
            loss = policy_loss + ppo["value_coef"] * value_loss - ppo["entropy_coef"] * entropy.mean()

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), ppo["max_grad_norm"])
            optimizer.step()

            with torch.no_grad():
                totals["policy_loss"] += policy_loss.item()
                totals["value_loss"] += value_loss.item()
                totals["entropy"] += entropy.mean().item()
                totals["approx_kl"] += ((ratio - 1) - log_ratio).mean().item()
                totals["clip_fraction"] += ((ratio - 1).abs() > clip).float().mean().item()

            batches += 1

    return {key: value / batches for key, value in totals.items()}


def save_checkpoint(path: Path, model: ActorCritic, optimizer: torch.optim.Optimizer, metadata: dict) -> None:
    torch.save(
        {"model": model.state_dict(), "optimizer": optimizer.state_dict(), "metadata": metadata},
        path,
    )


def load_policy(path: Path) -> tuple[ActorCritic, dict]:
    """Load a saved policy for evaluation; metadata holds sizes and settings."""

    checkpoint = torch.load(path, map_location="cpu")
    metadata = checkpoint["metadata"]
    model = ActorCritic(metadata["observation_size"], metadata["action_count"], metadata["hidden_size"])
    model.load_state_dict(checkpoint["model"])
    model.eval()
    return model, metadata
