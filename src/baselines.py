"""Fixed-time and actuated baselines.

Both return phase requests that go through the same safety controller as the
learned policy. They decide every simulation step and only request a switch;
holding the current green needs no request.
"""

from src.state import SignalState


class FixedTimeController:
    """Switch to the next phase once the current green has run green_s."""

    def __init__(self, intersections_config: dict, green_s: float) -> None:
        self.intersections = intersections_config["intersections"]
        self.green_s = green_s

    def requests(
        self,
        time_s: float,
        signal_states: dict[str, SignalState],
        vehicles: list[dict],
        states: dict | None = None,
    ) -> dict[str, int]:
        requests = {}

        for node_id, signal in signal_states.items():
            if signal.transition_state == "green" and signal.elapsed_green_s >= self.green_s:
                action_count = len(self.intersections[node_id]["actions"])
                requests[node_id] = (signal.active_green_phase + 1) % action_count

        return requests


class ActuatedController:
    """Gap-based actuation using virtual detectors near each stop line.

    After minimum green, switch when no vehicle on the served approaches is
    within detector_distance_m of the stop line while another phase has one.
    Maximum green is left to the safety controller.
    """

    def __init__(
        self,
        intersections_config: dict,
        lane_geometry: dict[str, dict],
        min_green_s: float,
        detector_distance_m: float,
    ) -> None:
        self.intersections = intersections_config["intersections"]
        self.lane_geometry = lane_geometry
        self.min_green_s = min_green_s
        self.detector_distance_m = detector_distance_m

    def requests(
        self,
        time_s: float,
        signal_states: dict[str, SignalState],
        vehicles: list[dict],
        states: dict | None = None,
    ) -> dict[str, int]:
        # Vehicles inside each lane's detector zone, keyed by lane.
        detected: dict[str, int] = {}

        for vehicle in vehicles:
            lane = self.lane_geometry.get(vehicle["lane"])

            if lane and lane["length_m"] - vehicle["lane_position_m"] <= self.detector_distance_m:
                detected[vehicle["lane"]] = detected.get(vehicle["lane"], 0) + 1

        requests = {}

        for node_id, signal in signal_states.items():
            if signal.transition_state != "green" or signal.elapsed_green_s < self.min_green_s:
                continue

            node = self.intersections[node_id]
            demand = [
                sum(
                    detected.get(lane_id, 0)
                    for slot in action["served_approaches"]
                    for lane_id in node["approaches"][slot]["incoming_lanes"]
                )
                for action in node["actions"]
            ]
            active = signal.active_green_phase
            waiting = [i for i, calls in enumerate(demand) if calls > 0 and i != active]

            if demand[active] == 0 and waiting:
                requests[node_id] = max(waiting, key=lambda i: demand[i])

        return requests
