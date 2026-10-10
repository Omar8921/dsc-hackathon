"""Validate phase requests and execute only safe signal transitions.

A controller (baseline or policy) only requests a green phase by action index.
This module decides what the signal actually shows:

1. A request for the current green holds it, unless maximum green forces a switch.
2. A switch before minimum green is rejected.
3. Every permitted change runs green -> yellow -> all-red -> requested green.
4. Requests during a transition are ignored.
5. Maximum green forces a switch to the next phase.
6. An invalid or missing request falls back to a fixed-time rule.
"""

import math
import numbers
from dataclasses import dataclass

from src.state import SignalState


# Reasons a request was not applied as asked.
MIN_GREEN = "min_green"
IN_TRANSITION = "in_transition"
INVALID_REQUEST = "invalid_request"
MAX_GREEN = "max_green"


@dataclass
class RequestRecord:
    time_s: float
    intersection_id: str
    # As received; None for changes forced by maximum green.
    requested_action: object
    # The green the signal is holding or changing to after this decision.
    applied_action: int
    transition_state: str
    override_reason: str | None


class IntersectionSignal:
    """Safety state machine for one intersection's signal."""

    def __init__(
        self,
        intersection_id: str,
        actions: list[dict],
        timing: dict,
        time_s: float = 0.0,
        initial_action: int = 0,
    ) -> None:
        if not 0 < timing["min_green_s"] <= timing["max_green_s"]:
            raise ValueError("Safety timing needs 0 < min_green_s <= max_green_s.")

        if timing["yellow_s"] <= 0 or timing["all_red_s"] <= 0:
            raise ValueError("Safety timing needs positive yellow_s and all_red_s.")

        self.intersection_id = intersection_id
        self.actions = actions
        self.timing = timing
        self.green_action = initial_action
        self.target_action = initial_action
        self.stage = "green"
        self.stage_start_s = time_s

    def advance(self, time_s: float) -> RequestRecord | None:
        """Finish timed stages and enforce maximum green at a step boundary."""

        elapsed = time_s - self.stage_start_s

        if self.stage == "yellow" and elapsed >= self.timing["yellow_s"]:
            self._enter("all_red", time_s)
        elif self.stage == "all_red" and elapsed >= self.timing["all_red_s"]:
            self.green_action = self.target_action
            self._enter("green", time_s)
        elif self.stage == "green" and elapsed >= self.timing["max_green_s"]:
            self._start_change(self._next_action(), time_s)
            return self._record(time_s, None, MAX_GREEN)

        return None

    def request(self, requested: object, time_s: float) -> RequestRecord:
        """Handle a phase request made at a step boundary."""

        valid = (
            isinstance(requested, numbers.Integral)
            and not isinstance(requested, bool)
            and 0 <= requested < len(self.actions)
        )
        action = int(requested) if valid else self._fallback_action(time_s)
        reason = None if valid else INVALID_REQUEST

        if self.stage != "green":
            ignored = action != self.target_action
            return self._record(time_s, requested, reason or (IN_TRANSITION if ignored else None))

        if action == self.green_action:
            return self._record(time_s, requested, reason)

        if time_s - self.stage_start_s < self.timing["min_green_s"]:
            return self._record(time_s, requested, reason or MIN_GREEN)

        self._start_change(action, time_s)
        return self._record(time_s, requested, reason)

    def phase_index(self) -> int:
        """Return the SUMO phase index for the current stage."""

        # Yellow and all-red belong to the green being left.
        action = self.actions[self.green_action]
        return {
            "green": action["green_phase"],
            "yellow": action["yellow_phase"],
            "all_red": action["all_red_phase"],
        }[self.stage]

    def signal_state(self, time_s: float) -> SignalState:
        return SignalState(
            active_green_phase=self.green_action,
            transition_state=self.stage,
            elapsed_green_s=time_s - self.stage_start_s if self.stage == "green" else 0.0,
        )

    def _fallback_action(self, time_s: float) -> int:
        # Fixed-time rule: switch once the green has run fallback_green_s.
        if self.stage != "green":
            return self.target_action

        if time_s - self.stage_start_s >= self.timing["fallback_green_s"]:
            return self._next_action()

        return self.green_action

    def _next_action(self) -> int:
        return (self.green_action + 1) % len(self.actions)

    def _start_change(self, action: int, time_s: float) -> None:
        self.target_action = action
        self._enter("yellow", time_s)

    def _enter(self, stage: str, time_s: float) -> None:
        self.stage = stage
        self.stage_start_s = time_s

    def _record(self, time_s: float, requested: object, reason: str | None) -> RequestRecord:
        return RequestRecord(
            time_s=time_s,
            intersection_id=self.intersection_id,
            requested_action=requested,
            applied_action=self.target_action,
            transition_state=self.stage,
            override_reason=reason,
        )


class SafetyController:
    """Run one safety state machine per intersection and apply phases to SUMO.

    At each step boundary: begin_step(), then any request() calls, then apply().
    """

    def __init__(
        self, adapter, intersections_config: dict, timing: dict, time_s: float = 0.0
    ) -> None:
        nodes = intersections_config["intersections"]
        self.adapter = adapter
        self.signal_ids = {node_id: node["signal_id"] for node_id, node in nodes.items()}
        self.action_names = {
            node_id: [action["name"] for action in node["actions"]]
            for node_id, node in nodes.items()
        }
        self.signals = {
            node_id: IntersectionSignal(node_id, node["actions"], timing, time_s)
            for node_id, node in nodes.items()
        }
        self.records: list[RequestRecord] = []
        self._applied: dict[str, int] = {}
        self._last_record: dict[str, RequestRecord] = {}
        self._override_count = dict.fromkeys(nodes, 0)

    def begin_step(self, time_s: float) -> None:
        for signal in self.signals.values():
            record = signal.advance(time_s)

            if record is not None:
                self._log(record)

    def request(self, node_id: str, requested: object, time_s: float) -> RequestRecord:
        record = self.signals[node_id].request(requested, time_s)
        self._log(record)
        return record

    def _log(self, record: RequestRecord) -> None:
        self.records.append(record)
        self._last_record[record.intersection_id] = record

        if record.override_reason is not None:
            self._override_count[record.intersection_id] += 1

    def apply(self) -> None:
        """Send phase changes to SUMO."""

        for node_id, signal in self.signals.items():
            phase = signal.phase_index()

            if self._applied.get(node_id) != phase:
                self.adapter.set_signal_phase(self.signal_ids[node_id], phase)
                self._applied[node_id] = phase

    def signal_states(self, time_s: float) -> dict[str, SignalState]:
        return {node_id: signal.signal_state(time_s) for node_id, signal in self.signals.items()}

    def control_summary(self, time_s: float) -> dict[str, dict]:
        """Describe each signal's control state for telemetry, keyed by signal ID."""

        summary = {}

        for node_id, signal in self.signals.items():
            names = self.action_names[node_id]
            record = self._last_record.get(node_id)
            requested = record.requested_action if record else None
            summary[self.signal_ids[node_id]] = {
                "active_action": names[signal.green_action],
                "target_action": names[signal.target_action],
                "transition_state": signal.stage,
                "elapsed_green_s": signal.signal_state(time_s).elapsed_green_s,
                "override_count": self._override_count[node_id],
                "last_request": None if record is None else {
                    "time_s": record.time_s,
                    "requested_action": (
                        names[int(requested)]
                        if isinstance(requested, numbers.Integral)
                        and not isinstance(requested, bool)
                        and 0 <= requested < len(names)
                        else None
                    ),
                    "applied_action": names[record.applied_action],
                    "override_reason": record.override_reason,
                },
            }

        return summary


def audit_phase_timeline(
    phases: list[int], actions: list[dict], timing: dict, step_length_s: float
) -> list[str]:
    """Return every safety-rule violation in a per-step list of shown phases.

    Each entry is the phase shown during one simulation step. The last segment
    may be cut short by the end of the episode, so only its upper limits apply.
    """

    kinds = {}

    for action in actions:
        kinds[action["green_phase"]] = ("green", action["action"])
        kinds[action["yellow_phase"]] = ("yellow", action["action"])
        kinds[action["all_red_phase"]] = ("all_red", action["action"])

    # Group consecutive steps into [phase, start, duration] segments.
    segments = []

    for step, phase in enumerate(phases):
        if segments and segments[-1][0] == phase:
            segments[-1][2] += step_length_s
        else:
            segments.append([phase, step * step_length_s, step_length_s])

    limits = {
        "yellow": timing["yellow_s"],
        "all_red": timing["all_red_s"],
    }
    violations = []

    for i, (phase, start, duration) in enumerate(segments):
        where = f"phase {phase} at {start:g} s"

        if phase not in kinds:
            violations.append(f"{where}: not in the mapping")
            continue

        kind, action = kinds[phase]
        last = i == len(segments) - 1

        if kind == "green":
            if not last and duration < timing["min_green_s"]:
                violations.append(f"{where}: green for {duration:g} s, below minimum")

            if duration > timing["max_green_s"]:
                violations.append(f"{where}: green for {duration:g} s, above maximum")
        else:
            expected = limits[kind]

            if duration > expected or (not last and not math.isclose(duration, expected)):
                violations.append(f"{where}: {kind} for {duration:g} s, expected {expected:g} s")

        if last:
            continue

        next_kind, next_action = kinds.get(segments[i + 1][0], (None, None))
        allowed = {
            "green": next_kind == "yellow" and next_action == action,
            "yellow": next_kind == "all_red" and next_action == action,
            "all_red": next_kind == "green" and next_action != action,
        }[kind]

        if not allowed:
            violations.append(f"{where}: {kind} followed by phase {segments[i + 1][0]}")

    return violations
