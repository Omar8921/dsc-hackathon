# Idea A — Unified-Admission Choice Planner ("Raghbati / رغباتي")

**One-liner:** A Tawjihi student enters their score, field and constraints, and gets a **ranked list of university choices with admission probabilities**, plus an Arabic explanation of the risk in their list ("you put 8 reach choices and no safe one"). Labour-market warnings come from the official "stagnant majors" list.

Sector fit: Education & learning + public services (the Unified Admission Coordination Unit is a public service).

## The problem in Jordan
- **~74,000 students** apply to public universities through Unified Admission every year (74,521 in 2025-26). **46,566 were offered a place and 27,955 (37.5%) were not.** ([MoHE](https://www.mohe.gov.jo/EN/NewsDetails/Ministry_of_Higher_Education_and_Scientific_Research_Unified_Admission_Coordination_Unit))
- The state runs a whole **"misplaced choice" (خطأ في الاختيار) round** each year for students who ranked their choices wrong, limited to **only 3 options**. That round exists because mis-ranking is common enough to need it. ([Jordan News](https://www.jordannews.jo/Section-109/News/Online-Application-Opens-for-Misplaced-Choice-Students-and-Those-Wishing-to-Transfer-Between-Majors-or-Universities-45102))
- **2026 is the first cohort under the new "fields & tracks" Tawjihi system.** Health-field students compete across 151+ specialisations and engineering-field students across 177+ in 10 public universities. Experts publicly warned the system doesn't address matching students to specialisations. ([Jordan News, Sept 2026](https://www.jordannews.jo/Section-109/News/74-000-students-navigate-Jordan-s-new-university-admissions-55056))
- The Civil Service Bureau classifies **39 majors as "stagnant"**: more than 500 applicants waiting and at most 1% hired over 10 years. About **400,000 graduates are unemployed**. Students pick these majors without knowing. ([Jordan News](https://www.jordannews.jo/Section-109/News/39-stagnant-majors-will-no-longer-be-accepted-by-Civil-Service-Bureau-20155), [Jordan Times](https://jordantimes.com/node/333913))
- 118,635 students passed Tawjihi in 2025. ([AACRAO/MoE](https://aacrao.org/edge/emergent-news/tawjihi-pass-rate-stands-at-63.1-in-jordan))

## Who is left out today
Students in governorates and first-generation university families with no counsellor and no older sibling who "knows the system". Today they rely on WhatsApp groups and last year's cut-off lists in news articles, with no idea how likely they are to get in.

## Proof it works elsewhere: China's gaokao "zhiyuan" tools
- **Alibaba's Quark Gaokao** generates application lists with admission probabilities from score + historical data. It passed **100 million uses of its AI features** in one gaokao season and is free. ([arXiv 2411.10280](https://arxiv.org/html/2411.10280v2), [TechNode](https://technode.com/2025/06/13/tencent-launches-ai-tool-for-college-application-advice-post-gaokao/))
- Tencent and QQ Browser launched competing tools. A paid human "application planner" industry existed before, so the AI made an expensive service free.
- The China case is the same problem as Jordan's: a single national exam, a ranked choice list, and published historical cut-offs.

## What we'd build (11-hour MVP)
1. **Data:** scrape/collect the published minimum admission averages (معدلات القبول) per major × university for the last 2–4 years, for **one field only** (e.g. engineering or health). Add the stagnant-majors list.
2. **Model:** per choice, P(admit | score, field) from the historical cut-off distribution (trend + variance across years; simple Bayesian/quantile model). Honest calibration plot on held-out year.
3. **Planner:** optimise the order of the list (reach / target / safe), flag "wasted" choices (impossible or dominated), flag stagnant majors.
4. **AI explainer (LLM):** Jordanian-Arabic explanation of the list, answers "what if I drop Hashemite civil eng?", warns about the new fields system.
5. **UI:** Arabic-first mobile web (RTL), shareable result card (students share in WhatsApp groups, which is also the distribution channel).

## Where the AI adds real value
Probability modelling from noisy multi-year cut-offs, combinatorial list optimisation, and a conversational explainer in dialect. A static website of last year's cut-offs can't do any of these.

## Scorecard (1–5)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% |
|---|---|---|---|---|---|
| 5 | 4 | 4 | 4 | 4 | 5 |

## Risks / open questions
- **Data collection time:** cut-off lists are published as news tables/PDFs. Needs one person for ~2–3 h. Mitigation: restrict to one field and the last 3 years.
- **New fields system (2026)** makes history only partly comparable. Be honest in the pitch: show uncertainty bands and call it "risk guidance".
- Cut-offs depend on seat counts and applicant pools we don't see. The model gives guidance, not a guarantee.
- Timing: the next cycle is summer 2027, so the "next step" pitch writes itself (pilot with schools/MoHE before the 2027 cycle).

## Business / scale path
Free for students. B2G: offer it to the Unified Admission Coordination Unit as a "pre-submission check" (they already redesigned their software to reduce errors). B2B: schools and private tutoring centres. Running cost is tiny: one LLM call per session plus static data.

## 7-minute demo sketch
Persona: Lana from Ma'an, 91.4 in the engineering field. Her actual list → the app flags 6 near-impossible picks and 0 safe ones → reorders it → probability of getting *some* engineering seat goes from ~40% to ~90% → the LLM explains it in Jordanian Arabic → she shares the result card.
