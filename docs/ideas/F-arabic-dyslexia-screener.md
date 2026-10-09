# Idea F — Arabic Dyslexia Early-Screening Game ("Harf / حرف")

**One-liner:** A 10-minute gamified test for grades 1–4, played on a parent's phone or a school tablet. The child does Arabic letter/sound/word tasks and reads aloud. A model flags **dyslexia risk** and tells the parent and teacher what to do next (resource room, specialist).

Sector fit: Education & learning + accessibility & inclusion.

## The problem
- Meta-analysis: **about 1 in 9 Arab primary pupils have dyslexia.** ([search summary; find the primary paper if chosen](https://behavioristbookclub.com/aba-research/assessment-research/prevalence-of-developmental-dyslexia-among-primary-school-children-in/))
- Jordanian research has screening scales (Al-Karak, 40 + 40 children) and eye-tracking pre-screens built on Jordan MoE textbook text. These are lab tools that don't reach families. ([Jordanian Educational Journal](https://digitalcommons.aaru.edu.jo/jaes/vol7/iss4/6))

## Proof it works elsewhere
- **Dytective** (Spain, Luz Rello / Change Dyslexia): ML on game interaction data predicts dyslexia with **~83–86% accuracy** (243 participants; English version 84.6%). ([Change Dyslexia pubs](https://www.changedyslexia.org/publications/pdfs/2016-Pervasive%20Health-Dytective%20Detecting%20Risk%20of%20Dyslexia.pdf), [Frontiers 2021](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2021.628634/pdf))
- **ArabLexify**, an Arabic app validated with 1,200 children aged 6–12, reports AUC > 0.9. It proves Arabic screening works, **but it's also a direct competitor**. ([Society for Science abstract](https://abstracts.societyforscience.org/Home/PrintPdf/25634))

## Scorecard (1–5)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% |
|---|---|---|---|---|---|
| 4 | 4 | 2 | 3 | 4 | 4 |

## Why it's ranked lower for this hackathon
- **We can't get labelled data from children in 11 hours**, and the data rules forbid real personal data without consent. The classifier would be synthetic/mocked, which hurts "Technical Implementation" and honesty.
- Medical/diagnostic claims are risky in front of a domain judge.
- Very strong as a **post-hackathon research project** for our AI researcher (partner with a university special-ed department).
