# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section; don't let it grow forever).

_Last updated: 2026-10-10 (Day 2), Faris planning session._

## Status
- **Idea chosen: adaptive traffic signals, brand فارس / Faris** (Oct 10). All work lives in [docs/signals/](docs/signals/): 01 problem, 02 users, 03 feasibility, 04 impact, 05 branding, 06 revenue/costs, 07 pitch deck (HTML, Arabic RTL, ←/PageDown = next, F = fullscreen).
- Decisions for today are in the decision log (2026-10-10 entries). Key ones: GAM buyer, fully automatic within safety limits, 7th Circle cluster first, JD 200/month per junction, **don't mention the existing smart-signal pilot**.
- Still open: feature list, modules, tech stack, user flow, pitch storyline and script.

## Next actions
1. Lock features/modules, then build: SUMO baseline (Webster) vs controller, YOLO counting on recorded footage, Arabic operator console.
2. Put the SUMO X% into deck slide 9 and impact doc 04 (replace scenarios).
3. Fix 01: remove pilot references (fact 5, "who it reaches", "why now"), the local-path source on line 80, and change "16 hours/yr" to the 5–14 h range.
4. Name the 7th Circle neighbouring junctions; verify the FHWA cost page in a browser; fill team names in the deck.
5. Deck loads IBM Plex Sans Arabic from Google Fonts. Check the venue has internet, or bundle the font locally.

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
