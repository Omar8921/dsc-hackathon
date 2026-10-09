# Idea C — Electricity "Tier-Cliff" Forecaster ("Shariha / شريحة")

**One-liner:** Mid-month, tell a household **"at your current pace you'll cross 300 kWh on the 19th, and your bill will be ~JD 31 instead of ~JD 15"**. It names the 1–2 appliances driving the jump and how many kWh/day to cut to stay in the cheaper block. Works from a smart-meter reading or a **photo of the meter** sent on WhatsApp.

Sector fit: Environment & sustainability (energy) + public services (utility).

## The problem in Jordan
- Since April 2022 the **subsidised household tariff is block-based: 50 fils/kWh for 1–300, 100 fils for 301–600, 200 fils above 600.** Non-subsidised: 120 / 150 fils. ([Jordan News](https://www.jordannews.jo/Section-109/News/New-electricity-tariffs-to-be-applied-in-1st-trimester-of-this-year-11473))
- So the marginal price **doubles at 300 kWh and quadruples at 600 kWh**. Winter electric heating pushes families over the line. Winter load hit **4,010 MW, the highest in the Kingdom's history**, and the regulator itself attributed higher bills to winter consumption. ([Jordan News](https://www.jordannews.jo/Section-109/News/Higher-electricity-bills-due-to-rise-in-winter-consumption-says-regulator-12827))
- **91.3% of households now have smart meters** (JEPCO: 1.56M, 95% of its subscriptions). ([Jordan News](https://www.jordannews.jo/Section-33/Trade-Industry/Smart-Electricity-Meters-Installed-in-91-3-of-Jordanian-Households-46793)) The data exists, but the JEPCO app shows **history and averages, not a forward forecast or a tier alert** (based on its store listing; verify).

## Who is left out today
Elderly and low-literacy households who don't use the utility app; tenants; anyone outside JEPCO's area (IDECO north, EDCO south). They find out about the tier jump only when the bill arrives.

## Proof it works elsewhere
- **Opower home energy reports**, randomised trial with ~600,000 households across 12 utilities: **1.4–3.3% consumption reduction (avg 2.0%)**. Monthly feedback beat quarterly. ([J-PAL / Allcott](https://www.povertyactionlab.org/evaluation/opower-evaluating-impact-home-energy-reports-energy-conservation-united-states))
- US utilities run "bill watch" / high-usage alerts, e.g. New Jersey's Energy Bill Watch program ([NJ BPU 2026](https://www.nj.gov/bpu/pdf/boardorders/2026/20260422/3B%20ORDER%20Energy%20Bill%20Watch.pdf)), and JPS Jamaica's high-usage SMS alerts.
- In a block tariff the payoff is bigger than Opower's 2%, because the alert targets the exact kWh that cost 2× or 4×.

## What we'd build (11-hour MVP)
1. Input: meter photo → vision model reads kWh (OCR), or a manual reading.
2. Forecast: readings + days elapsed + Open-Meteo temperature forecast (heating degree-days) → end-of-cycle kWh with an interval.
3. Bill engine: exact tariff blocks + subsidy eligibility → JD amount and crossing date.
4. LLM coach in Jordanian Arabic: asks what heaters/appliances they have and gives a concrete plan ("the oil heater 6 h/day ≈ 9 kWh/day; switch 2 h to the gas soba").
5. WhatsApp-style chat UI (or real WhatsApp via Twilio sandbox) so elderly users don't install anything.

## Scorecard (1–5)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% |
|---|---|---|---|---|---|
| 4 | 3 | 5 | 4 | 5 | 4 |

## Risks / open questions
- Energy-saving apps are semi-common. **The tier-cliff framing is what keeps it from being generic.** Keep the pitch on that.
- No access to real smart-meter APIs. Demo uses photos and synthetic household traces (labelled).
- The utility could add the feature itself. That's also the business path (sell to or partner with JEPCO).
- Is the subsidised block applied per month or per billing cycle, and does the subsidy flip off above some threshold? **Verify with EMRA's tariff table before building.**

## Business / scale path
B2B2C with distribution companies (JEPCO/IDECO/EDCO) or EMRA. The payoff for them is peak-load reduction in winter. Cost is near zero per user.
