# 03. Feasibility: how it actually gets deployed

**Draft v1, Oct 10 2026.** This is a plan on paper. At the hackathon we build and demo the system on simulation and recorded footage; nothing touches a real signal. Decisions behind this page:
- The AI runs the lights **fully automatically from the first day on the street**, inside fixed safety limits.
- Both integration routes are described (central software and edge box). The choice per junction is made with GAM.
- The first site is the **7th Circle (الدوار السابع)** plus a few neighbouring signalised junctions.
- We don't mention any existing smart-signal pilot.

## 1. Why this can be done now

| What a deployment needs | Does Amman already have it? | Source |
|---|---|---|
| Cameras watching the junctions | **Yes.** GAM runs about **5,600 cameras**, mostly for **traffic counting and flow analysis** (only 25% are for violations) | Jordan News / Al-Mamlaka, Apr 2026 |
| A central place that controls the lights | **Yes.** GAM's **central control centre** manages traffic lights for **200+ intersections** | same |
| Lights linked to that centre and to cameras | **Yes.** The Traffic Department director describes signals linked to GAM's central control and to traffic cameras | Al-Mamlaka, Aug 2026 |
| An owner who wants it | **Yes.** GAM's traffic leadership talks publicly about the congestion crisis | Al-Rai, Aug 2026 |
| Legal basis for processing camera data | **Yes**, if we store counts only. Jordan's **Personal Data Protection Law No. 24 of 2023** has been in force since **17 Mar 2024**; we design so that no personal data is kept | Clyde & Co |

So we add **software**, not roads, poles or cameras.

## 2. The first site: 7th Circle cluster
- **Why the 7th Circle:** it's one of west Amman's best-known bottlenecks. It was **converted from a roundabout to traffic lights**, and GAM later cited it as the example when it did the same at the 8th Circle (2014). So it is signalised, busy, and recognisable to every judge.
- **The cluster:** the 7th Circle plus **3–5 neighbouring signalised junctions**, picked with GAM by two rules: (1) a GAM camera already sees each approach, and (2) the junctions feed each other, so coordination matters.
- **Why a cluster and not one junction:** our idea depends on the fact that a light's timing pushes queues into the next junction. One junction can't show that.

> To do before the pitch: name the neighbouring junctions on a map (Google Maps / OSM) and confirm that each one is signalised.

## 3. Rollout plan

"Fully automatic from day one" means automatic **from the first day on the street**. All the testing happens before that, in a digital copy of the cluster, so the street never sees a half-tested version.

| Phase | When | What happens | Exit check |
|---|---|---|---|
| **0. Agreement** | Weeks 0–4 | MoU with GAM's Traffic Executive Directorate. Access to camera feeds, current timing plans and controller details for the cluster. PSD Traffic Department informed as partner. | Signed MoU, data access |
| **1. Digital twin** | Weeks 4–10 | Build a simulation of the cluster, calibrated on real counts from GAM's cameras. Replay real weekdays, school-opening weeks and Fridays, comparing the current plan against our controller. GAM's engineers sign off the safety limits. | Twin matches real queues; GAM signs the safety limits |
| **2. Go live, automatic** | Month 3 | The controller takes over the cluster **automatically, 24/7**, within the safety limits. The operator watches on the Arabic console and can override. | No safety incident; uptime target met |
| **3. Measure** | Months 3–6 | The same cameras measure before vs after: average wait, longest queue, stops and travel time through the cluster. A monthly report goes to GAM. | Agreed % reduction in delay |
| **4. Scale** | Month 6+ | Corridor by corridor across GAM's 200+ intersections, then other cities (Zarqa, Irbid, Aqaba) through their municipalities. | GAM contract / tender |

## 4. Safety: what makes "automatic" acceptable
The AI picks timings **only inside limits set by GAM's engineers**. It can't break them:
- **Minimum green** for every approach, so no road is starved.
- **Pedestrian crossing time** and **all-red clearance** are always kept.
- **Maximum cycle length**, so no driver waits longer than today's worst case.
- **Automatic fallback to GAM's existing fixed plan** if a camera fails, the picture is unclear (night, rain, dust), the link drops, or the AI's own confidence is low.
- **One-click override** for the operator, and every AI decision is **logged with its reason** in Arabic.

## 5. How it connects (both routes, decided per junction)

| | **A. Central (software only)** | **B. Edge box per junction** |
|---|---|---|
| How | Reads GAM's camera feeds and sends timing plans through GAM's control centre | A small computer in the signal cabinet runs the camera AI and talks to the controller locally |
| New hardware | None | One box per junction |
| Keeps working if the network drops | Falls back to the fixed plan | Yes, keeps optimising locally |
| Depends on | The signal-controller vendor allowing timing commands from the centre | Site visits and cabinet access |
| Best for | Junctions already linked to central control | Junctions with weak links or older controllers |

Default: **A wherever possible, B where needed.** The final mix is a Phase 0 question for GAM.

## 6. Privacy by design
- The cameras are GAM's. We **process video in memory and keep only numbers**: counts, queue length and waiting time per approach.
- **No number plates, no faces, no tracking a car across junctions.** No footage is stored by us.
- Data stays on GAM's or a Jordanian government host.
- Hackathon demo footage: filmed in a public place on the day, with faces and plates blurred, and labelled as such.

## 7. Who has to say yes

| Stakeholder | Role | What they need from us |
|---|---|---|
| GAM, Traffic Executive Directorate | Owner and buyer | Safety limits, measured results, cost per junction |
| PSD Traffic Department (إدارة السير) | Partner | Less manual traffic policing at the cluster |
| Signal-controller vendor | Technical gate (route A) | A defined interface for timing commands |
| Ministry of Digital Economy / data protection | Compliance | Proof that no personal data is stored |

## 8. Who builds and runs it
- **Today:** our 4-person team (3 AI/data science, 1 software engineering) builds the controller, the vision counting, the simulation and the console.
- **For the deployment we would add:** a **traffic engineer** (advisor or hire) to set the safety limits with GAM, and a **local systems integrator** for cabinet work on route B.

## 9. Risks and what we do about them

| Risk | Likelihood | What we do |
|---|---|---|
| The controller vendor won't accept outside timing commands | Medium | Route B edge box; or GAM requires the interface in its next controller tender |
| Cameras don't see the whole queue on an approach | Medium | Pick the cluster by camera coverage; add one low-cost camera where needed |
| GAM is uneasy with full automation | Medium | Hard safety limits, automatic fallback, one-click override, and the twin results before go-live |
| Bad weather or night lowers vision accuracy | Medium | Confidence check → fallback to the fixed plan; train on night and rain footage |
| Data-access approval takes long | High | Phase 1 can start on footage we record ourselves in public |
| Budget or procurement delays | Medium | A small cluster priced as a pilot; see the revenue and costs section |

## 10. What we prove at the hackathon vs what stays on paper

| Shown live | On paper only |
|---|---|
| Vision counting on real recorded junction footage | A live link to GAM cameras |
| A SUMO simulation of a junction, our controller against a properly tuned fixed plan | Any real signal being controlled |
| Arabic operator console | The 7th Circle cluster model (unless we have time to build it) |
| Safety limits and fallback working in simulation | Field results |

## Sources
- [GAM: 5,600 traffic monitoring cameras, only 25% for violations; central control centre, 200+ intersections (Jordan News, updated 29 Apr 2026)](https://www.jordannews.jo/Section-109/News/GAM-5-600-Traffic-Monitoring-Cameras-in-Operation-Only-25-Dedicated-to-Traffic-Violations-50992), accessed 2026-10-10
- [مدير إدارة السير: حلول مرورية جديدة في عمّان (Al-Mamlaka, 26 Aug 2026)](https://www.almamlakatv.com/news/208193-), accessed 2026-10-10
- [إزالة الدوار الثامن نهاية أيلول (ArabiaWeather, 5 Aug 2014), on the 7th Circle's conversion to traffic lights](https://arabiaweather.com/en/content/إزالة-الدوار-الثامن-نهاية-أيلول), accessed 2026-10-10
- [Jordan issues first personal data protection law (Clyde & Co, Oct 2023)](https://www.clydeco.com/fr/insights/2023/10/jordan-issues-first-personal-data-protection-law), accessed 2026-10-10
- GAM congestion statement (Al-Rai, 4 Aug 2026): see [01](01-problem-statement.md)
