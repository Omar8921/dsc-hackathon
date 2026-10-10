"""Check when persistent-congestion alerts start, repeat, and clear."""

import unittest

from src.congestion_detector import CongestionDetector, worst_approach_queue
from src.state import APPROACH_ORDER, ApproachState, IntersectionState, NeighborState, SignalState


SETTINGS = {"min_normalized_queue": 0.5, "persist_s": 30, "clear_s": 30}


def state_with_queue(queue: int) -> dict[str, IntersectionState]:
    """A0 with `queue` vehicles queued on its north approach (storage 20)."""

    approaches = {
        slot: ApproachState(
            vehicle_count=queue if slot == "N" else 0,
            queue_count=queue if slot == "N" else 0,
            occupancy=0.0,
            arrival_rate_vps=0.0,
            mean_wait_s=0.0,
            mean_speed_mps=13.89,
            downstream_occupancy=0.0,
            storage_capacity=20,
            speed_limit_mps=13.89,
        )
        for slot in APPROACH_ORDER
    }
    state = IntersectionState(
        sim_time_s=0.0,
        intersection_id="A0",
        signal=SignalState(0, "green", 0.0),
        approaches=approaches,
        neighbors={slot: NeighborState(False, None, 0.0, 0.0) for slot in APPROACH_ORDER},
    )
    return {"A0": state}


class CongestionDetectorTest(unittest.TestCase):
    def run_timeline(self, detector, queues_by_time):
        for time_s, queue in queues_by_time:
            detector.update(time_s, state_with_queue(queue))

    def test_worst_approach_queue(self) -> None:
        self.assertAlmostEqual(worst_approach_queue(state_with_queue(12)["A0"]), 0.6)

    def test_alert_needs_30_seconds_above_both_thresholds(self) -> None:
        detector = CongestionDetector({"A0": 0.3}, SETTINGS)

        # 0.6 is above both 0.3 (reference) and 0.5 (minimum).
        self.run_timeline(detector, [(t, 12) for t in range(0, 30)])
        self.assertEqual(detector.events, [])

        self.run_timeline(detector, [(30, 12)])
        self.assertEqual(len(detector.events), 1)
        event = detector.events[0]
        self.assertEqual((event.status, event.started_s, event.reference_threshold), ("active", 0, 0.5))

    def test_queue_below_the_reference_does_not_alert(self) -> None:
        # 0.6 exceeds the 0.5 minimum but not this intersection's 0.7 reference.
        detector = CongestionDetector({"A0": 0.7}, SETTINGS)
        self.run_timeline(detector, [(t, 12) for t in range(0, 120)])
        self.assertEqual(detector.events, [])

    def test_no_duplicate_while_active_and_clears_after_30_seconds(self) -> None:
        detector = CongestionDetector({"A0": 0.3}, SETTINGS)
        self.run_timeline(detector, [(t, 12) for t in range(0, 100)])
        self.assertEqual(len(detector.events), 1)

        # Below the trigger from 100 s: still active at 129 s, resolved at 130 s.
        self.run_timeline(detector, [(t, 2) for t in range(100, 130)])
        self.assertEqual(detector.events[0].status, "active")
        self.run_timeline(detector, [(130, 2)])
        self.assertEqual(detector.events[0].status, "resolved")

        # A later congestion episode is a new event.
        self.run_timeline(detector, [(t, 19) for t in range(200, 231)])
        self.assertEqual([event.status for event in detector.events], ["resolved", "active"])
        self.assertEqual(detector.events[1].severity, "severe")

    def test_short_dip_does_not_clear_an_alert(self) -> None:
        detector = CongestionDetector({"A0": 0.3}, SETTINGS)
        self.run_timeline(detector, [(t, 12) for t in range(0, 40)])
        self.run_timeline(detector, [(t, 2) for t in range(40, 50)])
        self.run_timeline(detector, [(t, 12) for t in range(50, 100)])
        self.assertEqual(len(detector.events), 1)
        self.assertEqual(detector.events[0].status, "active")


if __name__ == "__main__":
    unittest.main()
