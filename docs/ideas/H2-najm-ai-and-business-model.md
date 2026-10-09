# Idea H (part 2) — Where the AI earns money, and the business model

Companion to [H-najm-for-jordan.md](H-najm-for-jordan.md). Written 2026-10-09.
**All numbers marked _(assumption)_ are ours and must be replaced or validated before going on a slide.**

## 0. The core principle
> **The fault % is the feature drivers love. Damage, fraud and leakage AI is what insurers pay for.**

Nobody pays for a fault percentage: it's a public decision, and the officer signs it. If our AI only "suggests fault", the business judge will (correctly) say "nice, but who pays?". The AI is convincing only if **each AI component sits on a cost line that someone already pays today**.

## 1. Where the money goes today (Jordan motor insurance)
| Fact | Value | Source |
|---|---|---|
| Motor gross written premiums 2024 | **JD 272M** (34% of market) | [ME Insurance Review](https://meinsurancereview.com/Magazine/ReadMagazineArticle?aid=49237) |
| Motor **paid claims** 2024 | **JD 261.4M** (+8.9% y/y). Revised figures differ slightly (≈JD 258M). | same; [revision](https://meinsurancereview.com/News/ViewNewsLetterArticle/id/94779/Type/MiddleEast/Jordan-Insurance-premiums-climb-by-nearly-10-in-2025) |
| Motor paid claims 2025 | ≈ JD 278–288M (source is internally inconsistent) | same |
| → Claims alone ≈ **96% of premiums**, *before* commissions, salaries and surveyors | | our arithmetic |
| CBJ refused MTPL price rise (Feb 2025); 4 insurers liquidated; MEICO exits motor (Jan 2026) | | see H file |
| Fraud is estimated at **up to ~10% of claims spend** (Europe; dated, not motor-specific). Germany: ~10% of claims suspicious, half of them motor. | | [Insurance Europe](https://www.insuranceeurope.eu/mediaitem/2bf88e16-0fe2-4476-8512-7492f5007f3c/Insurance%20fraud%20-%20not%20a%20victimless%20crime.pdf), [GDV via XPRIMM](https://xprimm.com/GDV-Costs-of-fraudulent-claims-is-increasing-in-line-with-the-increasing-benefits-in-P-C-insurance-articol-124-21762.htm) |
| Registered vehicles ≈ **1.8M** (Dec 2021, latest found) | | [CEIC](https://www.ceicdata.com/en/indicator/jordan/number-of-registered-vehicles) |

**Insurers can't raise prices, so the only way to survive is to cut what each claim costs.** That's our opening.

## 2. Each AI component → the cost line it attacks → the KPI we'd measure
| # | AI component | What it does | Who saves / earns | KPI | Build in hackathon? |
|---|---|---|---|---|---|
| 1 | **Guided capture + photo QA** (vision) | Live check: plate readable, 4 corners, damage close-up, no gallery uploads, GPS/time locked | Insurer: fewer "come back for more photos" loops; makes remote handling possible at all | % of cases complete on first try | ✅ |
| 2 | **Damage detection + repair estimate** (vision + price table) | Detect parts and damage type/severity, then a JD estimate range from a parts × labour table | Insurer: **skip or shorten the surveyor visit** on small claims; **cap inflated garage quotes** (leakage) | Estimate error vs final invoice; % of claims settled without a surveyor | ✅ (estimate table is synthetic) |
| 3 | **Fraud / staged-accident scoring** | Damage pattern vs the story; old rust or prior damage; same people or plates across cases; location/time anomalies; Najm-style indicators | Insurer: **catch fraud** (largest € in the table above) | Precision of top-5% flagged cases; JD of leakage avoided | ✅ basic rules + LLM checks; history mocked |
| 4 | **Statement reconciliation** (LLM, Arabic dialect) | Two drivers' accounts → structured facts → contradictions highlighted against photos | PSD officer: decides in ~1 min instead of travelling; fewer disputes later | Officer minutes per case; % of objections | ✅ |
| 5 | **Fault suggestion with rule citation** | Scenario + facts → split (100/0, 75/25, 50/50) + the traffic-law rule + confidence | PSD (speed); drivers (transparency) | Agreement rate with officer's final decision | ✅ (6–8 scenarios) |
| 6 | **Accident analytics** (aggregate, anonymised) | Hotspots by street/time/scenario | GAM / PSD / Ministry of Transport (road-safety fixes); insurers (risk) | — | Optional dashboard |

Components **2 and 3 are the revenue engine**, **4 and 5 are the adoption engine** (they make PSD say yes), and **1 makes everything else possible.**

## 3. Who pays, and how (revenue model)
**Drivers pay nothing.** Any fee at the roadside kills adoption, and the app replaces something "free" (the officer).

### Lesson from Najm (important for the pitch)
Najm used to earn **>95% of its revenue per accident**. Its CEO called that model "very painful", because the company made more money when there were more accidents. With SAMA's backing it **switched to a fee per insurance policy**, which aligns it with road safety. Revenue was **SAR 750M in 2021** (vs ~SAR 300M in 2018), with a **~7% target margin**. ([Argaam](https://argaam.com/en/article/articledetail/id/1592427), [Okaz](https://www.okaz.com.sa/economy/na/2248518))

### Our model: phased
| Phase | Customer | Pricing | Why they pay |
|---|---|---|---|
| **1. Insurer pilot (no law change needed)** | 1–2 insurers (motor-heavy) | **Per processed claim** SaaS fee, e.g. JD 3–6 _(assumption)_ | They get structured photos + damage estimate + fraud score at first notice of loss, *even while the officer kroka still exists*. Savings per claim > fee. |
| **2. PSD × JIF remote-kroka pilot** | JIF (on behalf of members) + PSD | Per case during the pilot | PSD frees officers and reduces congestion; JIF gets faster, cleaner data into E-Kroka |
| **3. National scale** | JIF / all motor insurers | **Per-policy levy** (Najm's current model), e.g. JD 0.5–1 per policy per year _(assumption)_ | Predictable revenue tied to fewer accidents, not more |
| Add-on | GAM, PSD, Ministry of Transport | Annual analytics licence | Hotspot and scenario data for road-safety spending |
| Add-on (careful) | Approved garages / towing | Referral fee | Only through insurer-approved networks, so there's no conflict of interest with the estimate |

## 4. Back-of-envelope (show the logic, label the assumptions)
**What the AI can save insurers (value created):**
- Motor paid claims ≈ **JD 260–285M/yr**.
- If fraud plus overpayment is even **5%** of that _(assumption, half the European estimate)_, that's **≈ JD 13–14M/yr** of leakage.
- If our scoring and estimate cap recover **one-fifth** of that _(assumption)_, that's **≈ JD 2.6–2.8M/yr**, about **1% of motor claims**.
- Plus surveyor time saved on small claims _(unknown cost per visit; ask an insurer)_.

**What we'd charge (value captured):**
- Phase 3 levy: **1.8M vehicles × JD 0.5–1 ≈ JD 0.9–1.8M/yr**. That's **less than the ~JD 2.7M we'd save insurers**, so the deal makes sense for them before even counting PSD and congestion benefits.
- Phase 1 per-claim: you only need a few thousand claims a month at JD 3–6 to cover a small team.

**What it costs to run:**
- AI inference: ~10 photos + a few LLM calls per case, **cents per case** _(measure during the build and put the real number on the slide)_.
- Cloud (Supabase) is small. The main costs are an ops/support team plus insurer integration work.
- Remote officers are PSD staff, but fewer of them are needed than for field visits.

**The one-sentence answer for "who pays and what does it cost to run":**
> "Insurers pay per claim at first, then a sub-JD levy per policy, as Najm does today. Our AI saves them more than it costs by cutting fraud and overpaid repairs on a motor book where claims already eat ~96% of premiums. Each case costs us cents in AI inference."

## 5. Why this is credible (not "AI slop")
1. **The cost lines are real and already being paid:** surveyor visits, inflated invoices, staged accidents (PSD warning, Aug 2024), officer field time.
2. **Each AI output is checked by a human** at the point of decision (officer for fault, adjuster for payout). AI reduces the work; humans stay accountable.
3. **The incentives line up:** a per-policy fee means we make more when there are *fewer* accidents. Najm learned this the hard way.
4. **It's measurable from day 1** with the KPIs in the table. Phase 1 needs no legislation.
5. **There's an integration point:** E-Kroka already feeds insurers, so we don't need a new pipe.

## 6. What to show in the demo so the AI looks convincing
- **The fraud moment:** case 2 of the demo shows "damage pattern doesn't match a rear-end story + rust in the dent", the AI flags it, and the officer sees *why*.
- **The estimate moment:** "AI estimate JD 180–240" next to a (synthetic) garage quote of JD 410, flagged as above range.
- **The speed moment:** the officer console approves a clean case in under 30 seconds.
- **The honesty slide:** what's real (vision, LLM, rules, two-phone flow) vs mocked (insurer/E-Kroka integration, case history, price table).
- **One accuracy number** measured on a small labelled test set we build ourselves (e.g. damage detection on 50 images; fault agreement on 30 synthetic scenarios).

## 7. Open questions to validate (ask an insurer/mentor on Day 1)
- Average cost of a surveyor visit and average minor-claim size in Jordan.
- How many of the ≈175k non-injury accidents become insurance claims?
- Does JIF charge insurers per E-Kroka today? (That would be the price anchor.)
- Is CBJ open to a per-policy levy, as SAMA was for Najm?
