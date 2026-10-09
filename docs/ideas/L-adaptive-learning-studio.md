# Idea L — Adaptive Learning Studio ("Lovable for learning")

> Teammate's idea (2026-10-09): "I give it my GitHub repo, it sees my real level, and builds a personalised roadmap. Not a markdown file but **interactive modules**: a map, exams, resources, capstones, a history of my weak points." Below: polished, stress-tested, and reshaped for our sector.

## 1. Is "AI roadmap builder" on the crowded list?
**The generic version: yes, effectively.** It sits next to #4 on our avoid list (AI tutor / study assistant), and it's one of the first ideas any LLM suggests. There are dozens of hobby versions: DevAtlas, Coders.sh, MindRoute, DeepLearning.AI's roadmap tool, roadmap.it, CodeWords templates, "SkillMap AI" in idea lists ([search summary](https://github.com/habeebmoosa/getroadmaps), [DEV](https://dev.to/nk2552003/introducing-mindroute-your-personalized-ai-learning-roadmap-generator-kp), [DeepLearning.AI](https://community.deeplearning.ai/t/deeplearning-ai-course-roadmap-tool-personalized-study-plans/885591)). **Almost all of them ask "what's your level?" and output text.**

**The teammate's three twists are what make it not generic:**
1. **Evidence, not self-report.** It reads what you actually built (repo/code) instead of asking you. Only a few small projects do this (project-suggester, Skillsize's "stated vs demonstrated" gap report), and none end-to-end.
2. **Output is interactive modules, not text.** It's generative UI: the AI fills *pre-built, typed module templates* with your personal content.
3. **It's a living plan.** Every answer and every mistake updates your model, and the roadmap re-plans itself.

## 2. How to make it not feel like "a bunch of random features"
The anti-slop rule: **one learner model, one loop. Every feature is just a view on the learner model or a step in the loop.** If a feature isn't one of those, cut it.

```
            ┌──────────── LEARNER MODEL ────────────┐
            │ concept graph (skills + prerequisites)│
            │ mastery per concept  (0–1, updated)   │
            │ mistake log (tagged misconceptions)   │
            │ evidence links (code lines / answers) │
            └───────────────────────────────────────┘
   DIAGNOSE ──► GENERATE ──► PRACTICE ──► UPDATE ──► RE-PLAN ──┐
      ▲                                                        │
      └────────────────────────────────────────────────────────┘
```

| Feature the teammate listed | What it really is |
|---|---|
| The **map** | A *view* of the concept graph, coloured by mastery |
| **Exams** | *Probes* that measure mastery on specific nodes |
| **Weak-point / error history** | A *view* of the mistake log |
| **Resources** | Attached to graph nodes, ranked by your weak points |
| **Capstones** | Unlocked when a cluster of nodes reaches mastery. They're *about your own work* (e.g. "add context cancellation to *your* repo X") |
| **Things to focus on** | Lowest-mastery nodes whose prerequisites are already mastered (the "frontier") |

**Technical shape (what makes it reliable in a live demo):**
- A **fixed library of ~6–8 module types** (React components), each with a **strict JSON schema** (Zod or structured outputs). The LLM *only* outputs JSON that fills a schema; rendering is deterministic, so the demo can't break into gibberish.
  - Candidate modules: `ConceptMap`, `Quiz` (wrong answers tagged with the misconception they reveal), `Simulation` (parameter sliders + formula/code), `OrderSteps` (drag-and-drop), `WorkedExample` (step-through), `CodeExercise` (sandbox + tests), `Flashcards` (spaced repetition), `Capstone` (brief + rubric).
- **Mastery estimation** with Bayesian Knowledge Tracing or Elo-style updates. This is a real ML component for our data scientists, with decades of research behind it. Intelligent tutoring systems beat teacher-led large-group instruction (g≈0.42, 107-study meta-analysis); the RAND Cognitive Tutor trial gave modest, real gains. ([summary](https://arxiv.org/pdf/1802.08616), [Evidence for ESSA](https://evidenceforessa.org/?p=637))
- **Proof that this format works:** Google's **"Learn Your Way"** turns a textbook into personalised interactive formats (mind maps, quizzes, audio, immersive text). In a study with 60 Chicago high-schoolers it scored **77% vs 68%** on 3-day retention against a standard digital textbook (Google-funded). ([Google Research](https://research.google/blog/learn-your-way-reimagining-textbooks-with-generative-ai/), [arXiv 2509.18664](https://arxiv.org/pdf/2509.18664))

## 3. The sector problem (be honest)
Version 1 (**developer + GitHub**) is the most fun to build, and the "paste a judge's GitHub, watch their map light up" demo is a real wow. But:
- **"Skills-gap analysis, career guidance" is literally the economy sector's example list.** We're placed in **society**.
- The society panel will ask **"who is left out today?"** Developers learning Go aren't left out; they have roadmap.sh, docs and YouTube.

So we keep the engine (evidence → learner model → generated interactive modules → re-plan) and **point it at the group that is left out.**

## 4. Version 2 (recommended for our sector): the classroom
**One-liner:** A Jordanian teacher photographs a page of the national textbook. Within ~60 seconds the studio generates a **playable interactive lesson** (simulation, quiz with misconception-tagged answers, drag-and-drop steps) in Arabic. Students open it by QR. Every answer feeds a **live class map** for the teacher ("62% think heavier objects fall faster"), and **each student gets their own personal map and auto-generated remedial modules.**

It's the teammate's idea (personal map, exams, weak-point history, adaptive modules), but delivered **through the teacher**, so one upload reaches 40 students.

**Who is left out today (the Jordan numbers):**
- **Learning poverty: 52% before COVID → over 60% now**, per the Education Minister. That's the share of 10-year-olds who can't read and understand a simple text. ([Jordan News](https://jordannews.jo/Section-109/News/Learning-poverty-surges-from-52-5-to-over-60-post-COVID-Mahafzah-34800), [World Bank brief](https://documents1.worldbank.org/curated/en/403191624871019778/pdf/Jordan-Learning-Poverty-Brief-2021.pdf))
- **PISA 2022 math: 361, down 39 points from 2018, the lowest Jordan has ever scored.** Almost no top performers. ([OECD country note](https://www.oecd.org/en/publications/pisa-2022-results-volume-i-and-ii-country-notes_ed6fbcc5-en/jordan_d1c865b3-en.html))
- **826 double-shift schools (20.6%), with 29.4% of public-school students in them** (ministry figure, ~2020–21). Classes of **45+**, reaching 50–60 in the north. ([Jordan Times](https://jordantimes.com/node/270364), [Nature blog](https://blogs.nature.com/blog/schooling-syrias-refugees/))
- One teacher with 45 students and a shortened shift **cannot differentiate**. Personalisation today exists only for families who can pay for private tutoring. *That* is who's left out.

**Proof of demand abroad:**
- **MagicSchool** (AI tools for teachers): ~4–5M educators, 10,000+ schools, raised ~$45M (2025). Its lessons and worksheets are mostly text and English-first. ([Dealroom](https://app.dealroom.co/news/feed/magic-school-raises-45m-relocates))
- **Khanmigo** teacher tools are free in 49 countries (English). **Diffit** is used by districts at ~$3/student.
- **Google Learn Your Way:** interactive, personalised formats beat a static textbook on retention (77% vs 68%).
- **Gap:** Arabic-first, aligned to the Jordanian curriculum, **interactive (not worksheets)**, with a real per-student learner model.
- Note: the MoE's COVID-era platform **"Darsak" (درسك)** hosts recorded video lessons. We'd complement it with interactivity and personalisation (verify current status; don't reuse the name).

**The "Lovable for X" angle:** like Lovable (prompt → working app; $100M ARR in 8 months, $400M by Feb 2026 per TechCrunch-cited reports), Gamma (prompt → deck; $100M ARR, profitable, ~50 staff) or Replit, but for **one job: turning any curriculum page into a playable, adaptive lesson.** ([Lovable](https://en.wikipedia.org/wiki/Lovable_(company)), [Gamma via TechCrunch](https://techcrunch.com/?p=3066533))

## 5. The 7-minute demo (built around the "what wins" patterns)
1. **(0:00–0:45)** "Six out of ten Jordanian 10-year-olds can't read a simple text. One teacher, 45 kids, half a day." One slide.
2. **(0:45–2:00) The whoa moment:** photograph a real page of the Jordanian Grade-8 science book on stage → a progress view shows modules being built → **a working simulation + quiz appears.**
3. **(2:00–3:30) The judges play:** a QR on screen, the 3 judges answer on their phones. **The teacher dashboard updates live** ("2 of 3 judges think X: misconception tagged").
4. **(3:30–4:30) Personalisation:** open the judge who got it wrong. Their personal map shows the weak node, and a **remedial module generated just for them** appears. The next lesson re-plans.
5. **(4:30–5:30) Under the hood:** the module library + schemas (why it can't hallucinate a broken UI), the BKT mastery model, and what's mocked.
6. **(5:30–6:30) Business:** free for teachers; schools/donors/MoE pay per student per year (MagicSchool-style $5/student and Diffit ~$3/student as price anchors); funders with Jordan education budgets (e.g. the Jordan Compact education fund).
7. **(6:30–7:00) Next step:** a pilot with 3 double-shift schools for one term, measured with a pre/post quiz.

## 6. The developer version isn't wasted
Keep it as the **"same engine, second market"** slide: "the same studio reads a GitHub repo and builds a Go learning path whose capstones are improvements to *your own code*." It shows the platform is general, and it's the B2C/economy-sector expansion. If a mentor says crossing into economy is OK, it could even be the main demo.

## 7. Scorecards
| Version | Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|---|
| L1 — Developer learning OS from GitHub | 2 | 4 | 4 | 5 | 4 | 4 | **3.65** (sector mismatch hurts impact) |
| **L2 — Classroom studio (curriculum page → interactive adaptive lesson)** | 4 | 4 | 4 | 5 | 4 | 5 | **4.25** |

## 7b. Honest check: how does it score on "Impact on Jordan" (25%)? (added in round 5)
Rubric: *"A real problem with a clear group of people in Jordan who benefit."*

**What's strong:** the problem is real and huge (learning poverty 52% → 60%+, PISA math 361, 826 double-shift schools).

**What's weak:**
1. **Mismatch between headline stat and product.** Learning poverty measures *10-year-olds who can't read a simple Arabic text*. Our demo (a science simulation from a Grade-8 page) doesn't touch that number. A sharp domain judge will notice.
2. **Reach goes through teachers and devices.** The kids most affected (double-shift public schools, poorer families) are the least likely to have phones in class or data at home. "Does your app actually reach them?" is the exact question this sector's panel is told to ask.
3. **The evidence is small or foreign:** Google Learn Your Way (60 US students, Google-funded); tutoring-system meta-analyses g≈0.27–0.42. Promising, not proof for Jordan.
4. **"Clear group" is fuzzy:** "teachers and students" is everyone. Impact scores reward a narrowly defined group.
5. **Crowding:** "AI for teachers" will appear at other tables.

**Honest Impact score: 3/5, not 4.** Revised weighted total: 0.75 + 0.8 + 0.8 + 0.75 + 0.4 + 0.5 = **4.00**. The developer/GitHub version: **1–2/5** on Impact (developers aren't left out, and it's the economy sector).

**What would raise it to 4–5:** narrow the target to **early-grade Arabic reading** (Grades 2–4, where learning poverty is measured); make it work on **one shared device or a parent's phone** (voice: the child reads aloud and AI checks fluency and errors); **measure before/after on day one** with a small reading probe; and name a distribution channel (MoE early-grade reading programmes, donor-funded education programmes). That's a different product from the "Lovable for lessons" studio.

## 7c. How the *developer roadmap* version helps Jordan (round 7)
It does help Jordan, but through **jobs and skills**, not public services:
- **Tech graduates:** over **7,000 a year**, but only **~3,000 were registered as employed** with Social Security in 2020. Total ICT-sector employment is ~26,000. ([int@j](https://intaj.net/?p=20938)) An earlier int@j figure: under 40% of ICT grads find jobs in their field.
- **Employers say the gap is practical skills, English and soft skills.** 75% of ICT employers reported difficulty finding well-educated staff (older assessment). ([int@j](https://intaj.net/?p=20938), [Jordan Times](https://jordantimes.com/node/261579))
- **The government is already paying for this:** the **$200M World Bank "Youth, Technology & Jobs" project** (MoDEE) targeted 30,000 youth for digital skills but had trained ~8,000, with only 31.7% of funds disbursed by Oct 2025, running to Feb 2027. ([MoDEE](https://modee.gov.jo/EN/Pages/Youth_Technology_and_Jobs_Project), [Jordan News](https://www.jordannews.jo/Section-112/Economy/World-Bank-31-7-of-Youth-Technology-and-Jobs-Project-Funding-Disbursed-46248))
- **Story:** "Jordan produces 7,000 tech grads a year and employers still can't hire. Our roadmap reads what each grad actually built, closes *their* gap with projects on *their own code*, and gives employers evidence of real skill." The payer is the YTJ programme, bootcamps (DigiSkills) and universities.

**The catch:** this is the **economy sector's** stated topic ("Jobs, skills & the future of work… skills-gap analysis, career guidance"). Judged by the society panel, Impact is ~2. The rules allow crossing sectors **only after checking with a mentor**. If a mentor approves, Impact would be ~4 (clear group: tech grads; clear Jordan number; clear payer). If not, use the society-sector reading version instead (see 08, idea B1).

| Version | Impact | Innov. | Feas. | Tech | UX | Pitch | Weighted |
|---|---|---|---|---|---|---|---|
| Developer roadmap, judged as society | 2 | 4 | 4 | 5 | 4 | 4 | 3.65 |
| Developer roadmap, if a mentor approves the crossover | 4 | 4 | 4 | 5 | 4 | 4 | 4.15 |

## 8. Risks / open questions
- **Student devices:** phones may not be allowed in public classrooms. Mitigations: teacher-projector mode plus printed QR for homework on a parent's phone, and a low-bandwidth web app (no install).
- **Generation quality on stage:** pre-test on 5–10 real textbook pages; keep a cached "golden" output as a fallback; be honest about it.
- **Arabic STEM rendering** (RTL + equations + units): test early.
- **Crowding:** "AI for teachers" will appear at other tables. Our defence is the *interactive + learner model + live classroom loop* demo, not a lesson-plan text generator.
- **Curriculum copyright:** use only the page photographed on the day, for demo purposes.
- **Scope for 11 hours:** 4 module types max (Quiz, Simulation, OrderSteps, ConceptMap), one subject (science), one grade.
