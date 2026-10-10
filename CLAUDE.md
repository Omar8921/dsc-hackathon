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

All planning outputs are in [iteration_1/](iteration_1/README.md). Decisions: [docs/decision-log.md](docs/decision-log.md). Sources: [docs/sources.md](docs/sources.md).

**Don't mention the existing GAM/PSD smart-signal pilot** in pitch materials (team decision).

## Current phase
**Planning, iteration 1 done** (problem, users, feasibility, impact, branding, revenue, deck v1). Still to decide: feature list, modules, tech stack, user flow, pitch storyline and script.
**Don't scaffold or write application code until the team explicitly says we're moving to build.**
Check [HANDOFF.md](HANDOFF.md) first for the latest state.

## Team
4 people: 3 AI / data-science students (one is an AI researcher; two have industry experience at PwC and Amazon) + 1 computer-science student / software engineer.

## Tentative stack (not final)
- Simulation: SUMO (fixed plan tuned with Webster vs our controller). Vision: YOLO-style vehicle counting on recorded footage.
- Frontend: Arabic RTL operator console (web). Brand tokens are in [iteration_1/05-branding.md](iteration_1/05-branding.md).
- Backend: **Supabase** (Postgres, auth, storage, edge functions).
- AI: vision counting + timing controller; LLM for Arabic explanations of decisions.

## Honesty rules for this idea
- Only quote our own SUMO result for "X% less waiting", measured against a **properly tuned** fixed plan. Never against a weak baseline.
- Impact numbers in 04 are scenario arithmetic. Label them as such.
- We don't claim field results, a live camera integration, or control of a real signal.

## Repo conventions
- `main` is protected by convention. This branch (`iteration-1`) holds only Faris context. Older idea rounds are on `ideation/research`.
- Iteration outputs live in `iteration_N/` folders. Decisions are appended to `docs/decision-log.md`.
- Every factual claim gets a source link (add it to `docs/sources.md`).
- Update `HANDOFF.md` at the end of every working session.
