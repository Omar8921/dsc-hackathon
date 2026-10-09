# Idea B — AI Pedestrian-Risk Rating for School Routes ("Safe Route / طريق آمن")

**One-liner:** Feed street-level photos of the roads around a school (from Mapillary, Street View, or photos we take on the day) to a vision model. It scores pedestrian safety features iRAP-style (sidewalk, crossing, speed environment, lighting, barriers) and produces a **risk map and a prioritised fix list** for the municipality and the school.

Sector fit: Safety + urban planning & infrastructure + smart cities. The user is "the office that has to answer" (GAM / Ministry of Education / Public Security Directorate).

## The problem in Jordan
- **Pedestrians were 42.4% of all road deaths in 2024: 230 of 543 deaths**, 18,275 injuries. ([PSD via HPC/Roya](https://en.royanews.tv/news/59520/Jordan-sees-drop-in-road-fatalities))
- 2025: **187,000 accidents, 510 deaths.** ([Jordan News](https://www.jordannews.jo/Section-109/News/187-000-Traffic-Accidents-in-Jordan-in-2025-Result-in-510-Deaths-50151))
- 3,511 road deaths over 6 years. ([Jordan News](https://www.jordannews.jo/Section-109/News/Jordan-loses-3-511-lives-in-road-accidents-over-six-year-period-29630))
- PSD blames jaywalking and drivers not yielding. The infrastructure side (missing crossings and sidewalks) has no systematic audit we could find.

## Who is left out today
Children walking to public schools in dense east-Amman / Zarqa / Irbid neighbourhoods. Their routes have never been assessed because manual road audits are expensive and only cover highways.

## Proof it works elsewhere
- **iRAP's AiRAP** detects up to ~20 road attributes from street imagery to produce safety star ratings without field surveys. Main Roads Western Australia rated **~19,000 km** this way. ([iRAP](https://irap.org/?p=5931), [Anditi](https://anditi.com/case-study/mrwa))
- **Google.org gave iRAP USD 2M** to use AI plus Street View to star-rate roads around **schools in Vietnam**, nationwide. ([FIA Foundation](https://www.fiafoundation.org/news/star-rating-for-schools-boosted-by-us-2m-google-support), [Road Safety Awards](https://www.roadsafetyawards.com/irapreceivesgooglesupporttodeployartificialintelligence))
- Vietnam's school-route version is exactly what we would build for Jordan.

## What we'd build (11-hour MVP)
1. Pick 2–3 real schools in Amman. Collect images: Mapillary API (open), or walk a route on Day 1 and geotag photos (allowed: "data you collect on the day").
2. Vision-LLM (Claude / GPT-4o) with a structured iRAP-inspired rubric → JSON attributes per image → segment score.
3. Map (Leaflet) of segments coloured by risk, with a prioritised list: "Add a zebra crossing at X: covers the 400 m route most students take".
4. Arabic report generator for the municipality and the parent council.
5. Validation slide: compare model attributes against human labels on ~50 images (our own mini-benchmark). That covers "honesty about what is mocked".

## Where the AI adds real value
Converts unstructured imagery into a structured engineering audit at near-zero marginal cost. That job currently needs trained auditors on site.

## Scorecard (1–5)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 3 | 4 |

## Risks / open questions
- **Imagery coverage** of Amman side streets on Mapillary/Street View is uncertain. Fallback: on-site photos (HTU is in Amman, so we can shoot nearby streets).
- Linking to real accident locations: PSD publishes aggregates, not geo-points. We can't claim hotspot prediction.
- The end user is a government office, so a real pilot depends on GAM buy-in. That's a valid "next step", but slower.
- Less consumer-facing UX, which matters less here since UX is only 10%.

## Business / scale path
B2G: GAM, Ministry of Education (≈ 4,000 public schools), Ministry of Public Works. Donor angle: iRAP/FIA Foundation, UNICEF (child road safety). Cost per school audit is a few cents of API calls instead of auditor days.

## 7-minute demo sketch
Show a photo of a real street near HTU → the model fills the rubric live → map of a school's catchment turns red/amber/green → a one-page Arabic action report for the municipality.
