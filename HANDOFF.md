# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section; don't let it grow forever).

_Last updated: 2026-10-09 (Day 1), ideation session 2._

## Status
- Phase: **ideation**, no code. Branch `ideation/research`.
- History: R1 (A–F) rejected → R2 Najm (H) set aside → R3 learning studio (L) → R4 top 5 ([06](docs/06-top-5.md)) → R5 big problems ([07](docs/07-jordan-big-problems.md)) → **R6: solutions for smoking, reading, traffic → [docs/08-solutions-smoking-reading-traffic.md](docs/08-solutions-smoking-reading-traffic.md).**
- R6 scores: C2 Najm (traffic angle) 4.50 · **B1 Ismaa'ni 4.40** (teacher's phone records each child reading for 60 s → AI words correct/min + error tags → class grouped by level, TaRL method) · **A1 Bala Dukhan 4.15** (WhatsApp AI quit coach + 31 MoH clinics) · A2 3.85 · C1 AI signals 3.85 · B2 3.70 · C3 3.30.
- Key findings: MoH quit clinics reach ~10k smokers/yr (<1% of ~2M+); RAMP: only 19% of early-grade pupils met the oral fluency benchmark (2018); GAM already has 5,600 counting cameras plus smart-signal pilots; Google Read Along Arabic already exists.

## Next actions
1. Team picks from 08 (recommendation for a new direction: B1; second: A1).
2. If B1: test Arabic ASR on read-aloud with forced alignment early (biggest technical risk); write 5 leveled passages.
3. Then the build plan.

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
