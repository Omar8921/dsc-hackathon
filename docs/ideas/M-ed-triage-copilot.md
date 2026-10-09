# Idea M — ED Triage Copilot ("Farz / فرز"), Guardian adapted for Jordan

**Inspiration:** "Guardian" won 1st place (AI Hackathon Hamburg 2026, [winners](https://ai-beavers.com/hackathon/winners)). It is an AI assistant for NHS emergency departments: symptom intake, AI-assisted risk assessment, intake organisation, and multilingual patient communication, framed as decision support rather than a clinician replacement.

**Our take on why it won:** it lives inside a real, painful workflow; it's explicitly *decision support* (credible with clinical judges); and the demo is a single person walking through the door, which is easy to follow.

**What changes for Jordan:** language barriers matter less (most patients speak Arabic). What Jordan has instead is **crowded public EDs, patients who don't understand triage, and violence against staff**. So the Jordanian version has *two faces*: one for the nurse and one for the waiting family.

## Problem in Jordan
- **9.16M ED visits in MoH public hospitals 2018–2023 (~1.5M/yr); only 6.37% were admitted.** The large majority are lower-acuity. ([Int J Emerg Med 2025](https://intjem.biomedcentral.com/articles/10.1186/s12245-025-00952-x))
- Seasonal surges: **113,000 ED visits in 36 days**, 77,000 of them respiratory. ([Jordan News](https://www.jordannews.jo/Section-109/News/113-000-patients-visited-Jordan-emergency-departments-in-36-days-25702))
- **61.3% of patients in large public hospitals don't know a triage system exists** (n=726, 2024). To them, triage looks like queue-jumping. ([Emergency Care Journal 2024; verify it's the n=726 study](https://doaj.org/article/dc81b2be5e494c32be30250c09fbc796))
- **63.1% of Amman doctors were exposed to violence in the past year** (n=969). Public-sector doctors were the most affected. ([PLoS ONE 2021](https://doaj.org/article/f06528e985304743b4fb0589610c0df7)) In a 2023 study, 33% of staff faced physical and 53% verbal violence. ([MDPI 2023](https://www.mdpi.com/1660-4601/20/4/3675)) The JMA and unions say **most assaults happen in emergency departments** and cite heavy loads and too few staff. ([Jordan News](https://www.jordannews.jo/Section-109/News/Assaults-on-Medical-Staff-Drop-by-Half-Since-2016-But-Doctors-Say-Problem-Persists-54922), [Jordan News 2023](https://www.jordannews.jo/Section-109/News/12-cases-of-assault-on-doctors-and-nurses-in-2023-30662))
- Hakeem (EHS) connects **482 MoH + RMS facilities** (July 2026), so there's an integration target. ([Petra](https://www.petra.gov.jo/en/news/hakeem-system-expands-to-cover-482-healthcare-facilities-so-far-ceo))

## Evidence that AI triage support works
- **KATE** (US, retrospective, 166k encounters): correct ESI level **75.9% vs triage nurses 59.8%**. At the critical ESI 2/3 boundary: **80% vs 41.4%**. ([arXiv 2004.05184](https://arxiv.org/pdf/2004.05184))
- **NEJM AI, 3 EDs, before/after:** sensitivity for critical patients rose from **78.8% to 83.1%**, and arrival-to-care-area time fell by ~4 min. Nurses kept final authority, and the tool showed a rationale. ([secondary summary; find the NEJM AI paper before citing](https://www.2minutemedicine.com/?p=81873))
- **Warning:** general LLMs used alone make *unsafe* triage decisions ([medRxiv meta-analysis](https://www.medrxiv.org/content/10.1101/2024.05.20.24307543.full.pdf)). So **the LLM extracts and the rules score.** We never let a chatbot decide acuity.

## What makes it unique
1. **Dialect voice intake:** a patient or companion speaks Jordanian Arabic ("صدري بيوجعني من ساعة وإيدي الشمال تنمّل"). The LLM extracts structured findings (chief complaint, onset, red flags), and **validated rules (CTAS/ESI-style plus red-flag lists) produce the level.**
2. **Safety rule: the AI can only *escalate*, never lower,** a nurse's level. It flags what the nurse might have missed.
3. **Family-facing transparency:** a screen or SMS saying "You are category 4 (green). Two critical patients arrived ahead of you. Estimated wait ~40 min. If X gets worse, tell the nurse." This tackles the anger-and-violence loop directly. No product we found does this.
4. **Smart redirect:** low-acuity patients get the nearest open MoH health centre or a telemedicine option, which takes load off the ED.
5. **English handover note** for the doctor, auto-generated from the Arabic intake (doctors chart in English).

## MVP (11 hours)
- **Intake kiosk (tablet web app):** voice or text in Arabic, plus vitals typed by the nurse.
- **Scoring engine:** LLM → JSON findings → rule table → level + reasons + red flags.
- **Nurse dashboard:** live queue sorted by level and waiting time, one-click confirm or override (Supabase Realtime).
- **Family screen / SMS:** anonymised queue position + plain-Arabic explanation.
- **Doctor handover card** in English.
- **Validation slide:** agreement with expert levels on ~40 public/synthetic triage vignettes (e.g. ESI-handbook-style cases), measured by us.
- Mocked: Hakeem integration, real patient data (synthetic only, per the rules).

**Demo wow:** a judge (or teammate) role-plays a patient in Arabic at the kiosk. They're instantly flagged red, the queue on the big screen re-orders live, and the "family screen" updates with an explanation. Then a low-acuity case is redirected to the nearest health centre.

## How it makes money
- **Private hospitals first** (they compete on ED experience and serve medical tourists, where the multilingual feature from Guardian is valuable again): SaaS per ED per month or per triage.
- **MoH / Royal Medical Services:** a tender via EHS/Hakeem integration. Value to them: staff safety, throughput, fewer complaints.
- **Insurers / TPAs:** fewer avoidable ED claims through redirection.

## Scorecard
| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 5 | 4 | 5 | **4.50** |

## Risks
- Medical-safety scrutiny from the domain judge: keep decision support only, escalate-only, show the rules, and report measured agreement.
- Which triage scale Jordanian EDs actually use (CTAS vs ESI vs local): check with a mentor or doctor on Day 1.
- No real patient data allowed: role-play and synthetic vignettes only.
