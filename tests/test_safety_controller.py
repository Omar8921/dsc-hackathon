"""Check each safety rule and the phase-timeline audit without SUMO."""

import json
import random
import unittest
from pathlib import Path

from src.safety_controller import (
    IN_TRANSITION,
    INVALID_REQUEST,
    MAX_GREEN,
    MIN_GREEN,
    IntersectionSignal,
    SafetyController,
    audit_phase_timeline,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERSECTIONS = json.loads(
    (PROJECT_ROOT / "configs" / "intersections.json").read_text(encoding="utf-8-sig")
)
ACTIONS = INTERSECTIONS["intersections"]["A0"]["actions"]
TIMING = {"min_green_s": 10, "max_green_s": 60, "yellow_s": 3, "all_red_s": 1, "fallback_green_s": 30}

# Phase indices from the mapping: north-south green 0, yellow 1, all-red 2;
# east-west green 3, yellow 4, all-red 5.
NS_GREEN, NS_YELLOW, NS_ALL_RED, EW_GREEN = 0, 1, 2, 3


def run(signal: IntersectionSignal, end_s: int, requests: dict | None = None):
    """Step the signal from 0 to end_s; return shown phases and request records."""

    requests = requests or {}
    phases = []
    records = []

    for time_s in range(end_s):
        record = signal.advance(time_s)

        if record:
            records.append(record)

        if time_s in requests:
            records.append(signal.request(requests[time_s], time_s))

        phases.append(signal.phase_index())

    return phases, records


class IntersectionSignalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.signal = IntersectionSignal("A0", ACTIONS, TIMING)

    def test_requesting_the_current_green_holds_it(self) -> None:
        phases, records = run(self.signal, 30, {20: 0})

        self.assertEqual(set(phases), {NS_GREEN})
        self.assertIsNone(records[0].override_reason)
        self.assertEqual(records[0].applied_action, 0)

    def test_switch_before_minimum_green_is_rejected(self) -> None:
        phases, records = run(self.signal, 20, {5: 1})

        self.assertEqual(set(phases), {NS_GREEN})
        self.assertEqual(records[0].override_reason, MIN_GREEN)
        self.assertEqual(records[0].applied_action, 0)

    def test_permitted_switch_runs_yellow_then_all_red_then_green(self) -> None:
        phases, records = run(self.signal, 20, {10: 1})

        self.assertEqual(phases[:10], [NS_GREEN] * 10)
        self.assertEqual(phases[10:13], [NS_YELLOW] * 3)
        self.assertEqual(phases[13:14], [NS_ALL_RED])
        self.assertEqual(phases[14:], [EW_GREEN] * 6)
        self.assertIsNone(records[0].override_reason)
        self.assertEqual(records[0].applied_action, 1)

        state = self.signal.signal_state(19)
        self.assertEqual((state.active_green_phase, state.transition_state), (1, "green"))
        self.assertEqual(state.elapsed_green_s, 5)

    def test_requests_during_a_transition_are_ignored(self) -> None:
        _, records = run(self.signal, 20, {10: 1, 11: 0, 12: 1})

        # Asking to go back is ignored; asking for the target already underway is not an override.
        self.assertEqual(records[1].override_reason, IN_TRANSITION)
        self.assertIsNone(records[2].override_reason)
        self.assertEqual(self.signal.signal_state(19).active_green_phase, 1)

    def test_maximum_green_forces_a_switch(self) -> None:
        phases, records = run(self.signal, 70)

        self.assertEqual(phases[:60], [NS_GREEN] * 60)
        self.assertEqual(phases[60], NS_YELLOW)
        self.assertEqual(records[0].override_reason, MAX_GREEN)
        self.assertIsNone(records[0].requested_action)

    def test_invalid_requests_use_the_fixed_time_fallback(self) -> None:
        for bad in ("east", None, 2, -1, True, 0.5):
            with self.subTest(request=bad):
                signal = IntersectionSignal("A0", ACTIONS, TIMING)
                _, early = run(signal, 6, {5: bad})
                self.assertEqual(early[0].override_reason, INVALID_REQUEST)
                self.assertEqual(signal.phase_index(), NS_GREEN)

        # After fallback_green_s of green, the fallback switches phases.
        signal = IntersectionSignal("A0", ACTIONS, TIMING)
        phases, records = run(signal, 32, {30: None})
        self.assertEqual(records[0].override_reason, INVALID_REQUEST)
        self.assertEqual(phases[30], NS_YELLOW)

    def test_bad_timing_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            IntersectionSignal("A0", ACTIONS, {**TIMING, "min_green_s": 70})

        with self.assertRaises(ValueError):
            IntersectionSignal("A0", ACTIONS, {**TIMING, "all_red_s": 0})

    def test_random_requests_never_break_a_rule(self) -> None:
        rng = random.Random(7)
        choices = [0, 1, 0, 1, None, 5, "x"]
        requests = {t: rng.choice(choices) for t in range(5000) if rng.random() < 0.3}
        phases, _ = run(self.signal, 5000, requests)

        self.assertEqual(audit_phase_timeline(phases, ACTIONS, TIMING, 1.0), [])
        self.assertIn(EW_GREEN, phases)


class SafetyControllerTest(unittest.TestCase):
    def test_only_phase_changes_are_sent_to_sumo(self) -> None:
        class FakeAdapter:
            def __init__(self):
                self.calls = []

            def set_signal_phase(self, signal_id, phase):
                self.calls.append((signal_id, phase))

        adapter = FakeAdapter()
        safety = SafetyController(adapter, INTERSECTIONS, TIMING)

        for time_s in range(16):
            safety.begin_step(time_s)

            if time_s == 10:
                safety.request("B0", 1, time_s)

            safety.apply()

        b0_calls = [phase for signal_id, phase in adapter.calls if signal_id == "B0"]
        self.assertEqual(b0_calls, [NS_GREEN, NS_YELLOW, NS_ALL_RED, EW_GREEN])
        self.assertEqual(len([call for call in adapter.calls if call[0] == "A0"]), 1)

        summary = safety.control_summary(15)["B0"]
        self.assertEqual(summary["active_action"], "east_west")
        self.assertEqual(summary["transition_state"], "green")
        self.assertEqual(summary["last_request"]["requested_action"], "east_west")
        self.assertEqual(summary["override_count"], 0)


class AuditTest(unittest.TestCase):
    def audit(self, phases):
        return audit_phase_timeline(phases, ACTIONS, TIMING, 1.0)

    def test_legal_timeline_passes(self) -> None:
        cycle = [0] * 10 + [1] * 3 + [2] + [3] * 12 + [4] * 3 + [5]
        # The cut-off final green may be shorter than the minimum.
        self.assertEqual(self.audit(cycle + [0] * 4), [])

    def test_violations_are_reported(self) -> None:
        cases = {
            "short green": [0] * 5 + [1] * 3 + [2] + [3] * 10,
            "long green": [0] * 61 + [1] * 3,
            "short yellow": [0] * 10 + [1] * 2 + [2] + [3] * 10,
            "skipped all-red": [0] * 10 + [1] * 3 + [3] * 10,
            "green to green": [0] * 10 + [3] * 10,
            "unmapped phase": [0] * 10 + [7] * 3,
        }

        for name, phases in cases.items():
            with self.subTest(case=name):
                self.assertNotEqual(self.audit(phases), [])


if __name__ == "__main__":
    unittest.main()
