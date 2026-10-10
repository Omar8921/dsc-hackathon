# Iteration 1: فارس / Faris

**AI that gives the green light to whoever is actually waiting.** Faris reads the traffic cameras Amman already has, counts the queue on every approach, sets the green split each cycle within safety limits, and coordinates neighbouring junctions. It's sold to the Greater Amman Municipality (B2G).

Planning outputs from Oct 10 2026. Features, modules, tech stack, user flow and the pitch storyline/script are **not decided yet**.

| # | File | What's in it |
|---|---|---|
| 01 | [01-problem-statement.md](01-problem-statement.md) | The problem, 10 sourced facts, what we claim and don't claim |
| 02 | [02-target-users.md](02-target-users.md) | Buyer (GAM), partner (PSD Traffic Dept), user (control-room operator), beneficiaries (commuters, school runs), personas |
| 03 | [03-feasibility.md](03-feasibility.md) | 7th Circle cluster first, rollout phases, safety limits, integration routes, privacy, stakeholders, risks |
| 04 | [04-value-and-impact.md](04-value-and-impact.md) | 10/20/30% scenarios: hours given back, fuel and CO₂, from the cluster to Amman to Jordan |
| 05 | [05-branding.md](05-branding.md) | Name, tagline, living-dot logo, colours, type, Jordanian-dialect voice, CSS tokens |
| 06 | [06-revenue-and-costs.md](06-revenue-and-costs.md) | JD 3,000 setup + JD 200/month per junction, revenue plan, year-1 costs, funding gap |
| 07 | [07-pitch-deck.html](07-pitch-deck.html) | 15-slide Arabic RTL deck. Open in Chrome: ← / PageDown = next, → = back, F = fullscreen |

## Known to-dos
- 01 still mentions the existing smart-signal pilot (fact 5, "who it reaches", "why now"). The team decided not to mention it, so rewrite those parts.
- 01's "16 hours a year" per commuter should become the 5–14 h range from 04.
- 01's last source points to a local file on a teammate's laptop. Replace it with public links.
- Deck placeholders: SUMO result (X%), team names, a backup demo-recording link.
- Verify the FHWA cost page (06) in a browser before using those numbers on a slide.
- The deck loads IBM Plex Sans Arabic from Google Fonts, so it needs internet. Bundle the font if the venue is offline.
