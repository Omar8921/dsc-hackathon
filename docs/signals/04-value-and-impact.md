# 04. Value and impact

**Draft v1, Oct 10 2026.** Decisions behind this page:
- **Three scenarios: 10% / 20% / 30% less delay at the light.** The main slide uses **10%**. When SUMO gives our own number, it replaces these.
- **Headline units: hours given back, and fuel and CO₂.** No JD figure on the main slide.
- **Scale in three steps:** 7th Circle cluster → Amman (GAM's 200+ intersections) → Jordan (a projection).

Everything below is **arithmetic on stated assumptions**, not a measured result. Each assumption is listed so a judge can challenge it, and so we can swap in real numbers.

## The value in one line
Every green second given to an empty road is a second taken from a full one. We move those seconds to where the cars actually are, using cameras the city already owns.

## Assumptions

| # | Assumption | Value | Basis |
|---|---|---|---|
| A1 | Average signal delay per vehicle at a busy Amman junction, across the day | **40 s** | Between LOS D (35–55 s) and the middle of the HCM scale. Busy peaks are LOS E (55–80 s) or worse. **Assumption**: replace with the SUMO baseline / camera measurement |
| A2 | Vehicles crossing one busy junction per day | **40,000** | **Assumption** for a major urban junction. Sanity check: 200 junctions × 40,000 = 8M crossings/day, against the Traffic Department's **11.5M vehicle movements a day** in Amman |
| A3 | Effective days a year | **300** | Weekends and holidays are lighter |
| A4 | Fuel burned while waiting | **0.76 L per hour** | Argonne: a passenger car idles at **0.2–0.5 gal/h**. We take the **low end** (0.2 gal/h) |
| A5 | CO₂ per litre of petrol | **2.35 kg** | US EPA: 8,887 g CO₂ per gallon |
| A6 | Junctions at each step | Cluster **6**, Amman **200**, Jordan **300** | Cluster = 7th Circle + 5 neighbours. Amman = GAM's **200+ intersections**. Jordan = Amman + **~100 in Zarqa, Irbid and Aqaba** (**assumption**: no published count found; verify) |
| A7 | Delay reduction | **10% / 20% / 30%** | FHWA: adaptive signal control improves travel time by **more than 10% on average**, and **50%+ where timing is outdated**. 10% is the floor of that range, not a claim |

One junction's yearly delay: 40,000 vehicles × 40 s × 300 days ≈ **133,000 vehicle-hours a year**.

## Hours given back (vehicle-hours a year, at least one person per car)

| Scale | 10% (main slide) | 20% | 30% |
|---|---|---|---|
| **7th Circle cluster** (6) | 80,000 | 160,000 | 240,000 |
| **Amman** (200) | **2.7 million** | 5.3 million | 8.0 million |
| **Jordan** (300, projection) | 4.0 million | 8.0 million | 12.0 million |

We count vehicles, not passengers, so the real hours given back to people are **higher**. A bus or a car of three gets back three times as much. We don't publish an occupancy figure because we have no Jordan source for it.

## Fuel and CO₂ saved per year

Saved waiting time × 0.76 L/h × 2.35 kg CO₂/L.

| Scale | 10% | 20% | 30% |
|---|---|---|---|
| **Cluster**: fuel | 61,000 L | 122,000 L | 182,000 L |
| **Cluster**: CO₂ | 143 t | 286 t | 429 t |
| **Amman**: fuel | **2.0 million L** | 4.1 million L | 6.1 million L |
| **Amman**: CO₂ | **~4,800 t** | ~9,500 t | ~14,300 t |
| **Jordan**: fuel | 3.0 million L | 6.1 million L | 9.1 million L |
| **Jordan**: CO₂ | ~7,100 t | ~14,300 t | ~21,400 t |

This is conservative. It counts only idling fuel at the low Argonne rate, and ignores the extra fuel burned by stopping and starting, and by larger vehicles.

## What it means for one person (Rawan, the student commuter)
Peak delay is higher than the daily average, so for a peak-hour commuter we use **60 s per junction** (the LOS D/E boundary), **6 junctions each way** and **240 working days**:

| | 10% | 20% | 30% |
|---|---|---|---|
| Per day | 1.2 min | 2.4 min | 3.6 min |
| Per year | **~5 hours** | ~10 hours | ~14 hours |

> ⚠️ [01](01-problem-statement.md) says "about 16 hours a year", assuming 20 s saved per junction. That is about 33% of a 60 s peak delay, slightly above our high scenario. Change 01 to the range above so the slides stay consistent.

## Main slide (draft numbers, 10% scenario)
- **2.7 million hours a year** back to Amman's drivers
- **2 million litres of fuel** and **~4,800 tonnes of CO₂** a year
- **Zero new cameras.** The scale comes from software on GAM's existing 5,600

## Beyond the numbers
- **School mornings:** a fixed timetable can't follow the short, sharp school-run peak. A camera-driven controller adjusts to it every cycle.
- **Fewer officers directing traffic by hand** at junctions the timetable can't cope with. Not quantified.
- **A platform for later:** ambulance and civil-defence priority and BRT bus priority use the same controller (roadmap).
- **Built and run in Jordan:** a local team that can export to other cities in the region (scale step 4, not on the main slide).

## To replace when we have it
1. **A1** → the delay measured in our SUMO baseline (properly tuned fixed plan).
2. **A7** → our SUMO result X%, replacing the three scenarios.
3. **A2** → a real camera count at the 7th Circle if we can film it.
4. **A6** → the number of signalised junctions in Zarqa, Irbid and Aqaba, if a mentor knows it.

## Sources
- [HCM level-of-service criteria for signalised intersections (table in Sensors 2024, 24:6410)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11479351/table/sensors-24-06410-t001), accessed 2026-10-10
- [Argonne National Laboratory, idling fuel use, DEER 2012 (energy.gov)](https://www.energy.gov/sites/prod/files/2014/03/f8/p-09_gaines.pdf), accessed 2026-10-10
- [US EPA, Greenhouse gas emissions from a typical passenger vehicle (8,887 g CO₂ per gallon of gasoline)](https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle), accessed 2026-10-10
- [GAM: 5,600 cameras, 200+ intersections (Jordan News, Apr 2026)](https://www.jordannews.jo/Section-109/News/GAM-5-600-Traffic-Monitoring-Cameras-in-Operation-Only-25-Dedicated-to-Traffic-Violations-50992), accessed 2026-10-10
- [العساف: 11.5 مليون حركة مركبات يومياً في عمّان (Al-Mamlaka, Sep 2026)](https://www.almamlakatv.com/news/209556-), accessed 2026-10-10
- FHWA adaptive signal control figures: see [01](01-problem-statement.md)
