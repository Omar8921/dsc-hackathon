# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section; don't let it grow forever).

_Last updated: 2026-10-09 (Day 1), ideation session 2._

## Status
- Phase: **ideation**, no code. Branch `ideation/research`.
- History: round 1 (A–F) rejected → round 2 Najm (H) set aside for lack of wow → round 3 learning studio (L) → **round 4: top 5 in [docs/06-top-5.md](docs/06-top-5.md).**
- **Top 5:** 1 Farz ED triage copilot (M, 4.50; adapted from "Guardian", the Hamburg 2026 winner) · 2 Adaptive Learning Studio incl. GitHub roadmap builder (L, 4.25) · 3 Nabd CPR coach (I, 4.25) · 4 Katib Arabic clinic scribe (N, 4.20) · 5 Mish Mazbout scam checker (K, 4.10).
- Recommendation: **M (Farz)**. Its Jordan twist is a family-facing wait-transparency screen, because 61% of patients don't know triage exists and most violence against doctors happens in EDs. Safety rule: the LLM extracts, rules score, and the AI may only escalate.

## Next actions
1. Team votes on the top 5.
2. If M: ask a doctor/mentor which triage scale Jordanian EDs use (CTAS/ESI/local); collect ~40 triage vignettes for validation.
3. Then write the build plan (roles, scope, what's mocked, demo script).

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
