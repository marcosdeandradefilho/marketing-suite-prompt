# tecnica-render.md — build order, the self-quality render loop, a11y/perf checklist, deploy

This file is the engine of "qualidade absurda": you don't just generate the page, you RENDER it, LOOK at it,
critique it against the slop/IA checklists, and regenerate until it's genuinely premium.

## Output folder convention (zero-config, deployable)
```
pagina-<slug-produto>/
  index.html                      # root (required by every host) — the sales page
  politica-de-privacidade.html    # LGPD base (separated consents, legal basis, rights)
  obrigado.html                   # optional thank-you/confirmation page (lead capture / post-checkout)
  assets/css/styles.css
  assets/js/main.js               # motion + reduced-motion gate + sticky CTA + FAQ + cookie banner
  assets/pix.js  assets/qrcode.js # ONLY if a Pix box is included
  img/                            # screenshots/photos (placeholders + TROCAR markers)
  og-image.jpg                    # 1200x630 (or a marked placeholder)
  favicon                         # inline-SVG favicon is fine (wordmark initial), marked trocável
  README.md                       # deploy + where to paste checkout link/pixel/OG (PT-BR)
```
No package.json, no build, no node_modules. CDN `<script src>`/`<link>` only. Forward slashes. Keep total < 50MB
(Netlify Drop). Write files incrementally so an interruption leaves a usable partial.

You MAY inline all CSS/JS into a single self-contained `index.html` instead of separate files. That makes the
headless render trivially reliable (no relative-path fetches) and the file portable. For a sales page that's
often the better call. If you split into assets/, the render still works from `file:///` because they're
same-origin relative files (unlike base64-only PDF rendering). When in doubt for the render step, inline.

## Build order (Step 3-4 of SKILL.md)
1. `<head>`: lang=pt-BR, title, meta description, Open Graph (5 tags) + twitter card, favicon, font preconnect +
   `<link>` (only used weights, display=swap), the `<script>documentElement.classList.add('js')</script>`, the
   Meta Pixel slot comment. Inline critical above-the-fold CSS for first paint.
2. Design tokens: the 3 palette custom props (60-30-10) + `.dark`, the fluid type scale (clamp), spacing tokens.
3. Sections in the approved order (hero → ... → P.S.), semantic landmarks (one `<main>`, one `<h1>`, h2/h3
   hierarchy), `.reveal` on sections, real copy (no lorem, no placeholder text except marked TROCAR).
4. Conversion components (`componentes-conversao.md`): CTAs + sticky mobile bar, offer/pricing, proof (real or
   marked), FAQ (ARIA), ethical countdown only if real, comparison table if useful.
5. BR lock-in (`compliance-br.md`): cookie banner, form with separated consents, footer with CNPJ/Decreto fields,
   politica-de-privacidade.html.
6. Motion JS (`motion-efeitos.md`): the reduced-motion gate, the `.js` baseline, IntersectionObserver reveals,
   the GSAP `if(window.gsap)` block, sticky-CTA observer, FAQ toggles, cookie banner logic. All `defer`.
7. Pix box only if asked (run `assets/pix.js`).

## The headless browser (detect, first that exists)
**Windows:** `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` → `C:\Program Files\Microsoft\Edge\Application\msedge.exe` → Chrome paths.
**macOS:** `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` → Microsoft Edge → Chromium.
**Linux:** `google-chrome` / `chromium` / `microsoft-edge`.
Narrate plainly: *"Gerando um preview pra eu conferir o visual..."* — never expose the binary path/flags.

## The SELF-QUALITY LOOP (render → LOOK → critique → regenerate) — make-or-break
**MOBILE IS NON-NEGOTIABLE.** Most sales-page traffic (WhatsApp + Meta) opens on a phone, so you render and LOOK
at BOTH widths. Skipping the mobile render is the #1 way this skill ships a broken page (a desktop-only
layout that breaks on the phone, where most traffic is). Render order:
1. **Mobile first (390px wide)** — a true phone width. Render full-page AND a one-screen capture:
   ```
   <browser> --headless=new --disable-gpu --hide-scrollbars --window-size=390,8000 "--screenshot=<abs>/preview-mobile.png" "file:///<abs>/index.html"
   <browser> --headless=new --disable-gpu --hide-scrollbars --window-size=390,844  "--screenshot=<abs>/preview-mobile-1.png" "file:///<abs>/index.html"
   ```
   On the mobile shot CHECK: headline fits and is readable, CTAs are full-width and tappable, nothing overflows
   horizontally, the offer/price is large, the comparison table scrolls (not squished), spacing is sane.
2. **Desktop (1440px wide)** — full-page PNG (and a PDF if you want page-by-page reading):
   ```
   <browser> --headless=new --disable-gpu --hide-scrollbars --window-size=1440,7800 "--screenshot=<abs>/preview-desktop.png" "file:///<abs>/index.html"
   <browser> --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=<abs>/preview.pdf" "file:///<abs>/index.html"
   ```
   For colors/backgrounds to survive the PDF, set `-webkit-print-color-adjust:exact; print-color-adjust:exact` on `body`.
   (Windows note: if Edge writes "Acesso negado" to a OneDrive/Desktop path, render to a temp dir without spaces and copy back.)
   (To inspect a long page section-by-section, crop the PNG; in PowerShell avoid naming a variable `$h` AND `$H` — they collide, every crop comes out full-height.)
2b. **Confirm it rendered** (file exists, PNG > ~10KB / PDF starts with `%PDF-`). If not, don't claim you looked.
3. **LOOK** (Read the preview.pdf pages / the preview.png) and run all three gates:
   - **Anti-slop** (`anti-slop.md`): count the 15 tells on the actual render. 5+ = FAIL. Watch especially for
     left-colored-border cards, 3 identical centered cards, indigo/purple, Inter-everywhere, emoji, centered
     hero+2 buttons, fake faces.
   - **Anti-IA-writing** (`anti-ia-escrita.md`): Grep the HTML for `—`/`–` and the blacklist vocabulary; check
     sentence-length variety; no income/hype/fake-scarcity phrasing; no printed stats (`compliance-br.md`).
   - **Contrast/a11y** (`anti-slop.md` §contrast gate + the checklist below): the dark-text-on-dark / accent-CTA
     pairs pass AA.
4. **Regenerate** the specific problems (a section, the palette, a headline) and re-render. Repeat until premium.
   Cap ~3 iterations; keep the best version. Narrate each pass plainly ("o preview ficou genérico no hero, vou
   trocar o layout e gerar de novo").
5. **No headless browser found:** say so honestly, deliver the self-contained page, and tell the user to open
   `index.html` and check it. NEVER claim you audited a render you couldn't run.

## A11y / SEO / perf checklist (verify on the built page)
- `<html lang="pt-BR">`, one `<main>`, one `<h1>`, correct h2/h3 order, landmarks.
- Every `<img>` has `alt` (empty `alt=""` for decorative) + explicit `width`+`height` + `loading="lazy"` below the fold (NOT the hero).
- Every interactive element has a visible `:focus-visible`; tab order logical; the FAQ/cookie/menu work by keyboard; Esc closes.
- Contrast AA on all text + the CTA.
- `prefers-reduced-motion` gate present; JS-off baseline shows content; page works if GSAP/Lenis CDN fails.
- `font-display:swap` + preconnect; `<script defer>`; hero not lazy-loaded; CLS-safe images.
- Open Graph 5 tags + title + meta description; favicon; the Meta Pixel slot comment.
- Grep the final HTML: zero `—`, zero `lorem`, zero unfilled `{{TOKEN}}` except the intentional `{{LINK_CHECKOUT}}`/`{{URL_FINAL}}` (documented in README).
- **CSS `clamp()`/`calc()` MUST have spaces around `+` and `-`** (`clamp(2.6rem, 1.5rem + 4.5vw, 5.2rem)`, never `1.5rem+4.5vw`). Without the spaces the expression is INVALID and silently falls back to the browser default size, so the headline/price render tiny even though the CSS "looks" big. This was a real v1.0.x bug: the hero headline and the price both collapsed to UA defaults. After building, grep the CSS for `rem+`, `vw+`, `px+`, `em+` (and `+rem`/`+.`) and fix any hit; then confirm on the render that the H1 clearly dominates the lead and the price is the largest text in the offer card.
- **Don't trust gradient-clipped text for critical numbers.** `-webkit-background-clip:text;color:transparent` on the price/headline can render invisibly or thin in some engines. For the price use a SOLID color, large `font-size`, and verify it on the render.
- **Price `R$`+number: beware CLASS-NAME COLLISIONS, and verify on the REAL page (never an isolated test).** Real v1.0.x bug the user caught repeatedly: the `R$` span got `class="cur"` — the SAME class used for the blinking terminal cursor in the hero (`.cur{display:inline-block;width:8px;...}`). The `R$` inherited `width:8px`, so the symbol overflowed its 8px box and printed ON TOP of the `1`. No `gap` or alignment tweak could fix it because the cause was the collision, not spacing. Lesson 1: never reuse a generic class name (`.cur`, `.num`, `.price`, `.bar`, `.tag`) for two different elements — give the currency its own (`.rs`). After building, grep the CSS for any class used on both a decorative/utility element and a content element. Lesson 2: an ISOLATED render of just the price LIES — it lacks the page's other CSS so it hides collisions; ALWAYS confirm the price on a crop of the FULL real-page render, with vertical margin so the crop doesn't distort the symbol's position. Lesson 3 (milder, separate): align the `R$` by `baseline` not `flex-end` — with `line-height<1`, flex-end floats the small symbol to the number's vertical middle.
- **Decorative big number/word goes in its OWN space or is part of the sentence**, never a faint layer behind a heading (it makes the heading unreadable). Prefer "16 skills que..." (the number leads the real sentence) over a giant orphan "16" floating behind text.

## Deliver (Step 5)
Write/update `.claude/clientes/<slug>/brand.md` (palette hex, fonts, logo path, WhatsApp, Pix key, confirmed
copy) for the next run. Then, in PT-BR:
- **Publish:** Netlify Drop (drag the folder → instant URL), or paste into the Hotmart/Kiwify custom-page editor,
  or GitHub Pages, or send the ZIP. All need `index.html` at the folder root.
- **The TROCAR checklist:** paste the real checkout link where `{{LINK_CHECKOUT}}` is, paste the Meta Pixel,
  swap the OG image, add real depoimentos/prints, fill the CNPJ/razão social/encarregado in the footer + privacy
  page, swap placeholder product screenshots.
- **The honest receipt:** what you verified (rendered + looked, contrast checked, zero travessão, no income
  claims) and what the user still needs to test in the real world (live CDN load on the user's net, real mobile devices, the OG preview in
  WhatsApp, the real checkout, the page under live traffic). Never fake coverage.
- **Re-run reason:** "roda de novo pra gerar a versão fria pro Meta Ads, trocar a oferta/preço quando o lote
  virar, refazer pra outro produto, ou atualizar a prova social." Offer the next handoff
  (`/site-institucional`, `/mcp-meta`).
