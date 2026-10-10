# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section).

_Last updated: 2026-10-10 (Day 2), Faris planning, iteration 1._

## Status
- **Idea: فارس / Faris**, AI adaptive traffic signals on GAM's existing cameras, sold B2G. Branch `iteration-1` holds only this idea; older rounds are on `ideation/research`.
- **Iteration 1 done** → [iteration_1/](iteration_1/README.md): 01 problem, 02 users, 03 feasibility, 04 impact, 05 branding, 06 revenue/costs, 07 pitch deck (HTML, Arabic RTL).
- Key decisions ([docs/decision-log.md](docs/decision-log.md)): GAM buyer, PSD partner; fully automatic within safety limits; 7th Circle cluster first; JD 3,000 setup + JD 200/month per junction; don't mention the existing pilot.
- **Not decided yet:** feature list, modules, tech stack, user flow, pitch storyline and script.

## Next actions
1. Lock features and modules, then build: SUMO baseline (Webster) vs our controller, vehicle counting on recorded footage, Arabic operator console.
2. Put the SUMO X% into deck slide 9 and impact doc 04 (replacing the scenarios).
3. Fix 01: remove the pilot references, replace the local-path source, change "16 hours/yr" to the 5–14 h range.
4. Name the 7th Circle's neighbouring junctions; verify the FHWA cost page; add team names to the deck.
5. Check the venue's internet for the deck font, or bundle IBM Plex Sans Arabic locally.

## Key facts (sources in docs/sources.md)
- GAM: ~5,600 cameras (75% not for violations, mostly counting), central control for 200+ intersections.
- Amman: ~11.5M vehicle movements a day, ~2M vehicles; transport inefficiency ≈ 6% of GDP (World Bank).
- FHWA: adaptive signal control improves travel time >10% on average.
- 2.2M students back to school (Aug 2026); the Traffic Department advises leaving 10 min early in school season.
