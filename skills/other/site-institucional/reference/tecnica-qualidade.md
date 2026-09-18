# tecnica-qualidade.md — production quality for a zero-build static site

What separates a deliverable site from a toy: semantics, responsiveness, accessibility, performance,
SEO, and a clean folder. Sources: MDN, web.dev/Core Web Vitals, WCAG 2.1/2.2, Netlify/GitHub Pages docs.

## Semantic HTML5 (landmarks carry implicit ARIA roles)
`<header>`=banner · `<nav>`=navigation · `<main>`=main (**exactly ONE per page**) · `<aside>`=complementary ·
`<footer>`=contentinfo · plus `<section>`/`<article>`. Screen-reader users jump between landmarks + headings,
so a correct heading hierarchy (one `<h1>`, then `<h2>`/`<h3>`) is non-negotiable. Only treat a `<section>`
as a landmark if you give it an accessible name (`aria-label`/`aria-labelledby`).

## Navigation / header spec (CRITIC FIX — don't skip)
- **Sticky header:** `position:sticky; top:0; z-index:50;` add a `backdrop-filter:blur()` + bg on scroll
  (toggle a `.scrolled` class via a scroll listener or IntersectionObserver sentinel).
- **Anchor offset:** every in-page anchor target gets `scroll-margin-top: <header-height>` so the sticky
  header doesn't cover the heading on jump.
- **Smooth scroll:** CSS `html{ scroll-behavior:smooth; }` as the no-JS baseline; Lenis upgrades it when
  present — BOTH gated by `prefers-reduced-motion` (set `scroll-behavior:auto` under reduce).
- **Scrollspy active link:** IntersectionObserver on each section → toggle `aria-current="true"` / `.active`
  on the matching nav link.
- **Mobile hamburger:** a real `<button>` (not a div) with `aria-expanded` toggled true/false,
  `aria-controls="<menu-id>"`, `aria-label="Menu"`, full keyboard operability, visible `:focus-visible`.
  Close on Esc and on link click.

## Responsive (mobile-first)
Fluid type with `clamp(min, preferred+vw, max)` instead of stacked font-size media queries (smooth, no
jumps, a11y win). Use **container queries** (`@container`) when a component's layout depends on ITS container
(e.g. a card in a sidebar vs full width); media queries for page-level shifts. Test at common breakpoints
(~360 / 768 / 1024 / 1280). Touch targets ≥ **44×44 CSS px** (WCAG 2.5.5; 48 better; WCAG 2.2 minimum 24×24).

## Accessibility (WCAG 2.1/2.2 AA)
Contrast: normal text ≥ **4.5:1**; large text (≥18pt / 24px, or ≥14pt/18.66px bold) ≥ **3:1**; non-text UI/
graphics ≥ 3:1. Focus Visible (2.4.7): every interactive element has a visible indicator — use
`:focus-visible`, never `outline:none` without a replacement; WCAG 2.2 wants ≥2px-thick, ≥3:1 contrast.
Every `<img>` has `alt` (empty `alt=""` for decorative). Respect `prefers-reduced-motion` (see
`motion-efeitos.md`).

## Performance / Core Web Vitals (targets at 75th pct: LCP ≤2.5s · INP ≤200ms · CLS ≤0.1)
- **CLS:** ALWAYS set `width` + `height` (unitless px) on every `<img>` — browsers derive `aspect-ratio`
  and reserve space even with `width:100%;height:auto`. Reserve aspect-ratio for embeds/maps too.
- **LCP:** optimize the hero element (image/heading); do NOT `loading="lazy"` the hero/LCP image.
- **Images:** responsive `<img srcset sizes>` (or `<picture>`), `loading="lazy"` below the fold,
  `decoding="async"`, modern formats (WebP/AVIF + JPEG fallback). 
- **Fonts:** `font-display:swap`; preconnect both Google origins; request only used weights; prefer variable
  fonts for 3+ weights. (Self-hosting woff2 + preload ≈ 180ms faster LCP + GDPR-safe = the premium upgrade;
  Google Fonts CDN + preconnect + swap = the zero-config default.)
- **JS:** `<script defer>` (or `type=module`, defers by default). Inline critical above-the-fold CSS for
  first paint; keep JS tiny so INP stays low.

## Layout pitfalls that the render loop catches (don't ship these)
- **`height:100%` on an `<img>` collapses it to invisible** inside a grid/flex cell of indefinite height
  (the most common "empty image box" cause). Size images with **`aspect-ratio` + `width:100%`** instead.
  If an image must fill a cell whose height is set by a sibling, make the cell `position:relative` and the
  image `position:absolute; inset:0; width:100%; height:100%; object-fit:cover`.
  ```css
  .figure img{ width:100%; height:auto; object-fit:cover; aspect-ratio:4/5; display:block; }
  /* image grid with a definite container so 1fr rows resolve and images fill: */
  .gallery{ display:grid; grid-template-columns:repeat(4,1fr); grid-template-rows:repeat(2,1fr);
            gap:.8rem; aspect-ratio:2/1; }
  .gallery img{ width:100%; height:100%; object-fit:cover; }
  ```
- **`decoding="async"` images can paint blank** in a one-shot render even when loaded — the render script
  forces decode before the screenshot, but on the live site keep `decoding="async"` (it's correct there).
- **Map iframe shows empty in a headless screenshot** — it loads live in a real browser; don't "fix" it,
  just note it. Give `.map-wrap` a subtle background so it's not a stark empty box before load.

## Menu / price list / dish list pattern (restaurants, salons, services)
A long list of items must read elegant, not like a spreadsheet. Three-tier hierarchy, generous space:
```css
.course-head h3{ font-family:var(--serif); font-size:var(--t-2); }   /* course/section, serif display */
.course-head .line{ flex:1; height:1px; background:var(--line); }     /* thin rule beside the header */
.dishes{ columns:2; column-gap:clamp(2.5rem,5vw,4.5rem); }            /* ONE or TWO columns max, never 3+ */
.dish{ break-inside:avoid; padding-bottom:1.5rem; }
.dish h4{ font-weight:600; font-size:var(--t-0); }                    /* dish name, body face */
.dish p{ color:var(--ink-2); font-size:.95rem; }                     /* short description, lighter */
.dish .price{ color:var(--accent); font-weight:600; }                /* price small & quiet, or omit */
```
On mobile drop to a single column. Build the REAL items (from the client/fetched page); never generic
"Entradas / Principais" placeholder cards for a restaurant — the real menu IS the site.

## SEO / social (head requirements)
`<title>` · `<meta name="description">` · `<link rel="canonical">` · viewport meta · favicon (see below) ·
`site.webmanifest`. Open Graph minimum 5: `og:title`, `og:description`, `og:image`, `og:url` (= canonical),
`og:type`. Twitter/X: `twitter:card=summary_large_image` (X falls back to OG). Add JSON-LD LocalBusiness (see
`lock-in-br.md`) + `sitemap.xml` + `robots.txt`. lang: `<html lang="pt-BR">`.

> **Never reference a file you didn't create** (a 404'd `og:image`/icon looks broken when shared/inspected).
> For `og:image` (1200×630): either generate `og-image.jpg` by rendering the hero band with the bundled
> tool — `node assets/render.js <site>/index.html <site>/og-image.jpg 1200 0 0 630` — OR point `og:image` at
> a real photo already in `/img` (e.g. the hero). Don't leave it pointing at a non-existent file.

## Required files (404 / favicon / robots / sitemap)
- **`404.html`** (CRITIC FIX — don't omit): branded, nav back home + the WhatsApp CTA.
- **`robots.txt`**: allow all + `Sitemap: <canonical>/sitemap.xml`.
- **`sitemap.xml`**: list each page URL.
- Favicon (zero-config, no raster needed): emit an inline-**SVG** favicon
  (`<link rel="icon" href="data:image/svg+xml,...">` with the wordmark initial on the brand color). Do NOT
  reference `favicon.ico`/`apple-touch-icon.png` unless you actually create them — a missing icon 404s. The
  `site.webmanifest` should then list the **SVG** icon (or no `icons` array), `name`/`short_name`/
  `theme_color`/`background_color` — keep it consistent with what exists on disk.

## Deploy (layperson, no build) — put in the site's README.md
1. **Netlify Drop** (app.netlify.com/drop) — drag the project FOLDER onto the drop zone → instant public URL.
   No account needed to test. Keep the deploy < 50MB; no single file > 10MB.
2. **GitHub Pages** — repo with `index.html` at the top level of the publishing source (root or `/docs`),
   enable in Settings → Pages → serves at `username.github.io/repo`.
3. **Vercel** — drag-and-drop exists but it nudges Git/CLI; Netlify Drop is friendlier for a leigo.
4. **Simplest handoff** — ZIP the folder and send to the client / their host.
All four require `index.html` at the folder root.

## Output folder convention (zero-config)
```
site-<slug-cliente>/
  index.html                      # root (required by every host)
  404.html
  politica-de-privacidade.html    # LGPD base
  (servicos.html sobre.html contato.html)  # only multi-page: advogado/contador or on request
  assets/css/styles.css
  assets/js/main.js
  assets/pix.js  assets/qrcode.js  # only if Pix box is included
  img/                            # photos (placeholders + TROCAR markers)
  favicon.ico  apple-touch-icon.png  site.webmanifest
  robots.txt  sitemap.xml
  og-image.jpg (1200x630)         # or a marked placeholder
  README.md                       # deploy instructions (PT-BR)
  ENTREGA-whatsapp.txt            # client handoff message
```
No `package.json`, no `node_modules`, no build config — CDN `<script src>`/`<link href>` only. Use forward
slashes in paths. Keep total deploy < 50MB (Netlify Drop). Write files incrementally so an interruption
leaves a usable partial site.
