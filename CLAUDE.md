# CLAUDE.md

Context for AI assistants (Claude Code etc.) working in this repo. Shared by a 4-person team, so keep it accurate.

## What this repo is
Our team's project for **AI Quest 2026 — Future Jordan Hackathon** (HTU, 9–10 Oct 2026), sector **`next.society()` — Smart Society & Public Services**.

- Hard deadline: **submit by 1:00 PM, 10 Oct 2026**. Pitch: 7 min demo + 3 min Q&A from 1:30 PM.
- ~11 working hours total. "A small idea that works live beats a big one in slides."
- Judging: Impact on Jordan 25%, Innovation 20%, Feasibility & Scalability 20%, Technical Implementation 15% (working demo + **honesty about what's mocked**), UX 10% (**Arabic where relevant**), Pitch 10%.
- Data rules: public data, data collected on the day, or **clearly labelled synthetic** data. **No real personal data without consent.**

Full brief: [docs/00-hackathon-brief.md](docs/00-hackathon-brief.md)

## Current phase
**Ideation / planning. Do not scaffold or write application code unless the team explicitly says we're moving to build.**
Check [HANDOFF.md](HANDOFF.md) first for the latest state, then [docs/README.md](docs/README.md).

## Team
4 people: 3 AI / data-science students (one is an AI researcher; two have industry experience at PwC and Amazon) + 1 computer-science student / software engineer.

## Tentative stack (not final)
- Frontend: web app or mobile (undecided). Must support **Arabic / RTL**.
- Backend: **Supabase** (Postgres, auth, storage, edge functions).
- AI: LLM API and/or agents. The AI must do something a plain form/website can't.

## Idea principles (agreed)
1. Avoid the predictable ideas every team gets from an LLM. See [docs/01-common-ideas-to-avoid.md](docs/01-common-ideas-to-avoid.md).
2. One singular, real problem for a clear group in Jordan, backed by data and sources.
3. Prefer problems with a **proven solution abroad** (China, Saudi, UAE, India, etc.) that doesn't exist in Jordan yet.
4. Always answer: *who is left out today, and does our app actually reach them?*

## Repo conventions
- `main` is protected by convention. Work on branches (`ideation/research` holds the planning docs).
- Docs live in `docs/`. One file per idea in `docs/ideas/`, same template. Decisions are appended to `docs/03-decision-log.md`.
- Every factual claim in docs gets a source link (add it to `docs/sources.md`).
- Update `HANDOFF.md` at the end of every working session.
