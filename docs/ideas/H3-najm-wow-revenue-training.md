# Idea H (part 3): Najm for Jordan: the AI wow feature, the revenue model in plain words, and how we train the models

Companion to [H](H-najm-for-jordan.md) and [H2](H2-najm-ai-and-business-model.md). Written 2026-10-09 (round 7).

---

## 1. The wow feature: "AI draws the kroka" (accident reconstruction)

A kroka is *literally a drawing*: an officer looks at the cars, listens to both drivers and sketches what happened. So the obvious AI moment is: **the AI draws the kroka.**

**Input (collected on two phones in under 2 minutes):**
- Guided photos of both cars (where the damage is: car A rear-left, car B front-right).
- Each driver's **voice statement in Jordanian Arabic**, recorded separately.
- GPS location.

**What the AI produces in ~30 seconds:**
1. **An animated top-down reconstruction on the real street.** It pulls the road geometry (lanes, roundabout, junction) at the GPS point from OpenStreetMap and plays the two cars' paths up to the point of impact.
2. **An auto-drawn kroka sketch** in the official style (vehicle positions, directions, impact point, lane markings), ready for the officer to approve.
3. **Contradiction detection across evidence:** *"Driver B says he was stopped, but the damage is on B's front bumper and is consistent with forward movement."* It shows which sentence conflicts with which photo.
4. **Fault split plus the law it relies on** (e.g. 75/25 with the traffic-law article), with a confidence score.

**Why this is the right wow:**
- It's **visual, instant, and obviously impossible without AI**: it combines vision (damage location), speech/LLM (dialect statements), map data and legal reasoning into one picture.
- It's **exactly the job a human officer does today**, so judges immediately get it.
- It's the moment the room says "whoa": a scattered set of photos and voice notes becomes an animated replay of the crash.

**It's real abroad, but not in Arabic or Jordan:**
- **Liablix** (Italy, funded Dec 2025): photos of damaged vehicles → 3D reconstruction of the dynamics and responsibility, for insurers and fraud detection. ([StartupBusiness](https://www.startupbusiness.it/en/wp-json/wp/v2/posts/148639), [WebCatalog](https://webcatalog.io/en/apps/liablix))
- **Nexar**: dashcam-based automatic accident reconstruction plus an AI-written collision timeline, deployed with Mitsui Sumitomo Insurance. ([Nexar](https://data.getnexar.com/blog/nexar-releases-first-ever-ai-vision-technology-to-reconstruct-car-accident-scenes))
- **SkyeBrowse**: crash-scene 3D diagrams for police and insurers. ([SkyeBrowse](https://www.skyebrowse.com/crush-claims))
- **Research, 2026:** **TrafficRAG** (vision-language model describes the scene → retrieves traffic regulations and similar cases → LLM writes a legally grounded liability report; **liability-ratio error ≈5.5 percentage points**) ([arXiv 2606.01737](https://arxiv.org/pdf/2606.01737)); **AITP**, responsibility allocation with multimodal LLMs (CVPR 2026 Findings) ([arXiv 2604.20878](https://arxiv.org/pdf/2604.20878)); responsibility-percentage prediction benchmark ([arXiv 2607.03591](https://arxiv.org/abs/2607.03591)).

**How we build it in 11 hours (honest version):**
- **8 scenario templates** (rear-end, lane change, roundabout entry, junction right-of-way, reversing, parking-lot, U-turn, side-swipe), each a parameterised animation (lanes, directions, speeds, impact points).
- The LLM reads the evidence (damage locations from vision + both statements + road type) → picks the scenario and fills the parameters as **typed JSON** → a deterministic renderer animates it (SVG/Canvas over Leaflet + OpenStreetMap).
- Say this clearly on the honesty slide: **"template-based reconstruction from evidence, not a physics simulation."**

**The stage demo:** two toy cars on a printed map of a real Amman roundabout (e.g. 7th Circle). We crash them, two teammates (or a judge) take the guided photos and record voice statements, **one of them lying**. About 30 seconds later the screen shows the replay on the real roundabout, the auto-drawn kroka, the contradiction flag, and the fault split with the law. The "officer" clicks approve and the report goes to both insurers.

---

## 2. All AI features (what each one is, and whether it's trained, pretrained or rules)
| # | Feature | What it does | How it works | Trained by us? |
|---|---|---|---|---|
| 1 | **Guided capture + photo QA** | Live check that each required angle, the plate and the damage are visible, and no gallery uploads | Vision model + simple checks (blur, angle, plate readable) | No (pretrained) |
| 2 | **Damage detection** | Which part (bumper, door, lamp), what damage (dent, scratch, crack, glass), severity | **YOLOv8-seg fine-tuned on public datasets** + vision-LLM as a second opinion | **Yes** (see §4) |
| 3 | **Statement understanding** | Turns two dialect voice notes into structured facts (direction, lane, speed, signal, "I was stopped") | Arabic speech-to-text + LLM → JSON | No (pretrained) |
| 4 | **Contradiction detection** | Flags where statements disagree with each other or with the damage | LLM reasoning over facts + damage locations | No (prompted, evaluated by us) |
| 5 | **⭐ Reconstruction + auto-kroka** | Animated replay on the real street + official-style sketch | LLM picks scenario/params → template renderer + OpenStreetMap | No (rules + LLM) |
| 6 | **Fault split with legal citation** | 100/0, 75/25, 50/50 + the article it relies on + confidence | Retrieval over Jordanian traffic-law text + LLM (TrafficRAG-style); the officer approves | No (rules + retrieval); evaluated on our test cases |
| 7 | **Repair estimate range** | JD range per car | Damaged parts × severity × parts/labour price table | No (lookup table) |
| 8 | **Fraud signals** | Old damage/rust, story-damage mismatch, repeat plates/people, location/time anomalies | Rules + model scores; history mocked | Partly |

**The only model we actually train in the hackathon is #2.** Everything else uses strong pretrained models with structured outputs, rules and retrieval. That's the right engineering choice, and we should say so.

---

## 3. The revenue model in plain words
> **Drivers never pay. Insurers pay a fee for every accident we process, like a card network takes a fee per payment.** At scale it becomes a small fee per insurance policy, which is exactly how Najm works today.

### Why insurers pay (the chain of money)
1. Every minor accident becomes an insurance claim, and **insurers pay out ~JD 261M a year in motor claims against ~JD 272M of premiums** (≈96%). Motor insurance loses money, 4 insurers were liquidated, and the Central Bank won't let them raise prices. (Sources in H/H2.)
2. Each claim currently costs the insurer an officer kroka + a surveyor visit + days of back-and-forth + whatever fraud and overpriced repairs slip through.
3. We hand them a **complete, AI-checked case file in minutes**: photos, damage, estimate range, fraud flags, an approved kroka. That cuts surveyor work, leakage and fraud.
4. **They pay us a per-case fee that is smaller than what each case saves them.** That's the whole business.

This is **standard in insurtech, not a weird model**: Tractable charges insurers per AI estimate; **Najm itself earned >95% of its revenue per accident** before switching (with central-bank backing) to a per-policy fee, reaching **SAR 750M revenue in 2021**. ([Argaam](https://argaam.com/en/article/articledetail/id/1592427))

### Revenue streams, in order
| Stream | Who pays | Model | Illustrative size *(assumptions, label on slide)* |
|---|---|---|---|
| **1. Per-case processing fee** | Insurers (or JIF on their behalf) | JD 4–6 per processed accident | ≈175k non-injury accidents/yr × 50% adoption × JD 5 ≈ **JD 0.4–0.5M/yr** |
| **2. Per-policy platform levy** (phase 3, Najm's current model) | All motor insurers via JIF | ~JD 1 per policy per year | ~1.8M vehicles × JD 1 ≈ **JD 1.8M/yr** (replaces stream 1) |
| **3. Repair & towing network** | Insurer-approved garages, tow operators | Referral commission on jobs routed by the app | e.g. 50k jobs × JD 300 avg × 8% ≈ **JD 1.2M/yr** |
| **4. Data & analytics** | Insurers (risk pricing for comprehensive cover), GAM/PSD (accident hotspots) | Annual licence | Small at first |
| **5. Regional licensing** | Insurance federations / regulators in nearby markets | Platform licence | **The Palestinian Capital Market Authority sent a delegation to Jordan in May 2026 specifically to learn the E-Kroka system** ([Sada News](https://www.sadanews.ps/en/business/300610.html)), so neighbouring demand is real. Iraq, Palestine and others follow. |

**Honest sizing:** Jordan alone is a **JD 2–4M/yr** business at maturity, with software margins. That's real, but the bigger prize is being the regional "Najm-as-a-platform" for markets without one.

**Price justification for the business judge:** insurer savings were estimated in H2 at ≈JD 2.7M/yr from leakage and fraud alone (1% of motor claims), before surveyor time. Our fee is below that, so the deal makes sense for them on fraud and leakage alone.

---

## 4. How we train the damage model (and where the real data comes from)

### For the hackathon (Day 1, runs in parallel with app building)
Public, labelled datasets already exist. **We don't need crash photos from Jordan to show a working, measured model:**

| Dataset | Size | Labels | Licence |
|---|---|---|---|
| **CarDD** (USTC, 2022) | 4,000 images, 9,000+ instances | dent, scratch, crack, glass shatter, lamp broken, tire flat (classes from Ping An Insurance statistics) | check on cardd-ustc.github.io ([arXiv](https://arxiv.org/pdf/2211.00945)) |
| **VehiDE** (2023) | 13,945 images, ~32k instances, 8 damage classes | detection + segmentation | check before commercial use ([DOAJ](https://doaj.org/article/6e0eb600059440b390431a42dfe8d138)) |
| **Humans-in-the-Loop Car Parts & Damages** | 1,812 images (parts + damage polygons) | 8 damage classes + car parts | **CC0, public domain** ([HITL](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/)) |
| **Pixemantic Vehicle Damage-29** | ~5,200 images, 29 classes (parts + damage) | segmentation | check ([IEEE DataPort](https://ieee-dataport.org/documents/pixemantic-vehicle-damage-29)) |
| Roboflow Universe car-damage sets | 2k+ images each | segmentation | many CC-BY-4.0, verify per set |

**Plan:** fine-tune **YOLOv8-seg** on CarDD/VehiDE plus the CC0 parts set on a cloud GPU (Colab/Kaggle) for a couple of hours. Report **mAP on the held-out test split**, which is our honest accuracy number for the slide. Add a **"which car part"** head from the parts datasets so damage maps onto "front bumper / left door". Use a vision-LLM as a second opinion for anything the detector is unsure about.

### For production: the dataset already exists in Jordan
- **E-Kroka has run since 2013** (JIF + PSD). Officers attach **photos, a sketch and the at-fault decision** to every report, and insurers attach the **final settled amount**. That's **13 years of labelled data**: photo → damage, sketch → scenario, decision → fault %, settlement → repair cost. ([Ammon 2013](https://www.ammonnews.net/article/167241))
- **A data-sharing agreement with JIF** (anonymised: plates and faces blurred) is how the production models get trained on Jordanian cars, streets and garages. It's also the moat no competitor can copy.
- **Data flywheel:** every officer approval or override and every adjuster's final invoice becomes a new label, so the models improve with use.

### Fault % is *not* trained on crash photos
It's **retrieval over the traffic law plus LLM reasoning over structured facts**, which is the TrafficRAG approach (≈5.5-point liability-ratio error in research). For the hackathon we evaluate it on ~30 synthetic scenarios with expected answers written by us from the law text.

---

## 5. Updated scorecard (with the reconstruction wow)
| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 5 | **5** | 4 | 5 | 4 | 5 | **4.70** |

Innovation goes 4 → 5: auto-reconstruction plus contradiction detection plus an Arabic-dialect auto-kroka is new for Jordan and the region, and isn't just "copy Najm". The other scores are unchanged from H.
