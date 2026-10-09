# Idea N — Arabic Ambient Clinic Scribe ("Katib / كاتب")

**One-liner:** The doctor taps record. The consultation happens in Jordanian Arabic mixed with English medical terms. When it ends, the app produces (1) a structured clinical note in English ready for Hakeem, (2) a draft prescription and referral, and (3) a **take-home summary for the patient in simple Arabic, with audio**, so low-literacy patients don't forget the instructions.

## Problem in Jordan
- MoH runs **1,245 primary-care centres and 27 hospitals**, and Hakeem now spans **482 facilities**, so doctors type into an EHR all day. ([Wikipedia: Health in Jordan](https://en.wikipedia.org/wiki/Health_in_Jordan), [Petra](https://www.petra.gov.jo/en/news/hakeem-system-expands-to-cover-482-healthcare-facilities-so-far-ceo))
- Consultations are in **dialect + English code-switching**. Global scribes are built English-first. *We found no scribe for Jordanian dialect; verify.*
- Patients leave with verbal instructions they can't read back; literacy and elderly gaps (see the learning-poverty figures in idea L).

## Proof abroad
- **Kaiser Permanente (TPMG):** ambient AI scribes over **2.5M encounters** in the first year, about **15,791 hours of documentation saved**, with better patient interaction and doctor satisfaction (NEJM Catalyst). ([AMA](https://www.ama-assn.org/practice-management/digital-health/ai-scribes-save-15000-hours-and-restore-human-side-medicine))
- JAMIA 2025: about **20 min/day** less EHR time per physician. ([Healio summary](https://www.healio.com/news/rheumatology/20260113/ai-scribes-hold-transformative-potential-for-improving-physician-burden-patient-care))

## MVP
Record → Arabic speech-to-text (Whisper/other) → LLM → SOAP note (EN) + ICD-10 suggestions + prescription draft + patient summary (AR text + TTS audio) → the doctor edits and approves. Demo: two teammates role-play a 2-minute consult on stage and the note appears.

## Money
Per-doctor subscription for private clinics and hospitals; EHS/Hakeem integration deal for the public sector.

## Scorecard
| Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 4 | 5 | 4 | 4 | 4 | **4.20** |

## Risks
"AI scribe" is getting common globally, so dialect handling is the whole moat and needs to be shown live. Patient-consent framing is needed. The demo uses role-play only.
