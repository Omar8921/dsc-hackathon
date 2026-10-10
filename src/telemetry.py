"""Telemetry snapshots and the local HTTP endpoint that serves the viewer."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from src.simulation_adapter import SimulationAdapter


SCHEMA_VERSION = "0.1"


def build_snapshot(
    adapter: SimulationAdapter,
    run: dict,
    status: str,
    real_seconds_per_step: float,
    control: dict[str, dict] | None = None,
    states: dict | None = None,
    alerts: list[dict] | None = None,
    trips: dict | None = None,
) -> dict:
    """Combine one step of adapter readings into a telemetry snapshot.

    control is the safety controller's summary per signal ID, if one is running;
    states are the IntersectionState objects for the same step; alerts are the
    congestion events so far, or None when the detector is off; trips is the
    live finished-trip summary.
    """

    vehicles = adapter.read_vehicles()
    lanes = adapter.read_lanes()
    signals = adapter.read_signals()

    # Summarize each signal's incoming lanes for the intersection panel.
    for signal in signals:
        incoming = [
            lanes[lane_id]
            for lane_id in adapter.signal_lanes[signal["id"]]
            if lane_id in lanes
        ]
        signal["queue_count"] = sum(lane["halting_count"] for lane in incoming)
        signal["vehicle_count"] = sum(lane["vehicle_count"] for lane in incoming)

        if control is not None:
            signal_control = control.get(signal["id"])
            signal["control"] = signal_control

            # Per-approach measurements for the viewer's N/E/S/W table.
            if states is not None and signal_control is not None:
                intersection = states[signal_control["intersection_id"]]
                signal["approaches"] = {
                    slot: {
                        "queue": approach.queue_count,
                        "vehicles": approach.vehicle_count,
                        "mean_wait_s": approach.mean_wait_s,
                        "storage": approach.storage_capacity,
                    }
                    for slot, approach in intersection.approaches.items()
                }

    waiting_times = [vehicle["waiting_s"] for vehicle in vehicles]

    return {
        "schema_version": SCHEMA_VERSION,
        **run,
        "status": status,
        "sim_time_s": adapter.time_s(),
        "end_time_s": adapter.end_time_s,
        "real_seconds_per_step": real_seconds_per_step,
        "totals": {
            "running": len(vehicles),
            "departed": adapter.departed_total,
            "arrived": adapter.arrived_total,
            "waiting_to_insert": adapter.pending_count(),
            "mean_waiting_s": (
                sum(waiting_times) / len(waiting_times) if waiting_times else 0.0
            ),
        },
        "signals": signals,
        "lanes": lanes,
        "vehicles": vehicles,
        "alerts": alerts,
        "trips": trips,
    }


def _rounded(value, digits: int = 3):
    """Round floats recursively to keep the JSON payload small."""

    if isinstance(value, float):
        return round(value, digits)

    if isinstance(value, dict):
        return {key: _rounded(item, digits) for key, item in value.items()}

    if isinstance(value, (list, tuple)):
        return [_rounded(item, digits) for item in value]

    return value


def _encode(value) -> bytes:
    return json.dumps(_rounded(value), separators=(",", ":")).encode("utf-8")


class TelemetryServer:
    """Serve the viewer page, the static network, and the latest snapshot.

    Routes:
        GET  /               viewer page
        GET  /api/network    lane, junction, and signal geometry (fixed per run)
        GET  /api/snapshot   latest per-step snapshot
        GET  /api/catalog    runs the viewer may choose from
        POST /api/run        {"scenario", "controller"}: switch to another run
        POST /api/speed      {"speed"}: simulated seconds per real second

    POST requests are passed to on_command(path, payload), which returns a
    JSON-ready result or raises ValueError for a bad request.
    """

    def __init__(self, host: str, port: int, viewer_page: Path) -> None:
        self.viewer_page = viewer_page
        self.on_command = None
        self._lock = threading.Lock()
        self._network: bytes | None = None
        self._catalog: bytes | None = None
        self._snapshot = _encode(
            {"schema_version": SCHEMA_VERSION, "status": "starting"}
        )

        # Binding here fails fast if the port is taken, before SUMO starts.
        self._server = ThreadingHTTPServer((host, port), self._make_handler())
        self._thread = threading.Thread(
            target=self._server.serve_forever, daemon=True
        )

    @property
    def url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}/"

    def set_network(self, network: dict) -> None:
        with self._lock:
            self._network = _encode(network)

    def set_catalog(self, catalog: dict) -> None:
        with self._lock:
            self._catalog = _encode(catalog)

    def publish(self, snapshot: dict) -> None:
        body = _encode(snapshot)

        with self._lock:
            self._snapshot = body

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        # shutdown() waits for serve_forever, so only call it once serving.
        if self._thread.is_alive():
            self._server.shutdown()

        self._server.server_close()

    def _read(self, route: str) -> bytes | None:
        with self._lock:
            return {"network": self._network, "catalog": self._catalog}.get(route, self._snapshot)

    def _make_handler(self) -> type[BaseHTTPRequestHandler]:
        telemetry = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                path = urlsplit(self.path).path

                if path in ("/", "/index.html"):
                    self._send(
                        telemetry.viewer_page.read_bytes(), "text/html; charset=utf-8"
                    )
                elif path in ("/api/network", "/api/catalog"):
                    body = telemetry._read(path.rsplit("/", 1)[1])

                    if body is None:
                        self.send_error(503, "Not available yet")
                    else:
                        self._send(body, "application/json")
                elif path == "/api/snapshot":
                    self._send(telemetry._read("snapshot"), "application/json")
                else:
                    self.send_error(404)

            def do_POST(self) -> None:
                path = urlsplit(self.path).path

                if telemetry.on_command is None or path not in ("/api/run", "/api/speed"):
                    self.send_error(404)
                    return

                try:
                    length = int(self.headers.get("Content-Length") or 0)
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    result = telemetry.on_command(path, payload)
                except (ValueError, TypeError) as error:
                    self._send(_encode({"error": str(error)}), "application/json", status=400)
                    return

                self._send(_encode(result), "application/json")

            def do_OPTIONS(self) -> None:
                # CORS preflight, for an interface posting from its own origin.
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                # Lets the interface read the JSON routes from its own origin.
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args) -> None:
                # The viewer polls ten times per second; keep the console quiet.
                pass

        return Handler
