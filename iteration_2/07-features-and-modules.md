# 07. Features and modules (grounded in the code)

**Draft v1, Oct 10 2026 (iteration 2).** Every feature is mapped to the code on `feat/traffic-ai` and marked:
- ✅ **built**: in the code, working and tested.
- 🛠 **build today**: needed for the pitch, small enough for today.
- 🗺 **roadmap**: we say it on the roadmap slide only.

## Modules

| # | Module | What it does | Code | Status |
|---|---|---|---|---|
| M1 | **Perception** (يشوف) | Camera footage → vehicles, tracks, counts per approach | not on the branch (`scripts/run_perception.py`, `src/perception.py` are planned in PROJECT_STRUCTURE) | 🛠 |
| M2 | **Traffic state** | Per-junction measurements: queue, count, occupancy, arrivals, wait, speed, downstream; 44-number observation incl. neighbours | `src/simulation_adapter.py`, `src/state.py`, `src/observations.py` | ✅ (simulator source) |
| M3 | **Decision** (يقرّر) | Shared PPO policy asks for a green direction every 10 s; baselines for comparison | `src/policy.py`, `src/rl_environment.py`, `src/baselines.py`, `scripts/train.py` | ✅ |
| M4 | **Safety** (يحمي) | Enforces min/max green, yellow, all-red, fallback; logs requested vs applied | `src/safety_controller.py`, `configs/controller.json` | ✅ |
| M5 | **Alerts** (ينبّه) | Persistent-congestion detection per junction | `src/congestion_detector.py`, `configs/alerts.json`, `scripts/calibrate_alerts.py` | ✅ |
| M6 | **Evaluation** | Same demand, seeds and safety for every controller; held-out results table | `src/metrics.py`, `src/runner.py`, `scripts/evaluate.py` | ✅ |
| M7 | **Operator console** (يشرح) | Live map + Arabic panels, explanations, override | `viewer/index.html`, `src/telemetry.py` (API) | ✅ English viewer · 🛠 Arabic console |
| M8 | **Simulation / digital twin** | Network + demand + scenarios | `simulation/`, `scripts/generate_*.py`, `configs/` | ✅ corridor · 🗺 7th Circle |

## Full feature list

### M1 Perception
| Feature | Status |
|---|---|
| Pretrained YOLO vehicle detection on recorded junction footage | 🛠 |
| Tracking (IDs) + counts per drawn approach region | 🛠 |
| Queue / wait from video (needs tracking + stationary threshold) | 🗺 |
| Camera-confidence check → fallback | 🗺 |
| Feeding camera counts into the controller (camera adapter) | 🗺 (design keeps it separate in V1) |

### M2–M3 State and decision
| Feature | Status |
|---|---|
| 44-value observation, same for every junction | ✅ |
| Neighbour queues/occupancy as input | ✅ (coordination **not proven**) |
| One shared AI policy for all junctions (PPO, 2×64 network) | ✅ |
| Decision every 10 s, choose NS or EW green | ✅ |
| Reward: queue + downstream-congestion penalty | ✅ |
| Randomised training demand; held-out test seeds fixed before training | ✅ |
| Tuned fixed-timer and sensor-actuated baselines | ✅ |
| Faster decisions (every 1–5 s), turn phases, multi-lane | 🗺 |
| Independent-intersection generalisation test | 🗺 (in design, not done) |
| Emergency-vehicle and bus priority | 🗺 |

### M4 Safety
| Feature | Status |
|---|---|
| Min green 10 s, max green 60 s, yellow 3 s, all-red 1 s | ✅ |
| Reject early switches; ignore requests mid-transition | ✅ |
| Invalid AI output → fixed-timer fallback | ✅ |
| Log requested / applied / reason | ✅ |
| Pedestrian phases | 🗺 |

### M5 Alerts
| Feature | Status |
|---|---|
| Persistent-congestion alert (95th percentile + half-full, 30 s), clears after 30 s | ✅ |
| Incident demo scenario (blocked exit at B0 for 4 min) | ✅ |
| Notifying the Traffic Department (real message) | 🗺 |

### M7 Operator console
| Feature | Status |
|---|---|
| Live map, cars, light-colour history strips, waiting per direction | ✅ (English) |
| Scenario / controller / speed pickers | ✅ |
| Plain-language numbers + "technical details" toggle | ✅ (English) |
| JSON API (`/api/snapshot` etc.), embeddable in an iframe | ✅ |
| **Arabic RTL, dark Faris-branded page** wrapping the viewer | 🛠 |
| **Arabic sentence per decision** (templates in [05](05-branding.md)) | 🛠 |
| **Side-by-side timer vs AI headline numbers** in Arabic | 🛠 |
| One-click "back to the fixed plan" without restarting the run | 🗺 (needs a backend change) |

## What's missing to pitch, in priority order

| # | Gap | Why | Size | Suggested owner |
|---|---|---|---|---|
| 1 | **Arabic console page** (iframe + Arabic panels from `/api/snapshot`) | UX 10%, "Arabic where relevant", and our deck promises it | ~2–3 h | Software engineer |
| 2 | **Pretrained YOLO counting clip** on real footage | Backs "يشوف" and the camera story; otherwise say "counts from the simulator" | ~2 h | AI member |
| 3 | **Backup screen recording** of the demo (rush hour timer → AI; incident → alert) | If the live run breaks | 20 min | Anyone |
| 4 | Deck numbers and honesty slide match [00](00-what-is-built.md) | Technical score depends on honesty about what's mocked | done in [10](10-pitch-deck.html) | — |
| 5 | Rehearse the 3 Q&A answers: "why is the sensor rule better?", "is this coordination?", "what about pedestrians?" | They will be asked | 15 min | Presenters |

> ⚠️ **Licence check for M1:** the popular Ultralytics YOLO package is **AGPL-3.0**. Fine for a hackathon demo, but a paid B2G product would need their commercial licence or a permissively licensed detector. Mention it if asked; don't put it on a slide.

## Q&A answers grounded in the results
- **"Why is the simple sensor rule better than your AI?"** It reacts every second; our AI decides every 10 s and was trained for 35 minutes. Where traffic is lopsided, which is our problem, the AI already beats the timer by 10% (wait) and 23% (time lost). Faris runs whichever controller measures best per junction, and both go through the same safety layer.
- **"Is it coordinating junctions?"** Each junction's AI sees its neighbours' queues. We haven't proven coordination, and we don't claim it.
- **"Pedestrians?"** Not in V1. Pedestrian phases are the first thing added for a real junction.
- **"Is the alert an accident detector?"** No. It flags a queue that stays abnormally long. The cause could be an accident, a broken-down car or roadworks.
