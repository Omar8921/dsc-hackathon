# 02. Target users

**Draft v1, Oct 10 2026.** Decisions behind this page: we don't mention any existing smart-signal pilot. GAM is the buyer and PSD the partner. The product is B2G only, so citizens benefit but never open an app. The pitch spotlights commuters and school runs.

## The three roles

| Role | Who | What they do with it | What they care about |
|---|---|---|---|
| **Buyer** | **Greater Amman Municipality (GAM)**, Traffic Executive Directorate | Signs the contract, owns the signals and the central control centre | Visible drop in congestion, cost per junction, no new hardware, low risk |
| **Partner** | **PSD Traffic Department (إدارة السير)** | Co-sponsor, enforcement, its own 2,500+ cameras and control room | Fewer bottlenecks to police by hand, safety at junctions |
| **User** | **Control-room operator / traffic engineer at GAM** | Watches junctions, sees what the AI recommends and why, approves or overrides | Trust, explanation, one click back to the fixed plan |
| **Beneficiaries** | Everyone crossing a signalised junction | Nothing. They just wait less at the light | Time, fuel, getting kids to school on time |

## Why GAM is the buyer
- GAM runs a **central control centre that monitors and manages traffic lights** across Amman, covering **200+ intersections**.
- GAM operates **about 5,600 cameras**, and **only 25% of them are for violations**. Most are for **traffic counting and flow analysis**, which is exactly the input we need. (GAM's Executive Director of Traffic, Apr 2026.)
- GAM's traffic lights are already linked to central control and to traffic cameras, so the Traffic Department already works with GAM on signals (Traffic Department director, Aug 2026).

> Note for the slides: GAM's 5,600 cameras and PSD's 2,500+ cameras are **two different fleets with different owners**. Don't merge them into one number. We plug into GAM's counting cameras first.

## Spotlight beneficiaries (pitch)

**1. Daily commuters**
- Amman has about **11.5 million vehicle movements a day**, about **2 million vehicles**, and **about 500,000 more enter daily** (Traffic Department, Sep 2026).
- Illustrative: 6 junctions each way × 20 s saved ≈ **16 hours a year per commuter** (arithmetic, not a measured result; see [01](01-problem-statement.md)).

**2. Students and school runs**
- **About 2.2 million students** started the 2026/27 school year on **23 Aug 2026**. Nationally there are **7,818 schools** and **2,263,438 enrolled students** (2025/26).
- When schools open, the Traffic Department expects **more congestion in the morning and evening, especially in Amman**, and tells drivers to **leave at least 10 minutes earlier**.
- Why it fits us: school runs create a **sudden, short peak** at the same few junctions. A fixed timetable can't follow it, but a camera-driven controller can.
- Honest gap: **no published figure gives the share of Amman's peak traffic that is school runs.** Don't invent one.

## Who is left out today, and do we reach them?
- **Today:** junctions run on a **pre-set timetable**, so everyone in the loaded queue waits while the empty approach gets green.
- **With us:** every junction where a GAM counting camera already points at the approaches. We reach people **without them installing or doing anything**: drivers, bus and service-taxi riders, and school buses all sit in the same queue.
- **Roadmap, not MVP:** ambulance and civil-defence priority, and BRT bus priority.

## Personas (for the UX and the demo)
- **Operator: "Abu Khaled" (أبو خالد)**, a shift engineer at GAM's control centre. He watches dozens of junctions on a wall of screens and fixes jams by phone and gut feel. He'll only trust the AI if it **says why** and **can be overridden in one click**.
- **Commuter: "Rawan" (روان)**, an HTU student driving from Tla' Al-Ali to the campus. She loses time at the same three lights every morning while the side street sits empty on green.

_(The personas are illustrative and not based on real people.)_

## Sources
- [GAM: 5,600 traffic monitoring cameras, only 25% for violations; central control centre, 200+ intersections (Jordan News citing Al-Mamlaka, updated 29 Apr 2026)](https://www.jordannews.jo/Section-109/News/GAM-5-600-Traffic-Monitoring-Cameras-in-Operation-Only-25-Dedicated-to-Traffic-Violations-50992), accessed 2026-10-10
- [مدير إدارة السير: حلول مرورية جديدة في عمّان (Al-Mamlaka, 26 Aug 2026)](https://www.almamlakatv.com/news/208193-), accessed 2026-10-10
- [2.2 مليون طالب وطالبة يتوجهون إلى مدارسهم لبدء العام الدراسي 2026-2027 (Al-Mamlaka, 23 Aug 2026)](https://www.almamlakatv.com/news/207917-), accessed 2026-10-10
- [Comprehensive traffic security plan for the new school year (Jordan News, 21 Aug 2025)](https://www.jordannews.jo/Section-109/News/Comprehensive-Traffic-Security-Plan-for-the-New-School-Year-44249), accessed 2026-10-10
- Traffic Department figures (11.5M movements, 2M vehicles, 2,500+ cameras): see [01](01-problem-statement.md)
