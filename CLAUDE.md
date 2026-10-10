# CLAUDE.md

Context for AI assistants (Claude Code etc.) working in this repo. Shared by a 4-person team, so keep it accurate.

## What this repo is
Our team's project for **AI Quest 2026 — Future Jordan Hackathon** (HTU, 9–10 Oct 2026), sector **`next.society()` — Smart Society & Public Services**.

- Hard deadline: **submit by 1:00 PM, 10 Oct 2026**. Pitch: 7 min demo + 3 min Q&A from 1:30 PM.
- ~11 working hours total. "A small idea that works live beats a big one in slides."
- Judging: Impact on Jordan 25%, Innovation 20%, Feasibility & Scalability 20%, Technical Implementation 15% (working demo + **honesty about what's mocked**), UX 10% (**Arabic where relevant**), Pitch 10%.
- Data rules: public data, data collected on the day, or **clearly labelled synthetic** data. **No real personal data without consent.**

Full brief: [docs/00-hackathon-brief.md](docs/00-hackathon-brief.md)

## The idea: فارس / Faris
AI adaptive traffic signals for Amman. Faris reads the cameras GAM already has, counts queues per approach, sets the green split each cycle within GAM-signed safety limits, and coordinates neighbouring junctions. It's sold B2G to the Greater Amman Municipality. The first site is the 7th Circle cluster. Jordanian dialect, Arabic RTL, dark "control room" brand.

**Latest planning outputs: [iteration_2/](iteration_2/README.md)**, aligned with the implementation on branch `feat/traffic-ai` (start with [iteration_2/00-what-is-built.md](iteration_2/00-what-is-built.md)). Iteration 1 is kept for history. Decisions: [docs/decision-log.md](docs/decision-log.md). Sources: [docs/sources.md](docs/sources.md).

**Don't mention the existing GAM/PSD smart-signal pilot** in pitch materials (team decision).

## Current phase
**Build in progress.** The implementation lives on branch **`feat/traffic-ai`** (SUMO corridor, PPO controller, safety controller, baselines, evaluation, congestion alerts, live viewer). Planning docs live on this branch (`iteration-1`). Still open: Arabic console, YOLO counting clip, pitch storyline and script.
Check [HANDOFF.md](HANDOFF.md) first for the latest state.

## Team
4 people: 3 AI / data-science students (one is an AI researcher; two have industry experience at PwC and Amazon) + 1 computer-science student / software engineer.

## Stack (as built on `feat/traffic-ai`)
- Simulation: **SUMO 1.28** (`eclipse-sumo` via pip) through TraCI; a synthetic 3-junction corridor.
- AI: **shared PPO policy** in PyTorch (CPU), decides NS/EW green every 10 s; a separate deterministic **safety controller** applies it.
- Baselines: tuned fixed timer (12 s green) and sensor-actuated rule (60 m detector).
- Serving: Python `ThreadingHTTPServer` at `http://127.0.0.1:8000` + `viewer/index.html` (English, light) + JSON API.
- Not used: Supabase, LLM. Planned: pretrained YOLO counting clip; Arabic console wrapping the viewer. Brand tokens: [iteration_1/05-branding.md](iteration_1/05-branding.md) (+ viewer mapping in [iteration_2/05-branding.md](iteration_2/05-branding.md)).

## Honesty rules for this idea
- The measured result is: AI vs **tuned fixed timer** on held-out main-road rush hour = **−10% waiting, −23% time lost**. Always say it's one simulated corridor.
- Always disclose: the AI is **40% worse on balanced traffic**, and the **sensor rule beats the AI in every scenario**. Never present the sensor rule's numbers as the AI's.
- Impact numbers in 04 are projections. Label them as such.
- Say "persistent-congestion alert", not "accident detection". Say "uses neighbours' queues", not "proven coordination".
- We don't claim field results, a live camera integration, or control of a real signal. Real-footage counting only once the YOLO clip exists.

## Repo conventions
- `main` is protected by convention. This branch (`iteration-1`) holds only Faris context. Older idea rounds are on `ideation/research`.
- Iteration outputs live in `iteration_N/` folders (latest: `iteration_2/`). Code lives on `feat/traffic-ai`. Decisions are appended to `docs/decision-log.md`.
- Every factual claim gets a source link (add it to `docs/sources.md`).
- Update `HANDOFF.md` at the end of every working session.
