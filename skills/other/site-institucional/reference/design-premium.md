# design-premium.md — the craft that reads "expensive and current" (2026/2027)

Expensive = **restraint + intention + craft in the details**. Cheap/dated = defaults left untouched
(default font, default centered layout, default 16px everything, default gradient, default stock photo).
A site looks expensive when every one of those was a deliberate choice. **Pick a lane and commit** — a
confidently minimal site beats a timid maximal one. Then RENDER it and check it against the rubric in
`revisao-visual.md`; read `anti-slop.md` for the negative space of these rules.

## Typography (all free Google Fonts)
**Display / headline serifs (the "expensive" signal):** Fraunces (variable, opsz — the strongest single
pick), Playfair Display (classic luxury), Cormorant Garamond (high-fashion, only ≥24px), EB Garamond,
Newsreader, Instrument Serif (one-line hero). **Body / UI grotesque-sans:** Hanken Grotesk (best free
workhorse), Plus Jakarta Sans, DM Sans, Space Grotesk, Bricolage Grotesque (can do both heading+body),
Geist, Familjen Grotesk. **Mono accent (eyebrows/labels):** Space Mono, IBM Plex Mono.
**AVOID as headline:** Inter, Roboto, Poppins, Open Sans, Lato — the AI-tell faces. Inter is OK as body
but never the only/headline font.

**Pairings (serif display + grotesque body — contrast of voice):** Fraunces + Hanken Grotesk
(hospitality/wellness), Fraunces + Inter (tasteful neutral), Cormorant Garamond + Karla (luxe/spa),
Playfair Display + Lato (classic), Newsreader + Geist (editorial), EB Garamond + Space Grotesk. Prefer
ONE expressive serif + ONE clean sans. Three families only if the third is a mono accent.

**Exact numbers:**
- Body **18px** (`clamp(1.05rem, …, 1.18rem)`); 16px is the floor. Sub-16px body = instant amateur tell.
- Line-height: body **1.5–1.65**; headings **1.05–1.2** (tighter as size grows).
- Type scale ratio **1.25** (restrained) to **1.333** (editorial contrast). Hero headline = 3–5× body.
- Tracking: large display headings **−0.02em** (tightening big serifs is what makes them look "set");
  body **0**; all-caps eyebrows/labels **+0.06em…+0.12em**. Never widen lowercase body.
- Measure: cap body columns to **60–75ch** (`max-width:65ch`). Full-width body text is a top amateur tell.
- Weights: a real range (400 body / 500 emphasis / 600 headings). Large display serifs often best at 400–500.

```css
:root{
  --t-0:  clamp(1.05rem, 1rem + .2vw, 1.18rem);     /* body ~18px */
  --t-3:  clamp(2rem, 1.5rem + 2vw, 3.4rem);        /* section title */
  --disp: clamp(2.8rem, 1.7rem + 5.6vw, 6rem);      /* hero display */
}
body{ font-size:var(--t-0); line-height:1.6; }
.prose{ max-width:65ch; }                            /* never full-width body */
h1,.display{ line-height:1.05; letter-spacing:-.02em; }
```

## Color — restraint + scarcity
Method (better than blindly "60-30-10"): **one neutral foundation** (off-white OR near-black, picked
per niche) + **a second deeper neutral** for surfaces/borders + **exactly ONE accent** on actions/links
only (< 10% of surface). Tint the neutrals slightly toward the accent's hue so the palette feels
coordinated, not "grey + a random bright button."

**Never pure `#fff`/`#000`** — that flatness is a cheap tell. Use tinted values:
- Light bg (warm): `#FBF6EE` / `#FAF9F6` / `#F7F3E8`. Cool: `#F8FAFC`.
- Ink on light: `#2A2420` (warm) / `#1A1A1A` / `#181818`. Body text often softer at `#33302B`.
- Dark bg: `#14110E` (warm) / `#0E0E10` (cool) — never `#000`. Surface one step up: `#1C1714`.
- Text on dark: `#EDE9E1` / `#E8E6E1` — slightly off-white, never `#fff`.
- Borders/dividers: hairline `1px` at low opacity — `rgba(0,0,0,.08–.12)` light, `rgba(255,255,255,.10)` dark.
  Hairlines read far more premium than solid grey lines.

Wire the palette as CSS custom properties so it swaps from one place (and supports a `.dark` toggle):
```css
:root{ --paper:#FBF6EE; --ink:#2A2420; --ink-2:#6B6055; --accent:#7E2233; --line:rgba(42,36,32,.14); }
.dark{ --paper:#14110E; --ink:#EDE9E1; --ink-2:#B7AC99; --line:rgba(237,233,225,.12); }
```
> **The accent is NEVER indigo/violet/purple or a `from-indigo→purple` gradient** — the #1 AI-slop tell.
> Derive it from the brand color or the niche hint. Tasteful gradients = two near-identical tones, low
> angle (`#FBF6EE → #F2EFE9`); or one soft low-saturation radial glow matching the accent. A subtle grain
> overlay (~3–6%) over flat color kills the "sterile AI" look.

## LIGHT vs DARK (decide per niche — see `arquitetura-nichos.md`)
**Default LIGHT.** Light + warm = appetite/trust/freshness/legibility (restaurants, wellness, dental,
local, most B2B). **DARK** only when the brand is about mystery/luxury/the-product-glowing-in-a-spotlight
(fine dining/cocktail, barbershop, strength gym, luxury, agency/portfolio). Dark done plainly looks cheaper
than light done plainly — if unsure, go light. Offer a dark TOGGLE elsewhere; don't make dark the base
unless the niche calls for it.

## Layout & spacing (where amateur dies)
- **8px scale only:** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128. Random `13px`/`27px` = amateur.
- **Section padding (vertical): 96–160px desktop / 56–80px mobile.** Generous section padding is the #1
  thing separating pro from template. When in doubt, double the whitespace.
- Container max-width **1180–1280px**; page gutters ≥ desktop 64 / mobile 20–24 (don't let content touch
  the edge unless intentional full-bleed). Body column capped separately at ~65ch.
- Vertical rhythm: small gap heading→paragraph (8–16px), big gap between groups (32–48px). Proximity groups.
- **Composition:** move beyond center-stacked. 12-col grid with uneven spans (image cols 1–7, text 8–12);
  alternating image/text rows; bento grids of varied sizes for services (not 3 identical icon cards);
  intentional full-bleed for hero/statement images. Asymmetry must still align to an underlying grid.

## Hero patterns that look expensive
1. **Full-bleed image/video + restrained overlay** — great photo edge-to-edge, a scrim gradient for
   legibility, headline bottom-left, ONE CTA. (Best for restaurants, hospitality, architecture.)
2. **Editorial split** — oversized display headline left (cols 1–6), full-bleed photo right bleeding off-edge.
3. **Type-first** — one oversized variable-serif headline carries it, tiny mono eyebrow above, huge whitespace.
Concrete: headline ≤ 8 words at `--disp`, tracking −0.02em, line-height ~1.05; ONE primary CTA (a second
ghost link max); generous top padding so it's not jammed under the nav. The hero is the LCP — keep it fast
(don't lazy-load the hero image). **AVOID:** centered text + 2 buttons on light-grey, a slider/carousel,
multiple competing CTAs, generic stock hero, emoji in the headline.

## Imagery treatment (see `refazer-e-imagens.md` for the zero-config Pexels source)
One genuinely great image beats five mediocre ones. **Consistency of grade is the editorial secret** —
all photos share warmth/contrast/crop logic. Commit to a small set of aspect ratios (3/2, 4/5, 16/9, 1/1)
and reuse them. Full-bleed for hero/statement; contained with margin for supporting images; let some bleed
off one edge. A duotone/monochrome grade tied to the palette unifies mismatched sources. Caption images with
a small all-caps tracked eyebrow for an editorial feel. **Empty + intentional beats filled + generic** — but
never a literal empty box (verify every image renders; see the aspect-ratio pitfall in `tecnica-qualidade.md`).

## Trend status (2026/2027)
- **Use:** light-first warm palettes, oversized expressive + variable type, editorial asymmetry, bento grids,
  grain/texture overlays, tasteful scroll reveals/parallax, real photography with a consistent grade, one
  confident accent, big whitespace, dark mode as an option.
- **Avoid (dated/cheap):** purple/indigo gradients, everything centered + rounded, glassmorphism everywhere,
  heavy soft shadows on every card, autoplay carousels, slow preloaders/splash, neumorphism, emoji icons,
  stock handshake/team-at-laptop photos, sub-16px full-width body.

## Quick-start expensive baseline (safe default for the generator)
```
Fonts:    Fraunces (headings) + Hanken Grotesk (body)
Body:     18px / lh 1.6 / max 65ch / left-aligned
Headings: lh 1.05, tracking -0.02em, weight 400-500 serif / 600 sans
Scale:    1.25
Bg:       #FBF6EE warm light  (or niche dark #14110E only when the niche calls for it)
Text:     #2A2420 on light    /    #EDE9E1 on dark
Accent:   ONE, brand/niche — NOT blue/purple — reserved for CTAs (<10% surface)
Borders:  1px @ rgba(42,36,32,.12)
Spacing:  8px scale → 8/16/24/32/48/64/96/128 ;  section padding 96-160px desktop
Max-w:    1180px container, 65ch text
Motion:   fade+rise 16px, ~600ms ease-out-expo, stagger 60ms, respect reduced-motion
```
