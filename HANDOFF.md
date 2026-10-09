# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section; don't let it grow forever).

_Last updated: 2026-10-09 (Day 1), ideation session 2._

## Status
- Phase: **ideation**. No code written (intentional). The team is **still gathering ideas, no rush to commit yet.**
- Branch: `ideation/research` (planning docs). `main` only has `.gitignore` + an empty `README.md`.
- **Round 1 (ideas A–F) was rejected by the team.** The "common ideas to avoid" list was accepted.
- **Round 2:** a teammate's idea **"Najm for Jordan"** was researched and evaluated → [docs/ideas/H-najm-for-jordan.md](docs/ideas/H-najm-for-jordan.md). Score **4.50**, the current lead.
- A global scan of proven-abroad solutions added I (CPR coach, 4.25), K (scam checker, 4.10) and J (old buildings, 3.70). See [docs/04-global-scan.md](docs/04-global-scan.md).

## Key insight from round 2
Jordan **already has an electronic kroka (E-Kroka, JIF + PSD, since 2013)**, but an **officer still has to attend every minor accident in person**. Our gap is that "last physical step". The pitch is *not* "digitise the kroka"; it's "remote, AI-pre-assessed, officer-approved kroka for minor accidents", as done by Najm (KSA), Dubai Police and China's 12123.

## Next actions
1. Team reads H and decides whether it's the one (or keeps exploring; see "not yet explored" in 04-global-scan.md).
2. If H: **mentor check on sector fit** (it touches insurance, so confirm it counts as society/public service).
3. If H: collect "data on the day": ask ~20 people how long they last waited for a kroka and what it cost (no personal data, anonymous).
4. Then write a build plan: roles, scope (2 cars, no injuries, 6–8 scenarios), what's mocked, demo script.

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
