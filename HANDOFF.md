# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section).

_Last updated: 2026-10-10 (Day 2), iteration 2: docs aligned with the build._

## Status
- **Code:** branch `feat/traffic-ai` (Omar): SUMO 3-junction corridor, shared PPO controller, safety controller, tuned timer + sensor-rule baselines, held-out evaluation, congestion alerts, live viewer (English). How to run: [iteration_2/08](iteration_2/08-stack-run-and-deploy.md).
- **Docs:** [iteration_2/](iteration_2/README.md) redoes iteration 1 against the code. Start with [00-what-is-built](iteration_2/00-what-is-built.md).
- **Measured:** AI vs tuned timer on held-out rush hour = −10% waiting, −23% time lost; 40% worse on balanced; the sensor rule beats the AI everywhere; 0 illegal transitions in 27 runs.
- **Missing for the pitch:** Arabic console page, YOLO counting clip, backup demo video, storyline and script.

## Next actions
1. Build the Arabic console (iframe + `/api/snapshot`, labels and templates in [iteration_2/05](iteration_2/05-branding.md)).
2. Pretrained YOLO counting clip on real footage (watch the AGPL licence note in [iteration_2/07](iteration_2/07-features-and-modules.md)).
3. Team confirms the framing decision (decision log, 2026-10-10).
4. Record the demo (rush hour timer → AI; incident → alert) as a backup.
5. Storyline and script; team names in the deck; the 7th Circle's neighbouring junctions; verify the FHWA cost page.

## Key facts (sources in docs/sources.md)
- GAM: ~5,600 cameras (75% not for violations, mostly counting), central control for 200+ intersections.
- Amman: ~11.5M vehicle movements a day, ~2M vehicles; transport inefficiency ≈ 6% of GDP (World Bank).
- FHWA: adaptive signal control improves travel time >10% on average.
- 2.2M students back to school (Aug 2026); the Traffic Department advises leaving 10 min early in school season.
