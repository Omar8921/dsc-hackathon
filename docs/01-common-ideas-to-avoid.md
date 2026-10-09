# Ideas Everyone Else Will Pitch (and why we skip them)

Method: we asked the same question other teams will ask an LLM ("AI app ideas for Jordan, smart society sector") and wrote down what comes back. Those ideas are the **crowded zone**. Expect several teams per idea, and judges who have already seen five of them by the time we present.

Rule for us: **if an idea fits in one line that every LLM gives, either drop it or find a sharp, data-backed angle that the generic version misses.**

## The predictable list

| # | Generic idea | Why it's crowded / weak for us |
|---|---|---|
| 1 | Arabic chatbot for government procedures ("which documents do I need?") | Literally the website's example. Also **Sanad already digitised ~80% of services (1,920 of ~2,400)**, has 500+ services in-app, 1.3M monthly users and 3.5M downloads. Hard to argue who's left out. |
| 2 | Water consumption predictor / leak detector / saving tips | Website's own example → many teams. Leak detection needs hardware data we won't have. |
| 3 | Bus tracker / route planner / wait-time estimator | Website example; the **Amman Bus app already does real-time arrival** for formal buses. |
| 4 | AI personal tutor / Tawjihi study assistant | Most common LLM idea there is. Hard to show impact in a 7-min demo. |
| 5 | Healthcare appointment booking / symptom-checker chatbot | Crowded and risky (medical advice). Hospitals are already rolling out appointment systems. |
| 6 | Medication / appointment reminder app | Low novelty; the AI isn't needed. |
| 7 | Sign-language translator (camera → text) | Very popular demo; hard to do well in 11 h; Jordanian Sign Language datasets are scarce. |
| 8 | Voice assistant for elderly / low literacy | Generic; it's a feature, not a product, unless it's tied to one specific service. |
| 9 | Recycling classifier (photo → which bin) | Classic CV demo. Jordan lacks sorted-waste infrastructure, so it solves nothing downstream. |
| 10 | Air-quality / heat dashboard | Data-viz with no action loop; the AI adds little. |
| 11 | Emergency / incident reporting app (photo + GPS → authorities) | Crowded. Jordan already runs nationwide E9-1-1 with caller location. |
| 12 | Volunteer ↔ NGO / donation matching platform | Every hackathon has one; the AI is cosmetic. |
| 13 | Smart parking finder | Needs sensors/data we don't have. |
| 14 | Mental-health chatbot | Crowded, sensitive, hard to validate. |
| 15 | Traffic congestion predictor | No open real-time data; Google Maps already does it. |
| 16 | Food-waste / leftover food sharing | Crowded, and arguably belongs to the economy sector. |
| 17 | Tourist guide chatbot | Economy sector, extremely common. |
| 18 | Job / skills-gap matcher for graduates | Economy sector's own example. |
| 19 | Complaint-routing AI for municipalities | Common "classify text → department" demo. |
| 20 | Smart-city "digital twin" dashboard | Too big; slides-only risk. |
| 21 | **AI personalised learning roadmap generator** ("tell me your level, get a plan") | Dozens of hobby versions (DevAtlas, Coders.sh, MindRoute, DeepLearning.AI tool…). Almost all are self-reported and text output. See [ideas/L](ideas/L-adaptive-learning-studio.md) for the non-generic version. |

## Patterns that make an idea generic
- "**Chatbot for X**", where the LLM is the whole product.
- A **dashboard** with no decision or action at the end.
- Problems where an **official app already exists** (Sanad, Amman Bus, JEPCO app, Hakeem).
- Needs **hardware/IoT or private data** we can't get within the data rules.
- Pitches impact as "raising awareness".

## What we want instead (filters for our own ideas)
1. **One specific, painful decision or moment** for one specific group in Jordan.
2. A **proof abroad**: someone has solved the same problem elsewhere (China, Saudi, UAE, India, Kenya, EU...) with measurable results.
3. **Public Jordanian data** exists to make it real on Day 1, not mocked.
4. The AI does something a form/website **can't** (predict, read a photo, reason over messy rules, speak dialect).
5. Clear answer to **"who is left out today?"**
6. Demo-able end-to-end in ~11 hours by 4 people.
