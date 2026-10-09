# Demo & Pitch Guide

## 1. What wins hackathons (patterns from recent podium projects)
Research on recent winners (TreeHacks, Cal Hacks, HackMIT, AI hackathons in 2025–2026):
1. **Visible transformation in seconds.** Judges see an input go in and something surprising come out, live.
2. **The AI uses a camera, a microphone or a sensor, or it generates something interactive.** Almost none of the winners is just a chat window.
3. **A specific human beneficiary**, specific enough that you can feel it.
4. **Judges can touch it.** The best demos let the judge try it on their own phone.
5. **One loop, fully working.** If a judge can't grasp the value from the opening screen, "you've already lost points" ([lablab guide](https://lablab.ai/guide/how-to-win-an-ai-hackathon)).
6. **Startup framing.** Judges score technology, presentation, business value and originality: "Think startup pitch, not benchmark run" ([lablab](https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii)).

**For us:** a **"whoa" moment in the first 60 seconds**, ideally with the **judges taking part** (scan a QR code, use their own phone or voice). The output should be **interactive**, not a wall of text.

## 2. Demo rules
- **Rehearse the exact click path** at least 3 times. Same phone, same account, same data.
- **Fallbacks for everything:** a recorded video of the full flow, cached data/results, a text input if voice fails, a hotspot if the Wi-Fi fails.
- **"Data collected on the day" is allowed and impressive:** e.g. a quick consented survey of attendees. Collect zone-level or anonymous data only.
- Large fonts and a zoomed-in UI on the projector. Mirror the phone screen.
- Don't demo login or settings. Start the demo already logged in at the interesting screen.

## 3. Pitch structure (7 minutes including the demo)
| Time | Part | Content |
|---|---|---|
| 0:00–0:45 | **Problem** | A personal story or vivid example + 2 sourced numbers. Who exactly suffers, and who is left out. |
| 0:45–1:15 | **What we built** | One sentence, plus the AI's role in one sentence. |
| 1:15–4:30 | **Live demo** | The full loop, with the "whoa" moment early. Judge participation if possible. |
| 4:30–5:30 | **Impact & business** | What changes for users (minutes, JD, reach); who pays; rollout. |
| 5:30–6:30 | **Honesty + tech** | Real-vs-mocked table; one metric; architecture in one picture. |
| 6:30–7:00 | **Next step / ask** | The pilot partner, the first users, and what proves it worked. |

**Pitch deck:** use the same brand as the app (logo, colours, fonts, product name, terms; see [04-brand-and-design.md](04-brand-and-design.md)), with screenshots matching the current UI. 8–10 slides max: title, problem (with sources), who's left out, solution, demo (live), how it works, real vs mocked, business, roadmap, team/ask.

## 4. "Real vs mocked" table (template; put it in the deck)
| Real (working live) | Mocked / synthetic (labelled) |
|---|---|
| e.g. AI pipeline running on live input | e.g. integration with the government system |
| e.g. data collected today with consent | e.g. city-wide data = synthetic |
| e.g. model with a held-out test metric | e.g. payments / notifications simulated |

## 5. Time plan (≈11 working hours)
| Phase | Goal |
|---|---|
| First 1–2 h | Scope locked; repo, stack and data sources ready; tasks split by person |
| By the mid-point | **One ugly end-to-end loop working** (input → AI → output on screen) |
| Middle | Improve the AI quality, then the Arabic UX; prepare the data and the demo scenario |
| ~2 h before the deadline | **Feature freeze.** Only fixes, demo polish, README, deck |
| Last hour | Rehearse ×3 with a timer, record the backup video, submit **before 1:00 PM** |

## 6. Final checklist before submitting
- [ ] Demo runs end-to-end on the demo device, plus a backup video recorded
- [ ] README: what it is, how to run it, the stack, what's mocked, data sources
- [ ] Repo pushed; secrets/API keys **not** committed
- [ ] Deck: problem with sources, who's left out, demo, real-vs-mocked, business, next step
- [ ] Arabic / RTL checked on every screen in the demo
- [ ] Brand consistency pass: the app, the deck and the README side by side show the same logo, colours, fonts, name, tagline and terms
- [ ] Synthetic data clearly labelled; no personal data without consent
- [ ] Answers ready for the 10 Q&A questions in [01](01-judging-playbook.md)
- [ ] Pitch timed under 7:00
