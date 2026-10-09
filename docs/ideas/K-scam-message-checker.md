# Idea K — Arabic Scam-Message Checker ("Mish Mazbout / مش مزبوط")

**One-liner:** Forward any suspicious SMS, WhatsApp message, link or voice note to a WhatsApp bot. It answers in Jordanian Arabic: **scam / suspicious / looks fine**, explains *why* ("real traffic fines never come with a link"), and offers one-tap reporting to the Cybercrime Unit's coordination room.

Sector fit: Safety + accessibility (elderly / low digital literacy). ⚠️ It overlaps with the economy sector's "fraud awareness", so check with a mentor.

## Problem in Jordan
- **29,389 cybercrime cases in Jordanian courts in 2025** (National Center for Human Rights). ([Al Mamlaka](https://almamlakatv.com/news/209949-))
- The coordination room had blocked **2,300+ fraudulent websites and 2,200+ fraudulent WhatsApp numbers** (by July 2025), handles **~2,540 complaints per month**, and froze ≈JD 1M (Jan–May 2025). ([Al Jarida](https://www.aljarida.com/article/102203), [Al Rai](https://www.alraimedia.com/article/1732532/))
- Recurring waves: fake traffic-fine SMS ([Petra](https://www.petra.gov.jo/ar/index.php/en/news/psd-warns-against-fake-traffic-fine-messages)), fake Jordan Post / Customs messages ([Jordan News](https://www.jordannews.jo/Section-109/News/Jordan-Post-Warns-Against-Fraudulent-Messages-Using-Its-Logo-49975)), OTP theft ([Jordan News](https://www.jordannews.jo/Section-109/News/Citizens-Fall-Victim-to-Financial-Fraud-Urgent-Calls-to-Safeguard-Personal-Data-36938)), and **AI voice-clone "relative" calls** (TRC warning, March 2026, [Petra](https://www.petra.gov.jo/en/news/telecom-regulator-warns-of-rising-online-fraud-attempts)).

## Proof abroad
- **Singapore ScamShield** (Open Government Products + police): 119k downloads, 722,865 SMS reported and 5,537 scam numbers blocked in its first 6 months. ([SPF](https://police.gov.sg/Media-Room/News/20210529_scamshield_application_aids_in_scam_prevention_efforts))
- **Taiwan Cofacts** (crowdsourced fact-check chatbot on LINE) answered faster than professional fact-checkers and covered local small-time scams ([Cornell](https://news.cornell.edu/node/327621)). **Whoscall** reports 3B+ calls/SMS blocked (self-reported).

## Scorecard
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% | **Weighted** |
|---|---|---|---|---|---|---|
| 4 | 3 | 5 | 4 | 5 | 4 | **4.10** |

## Risks
- "Phishing detector" is a semi-common idea, and fraud awareness is in the *economy* sector's examples.
- Lasting value needs the PSD/TRC block-list feed. Without it, the bot only explains rather than protects.
