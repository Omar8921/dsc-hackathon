# Traffic Signal AI

A learned traffic-signal controller for a simulated corridor of connected
intersections. One shared PPO policy chooses a green phase (north–south or
east–west) for every intersection every 10 simulated seconds; a deterministic
safety controller decides what the lights actually show. The policy is
compared with fixed-time and actuated control on held-out traffic.

Design: [docs/TRAFFIC_AI_DESIGN.md](docs/TRAFFIC_AI_DESIGN.md) ·
File layout: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

**Faris (فارس):** the viewer is styled in the Faris brand (dark control-room theme, signal
colours as meaning) and lists the demo use cases only. The pitch deck is
[pitch/faris-deck.html](pitch/faris-deck.html): open it in a browser; ← / PageDown / Space
go forward, → / PageUp go back, F toggles full screen. Planning docs live on branch `iteration-1`.

## What is implemented

| Part | Status |
| --- | --- |
| SUMO corridor network: 3 signalized intersections, 4 approaches each | Done |
| Seeded demand: development, randomized training, and held-out test scenarios | Done |
| Lane / phase / neighbor mapping, checked against the network | Done |
| Per-intersection traffic state and the 44-value policy observation | Done |
| Safety controller: 10 s min green, 60 s max green, 3 s yellow, 1 s all-red | Done |
| Fixed-time and actuated baselines, common metrics | Done |
| Shared-policy PPO: one SUMO clock, all intersections act together | Done |
| Held-out evaluation script and results table | Done |
| Live browser viewer (embeddable), showing requests and applied signals | Done |
| Persistent-congestion alerts, shown in the viewer | Done |
| Independent-intersection generalization test | Not done |
| Pretrained YOLO demo on real footage | Separate session |

## Setup (Windows)

Tested with Python 3.12.9, SUMO 1.28.0 (`eclipse-sumo` from pip), and
PyTorch 2.14.1 (CPU).

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install eclipse-sumo traci sumolib numpy
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## Commands

Run everything from the project root.

```powershell
# 1. Network and demand (committed outputs are reproduced exactly)
.\.venv\Scripts\python.exe scripts\generate_network.py --config configs\network.json
.\.venv\Scripts\python.exe scripts\generate_demand.py --config configs\scenarios.json

# 2. Tests (a few start SUMO and take several seconds)
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# 3. Start the live viewer, then open http://127.0.0.1:8000/ and pick a
#    scenario, a controller (timer, sensors, or the AI), and a speed
.\.venv\Scripts\python.exe scripts\run_simulation.py

# 4. Run a baseline headless and save metrics to results/
.\.venv\Scripts\python.exe scripts\run_simulation.py --scenario simulation\scenarios\ew_heavy.sumocfg --controller fixed-time --headless

# 5. Train the shared PPO policy (checkpoints go to models/)
.\.venv\Scripts\python.exe scripts\train.py --config configs\training.json

# 6. Compare PPO with both baselines on the held-out test scenarios
.\.venv\Scripts\python.exe scripts\evaluate.py --checkpoint models\ppo_main\checkpoint_0120.pt

# 7. Start the viewer directly on a scenario and controller (both can be
#    changed in the page; ppo uses selected_checkpoint from configs/training.json)
.\.venv\Scripts\python.exe scripts\run_simulation.py --scenario simulation\scenarios\demo_incident.sumocfg --controller ppo

# 8. Recalibrate the congestion-alert reference (already calibrated in configs/alerts.json)
.\.venv\Scripts\python.exe scripts\calibrate_alerts.py
```

In the viewer, the panel shows plain-language numbers by default (average
time stopped per finished trip, cars stopped at lights, cars waiting by
direction, traffic-jam alerts). "Show technical details" adds the raw SUMO
measurements.

The viewer can be embedded in another web page:

```html
<iframe src="http://127.0.0.1:8000/" style="width:100%;height:100%;border:0"></iframe>
```

## Results

Held-out evaluation: 3 scenarios × 3 unseen seeds, 900 s each, identical
demand for every controller. Full table: [results/eval_final/summary.md](results/eval_final/summary.md).

How the comparison was kept fair:

- Test scenarios and seeds were fixed before training and never used for any choice.
- The PPO checkpoint (update 120 of 150) was selected on the development
  scenarios only.
- Baseline settings were tuned on the same development scenarios:
  fixed-time green 12 s (from 10–30 s), actuated detector 60 m (from 20–80 m).
- All three controllers run through the same safety controller.

Mean waiting time of completed trips, seconds (mean ± sd over seeds):

| Scenario | Fixed-time | Actuated | PPO |
| --- | --- | --- | --- |
| Balanced | 6.3 ± 0.5 | **4.8 ± 0.8** | 8.8 ± 0.8 |
| East–west heavy | 14.1 ± 3.6 | **7.5 ± 0.2** | 12.6 ± 0.5 |
| Demand shift | 9.0 ± 1.7 | **5.4 ± 1.1** | 9.2 ± 0.7 |

Mean time loss, seconds:

| Scenario | Fixed-time | Actuated | PPO |
| --- | --- | --- | --- |
| Balanced | 16.8 ± 1.3 | **13.0 ± 1.1** | 18.3 ± 1.6 |
| East–west heavy | 35.9 ± 7.9 | **20.5 ± 0.5** | 27.7 ± 1.3 |
| Demand shift | 23.3 ± 3.5 | **14.6 ± 1.5** | 19.9 ± 1.2 |

What this shows:

- **Safety held:** 0 illegal signal transitions in all 27 runs. The safety
  controller rejected 60–85 PPO switch requests per run, mostly for minimum green.
- **PPO vs tuned fixed-time:** better under east–west-heavy demand (10% less
  waiting, 23% less time loss), mixed under the demand shift (similar waiting,
  15% less time loss), worse under balanced demand (40% more waiting).
- **PPO vs actuated:** worse in every scenario. The actuated baseline reacts
  every second to vehicles at the stop line; the policy decides every 10 s.
- Training: 150 PPO updates (300 randomized episodes, about 35 minutes on a CPU).
  Development-scenario waiting fell from 12.2 s (update 10) to 9.5 s (update 120).

These results apply only to this simulated corridor and these scenarios.

### Congestion alerts

A separate detector watches each intersection's worst approach queue and
raises an alert when it stays above both its normal 95th percentile and half
the approach's storage for 30 s; it clears after 30 s below. The reference was
calibrated on the development scenarios with the actuated controller.
In `demo_incident`, a vehicle blocks the northbound exit of B0 for 240 s:
an alert is raised at B0 about 80 s after the blockage and resolved after it
clears, with no alerts at A0 or C0. It reports persistent congestion, not its cause.

## Limitations

- Simulation only. Nothing here has been validated on real intersections.
- One standardized intersection type: four single-lane approaches, two green
  phases, straight-through demand.
- The reward uses queue length as a proxy for delay; evaluation reports
  measured waiting time and time loss.
- Results apply only to the scenarios measured here.
