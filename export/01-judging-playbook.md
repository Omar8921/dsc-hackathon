# Judging Playbook

How to score high on each criterion, what each judge will ask, and how to grade ourselves honestly before we pitch.

## 1. Criterion by criterion

### Impact on Jordan (25%)
Judges want a real problem and a clear group in Jordan who benefit.
- **Name the group precisely** (not "citizens") and **size it with a sourced number**.
- **Say what the problem costs them** in time, money, safety or opportunity, with a source.
- **Answer the sector question out loud:** "Who does this reach that the current service does not?" Then show *how* we reach them (Arabic, voice, no app install, low data, works for low literacy).
- Show **what changes for them**, in a unit they feel: minutes saved, JD saved, a trip or visit avoided.
- ❌ Avoid: "raising awareness", unsourced statistics, impact that only happens if a ministry rebuilds everything.

### Innovation & Creativity (20%)
Judges want a fresh angle, or AI used where it truly adds value.
- **The AI must do something a form or website can't:** understand dialect, read a photo, reason over messy rules, predict, detect contradictions, negotiate a trade-off with a user.
- **Know what already exists in Jordan** (official apps and services, earlier student projects and award winners). Be ready to say in one sentence how we differ.
- A proven solution from abroad, adapted to Jordan, counts as a strength, but explain the twist.
- ❌ Avoid: "a chatbot for X" where the LLM is the whole product, buzzwords without substance.

### Feasibility & Scalability (20%)
Judges want a realistic path to real users, data and cost.
- **Who pays, and why:** name the institution or customer and the cost line it saves.
- **Who must say yes:** the ministry, regulator or partner. Is a licence or legal approval needed? Have a phased answer.
- **Where the data comes from**, today and in production.
- **Cost to run** (API costs per user, infrastructure) in rough numbers.
- **Rollout:** pilot (1 site / 1 partner) → city → national → region.

### Technical Implementation (15%)
Judges want a working demo and honesty about what is mocked.
- **One end-to-end loop working live.**
- **Show a "real vs mocked" table** in the pitch (template in [02](02-demo-and-pitch-guide.md)). Judges reward honesty.
- If you trained or evaluated a model, show **one honest metric on a held-out set**.
- Label synthetic data clearly. Never fake numbers.
- ❌ Avoid: overclaiming technology ("exponential", "99% accurate" with no test set).

### UX & Design (10%)
Judges want it usable by the intended users, including in Arabic.
- **Arabic / RTL** done properly, with dialect where users speak dialect.
- Few steps; the main action is obvious on the first screen.
- Fits the users: mobile-first, voice if literacy is an issue, readable font sizes, accessible contrast.
- Every stage of the flow has clear states (loading, error, confirmation).

### Presentation & Pitch (10%)
Judges want problem, demo, impact and next step, within time.
- Hit all four parts, and **finish on time** (7 min including the demo).
- A personal story or a vivid example in the first 30 seconds.
- End with a concrete next step (a pilot partner, a first users' group).

## 2. The three judges and what each will ask
| Judge | Cares about | Likely questions |
|---|---|---|
| **Domain** | Is the problem real? Would the institution use this? | Who exactly uses it? How do they do it today? Who's left out? Have you talked to real users? What does the institution need to change? |
| **AI / technical** | Is the AI real and necessary? What actually works? | Why AI, and not rules or a form? What model, and how did you test it? What's mocked? What happens when the AI is wrong? Compared to what baseline? |
| **Business** | Can this live after the hackathon? | Who pays, how much, and why? What does it cost to run? Who are the competitors? What's the regulation risk? How does it scale? |

## 3. Q&A prep (3 minutes; prepare 1-sentence answers)
1. Who is left out today, and how do you reach them?
2. Why does this need AI?
3. What's real in the demo and what's mocked?
4. What happens when the AI is wrong? (Human in the loop, confidence, fallback.)
5. Who pays? What does it cost per user?
6. What already exists in Jordan, and why isn't it enough?
7. Is it legal? Who must approve it?
8. Where does the data come from in production? What about privacy and consent?
9. What's the first pilot, with whom, and what metric proves it works?
10. How does it scale beyond Amman / beyond Jordan?

## 4. Grading ourselves (do this before the pitch)
- Score each criterion **1–5**, then:
  **Weighted = 0.25 × Impact + 0.20 × Innovation + 0.20 × Feasibility + 0.15 × Technical + 0.10 × UX + 0.10 × Pitch**
- Each person scores alone first, then compare. Argue about the gaps, not the averages.
- **Be equally strict on every part.** Write down the weakest 5 points a judge could attack, and a one-line answer to each.
- Any criterion at **≤ 3** is where the next hour of work should go.

| Score | Meaning |
|---|---|
| 5 | A judge would point to it as the best in the room on this criterion |
| 4 | Clearly strong, with one minor gap |
| 3 | OK but generic, or with an unanswered question |
| 2 | Weak; a judge will likely push on it |
| 1 | Missing |

## 5. Lessons from Jordanian student-app judging
From the winners of Jordan's Crown Prince Award for Best Government Services Application (judged by government officials):
- **AI is now expected.** Most recent winners use AI; the older winners didn't. Plain apps look dated.
- **The top prizes solve two problems at once** (e.g. one match that serves two groups).
- **"Report it to the authorities" apps place, but rank low.** The product should *resolve* something, not just forward it.
- Judges may already know similar Jordanian projects. Be ready with "how we're different" in one sentence.
