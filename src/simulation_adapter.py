"""SUMO lifecycle and raw traffic measurements through TraCI."""

import subprocess
import sys
from pathlib import Path

import traci
import traci.constants as tc


# Values SUMO sends back for every vehicle after each step.
VEHICLE_VARIABLES = [
    tc.VAR_POSITION,
    tc.VAR_ANGLE,
    tc.VAR_SPEED,
    tc.VAR_WAITING_TIME,
    tc.VAR_ACCUMULATED_WAITING_TIME,
    tc.VAR_LANE_ID,
    tc.VAR_ROUTE_ID,
    tc.VAR_TYPE,
]

# Values SUMO sends back for every normal lane after each step.
LANE_VARIABLES = [
    tc.LAST_STEP_VEHICLE_NUMBER,
    tc.LAST_STEP_VEHICLE_HALTING_NUMBER,
    tc.LAST_STEP_OCCUPANCY,
    tc.LAST_STEP_MEAN_SPEED,
]


def find_sumo_binary(name: str) -> Path:
    """Return a SUMO executable installed beside the venv's Python."""

    # On Windows, pip installs the SUMO launchers beside the venv's Python.
    executable = Path(sys.executable).parent / f"{name}.exe"

    if not executable.is_file():
        raise FileNotFoundError(
            f"Cannot find {executable}. "
            "Run this script using the project's Windows virtual environment."
        )

    return executable


class SimulationAdapter:
    """Own one SUMO process and read its state between simulation steps."""

    def __init__(self, sumocfg_path: Path, quiet: bool = False) -> None:
        self.sumocfg_path = sumocfg_path
        # Hide SUMO's console output, e.g. during tests and training.
        self.quiet = quiet
        self.step_length_s = 0.0
        self.end_time_s = -1.0
        self.lane_ids: list[str] = []
        self.signal_ids: list[str] = []
        self.signal_lanes: dict[str, list[str]] = {}
        self.departed_total = 0
        self.arrived_total = 0
        self._connected = False

    def start(self) -> None:
        """Launch SUMO headless and subscribe to the lanes it loaded."""

        traci.start(
            [
                str(find_sumo_binary("sumo")),
                "-c",
                str(self.sumocfg_path),
                "--no-step-log",
                "true",
                "--duration-log.statistics",
                "true",
            ],
            stdout=subprocess.DEVNULL if self.quiet else None,
        )
        self._connected = True

        self.step_length_s = traci.simulation.getDeltaT()
        self.end_time_s = traci.simulation.getEndTime()

        # Lanes inside junctions start with ":"; measure only road lanes.
        self.lane_ids = [
            lane_id
            for lane_id in traci.lane.getIDList()
            if not lane_id.startswith(":")
        ]

        for lane_id in self.lane_ids:
            traci.lane.subscribe(lane_id, LANE_VARIABLES)

        self.signal_ids = list(traci.trafficlight.getIDList())

        # A lane appears once per signal index it feeds; keep it once.
        self.signal_lanes = {
            signal_id: list(
                dict.fromkeys(traci.trafficlight.getControlledLanes(signal_id))
            )
            for signal_id in self.signal_ids
        }

    def step(self) -> None:
        """Advance SUMO by one step and subscribe to vehicles that entered."""

        traci.simulationStep()

        # SUMO drops a vehicle's subscription when the vehicle leaves.
        for vehicle_id in traci.simulation.getDepartedIDList():
            traci.vehicle.subscribe(vehicle_id, VEHICLE_VARIABLES)

        self.departed_total += traci.simulation.getDepartedNumber()
        self.arrived_total += traci.simulation.getArrivedNumber()

    def time_s(self) -> float:
        """Return the current simulation time."""

        return traci.simulation.getTime()

    def finished(self) -> bool:
        """Return whether the scenario's configured end time was reached."""

        # Stop at the configured end ourselves rather than waiting for SUMO
        # to close the connection.
        if self.end_time_s >= 0:
            return self.time_s() >= self.end_time_s

        return traci.simulation.getMinExpectedNumber() == 0

    def read_network(self) -> dict:
        """Read lane and junction geometry plus signal links from SUMO."""

        (min_x, min_y), (max_x, max_y) = traci.simulation.getNetBoundary()

        lanes = [
            {
                "id": lane_id,
                "edge": traci.lane.getEdgeID(lane_id),
                "shape": [list(point) for point in traci.lane.getShape(lane_id)],
                "width_m": traci.lane.getWidth(lane_id),
                "length_m": traci.lane.getLength(lane_id),
                "speed_limit_mps": traci.lane.getMaxSpeed(lane_id),
            }
            for lane_id in self.lane_ids
        ]

        junctions = [
            {
                "id": junction_id,
                "shape": [
                    list(point) for point in traci.junction.getShape(junction_id)
                ],
            }
            for junction_id in traci.junction.getIDList()
            if not junction_id.startswith(":")
        ]

        signals = []

        for signal_id in self.signal_ids:
            links = []

            # Entry i describes the movement controlled by signal index i.
            for index, connections in enumerate(
                traci.trafficlight.getControlledLinks(signal_id)
            ):
                if not connections:
                    continue

                from_lane, to_lane, _via_lane = connections[0]
                links.append(
                    {
                        "index": index,
                        "from_lane": from_lane,
                        "to_lane": to_lane,
                        "direction": self._link_direction(from_lane, to_lane),
                    }
                )

            signals.append({"id": signal_id, "links": links})

        return {
            "boundary": [min_x, min_y, max_x, max_y],
            "lanes": lanes,
            "junctions": junctions,
            "signals": signals,
        }

    def read_vehicles(self) -> list[dict]:
        """Return the subscribed values of every vehicle on the road."""

        vehicles = []

        for vehicle_id, values in traci.vehicle.getAllSubscriptionResults().items():
            # A vehicle without a lane is off the road, e.g. while teleporting.
            if not values[tc.VAR_LANE_ID]:
                continue

            x, y = values[tc.VAR_POSITION]
            vehicles.append(
                {
                    "id": vehicle_id,
                    "x": x,
                    "y": y,
                    "angle_deg": values[tc.VAR_ANGLE],
                    "speed_mps": values[tc.VAR_SPEED],
                    "waiting_s": values[tc.VAR_WAITING_TIME],
                    "accumulated_waiting_s": values[tc.VAR_ACCUMULATED_WAITING_TIME],
                    "lane": values[tc.VAR_LANE_ID],
                    "route": values[tc.VAR_ROUTE_ID],
                    "type": values[tc.VAR_TYPE],
                }
            )

        return vehicles

    def read_lanes(self) -> dict[str, dict]:
        """Return the subscribed measurements of every road lane."""

        lanes = {}

        for lane_id, values in traci.lane.getAllSubscriptionResults().items():
            lanes[lane_id] = {
                "vehicle_count": values[tc.LAST_STEP_VEHICLE_NUMBER],
                # SUMO counts vehicles below 0.1 m/s as halting.
                "halting_count": values[tc.LAST_STEP_VEHICLE_HALTING_NUMBER],
                # TraCI reports lane occupancy in percent.
                "occupancy": values[tc.LAST_STEP_OCCUPANCY] / 100.0,
                "mean_speed_mps": values[tc.LAST_STEP_MEAN_SPEED],
            }

        return lanes

    def read_signals(self) -> list[dict]:
        """Return the current state of every traffic light."""

        now_s = self.time_s()

        return [
            {
                "id": signal_id,
                "state": traci.trafficlight.getRedYellowGreenState(signal_id),
                "phase": traci.trafficlight.getPhase(signal_id),
                "next_switch_s": traci.trafficlight.getNextSwitch(signal_id) - now_s,
            }
            for signal_id in self.signal_ids
        ]

    def pending_count(self) -> int:
        """Return how many vehicles are due to depart but not yet inserted."""

        return len(traci.simulation.getPendingVehicles())

    def close(self) -> None:
        """Close the TraCI connection; safe to call more than once."""

        if self._connected:
            traci.close()
            self._connected = False

    @staticmethod
    def _link_direction(from_lane: str, to_lane: str) -> str:
        """Return SUMO's direction code (s, l, r, ...) for one movement."""

        for link in traci.lane.getLinks(from_lane, extended=True):
            if link[0] == to_lane:
                return link[6]

        return "?"
