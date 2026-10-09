# Idea I — Cardiac-Arrest Community Responder + AI CPR Coach ("Nabd / نبض")

**One-liner:** When someone collapses, the app (1) alerts CPR-trained volunteers within ~500 m and points them to the nearest AED, and (2) turns any bystander's phone into a **live CPR coach**. The camera watches the compressions (pose estimation) and a voice says in Jordanian Arabic "faster… good… push harder… keep going, the ambulance is 4 min away".

Sector fit: Safety & emergency response + community engagement.

## Problem in Jordan
- Estimated **out-of-hospital cardiac arrest survival in Jordan ≈ 3% (2.97%)**. This is a secondary citation inside a 2023 Jordanian BLS paper, so trace the primary source before using it on a slide. ([PMC10770436](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10770436/))
- Only **29%** of surveyed adults (n=300, north/middle/south) had any CPR training. ([PMC6206630](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6206630/)) Only 24.9% of *medical students* knew correct hand position. ([PMC10770436](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10770436/))
- Civil Defence response averages about **6.7 min urban / 11 min rural** in the northern governorates. Amman rush hour is worse. ([SWOV](https://swov.nl/en/publicatie/emergency-medical-service-rescue-times-road-accident-casualties-jordan), [Jordan Times](https://jordantimes.com/node/283660)) Brain damage starts within minutes without CPR.

## Proof abroad
- **Singapore myResponder** (9,167 cases): activation was associated with bystander CPR aOR 5.69, AED use aOR 2.23, and better 30-day neurologically-intact survival aOR 1.54. These are observational results; an earlier analysis was more mixed. ([PubMed 40383504](https://pubmed.ncbi.nlm.nih.gov/40383504/), [Annals SG 2021](https://www.annals.edu.sg/pdf/50VolNo3Mar2021/V50N3p212.pdf))
- **Europe, 5 sites (JACC 2023):** volunteer alerts gave bystander CPR 73.8% vs 61.9%, defibrillation 7.9% vs 4.6%, and 30-day survival 12.4% vs 10%. ([ACC](https://www.acc.org/Latest-in-Cardiology/Articles/2023/07/13/17/47/Activating-Volunteer-System-Increases-Bystander-CPR-AED-Use-and-Improves-Survival))
- **UK GoodSAM:** survival was about twice as likely when an alert was sent. ([NIHR](https://evidence.nihr.ac.uk/alert/more-people-survived-cardiac-arrest-first-aiders-goodsam-alert/))
- **Camera CPR feedback works on manikins:** a smartphone camera measured compression rate with an average error of 2.7/min and was within ±10/min 98% of the time ([PMC6277120](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6277120/)). MediaPipe pose tracking worked in 9/9 videos. App feedback improved rate, hand position and recoil for bystanders, but not depth ([Resuscitation 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC4982121)).

## MVP (11 h)
Volunteer registry + geo-alert (Supabase + PostGIS; volunteers simulated). AED map (seeded with a few real ones we find, labelled). **CPR coach:** browser/phone camera → MediaPipe Pose → wrist vertical oscillation → compressions per minute → Arabic voice feedback (TTS) and a metronome at 110/min. Post-event summary for the paramedic.

**Live demo:** one of us does CPR on a pillow on stage while the phone coaches in Arabic. That's a memorable moment.

## Scorecard
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 4 | 5 | **4.25** |

## Risks
- **Volunteer network chicken-and-egg:** it needs Civil Defence dispatch integration to be real. The AI coach is useful on its own.
- Jordan OHCA counts per year aren't public (the survival % comes from one citation chain).
- Medical liability: frame it as "dispatcher-assisted CPR, on your phone", following AHA/ERC guidance.
- Camera depth estimation is weak, so promise only rate and rhythm feedback.
