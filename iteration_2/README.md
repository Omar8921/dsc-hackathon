# Iteration 2: فارس / Faris, aligned with what is built

Iteration 1 was planned before any code existed. Iteration 2 grounds every document in the implementation on branch **`feat/traffic-ai`** (commit `3a789e8`) and redoes iteration 1 so the docs, the deck and the demo tell the same, true story.

**Start with [00-what-is-built.md](00-what-is-built.md).**

| # | File | Status |
|---|---|---|
| 00 | [00-what-is-built.md](00-what-is-built.md) | **New.** What the code does, features, measured results, what's missing |
| 01 | [01-problem-statement.md](01-problem-statement.md) | Revised |
| 02 | [02-target-users.md](02-target-users.md) | Small update |
| 03 | [03-feasibility.md](03-feasibility.md) | Revised |
| 04 | [04-value-and-impact.md](04-value-and-impact.md) | Revised |
| 05 | [05-branding.md](05-branding.md) | Brand unchanged + new section for the viewer |
| 06 | [06-revenue-and-costs.md](06-revenue-and-costs.md) | Small update |
| 07 | [07-features-and-modules.md](07-features-and-modules.md) | **New.** Full feature list by module, built / build today / roadmap, gaps to pitch, Q&A |
| 08 | [08-stack-run-and-deploy.md](08-stack-run-and-deploy.md) | **New.** Real stack, how to run on Windows, demo script, hosting options |
| 09 | [09-pitch-deck.html](09-pitch-deck.html) | Revised: slides 6, 7, 8, 9, 10, 14 |

## The key fact that changed the pitch
The AI (PPO) **beats a tuned fixed timer on main-road rush hour** (−10% waiting, −23% time lost, unseen traffic). That is exactly the lopsided-junction problem in our statement. But it is **40% worse on balanced traffic**, and a **simple sensor rule beats it everywhere**. Iteration 1 assumed an unknown "X%" win. Iteration 2 says what was measured, including the losses, because judges score honesty about what's mocked.

**Framing decision (team can override):** Faris is the platform (perception → decision → safety → alerts → Arabic console). Per junction it runs the controller that measures best, and it never labels the sensor rule as the AI. The pitch headline is the AI's rush-hour result.

## What changed from iteration 1, file by file

| Where | Iteration 1 said | Iteration 2 says | Why |
|---|---|---|---|
| 01 statement | "prove it on an Amman junction model" | Tested in a simulated **3-junction corridor** | That's what exists |
| 01 claims | X% vs a **Webster** plan; counts from **real footage** | **10% / 23%** vs a **tuned fixed timer** (12 s green, chosen on dev scenarios), plus the losses; real-footage counts only once YOLO exists | Measured results; YOLO isn't built |
| 01 facts / why now | Relied on the existing pilot | Pilot removed (team decision); GAM's cameras + control centre instead | Consistency with the decision log |
| 01 per person | "16 hours a year" | **5–14 hours a year** | Matches 04 |
| 01 sources | A file on a teammate's laptop | Public link + results file | Unreachable source |
| 03 safety | Pedestrian time, camera-confidence fallback, one-click override, Arabic log as if built | Built: 10 s min / 60 s max green, 3 s yellow, 1 s all-red, invalid → fixed timer, **0 illegal transitions in 27 runs**. The rest is **"to add"** | Only claim what's built |
| 03 rollout | AI controls the cluster | **Controller chosen per junction by measurement**; phase 1 extends the model to real layouts (turns, lanes, pedestrians) | The AI doesn't win everywhere; V1 is a simplified junction |
| 03 risks | — | + "AI not better than a simple rule", + "real junctions more complex" | Shown by our own results |
| 04 impact | 10% = FHWA floor | 10% = **our AI, measured** (rush hour); 20–30% = within the sensor rule's measured range | Anchored to data |
| 05 brand | — | Token map viewer → Faris; Arabic labels for every controller, scenario, override reason and alert; decision-sentence templates | The viewer is English and light |
| 06 costs | GPU for the controller; Supabase + LLM in the build | AI runs on a CPU; GPU only for perception; real build stack | Matches the code |
| CLAUDE.md stack | Supabase, LLM, Webster | Python + SUMO + PyTorch + HTML viewer | Matches the code |
| Deck slide 6 | يشوف / يقرّر / **ينسّق** / يشرح | يشوف / يقرّر / **يحمي** / **ينبّه** | Coordination isn't proven; safety and alerts are built |
| Deck slide 7 | Pedestrians, camera fallback | Real limits + **0 unsafe transitions in 27 runs**; pedestrians flagged as next | Built vs not |
| Deck slide 8 | Generic demo | Rush hour: timer vs Faris; incident → alert | The real demo |
| Deck slide 9 | X% placeholder | **10% / 23%** + the 3-scenario table, including the loss | Measured |
| Deck slide 10 | "if we save 10%" | "if the 10% **we measured** held across Amman" + labelled as a projection | Honesty |
| Deck slide 14 | Listed YOLO + Arabic console as working | Lists what's actually working, plus **what's still weak** (sensor rule better; balanced worse) | Technical score = honesty |

## Still open (team)
1. **Build today:** Arabic console page (iframe + `/api/snapshot`) and a pretrained-YOLO counting clip. See [07](07-features-and-modules.md) for the priority list.
2. Confirm the framing decision above.
3. Pitch storyline and script (deferred since iteration 1).
4. Record a backup demo video ([08](08-stack-run-and-deploy.md)).
5. Name the 7th Circle's neighbouring junctions; verify the FHWA cost page; add team names to the deck.
