# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section; don't let it grow forever).

_Last updated: 2026-10-09 (Day 1), ideation session 2._

## Status
- Phase: **ideation**, no code. Branch `ideation/research`.
- History: R1 rejected → R2 Najm (H) → R3 learning studio (L) → R4 top 5 → R5 big problems (07) → R6 solutions for smoking/reading/traffic (08; team not convinced they're "hackathon-winning") → **R7: Najm deep-dive → [docs/ideas/H3-najm-wow-revenue-training.md](docs/ideas/H3-najm-wow-revenue-training.md).**
- **Current lead: H (Najm for Jordan) = 4.70**, with the wow feature **"AI draws the kroka"**: photos + two dialect voice statements + GPS → animated reconstruction on the real OpenStreetMap street + auto-drawn sketch + contradiction detection + fault split with law citation; the officer approves. Template-based (8 scenarios), not physics.
- Revenue: insurers pay per processed case → later a per-policy levy (Najm's own path; SAR 750M in 2021); plus repair/towing network commissions, analytics, regional licensing (Palestinian CMA studied E-Kroka in May 2026). Jordan alone ≈ JD 2–4M/yr.
- Training: hackathon = YOLOv8-seg fine-tuned on CarDD (4k imgs) / VehiDE (13.9k) / HITL CC0 (1.8k), report test mAP; production = JIF E-Kroka archive since 2013 (photos + sketches + fault + settlements) under data-sharing. Fault % = law retrieval + LLM (TrafficRAG-style), not trained on photos.
- Roadmap planner: helps Jordan through jobs (7,000 ICT grads/yr, ~3,000 employed; $200M YTJ project), but that's the **economy** sector → 3.65 as society, 4.15 if a mentor approves the crossover.

## Next actions
1. Team decides: H (with reconstruction) vs others.
2. If H: mentor check on sector fit; Day-1 parallel tracks: (a) YOLOv8-seg training, (b) two-phone flow + Supabase, (c) reconstruction templates + OSM, (d) LLM statements/contradictions/fault RAG + test scenarios.

## Business model for H
See [docs/ideas/H2-najm-ai-and-business-model.md](docs/ideas/H2-najm-ai-and-business-model.md). In short: fault % is the hook for drivers. Damage estimation and fraud scoring are what insurers pay for, because motor claims are ≈96% of motor premiums (JD 261M of JD 272M in 2024). Phases: insurer per-claim pilot → PSD×JIF remote-kroka pilot → per-policy levy (Najm switched from per-accident to per-policy because per-accident fees reward more accidents).

## Key insight from round 2
Jordan **already has an electronic kroka (E-Kroka, JIF + PSD, since 2013)**, but an **officer still has to attend every minor accident in person**. Our gap is that "last physical step". The pitch is *not* "digitise the kroka"; it's "remote, AI-pre-assessed, officer-approved kroka for minor accidents", as done by Najm (KSA), Dubai Police and China's 12123.

## Open questions
- Is a PSD/JIF remote-kroka pilot already planned? (Search found none.)
- Current Jordanian fault-share rules: verify against compulsory insurance regulation No. 12/2010 and amendments.
- Car-damage dataset licence (CarDD) vs Roboflow CC-BY sets.
- Web vs mobile; which LLM/vision API keys the team has.

## Key facts to remember (sources in docs/sources.md)
- Jordan 2025: 187,213 accidents, 11,680 with injuries, so ≈175.5k non-injury (our subtraction). 91% inside cities.
- Motor insurance: JD 370M+ cumulative MTPL losses since 2001, 4 insurers liquidated, CBJ refused a price rise (Feb 2025), MEICO exits motor in Jan 2026. PSD warned of staged accidents (Aug 2024).
- Najm (KSA): insurer-owned (26 insurers), 10–14k accidents/day, 45 → ≤10 min target, remote "بلغ-صوّر-جنّب" service.
- Shanghai video quick-handling: avg 6 min/case. Dubai: app reporting without a patrol; AI fault determination in testing since GITEX 2023.
- Round-1 facts (admissions, electricity, floods, pedestrians) are still in docs/ideas/A–F.
