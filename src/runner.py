"""Common episode runner used for every controller.

One SUMO process owns the clock. At each step boundary the runner reads the
traffic state, collects every intersection's requests, lets the safety
controller apply the result, and only then advances the shared simulation.
"""

import json
from dataclasses import asdict
from pathlib import Path

from src.baselines import ActuatedController, FixedTimeController
from src.congestion_detector import CongestionDetector
from src.metrics import EpisodeRecorder, read_tripinfo, summarize_episode
from src.observations import observation_settings
from src.safety_controller import SafetyController
from src.simulation_adapter import SimulationAdapter
from src.state import StateBuilder


BASELINES = ("fixed-time", "actuated")
CONTROLLERS = (*BASELINES, "ppo")


def make_controller(
    run: dict, intersections_config: dict, controller_config: dict, lane_geometry: dict
):
    name = run["controller"]
    baselines = controller_config["baselines"]

    if name == "fixed-time":
        return FixedTimeController(intersections_config, baselines["fixed_time"]["green_s"])

    if name == "actuated":
        return ActuatedController(
            intersections_config,
            lane_geometry,
            controller_config["safety"]["min_green_s"],
            baselines["actuated"]["detector_distance_m"],
        )

    if name == "ppo":
        # Imported here so the baselines run without PyTorch.
        from src.policy import PolicyController, load_policy

        if not run.get("checkpoint"):
            raise ValueError("The ppo controller needs a checkpoint.")

        model, _ = load_policy(Path(run["checkpoint"]))
        return PolicyController(
            model,
            observation_settings(controller_config),
            controller_config["policy"]["decision_interval_s"],
        )

    raise ValueError(f"Unknown controller {name!r}; choose one of {CONTROLLERS}.")


def run_episode(
    sumocfg_path: Path,
    run: dict,
    intersections_config: dict,
    controller_config: dict,
    output_dir: Path,
    quiet: bool = False,
    on_step=None,
    alerts_config: dict | None = None,
) -> dict:
    """Run one scenario to its end time and save metrics.json in output_dir.

    run holds run_id, scenario, controller (one of CONTROLLERS), and for
    "ppo" the checkpoint path.
    on_step(adapter, control, states, alerts, status) is called at every step
    boundary, for example to publish telemetry to the viewer.
    alerts_config, when calibrated, enables the congestion detector.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    tripinfo_path = output_dir / "tripinfo.xml"
    timing = controller_config["safety"]

    adapter = SimulationAdapter(
        sumocfg_path, quiet=quiet, extra_args=["--tripinfo-output", str(tripinfo_path)]
    )
    adapter.start()

    try:
        geometry = {lane["id"]: lane for lane in adapter.read_network()["lanes"]}
        builder = StateBuilder(
            intersections_config, controller_config["observation"]["arrival_window_s"], geometry
        )
        safety = SafetyController(adapter, intersections_config, timing, adapter.time_s())
        controller = make_controller(run, intersections_config, controller_config, geometry)
        recorder = EpisodeRecorder(intersections_config)
        detector = (
            CongestionDetector(alerts_config["reference_p95"], alerts_config["settings"])
            if alerts_config and alerts_config.get("reference_p95")
            else None
        )

        def alerts() -> list[dict] | None:
            return None if detector is None else [asdict(event) for event in detector.events]

        while True:
            time_s = adapter.time_s()
            vehicles = adapter.read_vehicles()
            states = builder.update(time_s, adapter.read_lanes(), vehicles, adapter.read_signals())
            recorder.record_states(states)

            # Monitoring only: the detector never changes the signals.
            if detector is not None:
                detector.update(time_s, states)

            if adapter.finished():
                break

            # Every intersection decides before the shared simulation advances.
            safety.begin_step(time_s)
            requests = controller.requests(time_s, safety.signal_states(time_s), vehicles, states)

            for node_id, action in requests.items():
                safety.request(node_id, action, time_s)

            safety.apply()
            recorder.record_phases(adapter.read_phases())

            if on_step is not None:
                on_step(adapter, safety.control_summary(time_s), states, alerts(), "running")

            adapter.step()

        if on_step is not None:
            on_step(adapter, safety.control_summary(time_s), states, alerts(), "finished")

        totals = {
            "horizon_s": time_s,
            "departed": adapter.departed_total,
            "still_running": len(vehicles),
            "waiting_to_insert": adapter.pending_count(),
            "teleports": adapter.teleports_total,
        }
    finally:
        # Closing SUMO also finishes writing the trip output.
        adapter.close()

    summary = summarize_episode(
        run=run,
        recorder=recorder,
        trips=read_tripinfo(tripinfo_path),
        records=safety.records,
        totals=totals,
        intersections_config=intersections_config,
        timing=timing,
        step_length_s=adapter.step_length_s,
    )

    if detector is not None:
        summary["alerts"] = alerts()

    (output_dir / "metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return summary
