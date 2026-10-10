# Crown Prince Award winners vs our sector

Source: [cpa.jo](https://cpa.jo/home), the Crown Prince Award for Best Government Services Application (MoDEE + Crown Prince Foundation, for university students). The winners list comes from the site's own API (`/backend/api/portal/winners`): **19 winners across 4 editions** (2019, 2020, 2023, 2024). The 5th edition's winners will be announced on 15 Oct 2026, after our hackathon.

Why it matters: these are Jordanian **government** judges rewarding student apps for public services, which is almost exactly our sector. The list shows what they already reward, and what our judges may already have seen.

## All winners, sector fit

| Ed. | Rank | App | What it does (short) | Fits `next.society()`? |
|---|---|---|---|---|
| 1st (2019) | 1 | Khadamaty | Water/electricity bills + bill objection backed by a meter photo | ✅ public services |
| 1st | 2 | SOS Jo | Distress call with location + medical profile, auto-SMS to family | ✅ emergency (crowded, E9-1-1 exists) |
| 1st | 3 | Vaccines JO | National vaccination schedule, info, campaigns | ✅ health service (reminder app) |
| 2nd (2020) | 1 | Nabad | Organ/blood donation platform linking donors, banks, hospitals | ✅ health / inclusion |
| 2nd | 2 | Farm Jo | Crop production/consumption statistics for MoA | ❌ economy / agriculture |
| 2nd | 3 | دوائي | E-pharmacy: drug info, dose schedule, talk to doctor | ⚠️ health (crowded) |
| 3rd (2023) | 1 | سياحولوجيا | Interactive heritage experiences + tourist chatbot | ❌ tourism / economy |
| 3rd | 2 | مسار | University and major choice helper | ✅ education (= our rejected Idea A) |
| 3rd | 3 | زراعتي | Farmer data + decision support | ❌ agriculture / economy |
| 4th (2024) | 1 | Diente | Matches dental students needing clinical cases with patients who can't pay | ✅ health access / inclusion |
| 4th | 2 | Daleelak | AI assistant for government-service documents, steps and fees | ✅ but crowded (#1 on our avoid list; Sanad) |
| 4th | 3 | SustainMate | Sustainable building-material picker for engineers, AI impact scores | ⚠️ environment, but B2B for engineers |
| 4th | 4 | Badir | Infrastructure reports with AI photo analysis + citizen voting | ✅ smart city (crowded pattern) |
| 4th | 5 | MEDSHARE | Donating unexpired medicine, expiry checks | ✅ health / waste (JFDA rules are a risk) |
| 4th | 6 | صوتك | Citizen voting/suggestions + AI opinion analysis | ✅ community engagement |
| 4th | 7 | طريقك | Real-time accident reporting: location + vehicle info | ✅ transport / safety (**overlaps our H**) |
| 4th | 8 | Mafqodat | AI search and classification of lost items | ✅ public services |
| 4th | 9 | Creative Lab | Virtual chemistry lab for schools without labs | ✅ education |
| 4th | 10 | أمن النشامى | Report incidents, traffic violations, cybercrime | ✅ safety (crowded) |

**16 of 19 fit our sector; 3 are economy/agriculture/tourism.**

## Patterns in what wins
1. **AI is now expected.** 6 of the 10 4th-edition winners mention AI; none of the 2019–2020 winners do. An app with no AI would look dated to this panel.
2. **The top prizes solve two problems at once.** Diente (1st, 4th ed.) fixes students' clinical-training gap and poor patients' dental costs in the same match. Nabad (1st, 2nd ed.) links donors, banks and hospitals.
3. **"Report X to the authorities" apps win, but rank low.** Badir 4th, طريقك 7th, أمن النشامى 10th, SOS Jo 2nd in 2019. Reporting alone is table stakes; it has to *resolve* something.
4. **Chatbot for gov services still placed 2nd** (Daleelak), so judges like it, but every team will pitch it at our hackathon.

## Each aligned winner scored as *our* AI-hackathon project
Scores 1–5 on our rubric (Impact 25%, Innovation 20%, Feasibility 20%, Tech 15%, UX 10%, Pitch 10%). This assumes we build our own improved AI version in 11 h. A straight copy would score lower on Innovation, because these already won in Jordan.

| Winner → our version | Imp | Inn | Feas | Tech | UX | Pitch | **Weighted** |
|---|---|---|---|---|---|---|---|
| **طريقك → H: Najm for Jordan** (remote, AI-pre-assessed kroka; see [H3](ideas/H3-najm-wow-revenue-training.md)) | 5 | 5 | 4 | 5 | 4 | 5 | **4.70** |
| Diente → + AI case triage (patient photo + dialect symptoms → case type → the student who needs that case for their quota) | 4 | 3 | 4 | 3 | 4 | 4 | 3.65 |
| Khadamaty → AI meter-photo reading + bill anomaly + auto-written objection | 3 | 3 | 4 | 4 | 4 | 3 | 3.45 |
| Mafqodat → image-embedding lost-and-found | 2 | 3 | 5 | 4 | 3 | 3 | 3.30 |
| Badir → photo-classified infrastructure reports | 3 | 2 | 4 | 4 | 3 | 3 | 3.15 |
| مسار → admission planner (our Idea A) | 3 | 2 | 4 | 3 | 4 | 3 | 3.10 |
| Nabad → donor matching | 4 | 2 | 3 | 2 | 3 | 4 | 3.00 |
| Creative Lab → virtual lab | 3 | 2 | 3 | 3 | 4 | 3 | 2.90 |
| MEDSHARE → medicine donation + OCR expiry | 3 | 2 | 3 | 3 | 3 | 3 | 2.80 |
| Daleelak → gov-services chatbot | 2 | 1 | 5 | 3 | 4 | 2 | 2.75 |
| صوتك → participation + opinion analysis | 2 | 2 | 4 | 3 | 3 | 2 | 2.65 |
| SOS Jo → distress call | 3 | 1 | 4 | 2 | 3 | 2 | 2.55 |
| أمن النشامى → incident reporting | 3 | 1 | 4 | 2 | 3 | 2 | 2.55 |
| SustainMate → material picker | 2 | 2 | 3 | 3 | 3 | 2 | 2.45 |
| Vaccines JO → vaccine tracker | 2 | 1 | 5 | 1 | 3 | 2 | 2.35 |
| دوائي → e-pharmacy | 2 | 1 | 4 | 2 | 3 | 2 | 2.30 |

These are our team's judgement calls, not data. The impact scores need sources before they go in a pitch.

### Best per edition
- **1st (2019): Khadamaty.** A real AI hook (read the meter photo, flag the anomaly, draft the objection). Overlaps our Idea C, and the JEPCO app exists.
- **2nd (2020): Nabad.** The only strong society fit, but matching platforms are on our avoid list (#12).
- **3rd (2023): مسار.** The only society fit, and it is our already-rejected Idea A.
- **4th (2024): طريقك**, because it is the bare-bones version of our lead H. Runner-up: **Diente**.

## So what for us
- **Keep H (Najm for Jordan).** طريقك shows Jordanian government judges already value accident reporting, and its 7th place shows reporting alone isn't enough. H goes further: no officer on site for minor accidents, an AI-drawn kroka, fault split with a law citation, and a revenue model.
- **Pitch line:** "طريقك reports the accident. We close it in 10 minutes without a patrol." Expect a judge to ask how we differ from it; that's our answer.
- **Backup if H is rejected:** Diente + AI case triage. It hits pattern #2 (two problems in one match), has a clear "who is left out" (people who can't afford dental care), and builds fast. The risk is that it already won 1st place locally, so the AI triage has to be the headline.
