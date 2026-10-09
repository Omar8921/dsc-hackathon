# Idea D — Wadi Flash-Flood Go/No-Go for Trips ("Wadi Watch / راقب الوادي")

**One-liner:** Before a school trip, hike or canyon tour, check a site. The app looks at **rain forecast over the whole upstream catchment**, not just at the spot, and returns a clear Arabic **go / caution / no-go** with the reason. Example: "Sunny at Zarqa Ma'in, but 18 mm forecast 25 km upstream at 1 pm. Water can arrive within 40 minutes."

Sector fit: Safety & emergency response (early warnings).

## The problem in Jordan
- **25 Oct 2018, Zarqa Ma'in / Dead Sea:** a flash flood killed **21 people, mostly schoolchildren** on a school trip. The trip went ahead **despite official storm warnings and an MoE ban on Dead Sea trips in bad weather**. The Education and Tourism ministers resigned. ([Al Jazeera](https://www.aljazeera.com/news/2018/10/26/jordan-floods-schoolchildren-among-19-dead-after-bus-swept-away))
- **Nov 2018:** further floods killed 12 and forced the evacuation of **~4,000 tourists from Petra**. ([Gulf News](https://gulfnews.com/amp/world/mena/jordan-floods-12-killed-4000-tourists-evacuated-from-petra-1.60277010))
- Generic national weather warnings don't reach organisers in a usable form. The danger is **non-local**: it's dry where you stand while it rains upstream.

## Who is left out today
Teachers organising trips, small adventure-tour operators (Wadi Mujib, Wadi Ghuweir, Wadi Rum), and domestic hikers. None of them have hydrology expertise or a site-specific warning.

## Proof it works elsewhere
- The US NWS Flash Flood Guidance system and Israel's flash-flood warnings for Dead Sea/Negev wadis combine catchment rainfall with terrain.
- Google Flood Hub shows ML flood forecasting at scale but focuses on **riverine** floods. Desert flash floods are a recognised gap (to check before pitching).

## What we'd build (11-hour MVP)
1. Pre-compute catchments for ~15 popular Jordanian wadi sites from an SRTM DEM (whitebox/pysheds).
2. Pull hourly precipitation forecasts over each catchment (Open-Meteo, free, no key).
3. Risk rule + small model: catchment-weighted rain intensity × slope/size → lead-time estimate → traffic light.
4. LLM briefing in Arabic for a teacher or principal, plus a printable "trip approval" sheet.
5. Replay demo: run the model on **25 Oct 2018 historical weather** (Open-Meteo archive) and show it would have said **NO-GO** that morning.

## Scorecard (1–5)
| Impact 25% | Innovation 20% | Feasibility 20% | Tech 15% | UX 10% | Pitch 10% |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 4 | 4 | 5 |

## Risks / open questions
- **Low frequency:** a judge may ask "how often is this used?" Answer: every trip in the rainy season (Oct–Apr), plus tour operators daily.
- **Validation/liability:** we can't claim hydrological accuracy. Position it as decision support on top of official warnings.
- The DEM and catchment work is real GIS; it needs the AI/data people early on Day 1.
- The AI is more "model + LLM explainer" than deep AI. Innovation comes from the framing.

## Business / scale path
MoE (mandatory pre-trip check), Ministry of Tourism / Jordan Tourism Board for licensed adventure operators, Civil Defence. Low running cost.
