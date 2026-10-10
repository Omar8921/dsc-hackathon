"""Common evaluation metrics, computed the same way for every controller."""

import math
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from src.safety_controller import MAX_GREEN, RequestRecord, audit_phase_timeline
from src.state import IntersectionState


class EpisodeRecorder:
    """Collect the per-step measurements an episode summary needs."""

    def __init__(self, intersections_config: dict) -> None:
        nodes = intersections_config["intersections"]
        self.queues = {node_id: [] for node_id in nodes}
        # (intersection, approach) -> [waiting seconds summed over vehicles, vehicle-steps]
        self.approach_wait = {
            (node_id, slot): [0.0, 0]
            for node_id, node in nodes.items()
            for slot in node["approaches"]
        }
        # Phase shown during each step, keyed by signal ID.
        self.phases = {node["signal_id"]: [] for node in nodes.values()}

    def record_states(self, states: dict[str, IntersectionState]) -> None:
        for node_id, state in states.items():
            self.queues[node_id].append(
                sum(approach.queue_count for approach in state.approaches.values())
            )

            for slot, approach in state.approaches.items():
                totals = self.approach_wait[(node_id, slot)]
                totals[0] += approach.mean_wait_s * approach.vehicle_count
                totals[1] += approach.vehicle_count

    def record_phases(self, phases: dict[str, int]) -> None:
        for signal_id, phase in phases.items():
            if signal_id in self.phases:
                self.phases[signal_id].append(phase)


def read_tripinfo(path: Path) -> list[dict]:
    """Return the completed trips in a SUMO tripinfo file."""

    trips = []

    for trip in ET.parse(path).getroot().iter("tripinfo"):
        # Vehicles removed before their destination are not completed trips.
        if trip.get("vaporized", "") not in ("", "0", "false"):
            continue

        trips.append(
            {
                "time_loss_s": float(trip.get("timeLoss")),
                "waiting_s": float(trip.get("waitingTime")),
                "depart_delay_s": float(trip.get("departDelay")),
            }
        )

    return trips


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def _distribution(values: list[float]) -> dict | None:
    if not values:
        return None

    return {
        "mean": sum(values) / len(values),
        "p95": _percentile(values, 0.95),
        "max": max(values),
    }


def summarize_episode(
    *,
    run: dict,
    recorder: EpisodeRecorder,
    trips: list[dict],
    records: list[RequestRecord],
    totals: dict,
    intersections_config: dict,
    timing: dict,
    step_length_s: float,
) -> dict:
    """Combine trip output, per-step samples, and safety records into one summary."""

    nodes = intersections_config["intersections"]

    violations = {}

    for node_id, node in nodes.items():
        found = audit_phase_timeline(
            recorder.phases[node["signal_id"]], node["actions"], timing, step_length_s
        )

        if found:
            violations[node_id] = found

    # Highest mean waiting time per vehicle present, over the whole episode.
    approach_waits = [
        (node_id, slot, wait_sum / vehicle_steps)
        for (node_id, slot), (wait_sum, vehicle_steps) in recorder.approach_wait.items()
        if vehicle_steps > 0
    ]
    worst = max(approach_waits, key=lambda item: item[2], default=None)

    return {
        **run,
        "horizon_s": totals["horizon_s"],
        "trips": {
            "departed": totals["departed"],
            "completed": len(trips),
            "still_running": totals["still_running"],
            "waiting_to_insert": totals["waiting_to_insert"],
            "teleports": totals["teleports"],
        },
        # Completed trips only; unfinished vehicles are counted in "trips".
        "completed_trips": {
            "time_loss_s": _distribution([trip["time_loss_s"] for trip in trips]),
            "waiting_s": _distribution([trip["waiting_s"] for trip in trips]),
            "depart_delay_s": _distribution([trip["depart_delay_s"] for trip in trips]),
        },
        "queues": {
            node_id: {
                "mean": sum(samples) / len(samples) if samples else 0.0,
                "peak": max(samples, default=0),
            }
            for node_id, samples in recorder.queues.items()
        },
        "worst_approach": None if worst is None else {
            "intersection": worst[0],
            "approach": worst[1],
            "mean_wait_s": worst[2],
        },
        "safety": {
            "requests": sum(1 for record in records if record.override_reason != MAX_GREEN),
            "overrides": dict(
                Counter(record.override_reason for record in records if record.override_reason)
            ),
            "illegal_transitions": sum(len(found) for found in violations.values()),
            "violations": violations,
        },
    }
