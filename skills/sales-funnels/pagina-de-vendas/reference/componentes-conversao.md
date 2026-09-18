# componentes-conversao.md — conversion components (premium AND high-converting)

Each component below ships premium AND functional (focus
states, ARIA, validation). The numbers in the research are DIRECTIONAL benchmarks for YOUR build decisions; they
are NEVER printed on the page (see `compliance-br.md` §stats).

## Hero
Promessa → Prova → Ação on the first fold (see `design-premium.md` §hero). ONE primary CTA. Real product
screenshot/clip, never stock illustration. Proof glued near the CTA (logo strip or one strong line), not buried.

## CTA — optimization priority: COPY > placement > context > visual (don't start with color)
- **Color by CONTRAST, not a magic color:** "a high-contrast button beats a low-contrast one every time."
  Reserve ONE action color used only on buy buttons (the accent).
- **Copy:** 1st person + benefit ("Quero minha vaga", "Quero garantir o acesso"), never "Comprar"/"Enviar".
- **Size:** `min-height:48px; padding:16px 32px`; mobile `width:100%` in the thumb zone; desktop `width:auto`;
  label ≥17px bold. Too huge reads "pushy" (reactance).
- **Hover (desktop):**
```css
.cta{transition:transform .2s,box-shadow .2s}
.cta:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,0,0,.18)}
.cta:focus-visible{outline:3px solid var(--c-acc);outline-offset:3px}
```
- **Microcopy under the button** kills the last objection: "Pagamento único. Acesso imediato. [N] dias de garantia."
- **Repeat the CTA at pause points:** after hero, after proof, after the value stack, after FAQ, + the sticky
  mobile bar. ONE primary CTA per fold (no competing buttons).
- Wire the href to `{{LINK_CHECKOUT}}` and tell the user to paste the Hotmart/Kiwify/Cakto link (Step 5).

## Offer / pricing block
- **Anchor:** the "de R$X" struck-through, small (`font-size:1.2rem`, muted); the final price big (`~3rem`, bold,
  brand color); a "-NN%" chip in the corner. The "de" must be a REAL price (CDC, see compliance).
- **Value stack:** each item as a benefit ("16 skills que fazem o trabalho, template só lê", not "16 skills"),
  with an HONEST anchor value when you list one (alternative cost / real future price, never an invented total).
- **Single-tier vs tiers:** for a one-shot pagamento-único product, a single clear offer is honest and fine (a
  "value metric gate" / 3-tier SaaS framing is inapplicable — don't force tiers). If there ARE real tiers, a
  3-tier layout with the middle highlighted ("Mais Popular", only if true) + the target tier `transform:scale(1.04)`
  + a colored border converts well. The decoy move (cheap / target / premium) works only with real options.
- **Trust signals glued to the price/CTA:** garantia, "acesso imediato", "compra segura" (a cadeado/escudo SVG).
  Payment line: "à vista no Pix ou 12x de R$ XX no cartão".

## Proof / social proof
- **Card:** round photo 56px (or initials circle if no photo) + bold name + 1 line of context + the quote +
  optional 5 stars + optional real print. `alt` describing who it is.
- **Wall of Love:** a scannable grid that shows VOLUME, with an overall rating on top.
- **Raw WhatsApp/Instagram print** (unedited reads most authentic). A wall of real prints is gold.
- Place the strongest story right BEFORE a CTA.
- **No proof from the user → marked placeholder** (`<!-- TROCAR: depoimento real -->` + initials avatar). Never
  a fabricated face/name/number.

## FAQ accordion (ARIA APG pattern — functional, not decorative)
- Header = `<h3>` containing a `<button>` (not a `<div>`/`<a>`).
- Button: `aria-expanded="true|false"` (toggled on click) + `aria-controls="painel-ID"`.
- Panel: `<div id="painel-ID" role="region" aria-labelledby="botao-ID">`.
- Keyboard: Space/Enter toggles; the chevron icon is `aria-hidden="true"`; never `outline:none` without a
  replacement (`:focus-visible`).
- The FAQ doubles as an objection handler. Typical Qs: "Funciona no plano básico/PRO?", "Preciso ter
  experiência?", "Tem garantia?", "Como recebo o acesso?", "Serve pro meu caso?".

## Ethical countdown (only if real)
Tie it to a REAL server-anchored deadline (compute remaining time from a fixed target date in JS; it must NOT
reset on reload), on the SAME screen as the price, **max 1 scarcity surface per page**. Usually the lote→cheio
frame is enough and you don't need a timer at all. A timer that resets is a dark pattern (FTC) + CDC art. 37.

## Comparison table (você vs alternativas) — be honest
Rows = features, columns = alternatives, ✅/❌, YOUR column highlighted (border + brand color), sticky header on
scroll. Be honest (address the price objection too). Collapses on mobile to stacked cards or a horizontal scroll
with the "você" column pinned. Example axes: "[seu produto] vs fazer sozinho no YouTube vs contratar alguém" ×
"sem experiência / resultado de verdade / suporte / custo".

## Sticky mobile CTA bar
A fixed bottom bar on mobile with the price + the CTA, always visible:
```css
.sticky-cta{position:fixed;left:0;right:0;bottom:0;z-index:60;display:flex;gap:12px;align-items:center;justify-content:space-between;padding:10px 16px;background:var(--c-sec);box-shadow:0 -6px 24px rgba(0,0,0,.18)}
@media(min-width:768px){.sticky-cta{display:none}}
```
Show it after the hero scrolls out (IntersectionObserver on the hero). Keep the CTA tappable (≥48px).

## SEO / Open Graph head (the WhatsApp preview is part of the conversion)
The page is pasted in WhatsApp/Meta; a link with no OG card looks broken and loses clicks. Always emit:
```html
<html lang="pt-BR">
<title>...</title>
<meta name="description" content="...">
<meta property="og:title" content="..."><meta property="og:description" content="...">
<meta property="og:image" content="og-image.jpg"><meta property="og:url" content="{{URL_FINAL}}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,..."> <!-- wordmark initial, marked trocável -->
```
OG image 1200×630 (a marked placeholder if you can't generate one; tell the user to swap it). Add the Meta Pixel
slot as a clearly-marked comment in `<head>` so the user can paste their pixel for the Fase-2 Meta Ads:
`<!-- META PIXEL: cole aqui o seu código do Pixel da Meta (Gerenciador de Eventos) -->`.

## Checkout wiring (it must SELL, not just inform)
- Primary CTA href → `{{LINK_CHECKOUT}}` placeholder; instruct the user (Step 5) to paste their Hotmart/Kiwify/
  Cakto link. If they gave one, use it.
- Payment copy: Pix ("acesso imediato"), "12x de R$ XX", and Parcelamento Inteligente (Kiwify) framing when
  relevant ("parcele sem ter o valor todo no limite"). These DROP the financial objection.
- Pix QR box is OPT-IN/OFF by default (most sales pages send to a checkout, not a raw Pix). If asked, run
  `assets/pix.js` for a real EMV copia-e-cola + SVG QR; never a hand-made code (wrong CRC = dead string).
