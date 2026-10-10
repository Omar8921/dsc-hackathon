"""Check the team reward against hand-computed values."""

import json
import unittest
from pathlib import Path

from src.rl_environment import team_reward
from src.state import APPROACH_ORDER, ApproachState, IntersectionState, NeighborState, SignalState


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REWARD = {"congestion_weight": 0.25, "congestion_threshold": 0.8, "jam_occupancy": 0.667}


def make_state(queues: list[int], downstream: list[float]) -> IntersectionState:
    approaches = {
        slot: ApproachState(
            vehicle_count=queue,
            queue_count=queue,
            occupancy=0.0,
            arrival_rate_vps=0.0,
            mean_wait_s=0.0,
            mean_speed_mps=13.89,
            downstream_occupancy=occupancy,
            storage_capacity=25,
            speed_limit_mps=13.89,
        )
        for slot, queue, occupancy in zip(APPROACH_ORDER, queues, downstream)
    }
    return IntersectionState(
        sim_time_s=0.0,
        intersection_id="X",
        signal=SignalState(0, "green", 0.0),
        approaches=approaches,
        neighbors={slot: NeighborState(False, None, 0.0, 0.0) for slot in APPROACH_ORDER},
    )


class TeamRewardTest(unittest.TestCase):
    def test_reward_combines_queue_and_congestion(self) -> None:
        states = {
            "A": make_state([5, 0, 10, 0], [0.0, 0.6, 0.2, 0.0]),
            "B": make_state([0, 0, 0, 0], [0.0, 0.0, 0.0, 0.0]),
        }
        reward, terms = team_reward(states, REWARD)

        # Queue: (5/25 + 10/25) over 8 approaches. Congestion: 0.6 is above
        # 0.8 * 0.667 = 0.534, so 1 of 8 receiving lanes is congested.
        self.assertAlmostEqual(terms["mean_normalized_queue"], 0.075)
        self.assertAlmostEqual(terms["congested_receiving_fraction"], 0.125)
        self.assertAlmostEqual(reward, -(0.075 + 0.25 * 0.125))

    def test_empty_network_has_zero_reward(self) -> None:
        reward, _ = team_reward({"A": make_state([0] * 4, [0.0] * 4)}, REWARD)
        self.assertEqual(reward, 0.0)

    def test_jam_occupancy_matches_the_demand_vehicle(self) -> None:
        training = json.loads((PROJECT_ROOT / "configs" / "training.json").read_text(encoding="utf-8-sig"))
        scenarios = json.loads((PROJECT_ROOT / "configs" / "scenarios.json").read_text(encoding="utf-8-sig"))
        vehicle = scenarios["vehicle_type"]

        self.assertAlmostEqual(
            training["reward"]["jam_occupancy"],
            vehicle["length"] / (vehicle["length"] + vehicle["minGap"]),
            places=3,
        )


if __name__ == "__main__":
    unittest.main()
