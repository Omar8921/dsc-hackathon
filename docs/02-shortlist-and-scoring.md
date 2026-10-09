# Shortlist & Scoring

Scores are 1–5 per criterion, weighted by the official judging weights. They are our own judgment. **Re-score as a team**; the point is to argue about the numbers.

| Idea | Impact 25% | Innov. 20% | Feas. 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|---|
| [A — Unified-admission choice planner](ideas/A-admission-choice-planner.md) | 5 | 4 | 4 | 4 | 4 | 5 | **4.35** |
| [C — Electricity tier-cliff forecaster](ideas/C-electricity-tier-forecaster.md) | 4 | 3 | 5 | 4 | 5 | 4 | **4.10** |
| [D — Wadi flash-flood go/no-go](ideas/D-wadi-flash-flood-trip-check.md) | 4 | 5 | 3 | 4 | 4 | 5 | **4.10** |
| [B — AI pedestrian-risk rating of school routes](ideas/B-school-route-pedestrian-risk.md) | 4 | 5 | 3 | 5 | 3 | 4 | **4.05** |
| [E — Cheaper equivalent medicine finder](ideas/E-generic-medicine-price-check.md) | 4 | 3 | 4 | 4 | 4 | 4 | **3.80** |
| [F — Arabic dyslexia screener](ideas/F-arabic-dyslexia-screener.md) | 4 | 4 | 2 | 3 | 4 | 4 | **3.45** |

Parked: [G — informal transit mapping, water tankers, solar soiling, Takaful helper, etc.](ideas/G-parked-ideas.md)

## The filters each shortlisted idea passes
| Filter | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| One specific painful moment/decision | ✅ ranking choices | ✅ walking to school | ✅ crossing 300 kWh | ✅ trip morning | ✅ paying at pharmacy | ✅ child can't read |
| Proof abroad | ✅ China Quark (100M+ uses) | ✅ iRAP AiRAP / Google.org Vietnam | ✅ Opower RCT (600k homes) | ✅ NWS flash-flood guidance | ✅ India Jan Aushadhi | ✅ Dytective, ArabLexify |
| Public Jordan data on Day 1 | ✅ published cut-offs | ⚠️ imagery coverage | ✅ tariff + weather | ✅ DEM + Open-Meteo | ✅ JFDA open data | ❌ no labelled kids data |
| AI does what a form can't | ✅ probability + optimise + explain | ✅ vision audit | ✅ OCR + forecast + coach | ⚠️ model + explainer | ✅ vision + matching | ✅ ML classifier |
| Clear "who is left out" | ✅ governorate / first-gen students | ✅ kids in dense neighbourhoods | ✅ elderly, non-app users | ✅ teachers, small operators | ✅ uninsured chronic patients | ✅ undiagnosed kids |
| Not on the crowded list | ✅ | ✅ | ⚠️ energy-tips adjacent | ✅ | ⚠️ | ✅ |

## Recommendation
**Primary: Idea A (Unified-admission choice planner).**
- Strongest **Impact on Jordan** story: 74k students a year, 27,955 not placed last cycle, a state-run "wrong choice" round, the brand-new 2026 fields system, and 39 stagnant majors.
- Strongest **proof abroad**: the same exam-and-ranked-list system in China, with AI tools at 100M+ uses.
- **Data is public** and the model is real (not mocked). It suits a team of 3 data scientists plus 1 SWE.
- The demo is emotional and fits in 7 minutes: one student, before/after list.

**Backup / alternative if the team prefers something more "smart-city":** D (flash floods) has the best pitch moment (replaying 25 Oct 2018), and B (school-route audit) has the most impressive AI. **C is the safest build** if we're worried about time.

**Before committing (first 30–45 min of Day 1):** spend 20 min checking that we can actually get 2–3 years of per-major × per-university cut-off averages for one field (news sites publish the full tables). If we can't, fall back to D or C.
