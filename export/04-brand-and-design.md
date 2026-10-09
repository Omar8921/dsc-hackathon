# Brand & Design Consistency

**One theme and one brand across everything we produce:** the frontend, the pitch deck, the demo, the README, screenshots, posters and QR codes, the logo and any video. Judges should feel it's one product made by one team. Consistency also earns points under UX (10%) and Pitch (10%).

## 1. Rules
1. **Define the brand once, early** (§2, in the first hours) and treat it as the **single source of truth**. Nobody invents colours, fonts or names on the fly.
2. **Everything pulls from that source:**
   - **Frontend:** design tokens (colours, fonts, spacing, radius, shadows) live in one theme file (whatever the chosen framework uses for theming). Components use tokens only; no hard-coded hex values or one-off font sizes.
   - **Pitch deck:** the same logo, colours, fonts, icon style and product name as the app. Screenshots in the deck must match the current UI.
   - **Demo:** the demo data, sample names and copy use the same tone and terminology as the app and the deck.
   - **Docs and README:** the same product name, tagline and logo.
3. **Same words everywhere.** The product name, tagline, feature names and key terms are identical in the UI, the deck and the pitch script, in both Arabic and English. Keep them in the i18n/strings file and copy from there.
4. **Arabic first-class:** RTL layout, an Arabic font that pairs with the Latin font, and mirrored icons/arrows where direction matters. Arabic text is never an afterthought or a machine translation pasted in at the end.
5. **One icon set and one illustration/image style.** Don't mix icon libraries or visual styles.
6. **Accessible by default:** text/background contrast meets WCAG AA (4.5:1 for body text), readable sizes on phones and on the projector, and colour never the *only* signal.
7. **Changes go through the source.** To change a colour or font, update the theme/brand sheet, and it flows everywhere. Then update the deck to match.
8. **Before submitting, do a consistency pass:** put the app, the deck and the README side by side. Same logo, colours, fonts, name, tagline and terminology? Fix any drift.

## 2. Brand sheet (fill this in once, then link it everywhere)
| Item | Value |
|---|---|
| Product name (EN / AR) | |
| Tagline (EN / AR) | |
| Logo files (light / dark / icon) | path: |
| Primary colour | |
| Secondary / accent colour | |
| Neutrals (background, surface, text, muted) | |
| Status colours (success / warning / error / info) | |
| Latin font + weights | |
| Arabic font + weights | |
| Type scale (headings / body / caption) | |
| Corner radius, spacing unit | |
| Icon set | |
| Image / illustration style | |
| Tone of voice (e.g. friendly, clear, respectful; Jordanian dialect or MSA in the UI?) | |
| Key terms glossary (feature names in EN / AR) | |

Theme file in code: `path:` · Deck template: `path:`

## 3. AI assistants
When generating any UI, slide, image, document or copy: **read the brand sheet and the theme file first, and use only those tokens, fonts, names and terms.** If something needed isn't defined (e.g. a new status colour), propose an addition to the brand sheet instead of inventing a one-off value.
