# 05. Branding: فارس / Faris

**Draft v1, Oct 10 2026.** Decided with the team:
- Dark "control room" theme, with signal colours carrying meaning.
- IBM Plex Sans Arabic, Western digits.
- Everything in Arabic, **Jordanian dialect everywhere** (slides and app).

## Name and tagline
- **Name:** **فارس**, written **Faris** in English. It's just a name: no acronym and no backstory.
- **Tagline:** **الأخضر للي مستنّي**, "the green goes to whoever is waiting".
- Usage: on its own, write "فارس". In English text, write "Faris". Never "FARIS" or "Faris AI".

## Logo: the living dot
- An Arabic wordmark of **فارس** in IBM Plex Sans Arabic Bold (700). The dot of **ف** is drawn as a **signal light**.
- Build: type **ڡارس**, using the dotless feh (U+06A1), and place a circle where the dot would be. Diameter ≈ 20% of the cap height.
- **Static (default):** the dot is **green** (`--go`). Use it everywhere small: favicon, app header, slide footers.
- **Animated (title slide, app loading):** the dot cycles **red → amber → green** (about 1.5 s each), then stays green.
- **App icon:** the dot alone, or ڡ + dot, on `--bg`.
- Clear space: one dot diameter on every side. The minimum size is where the dot is still 4 px.

## Colour

The base is neutral; colour **only** carries meaning. The deck moves from red (problem) to green (result).

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0E1116` | Page and slide background |
| `--surface` | `#161B22` | Cards, panels |
| `--surface-2` | `#1E2530` | Raised panels, the selected junction |
| `--line` | `#2A313C` | Borders, dividers, lane markings |
| `--text` | `#F2F4F7` | Main text |
| `--muted` | `#8A94A6` | Labels, sources, captions |
| `--off` | `#3A3F48` | An unlit signal dot |
| `--stop` 🔴 | `#FF5A5F` | **Problem**: cost, congestion, a junction that's failing |
| `--wait` 🟠 | `#FFB020` | **Waiting**: delay, queues, "watch this" |
| `--go` 🟢 | `#2BD576` | **Result**: time saved, a clear junction, the logo dot |

Rules:
- Use one signal colour per number or element. Never use red, amber and green for decoration.
- On slides, problem numbers are `--stop`, waiting time is `--wait`, our results are `--go`.
- In the app, a junction's state uses the same three. The traffic-radio words make good labels: **سالكة** (go), **في أزمة** (stop), **بتستنّى** (wait).
- Coloured text should be at least 18 px or bold. All three signal colours pass AA on `--bg`.

## Typography
- **IBM Plex Sans Arabic** (Google Fonts), weights 400 / 500 / 600 / 700. Its Latin is Plex Sans, so English words and numbers match.
- **Western digits** (6%, 2,500) everywhere.
- Slide sizes: title 64–80 px / 700; headline 44–52 px / 600; hero number 96–140 px / 700; body 24–28 px / 400; source 14–16 px / `--muted`.
- App sizes: 14–16 px body, 12 px minimum, 24–32 px for live numbers.
- Never use weights below 400; thin Arabic disappears on projectors.

## Layout
- Everything is **RTL** (`dir="rtl"`). Numbers and units stay LTR inside the line (`<bdi>` or `unicode-bidi: isolate`).
- Slides: 16:9, **one idea per slide**, a hero number or one visual, lots of `--bg`.
- Motif: **lane markings**, a dashed `--line` rule used as a divider.
- Corners: 12 px on cards, 999 px on status pills.
- No gradients, glows or stock photos of traffic.

## Voice: Jordanian dialect everywhere
Short, direct, a bit warm, never cute when it's about safety.

| Where | Example |
|---|---|
| Slide headline | إشارة خضرا لشارع فاضي |
| Slide headline | الكاميرات موجودة. الناقص العقل اللي بيقرّر |
| App: AI explains itself | زدت الأخضر 12 ثانية لشارع المدينة لأنه الطابور صار 18 سيارة والفرعي فاضي |
| App: override button | رجّع عالخطة الثابتة |
| App: status | سالكة · بتستنّى · في أزمة |
| App: camera fallback | الكاميرا مش واضحة، رجعنا عالخطة الثابتة لحالنا |
| App: empty state | ولا تقاطع بحاجة إلك هلأ |

Rules: no English loanwords in the UI where a natural Jordanian word exists (e.g. "طابور", not "queue"). Technical terms used by GAM engineers (دورة، طور، أخضر أدنى) stay as they are.

## CSS starter
```css
:root{
  --bg:#0E1116; --surface:#161B22; --surface-2:#1E2530; --line:#2A313C;
  --text:#F2F4F7; --muted:#8A94A6; --off:#3A3F48;
  --stop:#FF5A5F; --wait:#FFB020; --go:#2BD576;
  --font:'IBM Plex Sans Arabic', system-ui, sans-serif;
}
html{direction:rtl;background:var(--bg);color:var(--text);font-family:var(--font)}
```
