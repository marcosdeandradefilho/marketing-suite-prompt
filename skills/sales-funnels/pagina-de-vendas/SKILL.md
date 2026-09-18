---
name: pagina-de-vendas
description: >-
  Cria uma PÁGINA DE VENDAS completa e de alta conversão (HTML/CSS/JS pronto pra publicar),
  com copy profissional e design premium, a partir de um briefing curto. Mostra a copy e a
  paleta pra você aprovar ANTES de montar. Use quando a pessoa quer criar, fazer ou montar uma
  página de vendas, landing page, página de captura, página de lançamento, carta de vendas, VSL
  ou página pra vender um curso/produto/serviço/mentoria. Gatilhos: "página de vendas", "cria uma
  landing", "landing page", "página pra vender meu curso", "página de lançamento", "carta de
  vendas", "copy de vendas", "página de captura de leads", "preciso vender X online", "página de
  vendas". NÃO é pra site institucional de empresa (isso é a /site-institucional).
argument-hint: "[produto + público + preço + objetivo, ou deixe vazio que eu pergunto o essencial]"
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch, WebSearch, AskUserQuestion
effort: xhigh
model: inherit
---

# Página de Vendas

You generate a COMPLETE, high-converting, premium sales page (zero-build HTML/CSS/JS) the user can
deploy or hand to a client. This is the flagship of the pack: the bar is **copy that a professional
copywriter would be proud of** + **design that looks expensive and current (2025/2026)**. Everything
the user sees is **Brazilian Portuguese, direct, anti-guru**: no hype, no time-to-money promises, no
income guarantees, R$ never a bare `$`. The output is the product. Premium is the DEFAULT.

Two things make this skill different from every "ChatGPT writes copy in chat" attempt:
1. **You show the COPY and the COLORS first and get approval BEFORE building** (the copy is the
   user's brand voice and money on the line — never surprise them with a finished page).
2. **You self-audit the built page**: render it headless, LOOK at it, count the AI-slop tells and
   AI-writing tells, and regenerate until it's genuinely impressive. The render loop is non-optional.

This file is the orchestrator. Read each reference file WHEN you reach the step that needs it
(progressive disclosure — do NOT read them all up front):
- `reference/fluxo-e-intake.md` — the conversation-first flow, intake fields, brand-kit reuse, the
  hot-vs-cold audience choice, the minimal-question model, the empty-input branch. **Read at Step 1.**
- `reference/compliance-br.md` — the income-claim ban, Meta Ads / Hotmart / Kiwify policy traps, CDC
  (preço-de, escassez), LGPD (separated consents), the "stats are directional, never printed on the
  page" rule. **Read at Step 1, before writing any copy or offer.** This protects the user's ad account.
- `reference/copy-estrutura.md` — the block-by-block anatomy, the frameworks (PAS/PASTOR/AIDA/Brunson),
  the awareness-level map, what each block must deliver. **Read at Step 2.**
- `reference/copy-craft.md` — headline/lead/hook/bullet library, the offer + value-stack + price-anchor
  + proof + objection + guarantee + ethical-urgency craft, the BR-voice corpus. **Read at Step 2.**
- `reference/exemplo-pagina-completa.md` — ONE full end-to-end page written block by block, the tone
  gabarito. **Read at Step 2** to calibrate voice.
- `reference/anti-ia-escrita.md` — the AI-writing tells (travessão ban etc.) + the mandatory self-check.
  **Read at Step 2, before writing copy, and run the self-check before Step 4.**
- `reference/design-premium.md` — typography, color (60-30-10), hero patterns for SALES pages, layout,
  the exact CSS values, the mobile breakpoints. **Read at Step 3.**
- `reference/anti-slop.md` — the AI-slop cluster to FORBID + the premium alternative for each + the
  premium-vs-guru tension + the contrast gate. **Read at Step 3, before writing any CSS.**
- `reference/motion-efeitos.md` — zero-build effects, exact GSAP/Lenis CDN, the reduced-motion gate,
  the performance budget, the CDN-fallback, mobile motion rules. **Read at Step 3.**
- `reference/componentes-conversao.md` — CTA, pricing/offer block, proof layouts, FAQ (ARIA), ethical
  countdown, comparison table, sticky mobile CTA, checkout wiring, SEO/Open Graph. **Read at Step 3-4.**
- `reference/tecnica-render.md` — the output-folder convention, the build order, the headless render
  command, the SELF-QUALITY LOOP (render → look → critique → regenerate), the a11y/SEO/perf checklist,
  deploy. **Read at Step 4.**
- `assets/pix.js` + `assets/qrcode.js` — only if a Pix box is requested (Step 4).

## Non-negotiable rules (read before anything)
1. **Copy-first, approval before build.** You ALWAYS present the proposed copy (at least: headline +
   subheadline + the offer block + the guarantee + the structure) AND the color/design direction in the
   chat, and get a "pode seguir" (or edits) BEFORE generating files. This is the user's voice and money.
2. **Premium by default, never generic.** Before writing CSS, read `reference/anti-slop.md` and actively
   avoid the AI-slop cluster (Inter-everywhere, indigo/purple accent, centered hero + 2 buttons, 3
   identical icon cards, left-colored-border cards, everything-rounded, uniform 0.1 shadow, emoji icons).
3. **Write like a human, not AI (read `reference/anti-ia-escrita.md`).** The #1 BR giveaway is the
   travessão "—": NEVER use `—` or `–` in any PT-BR output. Run the self-check (Grep the final HTML for
   `—`) before delivery. Vary sentence length, kill the AI vocabulary, swap generic for concrete.
4. **Never invent proof.** Testimonials, prints, case studies, numbers, logos, ratings appear ONLY if the
   user provides them. Unknown → a clearly-marked `<!-- TROCAR: depoimento real aqui -->` placeholder
   with an initials avatar, NEVER a fabricated face/name/result. Fake proof is fatal and illegal.
5. **No income promises, no fake scarcity (read `reference/compliance-br.md`).** Never "ganhe R$X",
   "fique rico", "renda garantida". Never a countdown that resets, fake "2 vagas", or a "de R$X" that
   isn't a real price. These ban the Meta ad and violate the CDC. Anchor on the cost of the ALTERNATIVE
   (a real dev/SaaS price) or the real future price, framed as the seller's, never the buyer's earnings.
6. **Stats stay off the page.** The conversion benchmarks in the research ("+45%", "+266%", etc.) guide
   YOUR build decisions; they are NEVER printed as claims on the generated page (that's a guru tell).
7. **BR lock-in is first-class.** Checkout block (Pix "acesso imediato" + "12x de R$" + trust signals),
   sticky mobile CTA, LGPD cookie banner + correctly-separated form consents, Open Graph card (the
   WhatsApp preview is part of the conversion). Pix QR box is OPT-IN and OFF by default.
8. **Mobile-first and fast.** Most traffic (WhatsApp + Meta) opens on a phone. Real mobile breakpoints,
   touch CTAs, the sticky mobile bar, a weight budget, lazy-loaded video, CDN fallback so the page still
   renders if GSAP/Lenis don't load. A beautiful page that loads in 8s is a loss, not a flagship.
9. **Anti-guru tone always.** No time estimates, no income guarantees, no hype adjectives. R$ only.
10. **NEVER claim "corrigido" or "pronto" without looking at the actual rendered file first.** After every
    render, you MUST read the PNG (using the Read tool on the screenshot file) and confirm with your own
    eyes that the issue is gone — including checking the area around it, not just the isolated element.
    An isolated render (a test-only HTML without the full page CSS) LIES — it hides class collisions and
    cascade issues. Always verify on the real full-page render. If the issue persists, fix and re-render
    before reporting anything to the user. Never render and then skip reading the file. The render exists
    to be LOOKED AT, not just generated.

## Step 0 — Detect path + scope (silently)
Classify into ONE path (semantic intent, robust to typos/slang):
- **NEW** — a product/offer to sell, or "cria uma página de vendas pra ...". → Step 1.
- **REBUILD** — a URL is present, or "refaz / melhora essa página de vendas". → read
  `reference/fluxo-e-intake.md` §rebuild: WebFetch the page, keep the real copy/offer/price, rebuild
  premium. If fetch is blocked/empty, ask the user to paste the content; never invent the offer.
- **CAPTURE/opt-in** — "página de captura / de lead / de inscrição (sem venda direta)" → same flow,
  shorter structure (no price/offer block; the CTA is the form), per the reference.
Off-topic, or an institutional company site → say plainly this builds sales/landing pages and point to
`/site-institucional`. If asked to fabricate proof, promise income, or fake scarcity → decline THAT part
in one sober PT-BR line and build an honest version. Never refuse for lack of input (empty → Step 1 asks).

## Step 1 — Intake + compliance frame (read `reference/fluxo-e-intake.md` then `reference/compliance-br.md`)
### 1a. Reuse context silently
`Glob .claude/clientes/<slug>/brand.md`, `.claude/brand-kit-freelancer.md`, `.claude/brand.md`. If found, Read and REUSE silently (name, palette hex, fonts, WhatsApp, Pix key, prior copy) — do
not re-ask what you already have. On a re-run for the same product, surface "o que mudei desde a última versão".
### 1b. Gather the brief
Required to proceed: **produto/oferta** · **público-alvo** · **preço** · **objetivo da página** (venda direta
de checkout / captura de lead / agendamento). Infer the rest (dor central, transformação, bônus, prova
disponível) and state your assumptions in the read-back so the user can correct.
- If the brief is clear → give ONE soft read-back line and proceed.
- If load-bearing fields are missing → ONE consolidated `AskUserQuestion` (fixed options + free-text rider):
  o que vende · pra quem · faixa de preço · objetivo. Never a long form. Empty input never dead-ends.
- Ask which audience temperature (read `fluxo-e-intake.md` §quente-vs-frio): **lista quente** (já conhece
  você/o tema, vai direto pro mecanismo + oferta) vs **tráfego frio / Meta Ads** (agita a dor no topo).
  Default to the one the brief implies; mention you can generate the other version later.
### 1c. Set the compliance frame NOW
Read `reference/compliance-br.md`. Decide the honest anchor (alternative cost or real future price), confirm
there are NO income claims, plan the guarantee (real days, ≥ the 7-day legal floor), and the urgency (only if
real). Note any risky thing the user asked for and the honest replacement you'll use.
Narrate up front (PT-BR, plain): *"Vou primeiro te mostrar a copy e as cores. Você aprova ou ajusta, e só
então eu monto a página inteira. No fim te explico como publicar e onde colar o link do checkout."*

## Step 2 — Write the copy + propose it (read copy-estrutura.md + copy-craft.md + exemplo-pagina-completa.md + anti-ia-escrita.md)
Pick the framework + block order for the audience temperature and awareness level. Write the PT-BR copy like a
real copywriter, not AI: no travessão, varied rhythm, concrete-over-generic, benefit-over-feature, the unique
mechanism named, the 3 core objections answered in the reader's own voice, the offer/value-stack BEFORE the
price, the guarantee in human language, ethical urgency only. Run the `anti-ia-escrita.md` self-check.
**Then PROPOSE, don't build yet.** Show in the chat, tight and scannable:
- the headline + subheadline (give 2 options for the headline),
- the section structure (the block list for this page),
- the offer + price framing + guarantee + urgency line,
- the design direction: palette (with hex), font pairing, hero style, in 2-3 lines. If the user gave no
  brand colors, PROPOSE a palette that fits the product and say it's theirs to swap.
Ask: *"Pode seguir assim, ou quer ajustar a copy/as cores?"* Apply edits. Only on a go-ahead → Step 3.

## Step 3 — Design system + build the page (read design-premium.md + anti-slop.md + motion-efeitos.md + componentes-conversao.md)
Bind the approved copy onto a premium layout. Pick: palette as 3 CSS custom props (60-30-10, one accent
reserved for CTAs, never indigo), a serif-display + grotesque-body pairing (Google Fonts CDN, fluid clamp
scale), the hero pattern (mesh-aurora dark OR product-screenshot editorial), section rhythm 80-120px, the
mobile breakpoints. Apply motion with RESTRAINT (1-2 purposeful effects: scroll reveals + maybe a SplitText
hero or scroll-progress bar) with the MANDATORY `prefers-reduced-motion` gate and the JS-off visible baseline.
Build the conversion components: CTA (copy-first, 1ª pessoa, repeated at pause points + sticky mobile bar),
offer/pricing block (anchor → value stack → price → guarantee → trust signals), proof (real or marked
placeholder), FAQ (ARIA accordion), ethical countdown (only if real, max 1 scarcity surface), Open Graph head.
Write the files incrementally per `reference/tecnica-render.md` so an interruption leaves a usable partial.

## Step 4 — Self-quality render loop + checkout/Pix + LGPD (read tecnica-render.md, then componentes-conversao.md)
This is the make-or-break of "qualidade absurda". Per `reference/tecnica-render.md`:
1. Detect a headless browser (Edge on Windows, Chrome/Edge on Mac/Linux). Render the page to a PNG (and/or PDF).
2. **LOOK at the screenshot — this is MANDATORY, not optional.** Use the Read tool to read the actual
   PNG file you just generated. Do NOT trust that it rendered correctly without looking. Do NOT use an
   isolated test-HTML (it lacks the full page CSS and hides collisions). Look at the REAL full-page render.
   Audit against the anti-slop checklist (count the tells; 5+ = fail) AND the anti-IA-writing self-check
   (Grep the HTML for `—` and the AI vocabulary) AND the contrast/a11y gate. If you can't see a section
   clearly, crop it — but crop from the REAL preview file, not a separate test.
3. If it reads generic, slop, or AI-written → fix the specific issue and re-render. Repeat until it's
   genuinely premium (cap a few iterations; keep the best). Narrate progress plainly in PT-BR.
4. **Before proceeding to Step 5 (delivery), read the final preview PNG one more time and confirm it
   looks right.** Only then say "tá pronto". This is the gate that prevents delivering broken pages.
Checkout: wire the primary CTA to a `{{LINK_CHECKOUT}}` placeholder (Hotmart/Kiwify/Cakto) and tell the user
where to paste it; add the trust signals + payment line. Pix QR box ONLY if asked → run `assets/pix.js` for a
real copia-e-cola + SVG QR (never a hand-made code). LGPD: cookie banner + form with SEPARATED consents
(delivery obligatory ≠ marketing optional) + a base política de privacidade page.

## Step 5 — Persist brand + deliver (read tecnica-render.md §deliver)
Write/update `.claude/clientes/<slug>/brand.md` (or the existing brand kit) with palette/fonts/copy so the next
run is instant. Then deliver in PT-BR:
- how to publish (Netlify Drop drag-the-folder / Hotmart-Kiwify custom page / GitHub Pages / the ZIP),
- where to paste the checkout link, the Meta pixel slot, and the OG image to swap,
- the **TROCAR checklist** (real proof, photos, checkout link, CNPJ in the footer),
- the re-run reason: *"roda de novo pra trocar a oferta, gerar a versão fria pro Meta Ads, refazer pra outro
  produto, ou atualizar o preço quando o lote virar."*
- an **honest receipt**: what you verified (rendered, contrast, no travessão) and what the user still needs
  to test in the real world (live CDN load, real mobile, the OG preview in WhatsApp, the real checkout). Never fake coverage.
Offer the next pack handoff: `/site-institucional` (for the company site), `/mcp-meta` (to run
the Meta Ads that point at this page).

## Degraded mode
- **No headless browser:** you cannot run the self-quality LOOK loop — say so honestly, deliver the
  self-contained page, and tell the user to open `index.html` and check it; never claim you audited the render.
- **CDN unreachable (GSAP/Lenis) at the user's end:** the page still renders (Tier-0 CSS reveals + the JS-off
  baseline); motion just doesn't enhance. The fallback is built in. Say so.
- **`node` unavailable (Pix):** never hand-write a Pix code (wrong CRC = dead string); offer the copia-e-cola
  flow without the QR, or skip the Pix box and keep the checkout-link CTA.
- **No brand color/logo:** propose a product-appropriate palette + a wordmark in Step 2, clearly labeled trocável.
- **WebFetch down (rebuild path):** ask the user to paste the current page's copy/offer; never invent the offer.
- **Empty/garbage input:** the Step 1 consolidated question; if refused, build a clear template page for a
  generic offer with sensible defaults and say which defaults you used. Never fabricate a real product's data.

## Edge cases
- User wants only the copy (no page) → write the copy doc and skip the build; offer to build the page after.
- User pastes raw page content instead of a URL → treat as rebuild intake, skip WebFetch.
- "página em inglês/espanhol" → build the PAGE in that language (it's the buyer's audience) but keep YOUR
  narration to the user in PT-BR.
- High-ticket (R$2.000+) → lean PASTOR/long-form + application/agendamento CTA instead of direct checkout.
- Product that is clearly illegal / a get-rich-quick scheme / a health-cure claim → decline; do not build it.
