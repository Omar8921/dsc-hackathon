"""Synchronous multi-intersection environment and the team reward.

One SUMO process owns the clock. At each decision boundary every intersection
submits a request; the safety controller applies them; the shared simulation
then runs for one decision interval in 1 s steps. Every agent receives the
same team reward, averaged over that interval.
"""

from dataclasses import dataclass
from pathlib import Path

from src.observations import build_observation, observation_settings
from src.safety_controller import SafetyController
from src.simulation_adapter import SimulationAdapter
from src.state import IntersectionState, StateBuilder


def team_reward(states: dict[str, IntersectionState], reward_config: dict) -> tuple[float, dict]:
    """Return one step's team reward and its two terms.

    reward = -(mean normalized queue + congestion_weight * congested receiving fraction)

    SUMO's lane occupancy counts vehicle lengths only, so a fully jammed lane
    reads about length / (length + minGap). A receiving lane counts as
    congested above congestion_threshold of that jam occupancy.
    """

    approaches = [approach for state in states.values() for approach in state.approaches.values()]
    threshold = reward_config["congestion_threshold"] * reward_config["jam_occupancy"]

    mean_queue = sum(a.queue_count / a.storage_capacity for a in approaches) / len(approaches)
    congested = sum(1 for a in approaches if a.downstream_occupancy > threshold) / len(approaches)

    reward = -(mean_queue + reward_config["congestion_weight"] * congested)
    return reward, {"mean_normalized_queue": mean_queue, "congested_receiving_fraction": congested}


@dataclass
class StepResult:
    observations: dict[str, list[float]]
    reward: float
    # The episode reached its time limit; not a terminal state of the task.
    truncated: bool
    info: dict


class TrafficSignalEnv:
    """Shared-clock environment for every intersection in one SUMO network."""

    def __init__(self, controller_config: dict, reward_config: dict, quiet: bool = True) -> None:
        self.controller_config = controller_config
        self.reward_config = reward_config
        self.quiet = quiet
        self.decision_interval_s = controller_config["policy"]["decision_interval_s"]
        self.settings = observation_settings(controller_config)
        self.adapter: SimulationAdapter | None = None
        self.agent_ids: list[str] = []
        self.phase_log: dict[str, list[int]] = {}

    def reset(self, sumocfg_path: Path, intersections_config: dict) -> dict[str, list[float]]:
        """Start a new episode and return every agent's first observation."""

        self.close()
        self.intersections_config = intersections_config
        self.agent_ids = sorted(intersections_config["intersections"])

        self.adapter = SimulationAdapter(sumocfg_path, quiet=self.quiet)
        self.adapter.start()

        geometry = {lane["id"]: lane for lane in self.adapter.read_network()["lanes"]}
        self.builder = StateBuilder(
            intersections_config,
            self.controller_config["observation"]["arrival_window_s"],
            geometry,
        )
        self.safety = SafetyController(
            self.adapter, intersections_config, self.controller_config["safety"], self.adapter.time_s()
        )
        # Phase shown during each step, for safety audits.
        self.phase_log = {signal_id: [] for signal_id in self.adapter.signal_ids}
        self.states = self._read_states()

        return self._observations()

    def step(self, actions: dict[str, int]) -> StepResult:
        """Apply every agent's request, then run one decision interval."""

        time_s = self.adapter.time_s()
        records_before = len(self.safety.records)

        # Every intersection's request is submitted before the clock advances.
        self.safety.begin_step(time_s)

        for agent_id in self.agent_ids:
            # A missing action reaches the safety controller as invalid.
            self.safety.request(agent_id, actions.get(agent_id), time_s)

        rewards = []
        queues = []
        congestion = []

        while True:
            self.safety.apply()

            for signal_id, phase in self.adapter.read_phases().items():
                self.phase_log[signal_id].append(phase)

            self.adapter.step()
            self.states = self._read_states()

            reward, terms = team_reward(self.states, self.reward_config)
            rewards.append(reward)
            queues.append(terms["mean_normalized_queue"])
            congestion.append(terms["congested_receiving_fraction"])

            elapsed_s = len(rewards) * self.adapter.step_length_s

            if self.adapter.finished() or elapsed_s >= self.decision_interval_s - 1e-9:
                break

            self.safety.begin_step(self.adapter.time_s())

        new_records = self.safety.records[records_before:]

        return StepResult(
            observations=self._observations(),
            reward=sum(rewards) / len(rewards),
            truncated=self.adapter.finished(),
            info={
                "time_s": self.adapter.time_s(),
                "mean_normalized_queue": sum(queues) / len(queues),
                "congested_receiving_fraction": sum(congestion) / len(congestion),
                "overrides": sum(1 for record in new_records if record.override_reason),
            },
        )

    def close(self) -> None:
        if self.adapter is not None:
            self.adapter.close()
            self.adapter = None

    def _read_states(self) -> dict[str, IntersectionState]:
        return self.builder.update(
            self.adapter.time_s(),
            self.adapter.read_lanes(),
            self.adapter.read_vehicles(),
            self.adapter.read_signals(),
        )

    def _observations(self) -> dict[str, list[float]]:
        return {
            agent_id: build_observation(self.states[agent_id], self.settings)
            for agent_id in self.agent_ids
        }
