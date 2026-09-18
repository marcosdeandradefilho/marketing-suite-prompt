# design-premium.md — the visual language that reads "expensive" for a SALES page (2025/2026)

The premium 2026 language is *"cinematic, editorial e
ruthlessly restrained"*. The discipline rule: **one thing can be loud (color OR layout), never both.** Read
`anti-slop.md` alongside this (the negative space of these rules) BEFORE writing any CSS.

## Sales page ≠ institutional site
A sales page is LONGER, copy-first, CTA-repeated at every conviction block, proof-heavy, single-goal. "Content
first: you don't design before you have the copy." So the design SERVES the approved copy from Step 2; it makes
the copy scannable and the CTA inevitable, it never competes with it. Scannability floor: body ≥16px, line
40-80 chars, a paragraph every 3-4 lines, a subhead every 2-3 paragraphs.

## Hero of a sales page = Promessa → Prova → Ação on the same fold
1. **Headline promessa** understood in <3s ("[resultado] sem [dor]").
2. **Subhead** that wins the BELIEF (the como, pra quem, the transformation).
3. **Support visual** = a REAL screenshot/clip of the product, NEVER stock illustration ("pessoas colaborando").
4. **ONE primary CTA** (conflicting CTAs drop conversion hard).
5. **Proof glued to the CTA** (a logo strip in the hero base, or one strong line/depoimento beside the CTA, not
   buried below).
Two premium hero canvases: **(A)** a muted autoplay video loop (lazy, see motion §perf), or **(B)** a dark
mesh-aurora gradient. Over it: an expressive **serif-italic headline** (Instrument Serif) mixed with a tight
sans, a glassmorphic floating nav. The hero is the LCP element: keep it fast, never lazy-load the hero image.

## Typography (Google Fonts CDN, free for commercial use)
- **Display/headline:** Instrument Serif (italic, expressive — the AI-brand "serif obsession" look), Fraunces
  (variable: weight + optical-size), Newsreader, Spectral, Playfair Display (luxo). Used MAXIMALLY (fills the
  viewport). 
- **Body/UI grotesque:** Geist, Hanken Grotesk, Bricolage Grotesque, Space Grotesk, Plus Jakarta Sans, Manrope,
  Sora. Inter is acceptable as body only, NEVER as the only/headline font.
- **Rules:** at most **2 typefaces** (1 display + 1 body); the headline font ≠ the body font; generous
  line-height on body, tight on display. Proven pairings: Instrument Serif + Geist/Hanken Grotesk; Fraunces +
  Space Grotesk; Playfair Display + Manrope. Prefer variable fonts (one file, full hierarchy).
- Load zero-config: preconnect both origins + `&display=swap`, request only the weights used.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```
Always bake a system fallback so it renders if the CDN is down: `'Hanken Grotesk',-apple-system,'Segoe UI',Roboto,sans-serif`
(and `'Instrument Serif',Georgia,serif`).

## Color — dark-default OR niche-rich, ONE accent, 60-30-10
- ~3/4 of top SaaS use dark + 1 accent (Linear-roxo, Raycast-vermelho, Mercury-lime, Ramp-amarelo). For a
  non-tech sales page, a rich accent (gold, emerald, royal blue, terracotta) over muted neutrals (charcoal,
  off-white, warm beige) reads premium. Derive the accent from the user's brand color when given.
- **Total 3-5 colors. 60-30-10:** 60% neutral, 30% secondary, **10% accent reserved for CTAs + active states
  only** (scarcity = the accent only where you want action, so the eye learns "is here que eu clico").
- Premium ≠ pure `#fff`/`#000`: off-white + near-black slate (charcoal #0A0A0A–#1A1A1A) + ONE accent. Ship 3
  CSS custom properties so palette + a `.dark` toggle swap from one place:
```css
:root{ --c-dom:#FAF8F5; --c-sec:#1A1714; --c-acc:#C8962B; } /* niche accent, NEVER indigo/#6366f1 */
.dark{ --c-dom:#0F0E0C; --c-sec:#EDE8E0; --c-acc:#E0AE3C; }
```
> The accent is NEVER `#6366f1` indigo / violet / a `from-indigo→purple` gradient — the #1 AI-slop tell.

## Layout
- **Whitespace is the luxury signal.** 80-120px+ between sections. "Emptiness creates value."
- **Show the real PRODUCT** (clip/screenshot per feature), not icons or illustration. Biggest anti-generic lever.
- **Avoid the dead cliché "stack of centered cards."** Use an editorial asymmetric grid (1 big feature + 2
  small, alternating image/text rows) or a bento grid. Repeat ONE component for elegant density (Raycast).
- Optional **blueprint grid** (Vercel): 1px lines, opacity 10-20% ("almost subliminal"), 24px spacing, "+"
  corner markers, as a subtle background texture.
- 12-column structural base, content container ~960-1140px for the reading column (a sales page is a column,
  not a dashboard); full-bleed allowed for hero / proof / CTA bands.

## CSS values (mind the breakpoints)
- **Body:** 17-18px, **never <16px**. Line-height 1.5. Measure 70-80 chars max (`max-width: ~68ch` on prose).
- **Spacing rhythm 8px:** 8 / 16 / 24 / 32 / 40 / 48 / 64 / 96 / 128 (use tokens `--space-*`).
- **Touch target:** 44-48px min.
- **Reading column / page width:** 960-1140px.
- **Type scale by breakpoint (use clamp, don't hard-code):**
  - Mobile (≤480px): H1 30-38px, H2 24-28px, section padding 48-64px.
  - Desktop padrão (992-1439px): H1 40-52px, H2 28-40px, section padding 64-96px.
  - Ultra-wide (1440px+): H1 44-56px, H2 34-44px, section padding 96-128px.
```css
:root{ --step-0:clamp(1rem,.95rem+.3vw,1.125rem);
       --h2:clamp(1.6rem,1.2rem+1.6vw,2.5rem);
       --h1:clamp(2.1rem,1.4rem+3.2vw,3.5rem); }
h1{font-size:var(--h1);line-height:1.05;letter-spacing:-.02em}
```

## Texture / grain (anti-flat-AI, pure CSS/SVG, zero asset)
Layer an inline-SVG `feTurbulence` grain over flat colors/gradients at low opacity (kills the "plastic AI
gradient" look). See `motion-efeitos.md` §grão for the exact snippet. Also tasteful: a subtle mesh of 2-3 soft
radial-gradient blobs (low saturation), glassmorphism cards (sparingly), `clip-path` geometric accents.

## Reference moves to steal (named brands)
- **STRIPE** — gold standard long-form; rich info tamed by type hierarchy + whitespace.
- **LINEAR** — opens with how the product FEELS, not what it does; restraint below the fold.
- **VERCEL** — blueprint grid + Geist + monochrome with 1 accent.
- **RAMP** — bold color tamed by a conservative layout.
- **RAYCAST** — elegant density via one uniform component; mono-color illustration.
- **RAMIT SETHI** (sales-page specific, premium-that-converts) — clean design lets the copy lead; lists each
  objection in the reader's exact voice; massive proof (many video testimonials on one page). Steal the
  objection-in-the-reader's-voice move and the proof density.

The four signals that make it look CARO: (1) radical whitespace, (2) restricted 3-5 color palette, (3)
intentional typography (≤2 faces, weight contrast, generous leading), (4) subtle motion WITH purpose (1-2
animations + the reduced-motion gate). "One or two well-placed animations differentiate more than a fireworks
show."
