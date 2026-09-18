---
name: site-institucional
description: >-
  Cria um site institucional completo e profissional (HTML/CSS/JS pronto pra publicar), bonito de
  verdade e moderno (2026), a partir de pouca informação — pra você ou pra um cliente. A skill PESQUISA
  referência do nicho, monta com foto real, e RENDERIZA o próprio site pra revisar no olho antes de
  entregar. Use quando a pessoa quer criar, fazer, montar ou refazer um site institucional, um site pra
  empresa, um site pro cliente, presença online de um negócio, ou pegar um site velho/feio e deixar
  profissional. Gatilhos: "preciso de um site", "cria um site", "faz um site institucional", "site pra
  minha empresa", "site pro meu cliente", "quero um site profissional", "refaz esse site", "deixa esse
  site mais moderno", "site institucional", "site-institucional". NÃO é pra página de vendas/landing de
  lançamento de infoproduto (isso é a /pagina-de-vendas).
argument-hint: "[nicho/empresa + WhatsApp, ou a URL de um site pra refazer, ou deixe vazio]"
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch, WebSearch, AskUserQuestion
effort: high
model: inherit
---

# Site Institucional

You generate a COMPLETE, genuinely beautiful, current (2026/2027) institutional website (zero-build
HTML/CSS/JS) the user can deploy or hand to a client — from minimal input. Everything the user sees is
**Brazilian Portuguese, direct, anti-guru**: no hype, no time-to-money promises, R$ never a bare `$`.

**The output IS the product, and the bar is: a client would happily pay for it and it beats whatever they
had.** Two non-negotiables make that real and separate this skill from a generic generator:
1. **It matches the niche** — you reference how real, good sites in that industry look (light vs dark,
   palette, type, the ANCHOR section) instead of dropping one template on everything.
2. **You SEE it before you ship it** — you render the site to an image, look at the pixels, grade it
   against a rubric, and fix what's ugly. Code that validates can still look cheap; only your eyes catch that.

This file is the orchestrator. Read each reference file WHEN you reach the step that needs it (progressive
disclosure — do NOT read them all up front):
- `reference/referencias-visuais.md` — **SEE ≥5 real, current reference sites before designing (the LOOK comes
  from here). Mandatory, every niche.** Uses `assets/referencias.js` to screenshot live URLs you then read.
- `reference/arquitetura-nichos.md` — the niche's FUNCTIONAL spine (the ANCHOR section, BR trust seals,
  structure, the menu pattern) + a fallback look when the web is down. NOT the primary look driver anymore.
- `reference/design-premium.md` — the 2026 craft with concrete numbers (type/color/spacing), light-first rule.
- `reference/anti-slop.md` — the forbidden AI-slop cluster + the premium alternative for each.
- `reference/revisao-visual.md` — **the render→look→fix loop + the 15-point rubric. The make-or-break step.**
- `reference/refazer-e-imagens.md` — the rebuild-from-URL path + the REAL Pexels imagery strategy (no key).
- `reference/motion-efeitos.md` — layered motion tiers, CDN tags, the mandatory reduced-motion + JS-off gates.
- `reference/lock-in-br.md` — WhatsApp float, BR footer, LGPD banner, Pix box, Maps, backend-free form, JSON-LD.
- `reference/tecnica-qualidade.md` — semantic/responsive/a11y/perf/SEO, the layout pitfalls, the menu pattern.- `assets/referencias.js` — bundled batch screenshotter for live REFERENCE sites (Step 1.5).
- `assets/render.js` — bundled zero-config screenshot of YOUR built site, for the visual review (Node + Chrome/Edge).

## Non-negotiable rules (read before anything)
1. **Design from real, current references you actually SAW — never from a template.** Before designing, run
   Step 1.5 (`referencias-visuais.md`): find and SCREENSHOT ≥5 current, beautiful sites in the niche and LOOK
   at them; pull the 2026 design language from what you see. Then apply the craft in `design-premium.md` +
   `anti-slop.md`: editorial/asymmetric layout, real serif+grotesque pairing, ONE confident accent, tinted
   neutrals (never `#fff`/`#000`), generous whitespace, real photography. Beautiful and current, never dated.
2. **Default LIGHT; match the niche.** Most niches want a light, warm base. Dark is opt-in ONLY for the niches
   that call for it (steakhouse/bar, barbershop, strength gym, luxury, agency/portfolio — see
   `arquitetura-nichos.md`). Never default to a dark "premium template."
3. **Lead with the ANCHOR.** Each niche has ONE thing its site is about (restaurant = the MENU + food photos;
   architect = the PORTFOLIO; lawyer = RESULTS/credibility; clinic = BEFORE/AFTER). Feature it prominently.
   The anchor content must be REAL — so if it's essential and not provided (a menu, a price list, projects),
   **ask for it (or the site URL) in the intake.** If still unavailable, build the anchor's real STRUCTURE
   (the layout, the course/section headers, realistic SAMPLE rows clearly marked `<!-- TROCAR: confirme … -->`)
   so the client only swaps the text — never generic "Entradas/Principais" filler cards, and never present an
   invented specific (a real price, a claim) as if it were the client's. This reconciles with rule 6: an
   honestly-labeled placeholder row is fine; a fabricated fact stated as real is not.
4. **Real photos.** Use real, niche-true photography via Pexels (no key; download local) — see
   `refazer-e-imagens.md`. Never Picsum, never `source.unsplash.com`, never an empty image box.
5. **SEE it before you ship it (make-or-break).** After building, RENDER the site with `assets/render.js`,
   READ the screenshots (desktop + mobile + hero/anchor crops), grade against the rubric in
   `revisao-visual.md`, and FIX until it genuinely looks good (≥13/15, every image renders, mobile clean).
   If you couldn't render, say so honestly — never claim a visual review you didn't do.
6. **Never invent the client's real data.** Real services, prices, phone, address, hours, CNPJ come ONLY from
   the user / the fetched page. Unknown → a marked `<!-- TROCAR: ... -->`, never a fabricated fact.
7. **Zero-config output.** Pure HTML/CSS/JS + CDN `<script src>`/`<link>` + local images only — no npm, no
   build, no API key. It opens by double-clicking `index.html`. (`node` + a browser are used only for YOUR
   review and for downloading photos — not required for the site to run.)
8. **Motion degrades safely.** Always emit the reduced-motion JS gate AND the `.js`-class baseline so JS-off
   users and crawlers see full content. Animate transform/opacity only.
9. **BR lock-in is first-class.** Floating WhatsApp (or tel: when the business only takes calls), footer with
   CNPJ/endereço/horário, LGPD cookie banner, contact path that works with no backend. Pix box OFF by default.
10. **Anti-guru tone always.** No time estimates, no income promises, no hype. R$ only; foreign price as `US$`.

## Step 0 — Detect the path + scope (silently)
- **REBUILD** — a URL is present, or "refaz / melhora / moderniza esse site." → Step 0.5.
- **NEW** — everything else (a niche, a business, "cria um site pra…"). → Step 1.
- **SIMPLE override** — "site simples / básico / rápido" → still beautiful + light, drop Tier-2 motion and
  heavy effects; keep it fast and tasteful. Note it in one line.
Off-topic / an infoproduct sales funnel → say plainly this builds institutional sites and point to
`/pagina-de-vendas`. Never refuse for lack of input.

### Step 0.3 — Reuse brand context
`Glob .claude/brand-kit-freelancer.md` (skill-07) and `.claude/clientes/<slug>/brand.md`. If found, Read and
REUSE silently (name, contato, Pix key, cores, fonte, prior client data). On a re-run, surface "o que mudei",
not a byte-identical reprint.

### Step 0.5 — REBUILD path
Read `reference/refazer-e-imagens.md`. WebFetch the URL with a verbatim-extraction prompt (every service/dish,
price, phone, address, hours, social link, headings, copy). **Capture the ANCHOR content** — for a restaurant
the menu is often a separate page/PDF; fetch it too or ask, because a rebuild without the real menu is worse
than the original. On a cross-host redirect re-call once. If empty/blocked/JS-only → ask the user (PT-BR) to
paste the content; NEVER scrape elsewhere or invent. Detect the niche, keep ALL real content, rebuild via
Steps 2–6. Colors/fonts usually aren't extractable → ask or propose from the niche; never claim a "detected"
palette you guessed.

## Step 1 — Intake (minimal questions) + reference the niche
Read `reference/arquitetura-nichos.md`.
- Niche clear from the message → proceed; don't interrogate. BUT if the niche's ANCHOR content is essential
  and missing (menu/prices, project portfolio, case results), it's fine to ask ONE focused thing for it —
  *"me manda o cardápio (ou o link do site) que eu coloco os pratos de verdade; senão monto com exemplos
  marcados pra você trocar."* — rather than silently shipping sample rows.
- Empty/zero-arg → ONE consolidated `AskUserQuestion` (fixed options + free-text rider): nicho · nome ·
  WhatsApp (com DDD) · cidade. In the chat add: *"Se quiser, me manda a cor da marca e um logo — senão eu
  escolho uma paleta que combina com o nicho e tu troca depois."*
- Niche refused/unknown → the **neutral "negócio local"** template (light, warm, safe non-purple palette).
Narrate up front (PT-BR, plain): *"Vou montar o site agora — vou te contando o que tô fazendo. No fim te
explico como publicar e o que trocar."*

## Step 1.5 — SEE real current references BEFORE designing (mandatory, every niche) — read referencias-visuais.md
The LOOK comes from real, current, beautiful sites you actually LOOK AT — not from memory or a template.
Run this on EVERY build:
1. `WebSearch` for 6–8 candidate references — mix **showcase/gallery/listicle pages** (*"melhores sites de
   <nicho> 2026"*, awwwards/godly/behance/dribbble/land-book, "best <nicho> websites" roundups — these show
   many curated current designs and rarely bot-block) **+ named real top sites** in the niche.
2. Screenshot them in one launch: `node "<SKILL>/assets/referencias.js" "<SITE>/_refs" 1600 <urls…>` (use a
   tall band ~5000 for a listicle to see many designs at once). It flags `OK` vs `BLANK/BLOCKED` (bot-walls,
   SPA loaders).
3. **READ each `OK` PNG with vision** — note base (light/dark), palette, type, hero/layout, imagery treatment,
   the "current/expensive" cues. Get **≥5 usable references SEEN**; if fewer loaded, add listicle/gallery URLs
   and re-run. Tell the user (PT-BR) which references you looked at and the pattern you saw.
4. Also `WebSearch site:pexels.com <niche subjects>` for the real photos (hero + anchor + gallery + portraits).
5. **Synthesize a 4-line brief** from what you SAW: BASE (light/dark + why) · PALETTE (3 hex + accent) ·
   TYPE (display + body) · ANCHOR + section order · the photo shortlist. Design Step 2 against it. Don't clone
   one site — synthesize the shared current language and adapt to the client's brand/content.
Only if the web is truly down do you fall back to the encoded niche DNA (`arquitetura-nichos.md`) — and say so.
That file is now the niche's FUNCTIONAL spine (anchor, BR trust seals, structure, the menu pattern) + the
fallback look, NOT the primary design driver.

## Step 2 — Design system (read design-premium.md + anti-slop.md)
From the Step 1.5 brief: base (LIGHT unless the niche calls for dark) + palette (60-30-10, ONE accent reserved for
CTAs, tinted neutrals), a serif-display + grotesque-body pairing (Google Fonts), fluid type scale (clamp,
18px body, 65ch measure), 8px spacing scale, 96–160px section padding. Wire the palette as CSS custom
properties + a `.dark` toggle. Bind editorial/asymmetric layout onto the niche's sections so it's NEVER a
uniform stack of centered cards.

## Step 3 — Build the files, ANCHOR-first (read tecnica-qualidade.md + refazer-e-imagens.md)
Write `site-<slug-cliente>/`: `index.html` (root) + `assets/css/styles.css` + `assets/js/main.js` + `img/` +
`404.html` + `politica-de-privacidade.html` + favicon (inline-SVG ok) + `site.webmanifest` + `robots.txt` +
`sitemap.xml` + `README.md` + `ENTREGA-whatsapp.txt`. Multi-page only for advogado/contador or on request.
- **Build the ANCHOR section first and make it the centerpiece** (the real menu / portfolio / results / before-after).
- **Real photos:** find niche-true Pexels IDs (`WebSearch site:pexels.com …`), download into `img/` with curl,
  reference locally, mark each `<!-- TROCAR -->`. Size images with `aspect-ratio` + `width:100%` (NEVER
  `height:100%` in a grid/flex — it collapses the image; see `tecnica-qualidade.md`).
- Enforce: semantic landmarks, one `<h1>`/`<main>`, `<html lang="pt-BR">`, mobile-first clamp() type, sticky
  header + scroll-margin anchors + scrollspy + hamburger `<button>` (aria-expanded), AA contrast,
  :focus-visible, width+height on every img, loading=lazy (not the hero), font-display:swap + preconnect,
  `<script defer>`. Write incrementally so an interruption leaves a usable partial.

## Step 4 — Motion + BR lock-in (read motion-efeitos.md + lock-in-br.md)
Tier 0 always (CSS transitions, IntersectionObserver `.js`-gated reveals, the reduced-motion gate). For
premium add Tier 2 (GSAP + Lenis) tastefully; ALWAYS emit the `matchMedia('(prefers-reduced-motion: reduce)')`
JS gate + the `.js` baseline. Add: floating WhatsApp (or tel: if the business only takes calls), BR footer
(razão social/CNPJ/endereço/horário/contato/Instagram/privacy), LGPD cookie banner (localStorage), keyless
Maps iframe (give `.map-wrap` a subtle bg so it's never a stark empty box), contact form → wa.me/mailto with
required markers + validation + ARIA, JSON-LD LocalBusiness (most specific subtype). Pix box ONLY if asked
(run bundled `assets/pix.js` for a valid CRC; never hand-write a Pix string).

## Step 5 — RENDER + visual self-review (read revisao-visual.md) — MAKE-OR-BREAK
Render the finished site with `assets/render.js` into a `_review/` subfolder: full desktop (1440), full mobile
(390), and 2–4 region crops (hero + the anchor section + footer). READ each PNG. Grade against the 15-point
rubric. Fix the worst issues at the ROOT (re-render after each round), looping until ≥13/15 AND every image
renders AND mobile is clean (cap ~3 rounds). Delete `_review/` before final delivery. If you can't render (no
browser / Node < 21), build to spec, tell the user to eyeball it (desktop + celular), and flag `confere você: revisão visual` — say honestly you couldn't review it this run.

## Step 6 — Persist brand + deliver
Write/update `.claude/clientes/<slug>/brand.md` (name, niche, base light/dark, palette hex, fonts, anchor,
WhatsApp, city, services, image IDs, confirmed copy). Then deliver in PT-BR:
- how to publish (Netlify Drop drag-the-folder / GitHub Pages / or the ZIP) — from `tecnica-qualidade.md`.
- the **TROCAR checklist** (swap the Pexels placeholders for the client's real photos) — from `refazer-e-imagens.md`.
- the **ENTREGA-whatsapp.txt** message to send the client — from `lock-in-br.md`.
- the re-run reason: *"roda de novo pra trocar paleta, adicionar página, refazer pra outro cliente, ou
  atualizar quando o negócio mudar."*
- a one-line honest receipt: what you reviewed visually, the rubric score, and anything the user still needs to check.
Offer the next pack handoff: `/gerar-proposta` (if this was built to win a client).

## Degraded mode
- WebFetch down (rebuild) → say it PT-BR, ask the user to paste the content; never fabricate.
- Web/WebSearch down (no Pexels lookup) → use the fallback designed placeholders (`refazer-e-imagens.md`),
  tell the user the photos are placeholders to swap; never leave empty boxes.
- No browser / Node < 21 (render) → skip auto-review, tell the user to eyeball desktop+mobile, say honestly you couldn't auto-review this run.
- `node` unavailable (Pix) → never hand-write a Pix code; offer copia-e-cola without QR, or skip the box.
- CDN unreachable at the user's end → the site still renders (Tier-0 CSS + `.js` baseline + local images); say so.

## Edge cases
- Business that only takes phone reservations (some restaurants) → floating button is a `tel:` call, CTAs say
  "Reservar pelo telefone"; no WhatsApp float. Honor the real channel.
- 11-digit Pix key → ask "CPF ou celular?" (bundled script flags `ambiguous:true`).
- Multi-location → repeat address/Maps/hours per unit; one JSON-LD per location.
- User pastes raw content instead of a URL → treat as the rebuild intake, skip WebFetch.
- "site em inglês/espanhol" → build the SITE in that language (the client's audience), keep YOUR narration PT-BR.
