# Idea H — "Najm for Jordan": Remote Minor-Accident Reporting with AI Pre-Assessment

> Team idea (from a teammate), researched and evaluated 2026-10-09. Working name: **Kroka Online / كروكتي** (rename freely).

**One-liner:** After a minor crash with no injuries, both drivers open the app instead of calling 911 and waiting at the scene. The app checks eligibility, guides them through photos, and asks each driver what happened. AI analyses damage and statements and proposes the **fault split with the rule it's based on**. A remote traffic officer approves it from a desk, the cars leave within minutes, and the report goes straight to both insurers.

## 1. What Najm is (the proof abroad)
- **Najm for Insurance Services** (Saudi Arabia) is owned by **26 shareholders, all licensed motor insurers**. It started as the inspector and liability assessor for minor accidents involving insured vehicles. It handles claims, determines liability and assesses damage. ([Al-Eqtisadiah, 3 May 2026](https://www.aleqt.com/%D8%A7%D9%84%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1/%D8%B1%D8%A6%D9%8A%D8%B3-%D9%86%D8%AC%D9%85-%D9%84%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A%D8%A9-%D8%A7%D8%B1%D8%AA%D9%81%D8%A7%D8%B9-%D8%A7%D9%84%D8%AD%D9%88%D8%A7%D8%AF%D8%AB-%D8%A7%D9%84%D9%85%D8%B1%D9%88%D8%B1%D9%8A%D8%A9-15-%D9%81%D9%8A-2025-%D9%88%D9%86%D8%A8%D8%A7%D8%B4%D8%B1-14-%D8%A3%D9%84%D9%81-%D8%AD%D8%A7%D8%AF%D8%AB-%D9%8A%D9%88%D9%85%D9%8A%D8%A7-9363))
- **Scale:** **10,000–14,000 accidents per day.** Average response is **45 min**, already cut to 20 min in some cases, with a new strategy target of **≤10 min**. Saudi accidents rose 15% in 2025. (same source)
- **Remote inspection "بلغ – صوّر – جنّب" (Report – Photograph – Move aside):** a General Traffic Department + Najm service. Drivers report in the Najm app, take guided photos, get an acceptance notice, then move the cars. Conditions: at least one party insured, **no injuries or deaths**, inside Najm's coverage area. ([Ajel](https://ajel.sa/local/traffic-launching-the-first-phase-of-the-remote-inspection-service-for-traffic-accidents), [Al-Muraba](https://www.almuraba.net/%d8%a7%d9%84%d9%85%d8%b9%d8%a7%d9%8a%d9%86%d8%a9-%d8%b9%d9%86-%d8%a8%d8%b9%d8%af-%d9%84%d9%84%d8%ad%d9%88%d8%a7%d8%af%d8%ab-%d8%a7%d9%84%d8%a8%d8%b3%d9%8a%d8%b7%d8%a9/))
- **Fault is given as percentages** (25 / 50 / 75 / 100%) by the investigator. Drivers can object within 10 days. ([Akhbaar24](https://www.akhbaar24.com/article/detail/474360), [Najm guide](https://giraffy.com/ksa/en/learn/insurance/car-insurance/najm-guide))
- Damage is valued separately by the **"Taqdeer" e-valuation programme** (Taqeem × Najm agreement), with no visit to a damage-assessment centre. ([Zawya](https://www.zawya.com/en/press-release/companies-news/taqeem-and-najm-sign-an-agreement-to-support-electronic-vehicle-damage-assessment-services-ta8qajfl))
- Najm publishes **fraud indicators** for staged accidents. ([Zawya](https://www.zawya.com/en/press-release/companies-news/najm-reveals-updated-criteria-and-indicators-for-detecting-insurance-fraud-in-traffic-accidents-vpby0ku4))

### Other countries doing the same thing
| Country | System | Evidence |
|---|---|---|
| UAE (Dubai) | Dubai Police app: minor-accident report **without waiting for a patrol**. An officer checks the data and sends the report to both drivers and insurers. **AI fault determination was announced at GITEX 2023** and has been in testing since (cuts steps from 7 to 4). | [Gulf News](https://gulfnews.com/uae/transport/dubai-soon-artificial-intelligence-will-analyse-and-send-traffic-accident-reports-1.98846127), [Dubai Media Office](https://mediaoffice.ae/en/news/2023/October/19-10/Dubai-Police-Implements-AI-in-Planning-and-Analysing-Traffic-Accidents), [100k+ app reports/yr](https://dubaieye1038.com/news/local/over-100000-minor-traffic-accidents-reported-via-dubai-police-app-this-year) |
| China | 交管12123 "事故视频快处" (video quick-handling). **Shanghai: all surface roads since 2024, avg 6 min per case.** Urumqi/Zhengzhou: remote officer decides liability by video, SMS result in under 10 min. Self-negotiation in-app for damage under ¥5,000. | [People's Daily 2026](https://cpc.people.com.cn/n1/2026/0205/c64387-40659869.html), [ifeng](https://news.ifeng.com/c/8ZlmQuuizNn), [The Paper](https://m.thepaper.cn/baijiahao_13871756) |
| Bahrain / Kuwait | Minor accidents reported via e-traffic app or the insurer. Kuwait allows fast settlement. | [GDN](https://www.gdnonline.com/Details/962113/Minor-traffic-accidents-to-be-handled-by-insurance-companies), [ME Insurance Review](https://www.meinsurancereview.com/Magazine/ReadMagazineArticle?aid=41269) |
| Global insurers | **Tractable** AI estimates repair cost from photos (GEICO, Tokio Marine, The Hartford, Covéa). Vendor claims ~3 min per appraisal. | [Tractable](https://tractable.ai/products/ai-estimating), [GEICO](https://tractable.ai/geico-partners-with-tractable-to-accelerate-accident-recovery-with-ai/) |

## 2. How it works in Jordan today
- **Process:** call 911 → **wait at the scene** for the traffic accident officer → the officer inspects the vehicles, hears statements and draws the **kroka (مخطط كروكي)** → insurers need the kroka to pay. ([gov portal service page](https://portal.jordan.gov.jo/wps/portal/Home/GovernmentEntities/Ministries/MinistryServiceDetails_ar/ministry+of+interior/public+security+directorate/services/obtain+an+electronic+kroke+chart?lang=ar&content_id=com.ibm.workplace.wcm.api.WCM_Content/Obtain), [Motory](https://jo.motory.com/ar/%D8%A7%D9%84%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/%D9%83%D9%8A%D9%81%D9%8A%D8%A9-%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D8%B9%D9%84%D8%A7%D9%85-%D8%B9%D9%86-%D8%AD%D8%A7%D8%AF%D8%AB-%D9%85%D8%B1%D9%88%D8%B1%D9%8A-%D9%88%D8%AA%D9%81%D8%A7%D8%B5%D9%8A%D9%84-%D9%86%D8%B8%D8%A7%D9%85-%D8%A7%D9%84%D9%83%D8%B1%D9%88%D9%83%D8%A9-%D9%81%D9%8A-%D8%A7%D9%84%D8%A3%D8%B1%D8%AF%D9%86-17710/))
- **⚠️ Jordan already has an "electronic kroka" (E-Kroka / ETARS).** It has existed since **Oct 2013**, built by the **Jordan Insurance Federation (JIF) + PSD**. The officer fills it **digitally in the field**, with GPS location, photos and vehicle data, and it feeds insurers directly. It was built to stop staged accidents and duplicate claims. A Palestinian delegation came to study it in **May 2026**. ([Ammon 2013](https://www.ammonnews.net/article/167241), [Sada News 2026](https://www.sadanews.ps/en/business/300610.html))
- **So the gap is not "digitise the kroka"; that's done.** The gap is: **an officer still has to physically come to every minor accident**, and drivers sit in traffic waiting. It's the same "patrol must attend" step that Saudi, Dubai and China have removed for minor cases.
- **Fault shares exist in Jordanian law:** under the compulsory motor insurance regulation, the insurer compensates **in proportion to the insured vehicle's contribution to the damage**, and courts deduct the victim's own share (e.g. 25%). (Legal summaries: [jordan-lawyer.com](https://jordan-lawyer.com/2022/05/07/%d9%85%d8%b3%d8%a4%d9%88%d9%84%d9%8a%d8%a9-%d8%b4%d8%b1%d9%83%d8%a7%d8%aa-%d8%a7%d9%84%d8%aa%d8%a3%d9%85%d9%8a%d9%86/), [lawpedia.jo](https://lawpedia.jo/?p=38242). **Verify against the current regulation (No. 12/2010 and amendments).**)

## 3. The problem in numbers
| Fact | Source |
|---|---|
| **187,213 accidents in 2025**, of which **11,680** caused injuries, which leaves **≈175,500 with no injuries (≈480/day)**. *(Subtraction is ours; the PSD category definitions aren't published in the summaries.)* | [Jordan News](https://www.jordannews.jo/Section-109/News/187-000-Traffic-Accidents-in-Jordan-in-2025-Result-in-510-Deaths-50151), [HPC](https://hpc.org.jo/en/node/42026) |
| **~91% of accidents happen inside cities**, where an immobilised car blocks traffic | same |
| ~160k cars enter Amman daily at peak hours | [Al Mamlaka](https://www.almamlakatv.com/news/105779) |
| Compulsory motor insurance (MTPL) is structurally loss-making: **JD 370M+ cumulative losses since 2001**, **4 insurers liquidated** | [Atlas Magazine](https://atlas-mag.net/en/articles/four-jordanian-insurance-companies-liquidated-0) |
| CBJ **refused an MTPL price increase in Feb 2025**. **MEICO is exiting motor insurance from 1 Jan 2026.** | [ME Insurance Review](https://www.meinsurancereview.com/News/View-NewsLetter-Article/id/91163/Type/MiddleEast) |
| **PSD warned (Aug 2024) of a rise in staged accidents** for insurance money | [Jordan Times](https://jordantimes.com/node/306165), [Roya](https://en.royanews.tv/news/53644) |

Insurers lose money on motor and can't raise prices, so **the only lever left is cutting the cost and fraud of handling claims.** That is exactly what a Najm-style system does, and why Saudi insurers built and own Najm.

## 4. Who's left out today ("society" sector question)
- Drivers stuck at the scene: anyone alone at night, the elderly, parents with kids in the car, drivers in peripheral areas where the officer takes longer.
- People pressured into **roadside cash settlements** with no record. Officials warn drivers not to pay people who say "the kroka is expensive" or "fault is obvious".
- **Everyone else on the road**, stuck in congestion behind two cars that legally can't move until the officer arrives.

## 5. What we'd build (11-hour MVP)
**Eligibility gate** (the "simple criteria"): no injuries · max 2 vehicles · both drivable · both drivers present and agree to use the app · both Jordanian-registered (compulsory insurance) · no government/diplomatic vehicle · no hit-and-run, no DUI suspicion. Anything else → "Call 911" (one tap).

**Flow:**
1. Driver A opens a case → **QR code** → Driver B scans and joins (Supabase Realtime keeps both phones in sync).
2. **Guided photo capture** of the scene, 4 corners per car, plates, damage close-ups. A vision model checks each photo live: plate readable? damage visible? correct angle? It re-prompts if not.
3. **Each driver answers separately** in Arabic (voice or text): what happened, direction, lane, signals. Then a **drag-and-drop sketch** (pick a scenario template: rear-end, lane change, roundabout entry, reversing, parking, junction).
4. **AI pre-assessment:**
   - Damage detection and severity per car (vision LLM, or a fine-tuned detector on a public car-damage dataset).
   - **Consistency check:** do the two statements contradict each other or the photos? (LLM, cites which sentence conflicts with which photo.)
   - **Fault suggestion:** maps the scenario to a **rulebook** built from Jordanian traffic law. Output is a split (e.g. 100/0, 75/25, 50/50) **plus the article/rule it relies on** and a confidence score.
   - **Fraud flags:** Najm-style indicators, e.g. damage inconsistent with the story, missing GPS/EXIF, same parties in previous cases (mocked history).
5. **Officer console (web):** queue of cases with photos, AI summary, suggested split → **approve / edit / call in**. *This is where the human decision stays; AI makes the officer 10× faster.*
6. Both drivers get the **kroka-style PDF** plus a "sent to insurer A/B" status (mocked integration with JIF / E-Kroka).

**Where AI adds real value:** photo quality control, damage reading, reconciling two Arabic-dialect statements, rule-based fault reasoning with citations, and fraud signals. A plain form can't do any of that. It's what turns "remote" from "officer looks at 30 photos" into "officer approves a pre-built case in 60 seconds".

**Data (fits the data rules):** synthetic, clearly labelled accident cases; a public car-damage image dataset (CarDD: 4,000 images / 9,000+ annotated damages, 6 classes, [arXiv](https://arxiv.org/pdf/2211.00945); check the licence, or use Roboflow CC-BY-4.0 sets); the traffic-law rulebook written by us from public law text; demo photos we take ourselves (toy cars or real dented cars in the HTU car park, with consent).

## 6. Evaluation

### Scorecard (1–5, official weights)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 5 | 4 | 5 | **4.50** |

This is the **highest score so far**, above every idea from round 1.

### Why it's strong
- **Big, measurable, everyday problem:** ≈175k non-injury accidents a year, almost all in cities. Every Jordanian driver has waited for a kroka or knows someone who has.
- **Proof abroad is excellent:** three independent systems (Saudi, Dubai, China) in production, with hard numbers (Shanghai 6 min/case; Najm 10–14k/day).
- **Clear owner and business model:** Najm is **insurer-owned**. The Jordanian equivalent is the **JIF**, which already co-built E-Kroka with PSD. Insurers lose money on motor, so they have a reason to pay. Business judge question ("who pays?") → insurers, per case, from claim-handling savings.
- **The integration point already exists** (E-Kroka database feeding insurers). We're the self-service front end plus AI triage, not a parallel system.
- **Demo is strong:** two phones, a QR join, live photo checks, the AI split appearing, the officer clicking approve, the PDF landing. That's a full story in about 3 minutes.
- **Our team fits:** a SWE for the two-party realtime app, and data scientists for vision, LLM reasoning and fraud scoring.

### Honest weaknesses / what judges will push on
1. **"Isn't this just copying Najm?"** Partly, and that's allowed: the hackathon rewards proven solutions applied to Jordan. **Our twists:** (a) AI pre-assessment is our default, while Najm/Dubai still mostly rely on human inspectors and Dubai's AI is only in testing; (b) built to plug into Jordan's existing E-Kroka, not to replace it.
2. **Legal authority:** a kroka is a PSD document, so a startup can't issue one. **Position it as a PSD × JIF remote-kroka service** (like Moroor × Najm). The officer approves; AI only recommends. Say this upfront in the pitch.
3. **AI fault accuracy:** keep to ~6–8 standard scenarios that cover most minor crashes. Always show the rule cited and a confidence score, and send low confidence to a human. Don't claim more.
4. **Fraud could increase** if nobody attends in person. Counter with fraud flags, mandatory live in-app camera (no gallery uploads), GPS/timestamp lock, and history checks.
5. **Sector fit:** it touches insurance (economy sector), but the core is a **PSD public service + mobility + congestion**, so it fits society. **Confirm with a mentor early.**
6. **Unknowns to check:** average kroka waiting time in Jordan (no official figure found; collect quotes from the team, family and taxi drivers on Day 1 as "data collected on the day"); whether any JIF/PSD remote pilot is already planned; current fees (only an old anecdote of a JD 5 paper report).

### Verdict
**Go, as the lead candidate.** It meets every filter we set (one painful moment, proof abroad, real Jordanian data, AI doing something a form can't, clear "who's left out", not on the crowded list). Keep the scope tight: **minor, two-car, no injuries, 6–8 scenarios, human-approved.**

## 7. 7-minute pitch outline
1. (45 s) A photo of two cars stopped on Mecca Street at 5 pm. "175,000 times a year."
2. (45 s) Saudi, Dubai and Shanghai already solved this. Jordan already has E-Kroka; only the "wait for the officer" step is left.
3. (3 min) **Live demo:** two phones → QR → guided photos → statements → AI split + rule → officer approves → PDF to insurers.
4. (1 min) What's real vs mocked (insurer/E-Kroka integration, case history).
5. (1 min) Business: JIF-owned like Najm; who pays; savings for insurers; fraud flags.
6. (30 s) Next step: a pilot with PSD Traffic + JIF on one district for minor accidents only.
