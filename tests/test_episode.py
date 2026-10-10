"""Run full headless episodes and check every intersection's state and observation.

This test starts SUMO, so it takes a few seconds.
"""

import json
import unittest
from pathlib import Path

from src.observations import (
    OBSERVATION_FIELDS,
    OBSERVATION_SIZE,
    build_observation,
    observation_settings,
)
from src.simulation_adapter import SimulationAdapter
from src.state import StateBuilder


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("balanced", "ew_heavy")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class EpisodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.intersections = load_json(PROJECT_ROOT / "configs" / "intersections.json")
        controller = load_json(PROJECT_ROOT / "configs" / "controller.json")
        cls.arrival_window_s = controller["observation"]["arrival_window_s"]
        cls.settings = observation_settings(controller)

    def test_every_intersection_produces_valid_observations(self) -> None:
        for scenario in SCENARIOS:
            with self.subTest(scenario=scenario):
                self._check_episode(
                    PROJECT_ROOT / "simulation" / "scenarios" / f"{scenario}.sumocfg"
                )

    def _check_episode(self, sumocfg_path: Path) -> None:
        nodes = self.intersections["intersections"]
        peak_queue = dict.fromkeys(nodes, 0)
        greens_seen = {node_id: set() for node_id in nodes}
        steps = 0

        adapter = SimulationAdapter(sumocfg_path, quiet=True)
        adapter.start()

        try:
            geometry = {lane["id"]: lane for lane in adapter.read_network()["lanes"]}
            builder = StateBuilder(self.intersections, self.arrival_window_s, geometry)

            while True:
                states = builder.update(
                    adapter.time_s(),
                    adapter.read_lanes(),
                    adapter.read_vehicles(),
                    adapter.read_signals(),
                )
                self.assertEqual(set(states), set(nodes))

                for node_id, state in states.items():
                    observation = build_observation(state, self.settings)
                    self.assertEqual(len(observation), OBSERVATION_SIZE)

                    for name, value in zip(OBSERVATION_FIELDS, observation):
                        if not 0.0 <= value <= 1.0:
                            self.fail(f"{node_id} at {state.sim_time_s} s: {name} = {value}")

                    for slot, approach in state.approaches.items():
                        if not 0 <= approach.queue_count <= approach.vehicle_count:
                            self.fail(f"{node_id} {slot} at {state.sim_time_s} s: bad counts")
                        peak_queue[node_id] = max(peak_queue[node_id], approach.queue_count)

                    for slot, neighbor in state.neighbors.items():
                        expected = nodes[node_id]["approaches"][slot]["neighbor"]
                        self.assertEqual(neighbor.intersection_id, expected)
                        self.assertEqual(neighbor.present, expected is not None)

                    if state.signal.transition_state == "green":
                        greens_seen[node_id].add(state.signal.active_green_phase)

                steps += 1

                if adapter.finished():
                    break

                adapter.step()
        finally:
            adapter.close()

        # One state at time 0, then one after every step up to the end time.
        self.assertEqual(steps, round(adapter.end_time_s / adapter.step_length_s) + 1)

        # The measurements are live: queues form and both greens are shown.
        for node_id in nodes:
            self.assertGreater(peak_queue[node_id], 0, node_id)
            self.assertEqual(greens_seen[node_id], {0, 1}, node_id)


if __name__ == "__main__":
    unittest.main()
