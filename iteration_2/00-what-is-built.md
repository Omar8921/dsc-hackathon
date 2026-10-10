# 00. What is actually built (branch `feat/traffic-ai`)

**Read this first.** Everything else in iteration 2 is aligned to this page. Source: the code, README, design doc and `results/eval_final/summary.md` on `origin/feat/traffic-ai` at commit `3a789e8` (Omar, 10 Oct 2026, 03:20).

## In one paragraph
A **SUMO traffic simulation of a 3-junction corridor** (A0 – B0 – C0, 300 m apart, one lane per approach, straight-through traffic only). Every 10 simulated seconds, **one shared AI policy (PPO, a small neural network)** looks at each junction's queues, plus its neighbours' queues, and picks which direction gets green: north–south or east–west. **Fixed timing rules** (the safety controller) carry out each choice safely. It enforces minimum and maximum green, yellow and all-red, and falls back to a fixed timer if a request is invalid. The AI is compared fairly against a **tuned fixed timer** and a **sensor-actuated rule** on traffic it never saw in training. A **congestion detector** raises alerts when a queue stays abnormally long. A **live browser viewer** shows all of it, and you can switch scenario and controller from the page.

## How it works

```
SUMO (1 s steps) ──► traffic state per junction (queue, count, occupancy, arrivals, wait, speed, downstream)
                         │
                         ├──► 44-number observation (own 4 approaches + neighbours + signal state)
                         │          │
                         │          ▼
                         │   Shared PPO policy (every 10 s): "I want NS green" / "I want EW green"
                         │          │
                         │          ▼
                         │   Safety controller: min green 10 s · max green 60 s · yellow 3 s · all-red 1 s
                         │   · invalid AI output → fixed-timer fallback · logs chosen vs shown phase + reason
                         │          │
                         │          ▼
                         │       SUMO lights
                         │
                         ├──► Congestion detector → alerts (active / resolved)
                         └──► Telemetry server (http://127.0.0.1:8000) → viewer + JSON API
```

## Features that exist today

| # | Feature | Where | Notes |
|---|---|---|---|
| 1 | 3-junction corridor simulation | `simulation/`, `scripts/generate_network.py` | Synthetic, not a real Amman layout |
| 2 | Seeded traffic scenarios | `configs/scenarios.json` | Balanced, **main-road rush hour** (600 vs 150 cars/h), demand shift, **incident at B0**, 9 held-out test runs |
| 3 | AI signal controller (shared PPO) | `src/policy.py`, `scripts/train.py`, `models/ppo_main/checkpoint_0120.pt` | Trained on a CPU in ~35 min; picks the phase every 10 s; sees neighbour queues |
| 4 | Safety controller | `src/safety_controller.py`, `configs/controller.json` | **0 illegal transitions in all 27 test runs.** In each run, 60–85 of the AI's switch choices came before the 10 s minimum green and waited for the next decision |
| 5 | Two baselines | `src/baselines.py` | Fixed timer (12 s green, tuned) and actuated (60 m virtual detector, tuned). Both go through the same safety controller |
| 6 | Fair held-out evaluation | `scripts/evaluate.py`, `results/eval_final/` | 3 scenarios × 3 unseen seeds; baselines tuned on dev scenarios only |
| 7 | Persistent-congestion alerts | `src/congestion_detector.py`, `configs/alerts.json` | Alert if the worst queue is above its normal 95th percentile **and** half full for 30 s. In the incident demo it fires ~80 s after the blockage and clears afterwards |
| 8 | Live viewer | `viewer/index.html`, `scripts/run_simulation.py` | City map, cars, light-colour strips, waiting per direction, alerts, scenario/controller/speed pickers, "technical details" toggle. **English, light theme** |
| 9 | JSON API | `src/telemetry.py` | `GET /api/network`, `/api/snapshot`, `/api/catalog`; `POST /api/run`, `/api/speed`. Each snapshot carries the phase the AI **chose**, the phase the lights **show**, and the timing rule that delayed a change, if any |
| 10 | Tests | `tests/` (12 files) | Safety, observations, reward, baselines, episodes, training |

## Measured results (held-out, mean over 3 seeds, 900 s each)

**Mean waiting time per completed trip (s), lower is better**

| Scenario | Fixed timer | Sensor rule (actuated) | AI (PPO) | AI vs timer |
|---|---|---|---|---|
| Balanced | 6.3 | **4.8** | 8.8 | **40% worse** |
| **Main-road rush hour** | 14.1 | **7.5** | 12.6 | **10% better** |
| Demand shift | 9.0 | **5.4** | 9.2 | ~same (3% worse) |

**Mean time lost per trip (s)**

| Scenario | Fixed timer | Sensor rule | AI (PPO) | AI vs timer |
|---|---|---|---|---|
| Balanced | 16.8 | **13.0** | 18.3 | 9% worse |
| **Main-road rush hour** | 35.9 | **20.5** | 27.7 | **23% better** |
| Demand shift | 23.3 | **14.6** | 19.9 | 15% better |

What this honestly says:
- **The AI wins exactly where our problem statement points:** the lopsided junction, a loaded main road crossing quiet side streets. There it cuts waiting by **10%** and time lost by **23%** against a properly tuned timer, on traffic it never saw.
- **It loses on balanced traffic** (40% more waiting than the timer).
- **The simple sensor rule beats the AI in every scenario.** It reacts every second; the AI decides every 10 s. In rush hour the sensor rule cuts waiting by **47%** against the timer.
- **Safety held everywhere:** 0 illegal transitions in 27 runs.
- These results apply **only to this simulated corridor**.

## Not built yet (from the branch's own README and design doc)

| Missing | Why it matters for the pitch |
|---|---|
| **Camera perception (pretrained YOLO on real footage)** | Listed as "separate session". Without it, we can't show "Faris reads the cameras". Today the counts come from the simulator |
| **Arabic, branded operator console** | The viewer is English with a light theme. Iteration 1 promised an Arabic dark "control room" screen that explains decisions (UX = 10%) |
| **Arabic explanation of each decision** | The data exists (chosen vs shown phase + timing rule); nothing turns it into a sentence yet |
| **Operator override button** | You can switch the controller from a dropdown, but that restarts the run. No one-click "back to the fixed plan" mid-run |
| **Independent-intersection generalisation test** | In the design, not done |
| Pedestrian phases, turning lanes, multi-lane roads, emergency priority | Out of V1 scope |
| Any real-world data, camera link or real signal | Simulation only |
| Supabase, LLM | Not used anywhere. The stack is Python + SUMO + PyTorch + a plain HTML viewer with a small Python HTTP server |

## Words to use and avoid (from the design doc)
- ✅ "a learned controller, evaluated against tuned baselines on held-out traffic"
- ✅ "persistent-congestion alert"; ❌ "accident detection"
- ✅ "uses neighbouring junctions' queues as input"; ❌ "proven coordination" (sharing weights alone doesn't prove it)
- ✅ "implemented a pretrained YOLO pipeline" (only once it exists); ❌ "trained our own detector"
- ❌ Never present the sensor rule's numbers as the AI's.
