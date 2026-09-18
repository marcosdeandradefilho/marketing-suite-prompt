# arquitetura-nichos.md — niche FUNCTION (anchor, seals, structure) + fallback look

> The LOOK (palette, type, light/dark, layout) now comes from the **live visual references you actually
> saw** in Step 1.5 (`referencias-visuais.md`) — not from this file. This file is the niche's FUNCTIONAL
> spine: the ANCHOR section, the BR trust seals, the structure essentials, and the menu pattern — the things
> live design references won't hand you. The palette/type hints below are a **SAFE FALLBACK** for when the
> web is down or no reference loaded, and a sanity check (e.g. don't ship a dark moody page for a warm bistro).
> Lead with what you saw; use this for function.

The niche still decides the FUNCTION of the site: the ONE section that matters most (the ANCHOR), the
structure, the trust seal, light-vs-dark as a sanity default. (Hints researched from real 2025–2026 sites.)

## THREE invariants (break the old bug)
1. **Default LIGHT.** Most category leaders are light-based. Dark is a deliberate, narrow exception
   (steakhouse/cocktail bar, hardcore gym, barbershop, some luxury/agency/portfolio). The generic
   dark "premium template" is WRONG for almost every niche — it's what made a cozy restaurant look
   like a moody landing page. When unsure → light + warm.
2. **Real photography of the actual place/people/work** — never empty placeholders. The #1
   cross-niche cheapening tell is bad/generic/missing images (see `refazer-e-imagens.md` for the
   zero-config Pexels strategy).
3. **Lead with the ANCHOR.** Each niche has ONE thing its site is really about. Feature it prominently
   (at or near the fold). Everything else orbits it. Burying the anchor under a generic hero+features
   stack is the mistake.

## The minimal-question run model
Run from just **NICHE**. Hard-required for full polish: **business name** + **contact** (WhatsApp/phone
for the CTA links). The niche auto-applies: base (light/dark), palette, type voice, the anchor section,
structure, CTA verb + pre-filled message, trust seal, single vs multi-page, footer placeholders. Ask at
most ONE consolidated `AskUserQuestion`: nicho · nome · WhatsApp/telefone · cidade · cor da marca
(opcional). Anything unknown → a marked `<!-- TROCAR -->`, never a fabricated fact. Empty/refused niche
→ the neutral default below.

## Standard structure (adapt per niche — the ANCHOR moves up)
Hero → [ANCHOR section, prominent] → supporting sections (sobre / diferenciais / equipe / depoimentos)
→ trust/credibility → contato (form + WhatsApp + mapa) → rodapé. Keep the BR section family but vary
the visual arrangement per section (editorial/asymmetric, alternating image/text, bento) — never a
uniform stack of centered cards. Single-page (anchor nav) is the default; multi-page only for
advogado/contador (per-area SEO pages) or on request.

---

## NICHE DNA — base · palette · type · ANCHOR · structure · imagery · register · tells

### 🍽 Restaurante / bistrô / fine dining  (the priority case)
- **Base: LIGHT + WARM.** Cream/ivory backgrounds make plated food look expensive and appetizing.
  **Dark ONLY for** steakhouse/chophouse, cocktail/late-night wine bar, izakaya, or an explicit
  "moody/intimate/date-night" brief — and even then warm-dark (espresso/charcoal/oxblood), never `#000`.
- **Palette:** cream/ivory `#FBF6EE`/`#F7F3E8` (not pure white) · warm espresso ink `#2A2420` (not `#000`)
  · earthy mids (terracotta `#C0582F`, sage/olive, clay) · ONE bold accent: burgundy/oxblood `#7E2233`,
  brass/gold `#B08D57`, or deep forest. Gold-on-cream = instant fine-dining signal. **Avoid** cold grey,
  neon, electric blue, purple.
- **Type:** serif-led, formal-but-warm. Display = elegant serif (Fraunces, Playfair, Cormorant,
  EB Garamond). Body = quiet grotesque (Hanken/DM Sans). Max two faces.
- **ANCHOR: the MENU + appetizing food photography.** Visitor priority: menu → hours → location →
  phone → reserve. The on-page HTML menu and great food photos are non-negotiable; everything orbits them.
- **Structure:** Hero (full-bleed signature dish OR warm room + name in serif + one line + Reservar/Ver
  cardápio) → short story teaser → **MENU (anchor)** → gallery (food + ambiance) → chef/sommelier →
  reservas (telefone/WhatsApp/iFood as relevant) → visite (map, **hours**, phone) → footer.
- **Imagery:** real food close-ups (natural side light, shallow depth) + room/atmosphere. Full-bleed
  hero, edge-to-edge gallery. Photography IS the design.
- **Register:** appetite, warmth, hospitality, craft. Generous whitespace, unhurried.
- **Tells:** dark moody page for a warm bistro · menu as a PDF download or generic "Entradas/Principais"
  placeholder cards (build the REAL menu) · bad/stock food photos · cold tech palette · wall-of-text menu.

**Text-heavy menu (dozens of dishes — e.g. a French carte) done elegantly:**
- **On-page HTML, never a PDF.** A high-intent sub-list (wines, tasting menu) can be its own page.
- **3-tier hierarchy:** (1) course header (Entrées / Soufflés / Viandes) in the serif display, with a
  thin rule — use the menu's own French words for authenticity; (2) dish name in the body face, medium
  weight; (3) one short description, lighter/smaller. Price small and quiet, or omit on fixed menus.
- **Columns:** fine dining = one calm wide column or **two columns max**. Three+ = "classifieds" = cheap.
- **Generous negative space** makes 40 dishes feel curated, not crammed. Optionally tab/anchor per course
  so the diner sees one course at a time. Keep it on a cream ground.

### 💆 Clínica estética / esteticista / med-spa
- **Base: LIGHT warm-neutral** (off-white/bone). Dark = rare high-fashion flex.
- **Palette:** warm off-white `#FAF7F2` · charcoal text `#2B2724` · ONE accent: terracotta, blush/nude,
  sage, or mauve; champagne/gold for luxe. **Avoid sterile medical blue** (that's dental's color).
- **Type:** high-contrast editorial **serif headline** + clean sans body (Playfair/Ivar + Lato/Montserrat).
- **ANCHOR: the real BEFORE/AFTER results gallery** (by treatment) + the treatments menu. Persistent
  "Agendar avaliação" CTA.
- **Structure:** Hero (luminous skin/treatment room + Agendar + a real before/after) → treatments →
  trust/credentials (ANVISA/biossegurança, press) → **before/after (anchor)** → reviews → providers →
  booking CTA.
- **Imagery:** real provider/facility/patient before-afters, warm-graded luminous skin, serene rooms.
- **Register:** calm, luxe, indulgent, credentialed. **Tells:** stock models in fake clinics; too clinical
  (sterile blue, sans-only); no real before/afters; no serif.

### ⚖️ Advogado / escritório de advocacia
- **Base: LIGHT** (white/off-white) with navy/ink content colors. **Dark** only for boutique/high-stakes
  litigation prestige, or as alternating dark bands.
- **Palette:** deep navy `#0B1F3A`/`#14233F` + light grey + white, restrained metallic accent (gold
  `#C9A24B`) on ≤10%. Alts: charcoal (criminal/authority), forest (estate), burgundy (heritage).
- **Type:** **serif carries the brand** (Tiempos/Canela/Noe register), clean sans body. Sans-only loses
  the institutional gravitas the niche expects.
- **ANCHOR: CREDIBILITY/PROOF** — case results, "como visto em" media, awards/badges, reviews — plus
  **áreas de atuação** as a self-select grid. Best firms put a result in the hero. Show **OAB** number.
- **Structure:** Hero (answers "podem cuidar do meu caso?" + área sub-line + clickable phone + Fale com
  um advogado + trust above fold) → results/proof → áreas de atuação → advogados (editorial portraits) →
  sobre/credibilidade → depoimentos (CAUTION: no result promises — OAB advertising rules) → contato.
- **Register:** authority, trust, gravitas, calm competence. Restraint = confidence. **Multi-page recommended.**
- **Tells:** gavel/scales/courthouse clichés; stock "fake lawyer" photos; sans-only; loud accents; no real
  results/headshots; hype (advocacy advertising is restricted in BR).

### 🏛 Arquiteto / arquitetura / design de interiores / construtora / imobiliária
- **Base: LIGHT (white).** The work is the content; the site is a frame. Interior design = warm-white.
- **Palette:** pure neutrals (white/near-black/greys), color comes from the project photos; ONE accent or
  none. Interior: cream/sand/taupe + one muted sage/terracotta. (Construtora/imobiliária similar, a touch warmer.)
- **Type:** neo-grotesque body/nav + an oversized editorial display serif in the hero.
- **ANCHOR: the PROJECT PORTFOLIO.** The project grid IS the site — full-bleed imagery, quality over
  quantity, projects open to large visuals with minimal text. (Imobiliária: the listings/imóveis grid.)
- **Structure:** Full-screen hero image → **selected projects/work grid (anchor)** → estúdio/sobre +
  filosofia → processo → serviços → contato (consultation prompt at the end of each project). Sparse nav.
- **Imagery:** full-bleed high-res professional photography — the single biggest quality lever. Big whitespace.
- **Register:** calm, restraint, precision, quiet luxury, gallery-like. **Seals:** CAU (arquiteto) / CREA
  (engenharia/construtora) / CRECI (imobiliária). **Tells:** low-res/dim photos; over-animation; cluttered
  nav/too many projects; dark neon SaaS template (wrong genre).

### 🏋️ Academia / personal trainer
- **FORK — detect the sub-niche first.** Strength/CrossFit/boxing/HIIT/most personal trainers → **DARK** +
  energetic accent (red/orange/electric, or gold for premium); makes action photos and CTAs pop. Yoga/
  Pilates/barre/wellness → **LIGHT/warm** + serif (beige/cream, ~85% of top Pilates sites). Cross them and
  the genre breaks.
- **Type:** dominant fitness = condensed bold uppercase (Oswald/Bebas/Montserrat). Wellness = serif headline + sans.
- **ANCHOR: the JOIN/conversion engine** — a repeated CTA above the fold ("Agende uma aula experimental"),
  the schedule ≤1 click away, transformation gallery + testimonials as proof. **Pricing visible, not behind a form.**
- **Structure:** Hero (photo/video bg + benefit + ONE CTA above fold) → sobre → modalidades/aulas grid →
  trainers → resultados/depoimentos → **schedule + pricing visible** → FAQ → final CTA. **Seal:** CREF.
- **Tells:** generic stock gym photos; pricing hidden; buried schedule; CTA below fold; wrong sub-niche skin.

### 💈 Salão de beleza / barbearia (two different aesthetics — detect which)
- **Salão → LIGHT/luxe.** Warm off-white/blush/greige base; high-contrast serif (Playfair/Cormorant/Didot)
  + sans; accent terracotta/dusty rose (gold if luxe). **Barbearia → DARK/vintage.** Charcoal `#161616`,
  bone text, black + gold `#C2A14D` + oxblood; bold condensed/slab + a badge/emblem logo.
- **ANCHOR:** services + price list + portfolio/gallery of real work → a persistent high-contrast
  "Agendar" CTA (sticky on mobile). **Imagery:** real clients/cuts, warm (salão) / dark moody (barbearia).
- **Tells:** stock beauty photos; script font as body; salão too stark/clinical; barbershop on a bright
  corporate template (kills the mood); no persistent Book button.

### 🦷 Dentista / clínica odontológica
- **Base: LIGHT/bright** (cleanliness must read as literal brightness). Two lanes: classic **trust blue +
  white** (sky/medical blue + teal), or rising **"spa dentistry"** warm neutrals (sage/soft terracotta +
  white). Add ONE warm "Agendar" accent.
- **Type:** friendly clean sans default; boutique adds a legible serif headline (softer than med-spa's drama).
- **ANCHOR: TRUST + the human team + frictionless BOOKING.** Authentic team/doctor photos; before/after only
  if cosmetic-leaning. One unmissable booking CTA in the nav. **Seal:** CRO.
- **Structure:** Hero (bright natural-light smiling patient/team + comfort headline + Agendar) → tratamentos
  → por que nós (anxiety-free, tech) → equipe (warm bios) → reviews → before/after (if cosmetic) → localização/
  convênios + persistent booking. **Tells:** stock perfect-model photos; dated clinical-blue gradient + clip-art
  tooth; clinical-equipment hero (triggers anxiety); borrowing med-spa's dark luxe look (reads off-brand).

### 📊 Contador / contabilidade
- **Base: LIGHT, almost always** (clean/airy = organized, transparent). Dark = premium/startup minority.
- **Palette:** navy + slate + white + ONE modern accent (teal/sky/emerald — emerald = the "money/growth"
  differentiator). Warm peach/cream = approachable boutique.
- **Type:** modern geometric sans OR a bold serif headline + sans body. Restraint = trust.
- **ANCHOR: SERVICES + TRUST/SPECIALIZATION** — signal a specialization above the fold ("Contabilidade para
  clínicas" beats "para todos"); third-party review widget; real named people + **CRC** + certifications.
- **Structure:** Hero (specialization + Peça uma proposta + review widget) → serviços (cards) → trust/
  credentials → equipe (real headshots + CRC) → pricing/packages (transparent) → depoimentos (specific
  results) → contato. Multi-page leans here. **Tells:** cliché finance stock (coins/calculator/handshake);
  vague positioning; no pricing path; cluttered nav.

### 💼 Consultoria / agência / B2B
- **Agency (creative) → EITHER/alternating** dark/light, oversized bold type, **ANCHOR = THE WORK / case
  studies** with named clients; custom imagery, never stock. **B2B consultancy → LIGHT**, navy+white+grey,
  clean sans or restrained serif, **ANCHOR = case studies/results** (lead the headline with the metric).
- **Structure (B2B):** Hero (who you help + outcome + 1 CTA) → problema → solução → serviços (as results) →
  prova social (logos/depoimentos) → processo → cases → contato. **Tells:** staged-handshake stock; Canva-2015
  template; buried case studies; vague hero.

### 🧰 Neutral default (niche unknown / "negócio local")
Cleaning, plumbing, handyman, generic shop. Job = trust + clarity + frictionless contact.
- **Base: LIGHT, warm-white** (`#F7F9FB`–`#FBF8F4`). Dark is risky (reads edgy, not trustworthy).
- **Palette:** deep navy as the "black" (`#102A43`) + white + one warm greige + ONE saturated CTA accent
  (confident orange/red `#E0502A`) — **never indigo/violet**. Charcoal text `#1F2933`, not pure black.
- **Type:** bold readable sans headline + clean sans body; optional single serif heading for "premium heritage".
- **ANCHOR: trust proof bar high up** (rating + nº reviews + license/anos/jobs) + clear services grid + an
  ever-present click-to-call / "Solicitar orçamento" CTA, sticky on mobile.
- **Structure:** Hero (outcome + phone + quote CTA) → proof bar → serviços grid → como funciona (3 steps) →
  depoimentos (real names) → área de atendimento → big quote CTA + footer with phone repeated.
- This reads premium across any unknown business; only swap the accent + anchor wording once the niche is known.

## Quick lookup

| Niche | Base | Accent | Type | ANCHOR |
|---|---|---|---|---|
| Restaurante/bistrô | **Light cream** (dark only steakhouse/bar) | oxblood/brass/forest | serif display + sans | **Cardápio + fotos de comida** |
| Estética/med-spa | Light warm | blush/terracota/sage/dourado | serif editorial + sans | **Galeria antes/depois** |
| Advogado | Light (dark = boutique) | navy + dourado | serif brand + sans | **Provas/resultados + áreas (OAB)** |
| Arquiteto/imobiliária | **Light/white** | nenhum/1 neutro | grotesca + serifa grande | **Portfólio de projetos** |
| Academia | **Fork:** dark (força)/light (wellness) | vermelho/laranja OU sage | condensada bold | **CTA Agendar + schedule/preço** |
| Salão / barbearia | Salão light · barbearia dark | terracota/rosa · dourado/oxblood | serifa contraste · condensada+emblema | serviços+preço+galeria → Agendar |
| Contador | Light | navy + teal/emerald | sans geométrica/serifa | **Serviços + especialização (CRC)** |
| Agência/B2B | agência: ambos · B2B: light | electric OU navy+laranja | bold grande OU sans limpa | **Os trabalhos / cases** |
| Dentista | **Light/bright** | azul confiança OU sage (spa) | sans amigável (+serifa) | **Confiança + equipe + agendar (CRO)** |
| Local genérico | **Light warm** | navy + laranja/vermelho | sans bold + sans | **Barra de prova + CTA contato** |

## Trust seals by niche
Estética → ANVISA/biossegurança · dentista → CRO · médico → CRM · advogado → OAB · contador → CRC ·
academia/personal → CREF · arquiteto → CAU · construtora/engenharia → CREA · imobiliária → CRECI.
Show the registration number where the niche expects it (footer and/or Sobre).
