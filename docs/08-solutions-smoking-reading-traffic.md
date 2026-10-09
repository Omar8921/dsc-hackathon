# Solutions for the three chosen problems (round 6, 2026-10-09)

The team picked three problems from [07-jordan-big-problems.md](07-jordan-big-problems.md): **smoking**, **children who can't read by age 10**, and **traffic congestion**.
Each solution is scored on the **6 official criteria** (1–5, official weights).

**What "AI that feels natural" means here (applied to every idea):** the AI does a job that **a human could do but can't afford to do at this scale or at this hour**, e.g. listen to 45 children read, answer a craving at 11 pm, or watch 200 intersections at once. If you removed the AI, the product would stop working, not just get less fancy.

---

## Problem A: Smoking
**Context:** men 55–66% smoke, adults ~35% (≈2M+ smokers, our estimate). **59% of smokers want to quit** and ~50% tried last year. ([Jordan Times survey](https://jordantimes.com/news/local/national-survey-reveals-high-tobacco-use-among-jordanians-urges-stronger-anti-smoking), [WHO EMRO](https://www.emro.who.int/jor/jordan-news/world-no-tobacco-day-2021-commit-to-quit.html))
**The gap:** MoH runs free quit clinics (23 → 31 clinics, free counselling and nicotine replacement). They handled **21,000 cases in two years (~10k/yr) at a 15% success rate.** ([Petra](https://www.petra.gov.jo/en/news/tobacco-consumption-in-jordan-balancing-economic-and-public-health-implications), [WHO EMRO](https://www.emro.who.int/tfi/news/jordan-successfully-bans-waterpipes-adapts-smoking-cessation-services-and-establishes-partnerships-during-covid-19.html), [Jordan News](https://www.jordannews.jo/Section-109/News/Health-ministry-allocates-JD700-000-to-expand-quit-smoking-clinics-28640)) **That's well under 1% of smokers reached per year.** The other 99% try alone and relapse at 11 pm with friends and shisha.

### A1. "Bala Dukhan / بلا دخان": AI quit coach on WhatsApp, connected to the MoH clinics
- **What it is:** a WhatsApp number (no app). You enrol and the coach builds a quit plan with you in Jordanian dialect, then stays with you for 12 weeks. There's a **"craving SOS"** (voice or text, any hour) that talks you through the next 5 minutes using proven CBT techniques. It **learns your triggers** (after coffee, after mansaf, shisha nights, exam stress) and messages you *before* them. It shows money saved in JD and health recovered. When you need nicotine replacement or more support, it **books you into the nearest free MoH clinic.**
- **Why the AI is needed:** 2M people can't each have a counsellor at 11 pm. Fixed text-message programmes already work (txt2stop, see below); an LLM adds what fixed texts can't: a real conversation in dialect, personal triggers, and timing.
- **Proof abroad:** **txt2stop (UK RCT, 5,800 smokers):** text-message support **doubled biochemically verified quitting at 6 months** (LSHTM impact case); self-reported 28-day abstinence 20% vs 14%. ([LSHTM](https://researchonline.lshtm.ac.uk/id/eprint/303/), [REF impact case](https://impact.ref.ac.uk/casestudies/CaseStudy.aspx?Id=43699)) **WHO "Florence"** is WHO's own AI quit coach, which shows WHO considers this the right direction, but it's English-first and has no outcome data. ([WHO](https://www.who.int/europe/news/item/14-02-2021-meet-florence-who-s-digital-health-worker-who-can-help-you-quit-tobacco))
- **MVP:** WhatsApp bot (Twilio sandbox), enrolment and quit-date plan, craving SOS (LLM with a CBT script as guardrails), trigger log → proactive nudges, savings tracker, clinic finder/booking (31 clinics, mocked booking), and a counsellor dashboard showing enrolled users and relapse-risk flags.
- **Demo moment:** a judge texts "بدي سيجارة هلأ" ("I want a cigarette right now") to the number on screen and gets a real, warm, specific response in dialect. Then the dashboard shows the trigger being learned.
- **Who pays:** MoH / WHO tobacco-control programmes (B2G); employers and health insurers (fewer smokers means lower medical costs); nicotine-replacement makers' sponsorship (handle carefully: no tobacco-industry money, per the WHO tobacco treaty).

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 5 | 3 | 4 | 4 | 5 | 4 | **4.15** |
*Impact 5: reaches the 99% the clinics never see. Innovation 3: quit bots exist abroad; Arabic dialect plus clinic integration is new for Jordan.*

### A2. Quit-clinic & pharmacy copilot (human + AI hybrid)
- **What it is:** helps the people who already treat smokers (MoH clinic counsellors and community pharmacists) treat **10× more patients and lose fewer of them.** At the first visit the AI handles the assessment (nicotine dependence score), suggests the replacement-therapy dose per guidelines for the pharmacist or doctor to confirm, and writes the plan. **Between visits** it does daily check-ins with the patient and flags who is about to relapse, so the counsellor calls the right 5 people today instead of everyone once a month.
- **Why the AI is needed:** follow-up is where the 15% success rate leaks. The AI does continuous follow-up and decides who needs a human now.
- **Proof abroad:** Cochrane 2019: **intensive pharmacy-delivered support beats minimal support (RR 2.30, low certainty).** ([Cochrane](https://cochranelibrary.com/cdsr/doi/10.1002/14651858.CD003698.pub2)) Very brief physician advice adds +1–3 points. ([Cochrane CD000165](https://www.cochrane.org/CD000165))
- **MVP:** clinician web console (assessment → plan → replacement-therapy suggestion), patient check-in via WhatsApp/SMS, relapse-risk ranking (rules plus a small model on check-in answers), outcome tracker.
- **Who pays:** MoH (more quitters per counsellor), pharmacies (replacement-therapy sales plus a service fee), insurers.

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 4 | 4 | 4 | 4 | 3 | **3.85** |
*Less "wow" on stage; stronger institutional story. Best built as A1's back office: same product, two sides.*

---

## Problem B: Children who can't read by age 10 (learning poverty)
**Context:** learning poverty 52% → **60%+**. Jordan's own early-grade survey (RAMP, K2–G3) found only **13% (2017) → 19% (2018) of pupils met the oral reading fluency benchmark**, and refugee-camp pupils progressed least. ([RTI RAMP 2018](https://shared.rti.org/node/715), [Jordan News](https://jordannews.jo/Section-109/News/Learning-poverty-surges-from-52-5-to-over-60-post-COVID-Mahafzah-34800)) Classes of 45+, 826 double-shift schools.
**The gap:** a teacher can't listen to 45 children read one by one, so struggling readers aren't identified until it's too late.

### B1. "Ismaa'ni / إسمعني": a 3-minute reading check that groups the class by level ⭐
- **What it is:** a teacher app on **one phone**. Each child reads a short Grade-level Arabic passage aloud for 60 seconds. AI speech recognition, aligned to the known text, scores **words correct per minute** and the **error pattern** (letter confusions, vowel-mark errors, skipped words) instantly. The app **sorts the whole class into reading levels** and gives the teacher **daily 20-minute group activities per level**. This is the "Teaching at the Right Level" method. It re-checks every 2 weeks and shows the principal and the education directorate who is moving and who is stuck.
- **Why the AI is needed:** scoring 45 recordings by ear takes a teacher hours, so it never happens. AI makes the standard international reading test (the same one RAMP used) take 3 minutes per child with instant results. That's the whole product.
- **Proof abroad:** **Teaching at the Right Level** (Pratham × J-PAL): multiple randomised trials in India, e.g. 17,266 students in Uttar Pradesh, with large gains in reading. Rated a **"Great Buy"** by the Global Education Evidence Advisory Panel (2023). ([J-PAL](https://www.povertyactionlab.org/evaluation/using-learning-camps-improve-basic-learning-outcomes-primary-school-children-india), [Pratham](https://www.pratham.org/guided-tour-of-teaching-at-the-right-level/)) **Amira** (AI that listens to children read): randomised trial effect +0.64; Evidence for ESSA average +0.15 over 15.6k students. ([Evidence for ESSA](https://evidenceforessa.org/?p=665))
- **Why it reaches the left-out:** it needs **no student devices**, only the teacher's phone, so it works in the double-shift and camp schools where kids have no phones. That directly answers this panel's "does your app actually reach them?".
- **MVP:** teacher PWA with a passage bank (5 leveled Arabic passages; use RAMP-style decodable texts we write ourselves), record → Arabic ASR (Whisper or another Arabic model) → **alignment to the expected text** (much easier than open transcription) → words correct per minute and error tags → class level grid → AI-generated daily group activities per level (from typed templates) → progress chart.
- **Demo moment:** a teammate (or judge) reads a passage on stage and **deliberately makes 3 mistakes**. Within seconds the screen highlights exactly those words, shows the error type and words correct per minute, and the child "drops" into a level group with tomorrow's activity ready.
- **Who pays:** MoE early-grade programmes, UNICEF / UNRWA schools (UNRWA runs ~170 schools in Jordan; verify), donors funding foundational learning; private schools per student per year.

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 5 | 4 | 4 | **4.40** |
*Impact 5: hits the exact learning-poverty measure with a reach model that needs no student devices. Feasibility risk: child Arabic speech recognition is weaker than adult; aligning to a known text reduces it, but it needs testing. Be honest in the pitch.*

### B2. Home read-aloud buddy on WhatsApp voice notes
- **What it is:** the child sends a **voice note** reading tonight's short story; the bot replies with gentle feedback and the next story at their level. The **parent gets a 20-second voice summary** ("Lana read 34 words a minute, tricky letter: ث"), which works for parents who can't read well themselves.
- **Why the AI is needed:** listening and correcting at home when no adult can.
- **Proof abroad:** Google Read Along (fluency +35–85% internal analysis; India, independent assessment of 3,500 students: 40% more improved a level). ([Google blog](https://blog.google/products-and-platforms/products/education/celebrate-international-literacy-day-read-along/))
- **⚠️ Honest problem:** **Google Read Along already exists in Arabic, for free** ([Ahram](https://english.ahram.org.eg/WorldCup/News/379544.aspx)). Our only edges are WhatsApp/no install, Jordanian curriculum texts, and the parent loop. Best used as **B1's homework extension**, not alone.

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 2 | 4 | 4 | 5 | 4 | **3.70** |

---

## Problem C: Traffic congestion
**Context:** **JD 1–1.5 billion a year** lost to congestion; public transport ~13% of trips; vehicles +5.5%/yr. ([Jordan News](https://www.jordannews.jo/Section-106/Features/Traffic-congestion-losses-amount-to-JD1-5-billion-annually-963), [CODATU](https://www.codatu.org/en/planning-sustainable-mobility-in-the-amman-metropolitan-area-jordan/))
**Important finding:** **GAM already has ~5,600 cameras, "primarily for traffic counting and flow analysis", a central control centre for 200+ signalised intersections, and has started smart signals at 4–5 pilot sites (2026).** ([Jordan News – cameras](https://www.jordannews.jo/Section-109/News/GAM-5-600-Traffic-Monitoring-Cameras-in-Operation-Only-25-Dedicated-to-Traffic-Violations-50992), [Jordan News – smart signals](https://www.jordannews.jo/Section-109/News/Smart-Traffic-Signals-Installed-at-Four-Amman-Sites-54743)) So any traffic idea must plug into this, not reinvent it.

### C1. "Ishara / إشارة": AI signal timing from existing cameras, coordinated across intersections
- **What it is:** take the camera feeds GAM already has. Computer vision counts queues per approach in real time. An optimiser re-times the signals every few seconds and **coordinates neighbouring intersections**, so a green wave forms instead of each light acting alone. An operator dashboard shows queue lengths, delay saved and incidents.
- **Why the AI is needed:** you can't have humans re-time 200 intersections every 2 seconds. Vision (counting) plus optimisation (timing) is the product.
- **Proof abroad:** **Surtrac (Pittsburgh, CMU):** pilot of 9 intersections, **travel time −25%+, stops and wait −25%+, idling ~−40%**; expanded to ~50 intersections. ([ITS DOT](https://www.itskrs.its.dot.gov/2013-b00820), [Fortune](https://www.fortune.com/2015/07/13/swarming-traffic-lights)) Maricopa County 2025: camera-based AI timing cut delay by 322 vehicle-hours a week at one intersection. ([ITS DOT 2025](https://www.itskrs.its.dot.gov/2025-b02021))
- **MVP:** record 10 minutes of video of a real busy intersection near HTU on Day 1 (public space; blur faces and plates). YOLO vehicle counting per lane → feed the counts into a **SUMO simulation** of that intersection plus 2 neighbours → compare fixed-time vs our adaptive controller → dashboard with before/after delay and queue.
- **Demo moment:** a split screen. Real Amman video with live vehicle counts on the left; the simulated intersection on the right, where switching from "current timing" to "AI timing" visibly melts the queue and the delay counter drops.
- **Who pays:** GAM / Ministry of Transport (B2G licence per intersection). Benefit pitch: if adaptive timing achieved even a fraction of Surtrac's −25% on the worst corridors, it would be worth millions of JD of the JD 1–1.5bn.
- **Honest weaknesses:** (1) **GAM is already piloting smart signals**, so our angle must be *network coordination using the cameras they already own*, and we should ask a mentor what their pilot actually does. (2) It's simulation only; real deployment needs GAM integration. (3) **"Who is left out?" is weaker:** drivers aren't the left-out group, though buses and service taxis stuck in the same traffic carry the low-income riders. (4) The user is an operator, so there's no citizen UX.

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 3 | 3 | 5 | 3 | 5 | **3.85** |

### C2. Remote minor-accident handling (Najm for Jordan), seen as a congestion fix
- Already fully researched: [ideas/H](ideas/H-najm-for-jordan.md) + [H2 business model](ideas/H2-najm-ai-and-business-model.md).
- **Traffic angle:** ≈175k non-injury accidents a year, **91% inside cities**, and every one blocks a lane until an officer arrives. Shanghai's video quick-handling averages **6 min per case**. Najm targets ≤10 min. Clearing lanes faster is a direct congestion fix.
- **Why the AI is needed:** photo checks, damage reading, reconciling two drivers' Arabic statements, fault rules with citations, fraud flags.
- It was set aside for "wow", but **for the traffic problem it's the strongest option**: it has a clear payer (insurers), a full user flow, and a two-phone live demo.

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 5 | 4 | 5 | **4.50** |

### C3. School-run pooling for private-school families
- **What it is:** parents at the same school (a trusted closed group, which solves carpooling's trust problem) get AI-matched into rotating car pools or shared vans. The optimiser builds routes and schedules each morning.
- **Data:** private schools hold ~33% of primary enrolment nationally (World Bank 2023, [Trading Economics](https://tradingeconomics.com/jordan/school-enrollment-primary-private-percent-of-total-primary-wb-data.html)). The Traffic Department warns of morning congestion when schools return ([Jordan News](https://www.jordannews.jo/Section-109/News/Comprehensive-Traffic-Security-Plan-for-the-New-School-Year-44249)). **No Amman figure exists for the share of peak trips that are school runs**, so impact can't be quantified.
- **Honest weaknesses:** route optimisation is real AI, but it doesn't feel magical. Carpool apps have a history of failing (Waze Carpool shut down in 2022). The impact numbers are weak.

| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 3 | 3 | 4 | 3 | 4 | 3 | **3.30** |

---

## Comparison (all round-6 solutions)
| Rank | Solution | Problem | Weighted | Main strength | Main risk |
|---|---|---|---|---|---|
| 1 | **C2: Najm for Jordan** | Traffic | **4.50** | Payer + measured proof abroad + full flow | Was set aside for wow |
| 2 | **B1: Ismaa'ni (3-min reading check + level groups)** | Reading | **4.40** | Hits the exact learning-poverty measure; no student devices needed; proven method (TaRL) | Child Arabic speech recognition accuracy |
| 3 | **A1: Bala Dukhan (WhatsApp quit coach)** | Smoking | **4.15** | Reaches the 99% the clinics miss; judge-participation demo | Quit bots exist abroad |
| 4 | A2: Quit-clinic & pharmacy copilot | Smoking | 3.85 | Institutional fit | Little stage wow |
| 4 | C1: Ishara (AI signals) | Traffic | 3.85 | Best visual demo | GAM already piloting; simulation only; weak "left out" |
| 6 | B2: Home read-aloud buddy | Reading | 3.70 | Easy UX | Google Read Along Arabic already exists |
| 7 | C3: School-run pooling | Traffic | 3.30 | — | Weak data and wow |

**Recommendation:** if the team wants a *new* direction, **B1 (Ismaa'ni)**. It's the cleanest match to the rubric: the biggest obvious problem, a measurable outcome (words correct per minute), proven method, AI that's essential, and a reach model that answers "who's left out". **A1** is the best second option and the most fun demo.
