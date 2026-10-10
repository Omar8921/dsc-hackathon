"""Convert raw intersection state into the fixed 44-value policy observation."""

import math

from src.state import APPROACH_ORDER, IntersectionState


APPROACH_FEATURES = (
    "queue",
    "vehicles",
    "occupancy",
    "arrival_rate",
    "mean_wait",
    "mean_speed",
    "downstream_occupancy",
)
NEIGHBOR_FEATURES = ("present", "queue", "occupancy")
SIGNAL_FEATURES = ("green_phase_0", "green_phase_1", "elapsed_green", "in_transition")

# Readable name of each observation value, in order.
OBSERVATION_FIELDS = (
    [f"{slot}.{name}" for slot in APPROACH_ORDER for name in APPROACH_FEATURES]
    + [f"neighbor_{slot}.{name}" for slot in APPROACH_ORDER for name in NEIGHBOR_FEATURES]
    + [f"signal.{name}" for name in SIGNAL_FEATURES]
)
OBSERVATION_SIZE = len(OBSERVATION_FIELDS)


def observation_settings(controller_config: dict) -> dict:
    """Collect the normalization settings from configs/controller.json."""

    return {
        **controller_config["observation"],
        "max_green_s": controller_config["safety"]["max_green_s"],
    }


def build_observation(state: IntersectionState, settings: dict) -> list[float]:
    """Return the normalized observation for one intersection.

    Values are clipped to [0, 1]; the raw state keeps the unclipped values.
    """

    values = []

    for slot in APPROACH_ORDER:
        approach = state.approaches[slot]
        storage = approach.storage_capacity
        values += [
            approach.queue_count / storage,
            approach.vehicle_count / storage,
            approach.occupancy,
            approach.arrival_rate_vps / settings["arrival_reference_vps"],
            approach.mean_wait_s / settings["wait_reference_s"],
            approach.mean_speed_mps / approach.speed_limit_mps,
            approach.downstream_occupancy,
        ]

    for slot in APPROACH_ORDER:
        neighbor = state.neighbors[slot]

        # No neighbor gives three zeros; "present" separates that from an
        # empty neighboring intersection.
        if neighbor.present:
            values += [1.0, neighbor.normalized_queue, neighbor.mean_occupancy]
        else:
            values += [0.0, 0.0, 0.0]

    signal = state.signal
    values += [
        1.0 if signal.active_green_phase == 0 else 0.0,
        1.0 if signal.active_green_phase == 1 else 0.0,
        signal.elapsed_green_s / settings["max_green_s"],
        0.0 if signal.transition_state == "green" else 1.0,
    ]

    # Fail loudly rather than letting clipping hide a broken measurement.
    for name, value in zip(OBSERVATION_FIELDS, values):
        if not math.isfinite(value):
            raise ValueError(f"{state.intersection_id}: {name} is {value}.")

    return [min(1.0, max(0.0, value)) for value in values]
