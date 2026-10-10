"""Persistent-congestion alerts.

Observes traffic and emits monitoring events; it never changes signals. An
alert starts when an intersection's worst approach queue stays above both its
reference 95th percentile and min_normalized_queue for persist_s, and clears
after clear_s below that level. It indicates persistent congestion, not its
cause.
"""

from dataclasses import dataclass

from src.state import IntersectionState


def worst_approach_queue(state: IntersectionState) -> float:
    """Highest queued-vehicles / storage ratio among the intersection's approaches."""

    return max(approach.queue_count / approach.storage_capacity for approach in state.approaches.values())


@dataclass
class CongestionEvent:
    event_id: str
    intersection_id: str
    started_s: float
    time_s: float
    severity: str
    observed_queue: float
    reference_threshold: float
    duration_s: float
    # "active" or "resolved".
    status: str


class CongestionDetector:
    def __init__(self, reference_p95: dict[str, float], settings: dict) -> None:
        self.reference_p95 = reference_p95
        self.settings = settings
        self.events: list[CongestionEvent] = []
        self._above_since: dict[str, float] = {}
        self._below_since: dict[str, float] = {}
        self._active: dict[str, CongestionEvent] = {}

    def threshold(self, node_id: str) -> float:
        # Both conditions must hold, so the higher of the two is the trigger.
        return max(self.reference_p95[node_id], self.settings["min_normalized_queue"])

    def update(self, time_s: float, states: dict[str, IntersectionState]) -> None:
        for node_id, state in states.items():
            queue = worst_approach_queue(state)
            threshold = self.threshold(node_id)
            event = self._active.get(node_id)

            if queue > threshold:
                self._below_since.pop(node_id, None)
                since = self._above_since.setdefault(node_id, time_s)

                # One event per congestion episode; duplicates are suppressed.
                if event is None and time_s - since >= self.settings["persist_s"]:
                    event = CongestionEvent(
                        event_id=f"{node_id}-{len(self.events) + 1}",
                        intersection_id=node_id,
                        started_s=since,
                        time_s=time_s,
                        severity="",
                        observed_queue=queue,
                        reference_threshold=threshold,
                        duration_s=0.0,
                        status="active",
                    )
                    self.events.append(event)
                    self._active[node_id] = event
            else:
                self._above_since.pop(node_id, None)

                if event is not None:
                    since = self._below_since.setdefault(node_id, time_s)

                    if time_s - since >= self.settings["clear_s"]:
                        event.status = "resolved"
                        del self._active[node_id]

            if event is not None:
                event.time_s = time_s
                event.duration_s = time_s - event.started_s
                event.observed_queue = queue
                # Severe once the worst approach is nearly full.
                if event.status == "active":
                    event.severity = "severe" if queue >= 0.9 else "elevated"
