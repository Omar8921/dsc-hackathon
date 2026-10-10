"""Raw traffic-state data structures and the builder that fills them."""

from collections import deque
from dataclasses import asdict, dataclass


SCHEMA_VERSION = "1.0"
APPROACH_ORDER = ("N", "E", "S", "W")

# The design counts vehicles below 0.1 m/s as queued, matching SUMO's halting rule.
HALTING_SPEED_MPS = 0.1


@dataclass
class ApproachState:
    vehicle_count: int
    queue_count: int
    occupancy: float
    arrival_rate_vps: float
    mean_wait_s: float
    mean_speed_mps: float
    downstream_occupancy: float
    storage_capacity: int
    speed_limit_mps: float
    measurement_valid: bool = True


@dataclass
class NeighborState:
    present: bool
    intersection_id: str | None
    normalized_queue: float
    mean_occupancy: float


@dataclass
class SignalState:
    # Action index of the current green, or of the last green during a transition.
    active_green_phase: int
    # "green", "yellow", or "all_red".
    transition_state: str
    # How long the current green has been shown; 0 during a transition.
    elapsed_green_s: float


@dataclass
class IntersectionState:
    sim_time_s: float
    intersection_id: str
    signal: SignalState
    approaches: dict[str, ApproachState]
    neighbors: dict[str, NeighborState]
    source: str = "sumo"
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict:
        return asdict(self)


class StateBuilder:
    """Turn per-step SUMO readings into one IntersectionState per intersection.

    Call update() once per simulation step: arrival rates and green timers
    depend on consecutive readings.
    """

    def __init__(
        self,
        intersections_config: dict,
        arrival_window_s: float,
        lane_geometry: dict[str, dict],
    ) -> None:
        self.intersections = intersections_config["intersections"]
        self.arrival_window_s = arrival_window_s
        self.lane_geometry = lane_geometry
        self._previous_ids: dict[tuple[str, str], set[str]] = {}
        self._arrivals: dict[tuple[str, str], deque] = {}
        self._phase: dict[str, int] = {}
        self._green_start_s: dict[str, float] = {}

    def update(
        self,
        time_s: float,
        lanes: dict[str, dict],
        vehicles: list[dict],
        signals: list[dict],
    ) -> dict[str, IntersectionState]:
        """Build the state of every configured intersection for this step."""

        vehicles_by_lane: dict[str, list[dict]] = {}

        for vehicle in vehicles:
            vehicles_by_lane.setdefault(vehicle["lane"], []).append(vehicle)

        phases = {signal["id"]: signal["phase"] for signal in signals}

        # Approaches first, because neighbor summaries read other intersections.
        approaches = {
            node_id: {
                slot: self._approach(
                    (node_id, slot),
                    node["approaches"][slot],
                    time_s,
                    lanes,
                    vehicles_by_lane,
                )
                for slot in APPROACH_ORDER
            }
            for node_id, node in self.intersections.items()
        }

        return {
            node_id: IntersectionState(
                sim_time_s=time_s,
                intersection_id=node_id,
                signal=self._signal(node_id, node, phases[node["signal_id"]], time_s),
                approaches=approaches[node_id],
                neighbors={
                    slot: self._neighbor(node["approaches"][slot]["neighbor"], approaches)
                    for slot in APPROACH_ORDER
                },
            )
            for node_id, node in self.intersections.items()
        }

    def _approach(
        self,
        key: tuple[str, str],
        approach: dict,
        time_s: float,
        lanes: dict[str, dict],
        vehicles_by_lane: dict[str, list[dict]],
    ) -> ApproachState:
        incoming = approach["incoming_lanes"]
        on_approach = [
            vehicle for lane_id in incoming for vehicle in vehicles_by_lane.get(lane_id, [])
        ]
        count = len(on_approach)
        speed_limit = max(self.lane_geometry[lane_id]["speed_limit_mps"] for lane_id in incoming)

        # IDs are compared across all of the approach's lanes, so a lane change
        # within the approach is not counted as an arrival.
        ids = {vehicle["id"] for vehicle in on_approach}
        arrivals = self._arrivals.setdefault(key, deque())
        arrivals.append((time_s, len(ids - self._previous_ids.get(key, set()))))
        self._previous_ids[key] = ids

        while arrivals and arrivals[0][0] <= time_s - self.arrival_window_s:
            arrivals.popleft()

        return ApproachState(
            vehicle_count=count,
            queue_count=sum(
                1 for vehicle in on_approach if vehicle["speed_mps"] < HALTING_SPEED_MPS
            ),
            occupancy=self._occupancy(incoming, lanes),
            arrival_rate_vps=sum(new for _, new in arrivals) / self.arrival_window_s,
            mean_wait_s=(
                sum(vehicle["waiting_s"] for vehicle in on_approach) / count if count else 0.0
            ),
            # An empty approach reports free-flow speed.
            mean_speed_mps=(
                sum(vehicle["speed_mps"] for vehicle in on_approach) / count
                if count
                else speed_limit
            ),
            downstream_occupancy=self._occupancy(approach["receiving_lanes"], lanes),
            storage_capacity=approach["storage_capacity"],
            speed_limit_mps=speed_limit,
        )

    def _occupancy(self, lane_ids: list[str], lanes: dict[str, dict]) -> float:
        """Return lane-length-weighted occupancy over the given lanes."""

        lengths = [self.lane_geometry[lane_id]["length_m"] for lane_id in lane_ids]
        occupied = sum(
            lanes[lane_id]["occupancy"] * length for lane_id, length in zip(lane_ids, lengths)
        )

        return occupied / sum(lengths)

    @staticmethod
    def _neighbor(
        neighbor_id: str | None, approaches: dict[str, dict[str, ApproachState]]
    ) -> NeighborState:
        if neighbor_id is None:
            return NeighborState(
                present=False, intersection_id=None, normalized_queue=0.0, mean_occupancy=0.0
            )

        neighbor = list(approaches[neighbor_id].values())
        storage = sum(approach.storage_capacity for approach in neighbor)

        return NeighborState(
            present=True,
            intersection_id=neighbor_id,
            normalized_queue=sum(approach.queue_count for approach in neighbor) / storage,
            # Plain mean over the neighbor's four approaches.
            mean_occupancy=sum(approach.occupancy for approach in neighbor) / len(neighbor),
        )

    def _signal(self, node_id: str, node: dict, phase: int, time_s: float) -> SignalState:
        # Read signal state from the phase SUMO actually showed, using the
        # configured mapping, so it reflects what drivers saw.
        for action in node["actions"]:
            kinds = {
                action["green_phase"]: "green",
                action["yellow_phase"]: "yellow",
                action["all_red_phase"]: "all_red",
            }

            if phase in kinds:
                break
        else:
            raise ValueError(
                f"{node_id}: signal phase {phase} is not mapped in configs/intersections.json."
            )

        transition_state = kinds[phase]

        if transition_state == "green" and self._phase.get(node_id) != phase:
            self._green_start_s[node_id] = time_s

        self._phase[node_id] = phase

        return SignalState(
            active_green_phase=action["action"],
            transition_state=transition_state,
            elapsed_green_s=(
                time_s - self._green_start_s[node_id] if transition_state == "green" else 0.0
            ),
        )
