# Idea J — Old-Building Safety Triage from Residents' Photos ("Saqf / سقف")

**One-liner:** Residents of old buildings photograph cracks, spalling and exposed rebar. A vision model grades severity and the app builds a **prioritised inspection list** for the municipality / Engineers Association. Danger signs get a red flag within hours, not after a collapse.

Sector fit: Urban planning & infrastructure + safety.

## Problem in Jordan
- **Jabal Al-Luweibdeh collapse, 13 Sept 2022: 14 dead.** The building was 50 years old (licensed 1956). Renovation work on the ground floor was suspected. GAM's deputy mayor said **examining old buildings "does not fall under GAM's responsibility, even if a complaint is received."** ([New Arab](https://www.newarab.com/news/14-dead-jordan-building-collapse-rescue-efforts-end), [Jordan News](https://www.jordannews.jo/Section-106/Features/Fears-of-more-old-buildings-collapsing-21876))
- After the collapse, the PM called for a **national survey of buildings over 50 years old**. GAM counted **325 old/collapsing buildings** (2018 survey) and **1,000+ deserted buildings**. **~350 at-risk buildings were flagged in Zarqa.** ([Jordan News – Zarqa](https://www.jordannews.jo/Section-109/News/350-buildings-in-Zarqa-at-risk-of-collapsing-21930), [Jordan Times](https://jordantimes.com/news/local/pm-stresses-adherence-building-codes))

## Proof abroad (weaker than other ideas)
- **FEMA ROVER / ATC-20** smartphone rapid assessment (US), but used by professionals. ([ATC](https://atcouncil.org/atc-67-4))
- Italy: a resident-operated damage app was tested in the 2012 Emilia earthquake. Haiti: engineer app (~20 min per building). ([PreventionWeb](https://www.preventionweb.net/go/69792))
- Turkey: deep-learning crack/spalling/rebar detection trained on 2023 earthquake images (research, ~94% lab accuracy, not deployed). ([arXiv 2510.21063](https://arxiv.org/pdf/2510.21063))

## Scorecard
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 4 | 3 | 4 | **3.70** |

## Why it's not ranked higher
- **Crack detection is not a safety verdict.** Domain judges (engineers) will push hard on this.
- No deployed citizen-AI example abroad (only research and professional tools).
- Unclear institutional owner: GAM publicly said this isn't its job.
