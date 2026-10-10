# Idea O2 — "Khatti / خطّي" deep dive: how it works, UX, demo, money, weak points

Companion to [O](O-quantum-amman-bus.md). Written 2026-10-09 (round 9). The team decided to drop "quantum" as the headline and make **AI** the core (quantum stays an optional future solver; see §3.6).

**One line:** *Tell Khatti your daily trip in your own words. When enough people share your corridor, Khatti designs a direct route, a licensed operator runs it, and GAM gets the evidence to make it permanent.*

**Pitch opener:** "Some days I take 3 buses and spend 2 hours to get somewhere 25 minutes away by car. I'm not alone: over half of Amman's transit riders commute an hour or more, and 40–47% of women surveyed turned down a job because of transport. Nobody designs routes around where people actually go, because nobody knows. Khatti finds out."

---

## 1. The core design decision: how routes get created

The question was: *is it dynamic for drivers, or does it create routes after N requests?* **Answer: neither extreme. It has three layers running at three speeds.**

| Layer | Speed | What happens | Why this speed |
|---|---|---|---|
| **1. Demand pool** | Continuous | Every trip description becomes a structured *trip intent*: origin, destination, time window, days, flexibility. Intents pile up on a demand map. | Collecting demand costs nothing and is legal on day one. |
| **2. Route proposal → pledge → launch** | Weekly | The engine clusters intents and designs candidate routes. A route goes to *pledge* when its cluster is big enough, and **launches when pledges reach that route's break-even number**. It then runs on a **fixed corridor and fixed times**, like a normal line. | Shanghai's model: 220+ demand-built "DZ" routes, opening at 15–20 riders per trip, live within ~3 days of approval ([Sixth Tone](https://www.sixthtone.com/news/1017072)). Riders need a predictable bus, and operators need a predictable shift. |
| **3. Daily stop tuning** | Each evening for the next day | Within a launched route's corridor, the optimiser picks **which pickup points to serve tomorrow** based on who booked, and sends the driver a manifest. It skips empty stops but never leaves the corridor or shifts times by more than a few minutes. | Small, safe flexibility. Riders keep their time; drivers keep their shape. |

**Why not fully dynamic (Uber-style, re-routed per request)?**
1. **Economics:** Swvl's fixed-route bus rental was ~¾ of direct costs, and its open-to-public rides had worse economics than contracted routes ([Friday Times](https://www.thefridaytimes.com/2022/12/27/swvl-the-numbers-for-pakistani-operations-help-comprehend-the-mobility-startups-exit-from-the-country/), [Enterprise](https://enterpriseam.com/egypt/whatsnext/with-a-long-road-to-profitability-a-rethink-of-the-traditional-ride-hailing-business-model-is-in-order/)). Fully dynamic microtransit is the most expensive kind of transit.
2. **Riders can't plan a commute around a bus whose time changes daily.**
3. **Law:** any passenger transport needs LTRC registration and a licence (Law 19/2017) ([Al Tamimi](https://www.tamimi.com/law-update-articles/ride-hailing-apps-in-jordan/)). A fixed route with a fixed operator is far easier to license than a roaming one.

**Why not "N requests → route" with a fixed N?** Because N should be **the number at which that route pays for itself**, and that's different per route (length, vehicle, fare, sponsor). See §5.2. *The unlock threshold isn't arbitrary; it's break-even.*

**The life of a route (state machine):**
```
DEMAND (intents pile up)
  → CANDIDATE   engine finds a cluster ≥ ~60% of break-even
  → PLEDGING    riders in the cluster are invited; AI flex-agent recruits near-misses (§3.4)
  → LAUNCHED    pledges ≥ break-even, operator accepts, 4-week trial
  → STABLE      load factor ≥ target for 4 weeks → evidence pack sent to GAM/LTRC
  → ADOPTED     GAM/LTRC makes it a permanent licensed line (or adds frequency to an existing line)
  ↘ RETIRED     load below threshold for 2 weeks → riders get alternatives, operator released
```
This is also the pitch's "society" story: Khatti is the **testing ground for new public routes**, not a competitor to Amman Bus.

---

## 2. User experience (four users)

### 2.1 Rider: WhatsApp-first, voice-first, Arabic
*Why WhatsApp:* no app download and works with voice notes, which suits low literacy and older riders. A web app (PWA) carries the same flows for the demo.

1. **"وين بتروح كل يوم؟"** The rider sends a voice note or text in dialect, e.g. *"بطلع من عند مخابز الريم بالهاشمي الشمالي، لازم أوصل الجامعة الأردنية قبل الثمانية، الأحد للخميس، هلأ بركب سرفيس وباصين."*
2. **AI confirms it back** with a map card: 📍 Hashmi al-Shamali (Al-Reem Bakery) → 📍 University of Jordan, arrive by 08:00, Sun–Thu. *"Today: 3 legs, about 95 min, about 1.20 JD (your estimate)."* ✅ / ✏️. *(The rider confirms the pin; we never guess silently.)*
3. **Their corridor:** *"14 people want a similar trip. 6 more and a direct route starts: about 40 min, 0 transfers, about 1.00 JD."* There's a **share link** ("send to classmates"), and growth is built in because the rider wants the route to unlock.
4. **Flex offer (AI agent):** *"If you can walk 5 min to دوار المدينة الرياضية and arrive by 7:45 instead, you join خط ٧, which is 2 riders away from launching. Deal?"*
5. **Pledge:** commit to a 4-week trial with a small deposit (CliQ / eFAWATEERcom / card), refunded if the route doesn't launch.
6. **Route live:** *"خط ٧ starts Sunday. Pickup 7:02 at X."* A QR boarding pass, live bus location, "share my trip" with family, and a women-only seat-row option (a pilot feature).
7. **Every week:** a one-tap rating plus "still need this route?". That feeds retire/adopt decisions.

### 2.2 Driver / operator (licensed coaster or bus operator)
- **Route offers:** "Morning run Hashmi → UJ, 22 pledged riders, JD X/day guaranteed for a 4-week trial. Accept?"
- **Evening manifest:** tomorrow's stop list in order, rider count per stop, navigation, QR scanner for boarding.
- **Weekly payout statement.** Operators are **existing licensed operators with spare peak capacity**. We recruit them; we don't compete with them.

### 2.3 GAM / LTRC planner dashboard
- **Unmet-demand heat map:** corridors where people want to go but no line serves them, with transfers and minutes lost.
- **Proposed routes**, each with an AI-written **Arabic evidence pack**: who rides, when, the time saved, the overlap with existing lines, and an alternative ("or add frequency to line 45").
- **Trial results** of launched routes: load factor, punctuality, retention, % women riders.
- **GTFS export** of Khatti routes. Amman has no public feed today (see [O §1](O-quantum-amman-bus.md)).

### 2.4 Sponsor (university, employer)
- "Your students/staff's trips": a cluster map of their commutes, proposed routes, a cost per rider, and an option to subsidise routes. Universities already run shuttles: UJ has 22-seat buses ([UJ](https://ipmd.ju.edu.jo/Pages/Transportation1.aspx)), and Al-Zaytoonah runs routes across Amman, Madaba, Salt and Zarqa but **cancels a trip below 7 students** ([ZUJ](https://www.zuj.edu.jo/Transportation-Department/Announcements.aspx)). They have exactly this problem today.

---

## 3. How it actually works (the engine)

```
voice / text (dialect)
   │  ① Speech-to-text (Arabic) → ② LLM extraction (structured JSON)
   ▼
trip intent {origin, dest, arrive_by, days, current_legs, flex_minutes, walk_max}
   │  ③ Geocoding: Amman landmark gazetteer (OSM + our list) → rider confirms pin
   ▼
demand pool (Supabase / PostGIS)
   │  ④ Clustering: group intents by origin zone + destination zone + time
   ▼
clusters
   │  ⑤ Candidate route generation: stops (walk ≤ ~600 m) + ordered path on road network (OSRM)
   │     + variants: direct express / feeder to nearest BRT station / extend an existing line
   ▼
candidate routes (each with riders served, minutes saved, cost, break-even N*)
   │  ⑥ Selection optimiser: pick the set of routes to launch under fleet/budget limits
   ▼
routes → PLEDGING  ──⑦ AI flex-agent recruits near-miss riders──►  LAUNCHED
   │  ⑧ Daily: per-route stop selection + order for tomorrow (small VRP)
   ▼
operator manifest + rider notifications + GAM dashboard (⑨ AI evidence pack)
```

### 3.1 ①–③ Understanding the trip (AI, the part a form can't do)
- Jordanians give directions by **landmarks, not addresses** ("عند إشارة الشرق الأوسط", "جنب مستشفى الأمير حمزة"). The LLM extracts landmark mentions and the time constraint; then a geocoder resolves them against an **Amman landmark gazetteer** (OSM POIs plus a hand-made list of ~200 roundabouts, malls, hospitals and universities).
- **Structured output:** `{origin_text, origin_landmarks[], dest_text, arrive_by, depart_after, days[], current_legs, current_minutes, current_cost, flex_minutes, walk_max, notes}`.
- Ambiguous? The bot asks *one* clarifying question ("دوار الداخلية ولا إشارة الداخلية؟"). The rider always confirms the pin.
- **Privacy by design:** we store the confirmed point **snapped to a ~300 m zone**, not the exact home, and raw voice is deleted after transcription.

### 3.2 ④ Clustering (ML)
- Each intent becomes a vector (origin x,y; destination x,y; arrival time; with weights). **HDBSCAN** or a simple grid-and-time bucketing groups them into "people who could share a vehicle".
- **"On the way" matching:** a rider whose origin lies *along* a corridor joins it even if their origin differs. That's done in ⑤ by checking the detour each rider adds.

### 3.3 ⑤–⑥ Designing routes (optimisation)
- **Candidates:** for each cluster, pick stop points (k-medoids on origins with a walk limit). Order them with a small TSP ending at the destination, capped so no rider rides more than ~1.5× the direct drive time. Generate **variants**: a direct express, a **feeder to the nearest BRT station** (cheaper, and uses the existing network), or a **"strengthen existing line X"** recommendation when one already almost serves the cluster.
- **Selection** as an integer programme (Google OR-Tools CP-SAT):
  - *maximise* Σ (riders served × minutes saved) − λ × operating cost
  - *subject to* each rider assigned to ≤ 1 route, a route is active only if assigned riders ≥ N\* (break-even), and vehicles available per time slot ≤ fleet offered by operators.
- Runs in seconds for hundreds of intents on a laptop.

### 3.4 ⑦ The flex-agent (AI, the wow)
- Many riders *almost* fit a route: 15 min off, or 600 m away. The optimiser computes **for each near-miss rider the smallest change that would put them on a route**, and the LLM turns it into a personal Arabic message (§2.1 step 4).
- That turns "12 of 20, stuck" into "20 of 20, launch". It's also a measurable AI effect we can show in the demo: *routes unlocked with vs without the flex-agent*.

### 3.5 ⑧–⑨ Daily ops + evidence
- **Nightly:** each launched route gets tomorrow's stop set and order from bookings (OR-Tools VRP with time windows). No-show handling comes in Phase 2 (a predictor trained on booking history).
- **The evidence pack** is generated by the LLM from the route's real numbers (riders, times, overlap with existing lines). It's a document GAM can forward internally. Numbers come from the database, never from the LLM.

### 3.6 Where "AI" and "quantum" honestly sit
| Component | Technique | Is it AI? |
|---|---|---|
| Voice/text → trip | STT + LLM structured extraction | ✅ yes (core) |
| Landmark geocoding + clarifying question | LLM + gazetteer | ✅ yes |
| Clustering demand | Unsupervised ML (HDBSCAN) | ✅ ML |
| Flex-agent negotiation | Optimiser + LLM | ✅ yes (wow) |
| Evidence pack for GAM | LLM over DB numbers | ✅ yes |
| Route selection / daily stops | Integer programming / VRP (OR) | ❌ classical optimisation |
| *Future:* demand forecast, no-show prediction | Supervised ML on booking data | ✅ (needs data) |

**Quantum:** the route-selection step is the only piece that maps to a QUBO. If the team's researcher wants it, show a **side-by-side table: CP-SAT vs a D-Wave hybrid / simulated-annealing run on the same instance**, framed as "quantum-ready, classical today". Don't headline it, and never say "exponential".

---

## 4. Demo plan (7 minutes, live)

### 4.1 The live moment
**Morning of Day 2:** QR posters around HTU say "كيف وصلت اليوم؟ احكيلنا بفويس نوت". Hackathon participants describe *their own* commute, with consent text and zone-level locations only. That's **real data collected on the day**, which the rules allow. By 1 PM we have, say, 80–150 trips.

**On stage:** a judge (or a teammate if they decline) sends a voice note of their commute. It appears on the map, joins a cluster, and **pushes a route over its threshold**. The route goes "LAUNCHED", and the driver phone on the table buzzes with a manifest.

### 4.2 Script
| Time | Beat | Screen |
|---|---|---|
| 0:00–0:45 | Personal story + stats (13% share, 40–47% of women turned down jobs, 1 h+ commutes) | Photo of the 3-bus trip on the map |
| 0:45–1:45 | Rider flow: voice note → AI confirms pins → "14 others, 6 to go" | Phone mirrored (WhatsApp-style web UI) |
| 1:45–3:00 | **Live:** the room's real data on the map (HTU survey). Clusters form. The engine proposes 3 routes with before/after (transfers, minutes, JD) | Planner dashboard |
| 3:00–3:45 | Flex-agent: near-miss rider gets an offer, accepts → the route crosses threshold | Phone + map |
| 3:45–4:30 | **Judge's voice note** → joins → the route launches → driver phone buzzes with the manifest | Two phones |
| 4:30–5:30 | GAM view: evidence pack in Arabic, GTFS export, unmet-demand heat map | Dashboard |
| 5:30–6:30 | Business: break-even thresholds, B2B sponsors, GAM licence; Swvl lessons | One slide |
| 6:30–7:00 | Honesty slide + ask (pilot with one university + GAM) | One slide |

### 4.3 What's real vs mocked (say it out loud; that's 15% of the score)
| Real | Mocked / labelled |
|---|---|
| Dialect voice → structured trip (live LLM) | City-wide demand beyond the HTU survey = **synthetic, labelled** |
| HTU participants' trips (consented, zone-level) | Operators, payments and fares are simulated |
| Clustering, route design, optimiser (live) | Travel times from OSRM (no live traffic) × a peak factor |
| Map, stops and roads from OpenStreetMap | Existing-network comparison uses riders' self-reported legs |
| Flex-agent messages (live LLM) | GAM dashboard is a prototype |

**Fallbacks:** a pre-recorded voice note, a cached survey snapshot, and a cached optimiser result in case the venue Wi-Fi dies.

**Demo caveat:** HTU attendees all share one destination (HTU). That's perfect for showing "many origins → one destination" route building. The synthetic layer shows multi-destination clustering.

---

## 5. How we make money

### 5.1 Lessons we're explicitly designing around (Swvl)
- Swvl rented buses and launched routes *then* searched for riders. Bus rental was ~¾ of direct costs ([Friday Times](https://www.thefridaytimes.com/2022/12/27/swvl-the-numbers-for-pakistani-operations-help-comprehend-the-mobility-startups-exit-from-the-country/)).
- Its consumer rides had worse economics. Corporate/school routes were better and reached ~70% of revenue by Aug 2022 ([Friday Times](https://www.thefridaytimes.com/2022/12/27/swvl-the-numbers-for-pakistani-operations-help-comprehend-the-mobility-startups-exit-from-the-country/), [Enterprise](https://enterpriseam.com/egypt/whatsnext/with-a-long-road-to-profitability-a-rethink-of-the-traditional-ride-hailing-business-model-is-in-order/)). Swvl entered Amman in 2019 and launched a B2B product in 2020 ([Enterprise](https://enterpriseam.com/egypt/2020/11/30/swvl-expands-to-jordan-with-new-product-targeting-businesses/)).
- **Khatti's differences:** (1) **demand before supply**: a route only launches after pledges reach break-even. (2) **Asset-light**: licensed operators own the vehicles and only run proven routes. (3) **B2B and government revenue from day one**, not just fares.

### 5.2 Route unit economics: where the threshold comes from
Break-even riders for a dedicated vehicle doing one morning + one evening run:

**N\* = C ÷ (2 × fare × (1 − commission))**, where C = the operator's daily cost for the two runs.

We **don't yet know C**. *Day-1 task: ask a coaster operator/mentor.* Illustrative only, with 15% commission:

| Operator cost C (assumed) | Fare JD 0.65 (Amman Bus level) | Fare JD 1.00 | Fare JD 1.25 |
|---|---|---|---|
| JD 30/day | 27 riders | 18 | 14 |
| JD 40/day | 36 | 24 | 19 |
| JD 60/day | 54 | 35 | 28 |

*(Amman Bus fares are 30–65 piasters, per [Al-Mamlaka](https://almamlakatv.com/news/23032-أجرة-باص-عمان-بين-30-65-قرشا).)*

**What the table tells us (honestly):**
- At Amman Bus fare levels, a dedicated 24-seat vehicle **can't** break even. Khatti routes must be **express routes priced near what multi-transfer riders already pay**, **sponsored**, or **use the operator's spare capacity** (lower C).
- The 3-bus rider already pays several fares a day. The women's survey found **JD 57/month** average spend ([Urbanet](https://www.urbanet.info/jordan-public-transport-women-work-force/)), roughly JD 1.3 per one-way workday trip (our arithmetic: 57 ÷ 22 days ÷ 2). So a **JD 1.00–1.25 direct route costs the same or less, with 0 transfers and half the time**.
- **Feeder-to-BRT variants** are shorter, so C is lower and N\* is smaller, and the BRT leg is already subsidised. They're often the best first routes.

### 5.3 Revenue streams (in order of when they start)
| # | Who pays | For what | Model |
|---|---|---|---|
| 1 | **Universities & employers** | Designing and filling their shuttle routes (they already run them and cancel low-demand trips) and new routes for staff/students | Per-route SaaS fee or per-rider fee. *First paying customer.* |
| 2 | **Riders (via operator)** | Seats on public Khatti routes | 10–15% commission on fares |
| 3 | **GAM / LTRC / MoT** | Demand-intelligence dashboard, route proposals with evidence, GTFS export, trial management | Annual licence per city. Donor-funded pilots: EBRD discussed restructuring routes in Irbid and Zarqa (Sep 2025) ([see O](O-quantum-amman-bus.md)) |
| 4 | **Operators** | Guaranteed-fill routes for spare peak capacity | Free to join; we earn via #2 |
| 5 | **Region** | Same platform for other MENA cities | Licensing. Planning-software precedent: Optibus valued at $1.3B, and Via bought Remix for $100M ([O §4](O-quantum-amman-bus.md)) |

**Honest sizing:** Jordan-only fare commissions are small. The business case is **B2B shuttles + government licences**, plus the data asset (the only live origin–destination demand map of Amman).

---

## 6. Weak points and concerns: the full list
Rated **H/M/L** for how much a judge could hurt us with it.

| # | Concern | Risk | Our answer / mitigation |
|---|---|---|---|
| 1 | **Is it legal to run new routes?** All passenger transport needs LTRC registration + licence (Law 19/2017); app-based transport is regulated separately (2018 regulation). In Jan 2026 the LTRC removed the cap on licensed apps and opened licensing to new ones ([ARIJ](https://en.arij.net/impact/following-an-arij-investigation-new-regulations-issued-to-regulate-the-ride-hailing-app-sector-in-jordan/)). | **H** | Phase 1 needs no new licence: the demand map + university/employer shuttles (private contracts with licensed operators). Phase 2: **only licensed operators**, LTRC as a partner, routes run as **4-week trials** with LTRC approval. Mentor question: what licence does a trial line need? |
| 2 | **Existing coaster/servees drivers will fight it** (Jordanian taxi drivers protested ride-hailing apps in the past; source still to add). | **H** | Recruit them: they *are* the operators. Khatti fills their seats; it doesn't replace them. Pitch line: "we bring them riders". |
| 3 | **Cold start:** no route until enough people sign up, and nobody signs up without routes. | **H** | Start where demand is concentrated: **one university** (thousands with the same destination and times) and **one industrial employer**. The rider sees progress ("6 to go") and shares the link. The flex-agent fills gaps. |
| 4 | **Unit economics** (Swvl's grave). | **H** | Demand-before-supply, break-even thresholds, asset-light, B2B first, feeder-to-BRT variants (§5). Show the formula on stage. |
| 5 | **Pledges ≠ riders** (people say yes and don't show). | M | A deposit/weekly pass on launch, a trial period, a pledge→ride conversion KPI, mild overbooking, and later a no-show predictor. Chinese media report Hefei's customised bus cancelling trips with under 10 bookings (primary link still to add), so plan for it. |
| 6 | **Selection bias:** app users aren't the whole population; the poorest and oldest are under-represented. | M | WhatsApp voice (no app), a phone-call line, sign-up points with partners (SADAQA, which ran the women-transport study; universities; municipalities). Weight demand by census population per zone on the GAM dashboard. |
| 7 | **"Who is left out?"** — people without smartphones. | M | Voice notes + phone line + a partner registering on their behalf. Be honest that day one reaches smartphone users first. |
| 8 | **Privacy:** home and work locations are sensitive, especially for women. | M | Zone-level storage (~300 m), exact pickup only shown to the driver *for booked riders on that day*, raw voice deleted, explicit consent, GAM only sees aggregates. |
| 9 | **Safety (women)** | M | Licensed vetted drivers, QR boarding (known riders only), live trip sharing, ratings, a women-only seat-row option, a pilot women-only route. Partner with SADAQA. |
| 10 | **Dialect ASR/geocoding errors** | M | The rider confirms the pin on a map. One clarifying question. A landmark gazetteer. In the demo, fall back to text. |
| 11 | **"Isn't this just Swvl / Careem Bus / a trip planner?"** (avoid-list #3) | M | Trip planners *route you on existing lines*; Khatti *creates lines* from proven demand and hands them to GAM. Swvl launched routes first; we launch only after break-even pledges. |
| 12 | **No GTFS / OD data**, so we can't compute the "current trip" accurately | M | Use the rider's self-reported legs and minutes (already in their voice note), plus OSRM drive time × a peak factor for the new route. Label it. Over time Khatti *creates* the OD data Amman lacks. |
| 13 | **Is it AI or just operations research?** | M | §3.6: five AI components; the flex-agent is the clear "a form can't do this" moment. |
| 14 | **Impact depends on GAM adopting routes** | M | It doesn't depend only on GAM: university/employer routes deliver impact without GAM. GAM adoption is the scale path, and the evidence pack makes it easy. |
| 15 | **Peak-only demand → idle vehicles midday, empty return trips** | M | Use operators' *spare* capacity (lower C). Match counter-peak demand (e.g. night-shift workers, hospital staff). Feeder variants. |
| 16 | **Traffic makes times unreliable** | L–M | A peak factor in planning, real arrival data from boarding QR scans, and recalibrating schedules weekly. |
| 17 | **Payments: cash culture** | L | CliQ / eFAWATEERcom / card, plus a cash-to-driver option with QR confirmation. Amman Bus already runs a card + QR app system. |
| 18 | **Why wouldn't GAM just build it themselves?** | L | Fine: the GAM licence is a revenue stream. Our edge is the dialect AI, the flex-agent and the demand data we've already collected. |
| 19 | **Demo risks:** noisy room, Wi-Fi, few survey responses | M | Text fallback, cached data, start the survey early in the morning, and have teammates seed real trips. |
| 20 | **Sector fit** | L | Transport & mobility + accessibility & inclusion + community engagement, all listed sub-areas of `next.society()`. |

---

## 7. 11-hour build plan (4 people)
| Hour | AI-1 (LLM/voice) | AI-2 (data/ML) | AI-3 researcher (optimiser) | SWE (app) |
|---|---|---|---|---|
| 0–1 | Prompt + JSON schema for trip extraction | Survey QR + consent text, start collecting | Problem formulation, OR-Tools setup | Supabase schema (intents, clusters, routes, pledges), Next.js RTL shell |
| 1–4 | STT (Arabic) + extraction + 30 test sentences | Amman landmark gazetteer (OSM Overpass + ~200 manual) + geocoder | Candidate generation (stops, ordering with OSRM) | Rider flow UI: voice → confirm → corridor card |
| 4–7 | Clarifying question + flex-agent messages | Clustering + synthetic city demand (labelled) | Selection model + break-even threshold logic | Planner dashboard map (Leaflet + OSM) |
| 7–9 | Evidence pack generator | Load the real survey data, sanity checks | Daily stop/VRP for the manifest; optional quantum-inspired comparison | Driver manifest view + live "route launched" event |
| 9–11 | Demo script, fallbacks, honesty slide | Metrics slide | Before/after numbers | End-to-end rehearsal ×3, deploy |

**Stack:** Next.js (RTL) + Supabase (Postgres/PostGIS, realtime for the "route launched" moment) + an LLM API + Arabic STT + OpenStreetMap (Overpass, Nominatim, OSRM) + Python service (OR-Tools, scikit-learn/HDBSCAN).

---

## 8. Pilot KPIs (what we'd promise a partner)
- Transfers per trip (target: 2–3 → 0–1), door-to-door minutes, rider cost per trip.
- Pledge → ride conversion, load factor per run, retention after 4 weeks.
- % women riders, % riders from zones with no current line.
- Routes adopted by GAM/LTRC or a university.

## 9. Re-score after the deep dive
| Criterion (weight) | Score | Why |
|---|---|---|
| Impact (25%) | 4 | Real, sourced pain (transfers, women's jobs, 1 h+ commutes). The university/employer path delivers impact even without GAM. |
| Innovation (20%) | 4 | Demand-pledged routes are new to Jordan; the flex-agent + dialect capture are novel. Proven abroad (Shanghai DZ). |
| Feasibility (20%) | 3 | Buildable in 11 h. Licensing, operators and economics are real hurdles, but there's a credible path (§5–6). |
| Technical (15%) | 4 | A real AI pipeline + a real optimiser + real data collected on the day, with an honest real-vs-mocked table. |
| UX (10%) | 5 | Voice notes in dialect, Arabic, WhatsApp-style, plus a live judge moment. |
| Pitch (10%) | 5 | Personal story, the room's own data, a route launching live on stage. |
| **Weighted** | **3.95** | Up from 3.80. |

**Compared with H (Najm, 4.70):** H still has the clearer payer (insurers) and a bigger measurable outcome (an officer visit avoided per minor accident). Khatti has the **better live demo** (the room's own data) and the **more personal story**. The weak spots are licensing (#1), driver opposition (#2) and economics (#4). If a mentor says LTRC trial routes and university shuttles are realistic, the gap narrows.

## 10. Numbers to verify before the pitch
1. An operator's real daily cost for a coaster/24-seat bus (C in §5.2): ask a mentor or a coaster driver.
2. What licence an LTRC trial line needs, and whether university shuttles need anything beyond the operator's existing licence.
3. Current coaster/servees fares (we only have Amman Bus's 30–65 piasters).
4. Jordan university enrolment (latest found via search: ~276k in 2014 with a 375k projection for 2030, attributed to the Higher Population Council; too old to quote, needs a primary source).
