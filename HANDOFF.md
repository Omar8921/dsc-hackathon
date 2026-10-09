# HANDOFF

Rolling "where are we" note. Read this first and **update it at the end of every session** (overwrite the Status section; don't let it grow forever).

_Last updated: 2026-10-09 (Day 1), ideation session 2._

## Status
- Phase: **ideation**. No code written (intentional). The team is still exploring.
- Branch: `ideation/research` (planning docs). `main` only has `.gitignore` + an empty `README.md`.
- Round 1 (A–F) rejected. Round 2: Najm-for-Jordan (H, 4.50) plus business model (H2), **now set aside by the team** in favour of more wow factor.
- **Round 3 (current):** a teammate's idea of a personalised learning roadmap from GitHub with interactive modules → [docs/ideas/L-adaptive-learning-studio.md](docs/ideas/L-adaptive-learning-studio.md).
  - The generic "AI roadmap generator" is crowded, and developer-focused learning is the *economy* sector's example, so it was reshaped into **L2: a classroom studio**. A teacher photographs a textbook page → a playable adaptive lesson in Arabic → a live class map plus per-student maps and remedial modules. Same engine as the teammate's idea. Score 4.25.
  - Anti-slop principle: **one learner model (concept graph + mastery + mistake log), one loop (diagnose → generate → practice → update → re-plan).** Every feature is a view on it. The LLM only fills typed module schemas.
- Hackathon-winner patterns: [docs/05-what-wins-hackathons.md](docs/05-what-wins-hackathons.md).

## Next actions
1. Team decides between L2 (classroom), L1 (developer version; needs a mentor OK to cross into economy), H, or I.
2. If L2: pick one subject and grade, and pre-test generation on 5–10 real textbook pages; choose 4 module types.

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
