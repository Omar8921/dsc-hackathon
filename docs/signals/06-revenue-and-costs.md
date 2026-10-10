# 06. Revenue and costs

**Draft v1, Oct 10 2026.** Decided with the team:
- GAM pays a **setup fee + a yearly licence per junction**.
- The 7th Circle cluster is a **paid pilot at 50%**.
- The price sits **well below imported systems**.
- **6 people** in year 1.

All prices are **our proposal**, not quotes. Costs are estimates; their basis is given in each row. 1 USD = 0.709 JD (fixed peg).

## 1. What imported systems cost (benchmark)
- The US DOT ITS cost database, summarising FHWA, lists the **capital cost per intersection** of established adaptive systems (2010 dollars, **excluding** yearly operation and maintenance): **SCATS $25–30k, SCOOT $30–60k, InSync $25–35k, OPAC $20–50k**. The overall range is **$8k–60k**. ⚠️ The page blocked direct access, so these figures come from the search index. Open the link once in a browser before putting them on a slide.
- Projects cost more when cabinets and communications also need upgrading.
- In JD, the imported capital cost alone is roughly **JD 18,000–43,000 per junction** for SCATS/SCOOT, before maintenance and before 16 years of inflation.

Why we can be cheaper: **no new cameras or detectors** (we use GAM's), software-first, Jordanian salaries, and local support.

## 2. Our price list (proposal)

| Item | Price | What's included |
|---|---|---|
| **Setup per junction** | **JD 3,000** (one time) | Survey, digital-twin calibration, safety limits signed with GAM, integration, go-live |
| **Licence per junction** | **JD 2,400 / year** (JD 200 a month) | Software, hosting, monitoring, updates, Arabic console, monthly results report, support |
| **Edge box** (only where route B is needed) | **JD 1,000** per junction, one time | Industrial AI box, enclosure, installation |
| **Pilot discount** | **50%** for the first 6 junctions, year 1 | |

**5-year cost to GAM for one junction:** 3,000 + 5 × 2,400 = **JD 15,000, all in**. That is **below the capital cost alone** of an imported system (JD 18k–43k).

**Cost per hour given back** (10% scenario, 13,300 vehicle-hours a year per junction, see [04](04-value-and-impact.md)): JD 2,400 ÷ 13,300 ≈ **JD 0.18 per vehicle-hour**.

## 3. Revenue plan

| Year | Junctions live (cumulative) | Setup revenue | Licence revenue | **Total** |
|---|---|---|---|---|
| **1**: 7th Circle pilot | 6 | 6 × 1,500 = 9,000 | 6 × 1,200 = 7,200 | **JD 16,200** |
| **2**: first corridors | 40 | 34 × 3,000 = 102,000 | 40 × 2,400 = 96,000 | **JD 198,000** |
| **3**: Amman roll-out | 120 | 80 × 3,000 = 240,000 | 120 × 2,400 = 288,000 | **JD 528,000** |
| **Steady state, Amman** | 200 | – | 200 × 2,400 | **JD 480,000 / year recurring** |
| **Steady state, Jordan** | 300 | – | 300 × 2,400 | **JD 720,000 / year recurring** |

The year-1 licence assumes the pilot runs a full year. If go-live is month 3, it's 9 months of licence (≈ JD 5,400).

Later revenue (not in the table): edge boxes, other Jordanian municipalities, and licensing to other cities in the region.

## 4. Year-1 costs (6 people)

| Item | Per month | Per year | Basis |
|---|---|---|---|
| 4 founders (AI × 3, software × 1) | 4 × JD 900 | 43,200 | Below the market rate on purpose. Jordan software-engineer pay is about **JD 800–2,000/month** |
| Traffic engineer | JD 1,500 | 18,000 | Senior hire. Sets the safety limits with GAM |
| Field / integration engineer | JD 1,000 | 12,000 | Cabinets, cameras, site visits |
| Employer on-costs (social security etc.) | ~15% | 11,000 | **Assumption**: check the current SSC rate |
| Compute and hosting (pilot) | JD 600 | 7,200 | **Estimate**: one cloud GPU server for ~24 camera streams, plus storage. Zero if GAM hosts |
| Liability insurance | – | 3,000 | **Assumption**: we control public infrastructure, so this is a must |
| Company registration, legal, contracts | – | 2,000 | **Assumption** |
| Co-working / incubator desk | JD 300 | 3,600 | **Assumption** |
| Test equipment (cameras, 1–2 edge boxes) | – | 3,000 | Edge dev kit ≈ $249 (NVIDIA Jetson Orin Nano Super), plus cameras and mounts |
| Contingency | – | 5,000 | |
| **Total year 1** | | **≈ JD 108,000** | |

## 5. The gap and how we fund it
- Year 1: **≈ JD 108k cost vs ≈ JD 16k revenue → about JD 92k to raise.**
- Options: an innovation grant or seed investment (e.g. Jordan's Innovative Startups and SMEs Fund, ISSF), a university incubator, or a climate / smart-city fund for the pilot.
- **Break-even:** with year-3 running costs of about **JD 250k** (team of ~10, estimate), licences alone cover it at **~105 junctions**, about **half of GAM's 200+**. With setup fees included, we break even during year 3.

## 6. What the hackathon build costs
| Item | Cost |
|---|---|
| SUMO simulation, YOLO vehicle detection, Python | Free / open source |
| Supabase (database, auth, hosting) | Free tier |
| LLM API for the Arabic explanations | A few dollars |
| Footage | Filmed on the day, faces and plates blurred |

## 7. Answers ready for judges
- **"Why so cheap?"** We don't sell hardware. GAM already paid for the cameras; we turn them into green time.
- **"What if GAM stops paying?"** The junction falls back to its existing fixed plan, so nothing breaks.
- **"Who else could buy?"** Every Jordanian municipality with signals, then cities in the region with the same fixed-time problem.

## Sources
- [Installation of Adaptive Signal Control Technology systems ranges from $8,000 to $35,000 per intersection (US DOT ITS JPO, with FHWA 2010 per-system costs)](https://www.itskrs.its.dot.gov/2015-sc00355), accessed 2026-10-10
- [Software engineer salary in Jordan, 2025 (Qureos: JD 800–2,000/month)](https://qureos.com/career-guide/top-in-demand-jobs-in-jordan), accessed 2026-10-10
- [NVIDIA Jetson Orin Nano Super Developer Kit, $249 (SparkFun)](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html), accessed 2026-10-10
