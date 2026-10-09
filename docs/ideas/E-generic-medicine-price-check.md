# Idea E — Cheaper Equivalent Medicine Finder ("Badeel / بديل")

**One-liner:** Photograph a medicine box or prescription. The app identifies the active ingredient, strength and form, then lists **JFDA-registered equivalents with official prices** and the yearly saving. Because Jordanian law requires physician approval for substitution, it also gives a one-line Arabic message the patient can show their doctor to ask for the generic.

Sector fit: Access to healthcare.

## The problem in Jordan
- **83% of patients say medicine costs are high.** Public-sector drugs are often out of stock, which forces patients to buy out-of-pocket at private pharmacies. ([PMC3987061](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3987061/))
- Patients would save **32%–74%** by using generics instead of originators. **78% of patients accept generic substitution.** ([PMC3987061](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3987061/))
- Some originator brands cost far more in Jordan than in the UK, e.g. **misoprostol ~19×, ranitidine >7×**. ([Kingston eprints](https://eprints.kingston.ac.uk/27794/))
- **Legal constraint:** private pharmacists may not dispense a generic without physician approval. Yet **92% of physicians welcome e-prescribing and 80% welcome generic-name (INN) prescribing**. ([PMC4366943](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4366943/))
- JFDA has registered **8,000+ medicines, more than half made locally**. ([Jordan News](https://www.jordannews.jo/Section-109/News/FDA-approved-over-8-000-medicines-more-than-half-locally-made-32430))

## Data
- **JFDA drug price dataset on the Jordan Open Data portal** (Open Jordanian License): [drug-prices-838-2021](https://opendata.gov.jo/en/dataset/metadata/drug-prices-838-2021), last updated July 2025. Also the OTC list 2024 and rational drug list 2024. **Download and inspect columns first thing on Day 1.**

## Who is left out today
Chronic-disease patients paying out-of-pocket: diabetes, hypertension, the uninsured, the elderly. They don't know an equivalent exists because nobody tells them.

## Proof it works elsewhere
- India's **Jan Aushadhi Sugam** app helps people find generic equivalents and stores. It is part of a national generic programme with large reported savings (look up figures if chosen).
- Saudi SFDA publishes a drug list with prices for consumers.

## MVP
Photo → vision-LLM extraction → match against JFDA list (fuzzy match + LLM disambiguation) → equivalents table → yearly-savings card → "ask your doctor" note in Arabic.

## Scorecard (1–5)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% |
|---|---|---|---|---|---|
| 4 | 3 | 4 | 4 | 4 | 4 |

## Risks
- **Regulation:** patients can't substitute at the pharmacy without the physician. The value depends on the doctor conversation.
- Medical-safety framing: equivalence must come strictly from the same active ingredient, dose and form.
- The 2021-vintage price data may be stale.
- "Medicine price app" ideas exist regionally, so novelty is moderate.
