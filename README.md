# Faris (فارس)

AI traffic signals for Amman, built for AI Quest 2026 (Future Jordan Hackathon, HTU), sector `next.society()`.

Most signals in Amman run on a fixed timetable. At a busy junction the main road can sit on red while the empty side street gets green. Faris watches the queues at each junction and its neighbours and asks for green where cars are actually waiting. A separate safety layer decides what the lights show, so the AI can never produce an unsafe signal.

Everything here runs in a traffic simulation. Nothing is connected to a real camera or a real traffic light.

## What the system does

The demo is a SUMO simulation of a road with three connected junctions (A0, B0, C0), 300 m apart, one lane per direction, straight-through traffic.

1. **Traffic state.** Every simulated second the backend reads each approach of each junction: queue, number of cars, occupancy, arrivals, waiting time, speed, and how full the road after the junction is. It turns this into 44 numbers per junction, including the queues at the neighbouring junctions.
2. **AI controller.** One shared neural network (PPO, two hidden layers of 64) runs for every junction. Every 10 seconds it asks for either north-south green or east-west green. It was trained in about 35 minutes on a laptop CPU, on randomised traffic.
3. **Safety controller.** The AI only makes requests. A deterministic controller decides what the lights do: at least 10 s and at most 60 s of green, 3 s yellow and 1 s all-red on every change. Invalid requests fall back to a fixed timer. Every request is logged with what was applied and why.
4. **Baselines.** The same safety controller also runs a fixed timer (12 s green) and a sensor rule (switches when no car is within 60 m of the stop line). Both were tuned on development traffic so the comparison is fair.
5. **Congestion alerts.** If a junction's worst queue stays above its normal 95th percentile and more than half full for 30 s, an alert is raised. It clears after 30 s below that level. It flags a long queue, not its cause.
6. **Live interface.** A small Python web server streams the simulation to a browser page with a city map, moving cars, light colours over the last two minutes, cars waiting per direction, and alerts. You can switch the scenario, the controller and the speed from the page.

## Results

Held-out test: 3 scenarios, 3 traffic seeds each that were never used in training, 900 s per run, the same traffic for every controller. Mean waiting time per finished trip, in seconds:

| Scenario | Fixed timer | Sensor rule | Faris AI |
| --- | --- | --- | --- |
| Balanced | 6.3 | 4.8 | 8.8 |
| Main-road rush hour | 14.1 | 7.5 | 12.6 |
| Demand shift | 9.0 | 5.4 | 9.2 |

- In main-road rush hour, a full main road crossing quiet side streets, Faris cut waiting by 10% and time lost by 23% compared with the fixed timer.
- On balanced traffic Faris was 40% worse than the fixed timer.
- The sensor rule did better than Faris in every scenario. It reacts every second, while Faris decides every 10 s.
- There were 0 unsafe signal changes in all 27 runs.

Full table: [results/eval_final/summary.md](results/eval_final/summary.md). These numbers only describe this simulated corridor.

## Tech stack

| Part | Tool |
| --- | --- |
| Traffic simulation | SUMO 1.28 (`eclipse-sumo` from pip), controlled through TraCI |
| AI | PyTorch (CPU), PPO implemented in `src/policy.py` |
| Web server and API | Python standard library (`src/telemetry.py`) |
| Interface | One HTML page with canvas and plain JavaScript (`viewer/index.html`) |
| Settings | JSON files in `configs/` |

## Run it locally

You need Python 3.12 and Git. These steps were tested on Windows. Setup takes 5 to 10 minutes because PyTorch is a large download.

**1. Clone the repository**

```powershell
git clone https://github.com/Omar8921/dsc-hackathon.git faris
cd faris
```

If you already cloned it before, run `git fetch` then `git switch main` and `git pull` inside that folder instead.

**2. Create a virtual environment and install the packages**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install eclipse-sumo traci sumolib numpy
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

On macOS or Linux (not tested by us):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install eclipse-sumo traci sumolib numpy torch
```

**3. Start the website**

```powershell
.\.venv\Scripts\python.exe scripts\run_simulation.py --scenario simulation\scenarios\ew_heavy.sumocfg --controller ppo
```

On macOS or Linux use `python scripts/run_simulation.py --scenario simulation/scenarios/ew_heavy.sumocfg --controller ppo`.

**4. Open http://127.0.0.1:8000 in your browser.**

Pick a scenario and who controls the lights, then press Run. Stop the server with Ctrl + C.

If the page keeps saying "connecting", look for a Windows Security pop-up asking about `sumo.exe` or `python.exe`. It can hide behind other windows. Click Allow. If port 8000 is busy, add `--port 8001` to the command.

## Other commands

Run these from the project folder.

```powershell
.\.venv\Scripts\python.exe scripts\run_simulation.py --scenario simulation\scenarios\demo_incident.sumocfg --controller ppo
```
Opens the congestion alert demo, where a stopped car blocks the road after B0 for four minutes.

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py --checkpoint models\ppo_main\checkpoint_0120.pt
```
Re-runs the held-out comparison. It takes a while.

```powershell
.\.venv\Scripts\python.exe scripts\train.py --config configs\training.json
```
Trains the AI again (about 35 minutes on a CPU).

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
Runs the tests. Some of them start SUMO.

## Project layout

| Folder | Contents |
| --- | --- |
| `src/` | Simulation adapter, traffic state, observations, AI policy, safety controller, baselines, alerts, metrics, web server |
| `scripts/` | Command line entry points: generate the network and traffic, run, train, evaluate |
| `configs/` | Safety timings, scenarios, training settings, alert thresholds |
| `simulation/` | SUMO network, traffic routes and scenario files |
| `models/` | Trained AI checkpoint used by the demo |
| `results/` | Held-out evaluation summary |
| `viewer/` | The web interface |
| `tests/` | Unit and episode tests |
| `pitch/` | Pitch deck |
| `docs/` | Design document and file structure |

## Limitations

- Simulation only. Nothing has been tested on real junctions, cameras or signal hardware.
- One simplified junction type: four single-lane approaches, two green phases, no turns and no pedestrian phases.
- The AI is not yet better than a simple sensor rule. It helps most when one road is much busier than the other.
- Car counting from real camera footage is not part of this code.
