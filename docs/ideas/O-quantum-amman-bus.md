# Idea O — "Quantum Amman Bus Optimization" (team whiteboard, round 8)

Written 2026-10-09. Origin: the team whiteboard ("By using quantum computing to optimise Amman Bus routes we could exponentially increase route quality and coverage") and a teammate's own commute: sometimes **3 buses and 2 hours** to get somewhere. Inspiration: D-Wave's [logistics-routing page](https://www.dwavequantum.com/solutions-and-products/quantum-optimization/logistics-routing/).

**TL;DR:** The problem is real and well-sourced. The quantum part, as written, would hurt us on the rubric. "Exponentially" isn't true, there's no quantum advantage on routing yet, and the bottleneck in Amman is **data and demand, not compute**. A reshaped version (§6) uses quantum as an *optional solver behind an AI demand engine* and scores ~3.8. That's a solid backup, but still below H (4.70).

---

## 1. The problem in Jordan (sourced)
- **Public transport carries only ≈13% of trips in Amman** (vs 58% in Istanbul). ([CODATU](https://www.codatu.org/en/planning-sustainable-mobility-in-the-amman-metropolitan-area-jordan/))
- **47% of women surveyed had turned down a job because of transport** (SADAQA + FES study, ~500 women, 11 governorates, 2019). Reasons: availability, cost, harassment. They spent **JD 57/month** on average on transport. ([Urbanet](https://www.urbanet.info/jordan-public-transport-women-work-force/), [World Bank blog](https://blogs.worldbank.org/en/arabvoices/addressing-womens-safety-concerns-public-transport-jordan-boost-their-economic-activity)). One Jordan Times quote says 40%, so cite it as "40–47%".
- **Over half of Amman transit users commute an hour or more per day.** ([Foreign Policy, 2023](https://foreignpolicy.com/2023/02/16/amman-jordan-public-transportation-brt-bus-women-mobility-labor/))
- **The formal network is small next to the city:** ≈300 buses (175 BRT + 131 Amman Bus). Ridership in Jan–Apr 2025: 7.2M BRT, 3.6M Amman Bus. ([Jordan News](https://www.jordannews.jo/Section-109/News/15-New-Electric-Buses-to-Operate-in-Amman-in-the-Second-Half-of-2025-42123))
- **Why "3 buses" hurts so much: transfers aren't integrated.** Bus↔BRT transfers are free only at six named interchanges ([Jordan News, 2022](https://jordannews.jo/Section-109/News/Transfers-between-Amman-bus-and-BRT-are-free-GAM-24475)). The card system covers only Amman Bus + BRT, not the privately owned buses ([Mastercard, 2023](https://www.mastercard.com/news/eemea/en/newsroom/press-releases/en/2023/february/mastercard-joins-forces-with-greater-amman-municipality-and-network-international-to-launch-jordan-s-first-transit-payment-ecosystem)). Coasters and servees are cash, and every leg costs a new fare.
- **There's no public data on the informal network.** We found **no Amman GTFS feed** (Transitland / Mobility Database searches came up empty). The only full map of coaster/servees routes is the volunteer Ma'an Nasel map from 2015 (76 routes). ([Jordan Times](https://jordantimes.com/news/local/map-outlines-public-transport-routes-amman))
- **Government is actively reshaping routes:** GAM merges BRT routes and adds new Amman Bus routes ([Jordan News](https://www.jordannews.jo/Section-109/News/BRT-routes-merged-frequencies-changed-15730), [13 new routes](https://www.jordannews.jo/Section-109/News/Amman-Bus-to-launch-13-new-bus-routes-in-coming-two-weeks-27406)). **EBRD + MoT discussed restructuring urban routes in Irbid and Zarqa (Sep 2025).** So there's a live buyer for route-planning tools.

**Who's left out:** people outside the BRT corridors, especially women and low-income workers, whose trips need coaster + servees + bus with separate cash fares. A 2023 Amman survey found **~71% would use an integrated BRT + on-demand feeder system**. ([Urban Science 2023](https://doaj.org/article/2c64b7e297dc4511a2b04a25fe72678b))

## 2. Reality check on the quantum part
| Claim on the board | What the evidence says |
|---|---|
| "Quantum computing to optimise routes" | Possible. Routing can be written as a QUBO and run on D-Wave. |
| "**Exponentially** increase route quality" | **Not supported.** Every 2025 VRP study we found runs in simulation or on small instances, and none beats Gurobi/CPLEX. Hierarchical multi-angle QAOA reaches ~95–98% of Gurobi's optimum on decomposed sub-problems. ([arXiv 2511.00506](https://arxiv.org/pdf/2511.00506), [arXiv 2304.09629](https://arxiv.org/pdf/2304.09629)) Pure-QPU results can be far from optimal, while D-Wave's *hybrid* (mostly classical) solver does well. ([arXiv 2412.07460](https://arxiv.org/pdf/2412.07460), [arXiv 2409.05542](https://arxiv.org/html/2409.05542v2)) |
| "Proven abroad" | **VW + D-Wave, Lisbon 2019:** 9 Carris buses, 4 days, 162 valid trips. **No published classical baseline**, and an Accenture expert questioned whether quantum is needed at all. ([arXiv 2006.14162](https://arxiv.org/pdf/2006.14162), [VW Group](https://www.volkswagengroup.it/en/lab/quantum-computers-for-traffic-optimisation-a-pilot-project-in-lisbon), [Quantum Insider](https://thequantuminsider.com/2019/12/19/volkswagen-traffic-jam-eradication-project-hits-the-road/)) A PR pilot, not a deployed system. |
| The D-Wave page itself | Marketing copy ("inherently scalable", "slash travel time"). Its case study is event-tour scheduling (80 events), not a city bus network, and it publishes no benchmark numbers. |
| Can we even run it today? | The **free Leap trial is ~1 minute of solver time**, and trial accounts may not get API tokens ([D-Wave developers](https://dwavesys.com/solutions-and-products/developer), [support forum](https://support.dwavesys.com/hc/en-us/community/posts/32226980341911/comments/32624479914519)). LaunchPad (3 months free) needs an application ([Quantum Insider](https://thequantuminsider.com/2025/01/22/d-wave-announces-new-leap-quantum-launchpad-program-to-support-quantum-computing-applications/)). Not something to rely on overnight. Ocean SDK's *classical* simulated annealer runs locally for free. |

**The real bottleneck isn't compute.** A city bus network with a few hundred candidate routes is solved fine by classical tools (OR-Tools, Gurobi, simulated annealing). Amman's problem is that **nobody knows where people actually want to go** (no OD data, no GTFS for the informal network), and **routes are set by GAM/LTRC planners**, not by an algorithm. A faster solver on missing data gives a faster wrong answer.

**The judge risk:** the AI/technical judge will very likely ask "why quantum, and how does it compare to classical?" If our answer is "it's exponential", we lose Technical Implementation (15%, which scores *honesty about what's mocked*) and Pitch credibility. Also, quantum optimisation **isn't AI**, and the brief needs AI that does something a form can't.

## 3. Scorecard: the idea *as written on the whiteboard*
| Criterion (weight) | Score | Why |
|---|---|---|
| Impact on Jordan (25%) | 3 | Real, big problem (13% share, 40–47% of women turning down jobs). But impact depends entirely on GAM adopting the routes, and there's no rider-facing change on demo day. |
| Innovation (20%) | 3 | Novel in Jordan, but judges know quantum hype. Without a benchmark it reads as a buzzword. |
| Feasibility & scalability (20%) | 2 | No GTFS or OD data, a 1-minute quantum trial, 11 hours. Scaling needs GAM data access. |
| Technical implementation (15%) | 2 | We can't show quantum beating classical live. "Exponential" is a false claim the rubric punishes. |
| UX (10%) | 2 | An operator dashboard; no citizen sees anything. |
| Pitch (10%) | 3 | Strong personal story ("3 buses, 2 hours"), a catchy hook, but a risky Q&A. |
| **Weighted** | **2.55** | |

## 4. Who would pay (economics)
- **Agencies do pay for transit-planning software.** **Optibus** (planning/scheduling) raised $100M at a **$1.3B valuation** and serves 1,000+ cities ([TechCrunch](https://techcrunch.com/?p=2318921), [Globes](https://en.globes.co.il/en/article-1001412135)). **Remix** (network-design tool, **born at a hackathon**) was bought by Via for **$100M** and had 350+ government customers ([FreightWaves](https://freightwaves.com/news/via-acquires-mapping-software-company-remix-for-100m), [Geoawesomeness](https://geoawesomeness.com/via-acquires-mapping-startup-remix/)).
- **Jordanian buyers:** GAM (owns Amman Bus + BRT and pays operators per bus-km under a PPP), LTRC (inter-governorate network: 1.6M passengers in 2025, 180 more buses planned for 2026) ([Petra](https://petra.gov.jo/videoconference/index.php/en/news/ltrc-advances-inter-province-transport-project-to-boost-efficiency-and-connectivity)), MoT + EBRD (Irbid/Zarqa restructuring). Model: per-city SaaS licence or donor-funded planning project. Jordan alone is a small market, but MENA cities copying Riyadh/Dubai feeder services are the scale story.
- **Savings argument for GAM:** the operator is paid per bus-km. Removing duplicate route-km and redeploying them to uncovered areas pays for itself. We'd need GAM's real cost per km to quantify it, which we don't have.
- **Rider-side revenue (if on-demand feeders):** fares, like Dubai's Bus-On-Demand. **Caution:** Swvl entered Amman in 2019 and pivoted to B2B ([Enterprise](https://enterpriseam.com/egypt/2020/11/30/swvl-expands-to-jordan-with-new-product-targeting-businesses/)), then retrenched from smaller markets in 2022 ([TechCrunch](https://techcrunch.com/2022/11/28/swvl-reduces-its-headcount-by-50-six-months-after-axing-400-staff/amp)). Privately run B2C microtransit in Amman has a hard history, so a public, GAM-run feeder is the safer model.
- **Quantum cost:** classical solvers cost nothing at our scale. Paying for QPU time adds cost with no proven benefit. Present quantum as a pluggable backend, not a cost line.

## 5. Proven abroad (better precedents than Lisbon)
| Where | What | Result |
|---|---|---|
| **Shanghai / Beijing, "customised bus" (定制公交)** | Riders submit home→work + time online, and a route opens once **15–20 riders** cluster | All 16 Shanghai districts. A 2023 study found substantial ridership growth and better transport equity in the suburbs. ([Sixth Tone](https://www.sixthtone.com/news/1017072), [Beijing gov](https://english.beijing.gov.cn/travellinginbeijing/transportation/bus/202306/t20230601_3119561.html)) |
| **Dubai RTA, Bus-On-Demand** | Shared minibuses booked by origin/destination | **527k riders in H1 2026, +25% YoY**, 20 areas, 55 buses. 86% satisfaction earlier. ([Khaleej Times](https://www.khaleejtimes.com/life-and-living/public-transport-in-uae/dubai-rta-bus-on-demand-al-satwa-al-quoz-mirdif-ridership), [RTA](https://www.mediaoffice.ae/en/news/2022/december/13-12/one-million-plus-riders-use-the-bus-on-demand-service)) |
| **Riyadh, Bus On Demand (Mar 2025)** | On-demand feeder to Metro/BRT stations via the Darb app | 7 zones. App reviews mention delays. ([List](https://www.listmag.com/en/travel-stay/new-on-demand-bus-service-links-residential-areas-to-the-riyadh-metro-3307)) |
| **Barcelona, Nova Xarxa** | Redesigned into fewer, frequent, grid lines with easy transfers | Attracted more demand than the old network. Transfers rose to ~26% of trips and were the driver. ([Berkeley ITS](https://its.berkeley.edu/publications/network-effects-bus-transit-evidence-barcelona%E2%80%99s-nova-xarxa-0)) |
| **Nairobi, Digital Matatus** | Phones mapped the informal routes into GTFS → Google Maps | Already in our parked [G1](G-parked-ideas.md). |

## 6. New perspectives / reshaped ideas
Each one keeps the teammate's problem ("3 buses, 2 hours") but moves the AI to where the bottleneck actually is.

### O1 — "Khatti / خطّي": crowdsourced demand → new routes, with a quantum-ready optimiser ⭐ (best version)
*Shanghai's customised bus + an AI demand engine + quantum as an honest benchmark.*
1. **Riders describe their trip in Jordanian dialect by voice or text**, e.g. "من دوار صويلح لعند الجامعة الأردنية الساعة ٧ الصبح، بركب ٣ باصات". An LLM extracts origin, destination, time and current legs, then geocodes them on OSM. *(This is the AI part a form can't do: messy dialect places like "عند الإشارة جنب مخابز ...".)*
2. **Demand map:** OD pairs are clustered, and each corridor shows "N people, avg 2.6 transfers, avg 95 min".
3. **Optimiser:** choose which candidate routes or feeder vans to add, under a fleet budget, to minimise total transfers and travel time for the cluster. This is written as a **QUBO** (route selection ≈ weighted set cover with a budget, which maps neatly) and solved **two ways side by side: classical (OR-Tools / simulated annealing) and D-Wave hybrid** if we get access. We show both results honestly. *"Quantum-ready, classical today" is a credible line; "exponential" is not.*
4. **Output for GAM:** "Open express route Sweileh → JU 7:00–8:30: 18 riders, 3 transfers → 0, 95 → 35 min." That's Shanghai's 15–20-rider threshold.
5. **Rider side:** "your route has 14/20 votes; share it to unlock."
- **Data on the day (allowed by the rules):** survey **the hackathon participants' own commutes** at HTU. That's 100+ real OD trips by noon, collected with consent. It's a great demo moment ("this is *your* data"). Network: Amman Bus/BRT lines hand-coded from public maps + the 2015 Ma'an Nasel routes, labelled as such.
- **Who's left out:** riders in areas no formal route serves. Their demand is invisible today, and this makes it visible.
- **Score:** Impact 4, Innovation 4, Feasibility 3, Tech 4, UX 4, Pitch 4 → **3.80**.

### O2 — Feeder-van dispatch to BRT (Riyadh/Dubai model)
A dial-a-ride VRP that routes 5–10 vans to pick riders up near home and drop them at BRT stations. This is **exactly the problem class on the D-Wave page** (fleet routing), so it's the most "honest quantum" fit. The weakness: it's an operator tool, it needs vans and an operator, and it echoes Swvl. → ~3.4.

### O3 — Transfer-sync: fewer minutes lost between buses, without buying a bus
Shift departure times on low-frequency routes so connections line up (timetable synchronisation, a classic QUBO problem). Pitch: "same buses, 20 minutes less per transfer". The weakness: BRT runs every ~5 min, so this only helps low-frequency lines, and we lack timetable data for coasters. → ~3.2.

### O4 — "Digital Matatus for Amman" 2.0 (revives G1)
Riders' phones record GPS on coasters/servees, the AI infers stops and routes, and the output is GTFS. That fixes the *data* gap every other option depends on. The weakness: it takes weeks of data collection, so the hackathon demo is thin. → ~3.3. It's the natural Phase 2 for O1.

### O5 — Women-safe route preference (sub-feature of O1)
Rank options by transfers, waiting at isolated stops, and time of day, not just minutes. It ties directly to the 40–47% stat. Better as a feature than a product.

## 7. Verdict
- **As written (2.55): don't pitch it.** Quantum is the wrong headline: unproven, not AI, and "exponentially" invites a hard Q&A.
- **O1 (3.80) is a genuinely good backup.** It keeps the teammate's real pain, has a strong personal-story opener, uses data collected on the day, and keeps quantum as an *honest benchmark* the technical judge will respect.
- **H (Najm, 4.70) still leads** on Feasibility (clear payer: insurers) and Impact (175k minor accidents a year, measurable minutes saved). O1's impact depends on GAM acting on the output, and that's the question the business judge will ask.
- **Mentor question if O1 goes ahead:** "Does GAM have origin–destination data or a GTFS, and would they look at crowdsourced demand?"

## 8. 11-hour MVP for O1 (if chosen)
| Track | Owner | Output |
|---|---|---|
| A. Dialect trip parser | AI 1 | LLM prompt + OSM/Nominatim geocoder for Amman landmarks, 30 test sentences |
| B. Survey + data | AI 2 | QR-code form for hackathon participants (consent), cleaning, OD clustering |
| C. Optimiser | AI 3 (researcher) | QUBO formulation, classical solver + D-Wave hybrid (if access) + the benchmark table |
| D. App | SWE | Arabic RTL web app: trip input, demand map, "proposed route" card, GAM dashboard, Supabase |
