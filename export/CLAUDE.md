# CLAUDE.md

Context for AI assistants (Claude Code etc.) working with our team. Shared by a 4-person team, so keep it accurate.

## The event
**AI Quest 2026, Future Jordan Hackathon** (HTU, 9–10 Oct 2026), sector **`next.society()` (Smart Society & Public Services)**.

- Hard deadline: **submit by 1:00 PM, 10 Oct 2026**. Pitch: **7 min presentation + demo, then 3 min Q&A**, from 1:30 PM.
- About **11 working hours** in total. "A small idea that works live beats a big one in slides."
- Judging: Impact on Jordan 25%, Innovation 20%, Feasibility & Scalability 20%, Technical Implementation 15% (working demo + **honesty about what's mocked**), UX 10% (**Arabic where relevant**), Pitch 10%.
- Data rules: public data, data collected on the day, or **clearly labelled synthetic** data. **No real personal data without consent.**

Full brief: [00-hackathon-brief.md](00-hackathon-brief.md). How to score well: [01-judging-playbook.md](01-judging-playbook.md). Demo and pitch: [02-demo-and-pitch-guide.md](02-demo-and-pitch-guide.md).

## Team
4 people: 3 AI / data-science students (one is an AI researcher; two have industry experience at PwC and Amazon) + 1 computer-science student / software engineer.

## Stack
**Not decided yet.** Whatever we choose must:
- Support **Arabic / RTL** in the user interface.
- Let us ship a working demo fast (prefer managed services and well-known tools the team already knows).
- Keep the AI meaningful: **it must do something a plain form or website can't.**

Once the stack is chosen, record it here (frontend, backend, database, AI/ML, hosting) so every assistant uses the same tools.

## How to write code
**Follow [03-engineering-guide.md](03-engineering-guide.md) for every coding task.** In short: read the existing code first and reuse what's there, ask the key questions, plan before executing, build in small verified steps, never swallow errors, test what you change, keep secrets server-side and enforce permissions on the server, and report honestly what's done and what's mocked.

## Brand & design
**Follow [04-brand-and-design.md](04-brand-and-design.md) for anything visual or written for users:** frontend, pitch deck, demo, docs, images. Use only the brand sheet's colours, fonts, logo, product name and terms (design tokens in one theme file, no hard-coded one-off values). Keep the app, the deck and the docs consistent in both Arabic and English.

## Working principles
1. **One end-to-end loop working live first**, then polish. Cut scope before cutting the demo.
2. Always be able to answer: *who exactly benefits in Jordan, who is left out today, and does our product actually reach them?*
3. **Every factual claim in the pitch needs a source.** Keep a sources list.
4. **Never overclaim.** No invented accuracy numbers and no "exponential" improvements. Label synthetic data and mocked integrations.
5. Privacy by default: consent, minimum data, aggregate where possible, delete raw data you don't need.

## Repo conventions
- `main` is protected by convention. Work on branches, and merge only working code.
- `README.md` must explain how to run the project (a required deliverable).
- Record decisions with date and reason in a decision log.
- Keep a short `HANDOFF.md` ("where are we, what's next") updated so anyone (human or AI) can pick up.
