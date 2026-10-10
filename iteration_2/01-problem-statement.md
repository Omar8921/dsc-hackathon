# 01. Problem statement

**Draft v2, Oct 10 2026 (iteration 2).** Aligned with what is built on `feat/traffic-ai` (see [00](00-what-is-built.md)).
Every number below carries a source. Secondary sources (an op-ed quoting an estimate) are marked as such; prefer the primary ones on slides.
Changes from v1: the existing pilot is no longer mentioned (team decision); the claims section now uses measured results; the per-person figure uses the range from [04](04-value-and-impact.md); the local-file source was removed.

## The statement

Amman's traffic signals give green by a pre-set timetable, not by who is actually waiting.
On lopsided junctions (a loaded main road crossing a quiet side street) the timetable gives
green to empty approaches while the loaded approach queues, so the delay is recoverable without
building anything. GAM already runs about 5,600 cameras, most of them for counting traffic. What is
missing is the software that turns what a camera sees into the green split, safely, and an Arabic
screen that lets a traffic operator supervise it. We built that controller and its safety layer, and
tested it in a simulated 3-junction corridor.

## The facts

| # | Fact | Why it matters | Source |
|---|---|---|---|
| 1 | Transport inefficiency costs Jordan about **US$3 billion a year, at least 6% of GDP** (World Bank, 2022) | The problem is national-economic, not a nuisance | World Bank, Jordan Public Transport Diagnostic |
| 2 | Delay and fuel losses from congestion in **Amman alone are put at about JD 1.5 billion a year** (GAM-linked estimate, as cited by Prof. Mohammad Al-Farajat, Sep 2026) | Amman carries most of the national cost | Ammon op-ed (secondary; quote as "reported") |
| 3 | Amman holds **about 2 million vehicles**, **about 500,000 more enter daily**, and the Traffic Department counts **about 11.5 million vehicle movements per day** (Brig. Raed Al-Assaf, Director of the Traffic Department, Sep 10 2026) | Sizes the exposure: every movement crosses signals | Al-Mamlaka, Al-Rai |
| 4 | The Traffic Department runs **more than 2,500 cameras** monitoring traffic, plus drones (same statement) | The sensing exists; no new hardware per junction | Al-Mamlaka, Al-Rai |
| 5 | GAM runs **about 5,600 cameras**, mostly for **traffic counting and flow analysis** (only 25% for violations), and a **central control centre for 200+ intersections** (Apr 2026) | The sensing and the central link exist; the missing piece is software | Jordan News / Al-Mamlaka |
| 6 | GAM's traffic operations director attributes the crisis to population growth, more vehicles and the concentration of activity in the capital (Aug 4 2026) | The institution owns the problem and talks about it publicly | Al-Rai |
| 7 | **Adaptive signal control improves travel time by more than 10% on average; where timing is outdated, 50% or more** (US FHWA) | Proof the mechanism works at scale elsewhere | FHWA EDC-1 ASCT |
| 8 | **Poor signal timing accounts for about 10% of all traffic delay** on major roads (Oak Ridge National Laboratory, cited by FHWA) | Signal timing is a known, large, cheap lever | FHWA report 11044 |
| 9 | Self-reported average one-way commute in Amman: **about 40 minutes for about 17 km; 73% of trips by car** (Numbeo, 97 contributors, updated Sep 28 2026) | The person-level cost in a unit they feel; weak source, label it | Numbeo (survey data, caveat on slide) |
| 10 | Jordan had **1.7 million registered vehicles and 2.8 million driving licences** in 2021 | Baseline for growth; most of it in Amman | Hala Akhbar, 2021 |

## Who is affected, and who the current service does not reach

- **Direct beneficiaries:** people crossing Amman's signalised junctions at peak: commuters,
  school and university trips (HTU students included), bus riders, delivery drivers. Fact 3 puts
  the daily exposure at about 11.5 million vehicle movements.
- **Who is left out today:** everyone at a signalised junction that runs on a pre-set timetable.
  The timetable can't see that the main road is full and the side street is empty. Our software
  uses the cameras the city already has (facts 4–5), so reaching them costs software, not hardware.
  Drivers don't install anything.
- **Secondary beneficiaries (roadmap, not MVP):** buses on the Amman BRT corridors and emergency
  vehicles, which the same controller can prioritise.

## What it costs a person (illustrative arithmetic, not a measured result)

If a peak-hour commuter crosses 6 signalised junctions each way (60 s delay each) and the delay
drops by 10–30%, they get back **1.2–3.6 minutes a day, about 5–14 hours a year** over 240 working
days, plus the fuel burned idling. 10% is what our AI measured on the rush-hour scenario (see below).
Say this as arithmetic on a slide; it is not a field measurement.

## Why now

GAM already owns the cameras and a central control centre (facts 4–5), and its traffic leadership
talks publicly about the crisis (fact 6). Cheap CPU-trained AI makes per-junction control affordable:
our policy trained in about 35 minutes on a laptop CPU. We offer an open, explainable controller
with a hard safety layer, measured simulation results and an Arabic operator screen.

## What we claim, and what we do not

- We claim: in a simulated 3-junction corridor (SUMO), under **main-road rush hour** (a loaded main
  road crossing quiet side streets), our AI controller cut mean waiting by **10%** and time lost by
  **23%** versus a **tuned fixed timer** (green time chosen on development scenarios), on traffic it
  never saw in training (3 seeds).
- We also say, unprompted: on **balanced** traffic the AI is **40% worse** than the timer, and a simple
  **sensor-actuated rule beats the AI in every scenario** (47% less waiting than the timer in rush hour).
- We claim: **0 unsafe signal transitions in 27 test runs**; every AI choice is carried out through fixed timing rules.
- We claim: persistent-congestion alerts fire in the incident scenario (~80 s after the blockage).
- Vehicle counts from real footage: **only once the YOLO demo exists**. Today counts come from the simulator.
- We do not claim: field results, a live camera integration, control of a real signal, accident
  detection, or proven coordination between junctions.

## Sources

- ⚠️ External link -- [Jordan Public Transport Diagnostic and Recommendations (World Bank, 2022)](https://www.worldbank.org/en/country/jordan/publication/jordan-public-transport-diagnostic-and-recommendations) -- accessed 2026-10-10
- ⚠️ External link -- [عمّان تختنق مروريا .. والحل ليس شارعاً جديداً بل نظاماً جديداً للحركة (Ammon op-ed, Prof. Mohammad Al-Farajat, 9 Sep 2026; secondary source for the JD 1.5 billion figure)](https://www.ammonnews.net/article/1027597) -- accessed 2026-10-10
- ⚠️ External link -- [إدارة السير: أكثر من 2500 كاميرا لمراقبة الحركة المرورية (Al-Mamlaka TV, 10 Sep 2026)](https://www.almamlakatv.com/news/209556-%D9%85%D9%86%D9%87%D8%A7-%D8%A7%D9%84%D8%AF%D8%B1%D9%88%D9%86%D8%B2-%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B3%D9%8A%D8%B1-%D8%A3%D9%83%D8%AB%D8%B1-%D9%85%D9%86-2500-%D9%83%D8%A7%D9%85%D9%8A%D8%B1%D8%A7-%D9%84%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%AD%D8%B1%D9%83%D8%A9-%D8%A7%D9%84%D9%85%D8%B1%D9%88%D8%B1%D9%8A%D8%A9) -- accessed 2026-10-10
- ⚠️ External link -- [العساف: 11.5 مليون حركة مركبات يومياً في عمّان (Al-Rai, Sep 2026)](https://alrai.com/article/10975799/) -- accessed 2026-10-10
- ⚠️ External link -- [أمانة عمان: الأزمة المرورية نتيجة للنمو السكاني وارتفاع أعداد المركبات (Al-Rai, 4 Aug 2026)](https://alrai.com/article/10970020/) -- accessed 2026-10-10
- [GAM: 5,600 traffic monitoring cameras, only 25% for violations; 200+ intersections (Jordan News, updated 29 Apr 2026)](https://www.jordannews.jo/Section-109/News/GAM-5-600-Traffic-Monitoring-Cameras-in-Operation-Only-25-Dedicated-to-Traffic-Violations-50992) -- accessed 2026-10-10
- ⚠️ External link -- [EDC-1: Adaptive Signal Control Technology (US FHWA)](https://www.fhwa.dot.gov/innovation/everydaycounts/edc-1/asct.cfm) -- accessed 2026-10-10
- ⚠️ External link -- [Examining the Effect of Traffic Probe Data on Traffic Signal Operations, FHWA-HRT-11-044 (ORNL figure on poor signal timing)](https://www.fhwa.dot.gov/publications/research/ear/11044/11044.pdf) -- accessed 2026-10-10
- ⚠️ External link -- [Traffic in Amman (Numbeo, user-reported, 97 contributors, updated 28 Sep 2026)](https://www.numbeo.com/traffic/in/Amman) -- accessed 2026-10-10
- ⚠️ External link -- [1.7 مليون مركبة و2.8 مليون رخصة قيادة في الأردن (Hala Akhbar, 2021)](https://www.hala.jo/2021/09/%D9%8A%D9%88%D9%85-%D8%A8%D9%84%D8%A7-%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%85-%D9%8A%D8%AF%D9%8A%D8%B1-%D8%B8%D9%87%D8%B1%D9%87-%D9%84%D9%84%D9%88%D9%82%D9%88%D8%AF/) -- accessed 2026-10-10
- Measured results: `results/eval_final/summary.md` on branch `feat/traffic-ai` (commit 3a789e8)
