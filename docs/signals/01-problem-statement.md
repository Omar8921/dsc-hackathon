# 01. Problem statement

**Draft v1, Oct 10 2026, 00:40.** Every number below carries a source. Secondary sources
(an op-ed quoting an estimate) are marked as such; prefer the primary ones on slides.

## The statement

Amman's traffic signals give green by a pre-set timetable, not by who is actually waiting.
On lopsided junctions (a loaded main road crossing a quiet side street) the timetable gives
green to empty approaches while the loaded approach queues, so the delay is recoverable without
building anything. The Traffic Department already operates more than 2,500 traffic cameras. What is
missing is the software that turns what a camera sees into the green split, and an Arabic screen
that lets a traffic operator supervise it. We build that software and prove it on an Amman junction
model.

## The facts

| # | Fact | Why it matters | Source |
|---|---|---|---|
| 1 | Transport inefficiency costs Jordan about **US$3 billion a year, at least 6% of GDP** (World Bank, 2022) | The problem is national-economic, not a nuisance | World Bank, Jordan Public Transport Diagnostic |
| 2 | Delay and fuel losses from congestion in **Amman alone are put at about JD 1.5 billion a year** (GAM-linked estimate, as cited by Prof. Mohammad Al-Farajat, Sep 2026) | Amman carries most of the national cost | Ammon op-ed (secondary; quote as "reported") |
| 3 | Amman holds **about 2 million vehicles**, **about 500,000 more enter daily**, and the Traffic Department counts **about 11.5 million vehicle movements per day** (Brig. Raed Al-Assaf, Director of the Traffic Department, Sep 10 2026) | Sizes the exposure: every movement crosses signals | Al-Mamlaka, Al-Rai |
| 4 | The Traffic Department runs **more than 2,500 cameras** monitoring traffic, plus drones (same statement) | The sensing exists; no new hardware per junction | Al-Mamlaka, Al-Rai |
| 5 | In **Aug 2026** the Traffic Department and GAM piloted **smart adaptive signals at 4 Amman sites**, described as moving from **"fixed control"** to control that responds to flow, linked to the control room and cameras | The approach is validated by the authority; the pilot's reach is 4 sites | Ammon, Al-Rai, Al-Mamlaka (Aug 2026) |
| 6 | GAM's traffic operations director attributes the crisis to population growth, more vehicles and the concentration of activity in the capital (Aug 4 2026) | The institution owns the problem and talks about it publicly | Al-Rai |
| 7 | **Adaptive signal control improves travel time by more than 10% on average; where timing is outdated, 50% or more** (US FHWA) | Proof the mechanism works at scale elsewhere | FHWA EDC-1 ASCT |
| 8 | **Poor signal timing accounts for about 10% of all traffic delay** on major roads (Oak Ridge National Laboratory, cited by FHWA) | Signal timing is a known, large, cheap lever | FHWA report 11044 |
| 9 | Self-reported average one-way commute in Amman: **about 40 minutes for about 17 km; 73% of trips by car** (Numbeo, 97 contributors, updated Sep 28 2026) | The person-level cost in a unit they feel; weak source, label it | Numbeo (survey data, caveat on slide) |
| 10 | Jordan had **1.7 million registered vehicles and 2.8 million driving licences** in 2021 | Baseline for growth; most of it in Amman | Hala Akhbar, 2021 |

## Who is affected, and who the current service does not reach

- **Direct beneficiaries:** people crossing Amman's signalised junctions at peak: commuters,
  school and university trips (HTU students included), bus riders, delivery drivers. Fact 3 puts
  the daily exposure at about 11.5 million vehicle movements.
- **Who the current smart-signal service reaches:** 4 pilot junctions (fact 5).
- **Who it does not reach yet:** everyone at every other signalised junction, still served by
  pre-set timing. Our software is the piece that lets the 4-site approach scale to the cameras the
  city already has (fact 4), at the cost of software, not hardware.
- **Secondary beneficiaries (roadmap, not MVP):** buses on the Amman BRT corridors and emergency
  vehicles, which the same controller can prioritise.

## What it costs a person (illustrative arithmetic, not a measured result)

If a commuter crosses 6 signalised junctions each way and adaptive control saves 20 seconds per
junction, that is 2 minutes each way, 4 minutes a day, about 16 hours a year over 240 working
days, plus the fuel burned idling. Say this as arithmetic on a slide; the measured number comes
from the simulation below.

## Why now

The authority has committed to adaptive signals (fact 5) and already owns the cameras and a
central operations room (fact 4). The vendor and algorithm behind the pilot are not public, so we
do not claim to beat it. We offer an open, explainable adaptive controller with a measured
simulation result and an Arabic operator screen, which is the part that makes the pilot scale.

## What we claim, and what we do not

- We claim: on a 4-way Amman-style junction model with a loaded main road and a quiet cross
  street, our adaptive controller cuts average waiting time by **X%** versus a **properly tuned
  fixed plan** (Webster-optimal cycle for the same demand), measured in SUMO microsimulation.
  X is whatever SUMO gives; it is not known yet and we will not quote any other number.
- We claim: vehicle counts come from computer vision on real footage of a junction.
- We do not claim: field results, a live camera integration, or knowledge of the pilot's internals.
- We never show the standalone model's figure (about 48% against a deliberately weak baseline).

## Sources

- ⚠️ External link -- [Jordan Public Transport Diagnostic and Recommendations (World Bank, 2022)](https://www.worldbank.org/en/country/jordan/publication/jordan-public-transport-diagnostic-and-recommendations) -- accessed 2026-10-10
- ⚠️ External link -- [عمّان تختنق مروريا .. والحل ليس شارعاً جديداً بل نظاماً جديداً للحركة (Ammon op-ed, Prof. Mohammad Al-Farajat, 9 Sep 2026; secondary source for the JD 1.5 billion figure)](https://www.ammonnews.net/article/1027597) -- accessed 2026-10-10
- ⚠️ External link -- [إدارة السير: أكثر من 2500 كاميرا لمراقبة الحركة المرورية (Al-Mamlaka TV, 10 Sep 2026)](https://www.almamlakatv.com/news/209556-%D9%85%D9%86%D9%87%D8%A7-%D8%A7%D9%84%D8%AF%D8%B1%D9%88%D9%86%D8%B2-%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B3%D9%8A%D8%B1-%D8%A3%D9%83%D8%AB%D8%B1-%D9%85%D9%86-2500-%D9%83%D8%A7%D9%85%D9%8A%D8%B1%D8%A7-%D9%84%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%AD%D8%B1%D9%83%D8%A9-%D8%A7%D9%84%D9%85%D8%B1%D9%88%D8%B1%D9%8A%D8%A9) -- accessed 2026-10-10
- ⚠️ External link -- [العساف: 11.5 مليون حركة مركبات يومياً في عمّان (Al-Rai, Sep 2026)](https://alrai.com/article/10975799/) -- accessed 2026-10-10
- ⚠️ External link -- [أمانة عمان: الأزمة المرورية نتيجة للنمو السكاني وارتفاع أعداد المركبات (Al-Rai, 4 Aug 2026)](https://alrai.com/article/10970020/) -- accessed 2026-10-10
- ⚠️ External link -- [إشارات ذكية في 4 مواقع بعمان (Ammon News, Aug 2026)](https://www.ammonnews.net/article/1024084) -- accessed 2026-10-09
- ⚠️ External link -- [4 إشارات ذكية تعيد ضبط طرق عمّان (Al-Rai, Aug 2026)](https://alrai.com/article/10973433) -- accessed 2026-10-09
- ⚠️ External link -- [EDC-1: Adaptive Signal Control Technology (US FHWA)](https://www.fhwa.dot.gov/innovation/everydaycounts/edc-1/asct.cfm) -- accessed 2026-10-10
- ⚠️ External link -- [Examining the Effect of Traffic Probe Data on Traffic Signal Operations, FHWA-HRT-11-044 (ORNL figure on poor signal timing)](https://www.fhwa.dot.gov/publications/research/ear/11044/11044.pdf) -- accessed 2026-10-10
- ⚠️ External link -- [Traffic in Amman (Numbeo, user-reported, 97 contributors, updated 28 Sep 2026)](https://www.numbeo.com/traffic/in/Amman) -- accessed 2026-10-10
- ⚠️ External link -- [1.7 مليون مركبة و2.8 مليون رخصة قيادة في الأردن (Hala Akhbar, 2021)](https://www.hala.jo/2021/09/%D9%8A%D9%88%D9%85-%D8%A8%D9%84%D8%A7-%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%85-%D9%8A%D8%AF%D9%8A%D8%B1-%D8%B8%D9%87%D8%B1%D9%87-%D9%84%D9%84%D9%88%D9%82%D9%88%D8%AF/) -- accessed 2026-10-10
- [Jordan smart-traffic plans research brief (carries the Aug 2026 pilot and Jenoptik sources)](/Users/sadasak/.kiro/crew/workspace/jordan-smart-traffic-plans-research.md) -- accessed 2026-10-10
