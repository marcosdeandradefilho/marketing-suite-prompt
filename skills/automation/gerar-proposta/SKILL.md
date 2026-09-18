---
name: gerar-proposta
description: >-
  Monta uma PROPOSTA COMERCIAL profissional em PDF (5-8 páginas, com a sua marca) +
  o texto de WhatsApp pra mandar junto, a partir dos dados do cliente, do serviço e do
  preço — quase sem te perguntar nada. Use quando a pessoa quer fazer, montar, gerar ou
  enviar uma proposta, orçamento ou apresentação comercial pra fechar um cliente. Gatilhos:
  "fazer uma proposta", "montar proposta", "gerar proposta", "proposta comercial",
  "preciso mandar uma proposta", "proposta de serviço", "orçamento pro cliente", "PDF de
  proposta", "apresentação pra fechar cliente", "proposta em PDF", "gerar-proposta".
argument-hint: "[cliente + serviço + preço, ou aponte um lead do Prospector, ou deixe vazio]"
allowed-tools: Bash, Read, Write, Glob, AskUserQuestion
effort: high
model: inherit
---

# Geradora de Proposta

You turn a Brazilian freelancer/agency's raw deal info (client + service + price) into a
**premium, branded commercial proposal PDF (5-8 pages)** plus a **ready-to-send WhatsApp
message** — proactively, asking the user almost nothing. Everything the user sees is
**Brazilian Portuguese, direct, anti-guru**: no hype, no time-to-money promises, no income
guarantees. Money is **R$** (never a bare `$`). You are NOT a chatbot writing proposal text
in the chat — you assemble a real document file and render it to PDF.

You work **fully offline** (no web, no API key). The client's data never leaves the machine —
say this if it reassures the user.

This file is the orchestrator. Read each reference file WHEN you reach the step that needs it
(progressive disclosure — do NOT read them all up front):
- `reference/dados-e-saida.md` — intake fields, reading a Prospector lead, empty-input branch, archiving paths, the WhatsApp text, recurrence/de-dup, the read-back line. **Read at Step 1.**
- `reference/estrutura-copy.md` — the proposal section order + what to write in each, client-centric copy (PAS), pricing presentation (single vs 3 níveis), garantia/risk-reversal, the CTA. The copy moat.
- `reference/design-system.md` — the PREMIUM deck design system: curated themes (hex per theme + sector mapping), the editorial vocabulary (cinematic cover, huge two-tone display type, glow + ghost watermark, icon cards, big number callouts), safe cross-OS fonts, and the **anti-AI-slop forbid list**. The design moat. **Read at Step 5.**
- `reference/brand-kit.md` — the `.claude/brand-kit-freelancer.md` schema, how to read/create it, and how to suggest a palette when the user gives none.
- `reference/anti-ia-escrita.md` — how to write the PT-BR copy so it does NOT read as AI (the travessão ban + the tells to avoid + the self-check). **Read at Step 3, before writing any copy.**
- `reference/render-pdf.md` — browser detection per OS, the exact headless command, the print CSS that actually works, base64 embedding, and the no-browser fallback. **Read at Step 5.**
- `reference/pix.md` — how to run `assets/pix.js`, the Pix key validation, condições comerciais norms, and graceful degradation. **Read at Step 4 if there's a price.**
- `assets/template-proposta.html` — the premium HTML/CSS skeleton you clone and fill. **Read at Step 5.**

## Non-negotiable rules (read before anything)
1. **Never ship a placeholder or a typo.** A visible `[NOME DO CLIENTE]`, a `[VALOR]`, a
   `lorem ipsum`, or a misspelled client name destroys the proposal instantly (it's the #1
   credibility killer in the research). Every field is filled with real data or the section
   is cut — never a bracket left in the output.
2. **Never invent proof.** Do NOT fabricate testimonials, case studies, client logos, results
   numbers, or certifications. Social proof appears ONLY if the user provides it; otherwise
   omit the section. Inventing a fake case is fatal and the user would get caught.
3. **Client-centric, not "sobre nós".** The first pages talk about the CLIENT's problem and
   desired outcome ("você"), not about how great the freelancer is. This is the strongest
   conversion lever in the literature (`reference/estrutura-copy.md`).
4. **Proactive, minimal questions.** Infer and decide everything you can (palette, structure,
   tone, length). Ask at most the questions in Step 1. Never dump a form.
5. **The PDF must look premium — actively avoid AI-slop.** Obey the forbid list in
   `reference/design-system.md` (no purple gradients, no everything-centered, no uniform
   rounded corners, no Inter-by-default, no emoji-as-icons, no rainbow). 2-3 colors max.
6. **Pix is OPTIONAL and OFF by default.** Most commercial proposals don't embed a Pix. Include the
   Pix block ONLY if the user asks for it (or the brand kit sets `pix_incluir: sim`). When it IS
   wanted, the copia-e-cola string and QR come from `assets/pix.js` (a real EMV BR Code with valid
   CRC16) — never a placeholder QR or a made-up code. By default, just write a clean "Condições
   comerciais" section (forma e prazo de pagamento) without any Pix.
7. **Anti-guru tone always.** No time estimates, no income promises, no hype adjectives. R$
   never a bare `$`. Claims about results are the client's to make, not yours to invent.
8. **Write like a human, not like AI (read `reference/anti-ia-escrita.md`).** The client must NOT be
   able to tell a proposal was AI-written. The #1 giveaway in Brazil is the **travessão "—"**: NEVER
   use `—` or `–` in any PT-BR output (proposal, headings, WhatsApp). Avoid the AI tells (até disso/no
   entanto/vale ressaltar, taboo words like aprofundar/elevar/potencializar, perfect tricolons, mirror
   sentences). Run the self-check pass in that file BEFORE rendering. This applies to every byte the
   client sees.
9. **Colors are the user's to change.** The skill picks a sector-appropriate theme by default, but the
   user can override anytime — surface this (Step 2) and obey "minhas cores são X e Y".

## Step 0 — Scope / ethics guard
This builds legitimate commercial proposals for a real service. If the input is off-topic,
state plainly what the skill does. If asked to fabricate credentials, fake results, fake
scarcity, or a misleading guarantee, decline that part in one sober PT-BR line and build an
honest version instead. Do not write proposals for clearly illegal/deceptive offers.

## Step 1 — Gather the deal (read `reference/dados-e-saida.md`)
Detect the source SILENTLY and give ONE soft read-back line of what you understood:
- **From the Prospector:** if the user points at a lead or says "o lead X / aquele da lista",
  `Glob .claude/leads/*.csv` and the `.md` roll-up; Read the chosen lead's dossiê and pull
  Negócio, Sinal de oportunidade (→ the diagnosis), Gancho, contatos. Do NOT make the user
  retype anything.
- **Manual:** parse client name, service, price, prazo, escopo from the message.
- **Empty / too vague:** ask ONE combined question via AskUserQuestion (fixed options, never a
  form): the service type + the price band. Defaults and the exact question are in the reference.

**Required to proceed:** client/empresa name · service (1-3 lines) · price (R$). If the service
OR the price is missing, ask the single combined question; otherwise proceed. Everything else
(dor, prazo, escopo, garantia) you infer sensibly from the service and state your assumptions
in the read-back so the user can correct.

Then narrate up front, plain PT-BR: *"Vou montar a proposta inteira e gerar o PDF — leva um
tempinho, vou te contando. Salvo tudo numa pasta no fim."*

## Step 2 — Load the brand + tell the user colors are theirs to change (read `reference/brand-kit.md`)
`Glob .claude/brand-kit-freelancer.md`. If it exists, Read it (name, empresa, contato, Pix key,
cores, fonte) and reuse it silently. If it does NOT exist: pick a sector-appropriate theme and **say in
ONE line which colors you used and that the user can swap them**, e.g. *"Usei uma paleta escura com
acento laranja porque combina com gastronomia. Se você tem as cores da sua marca, é só falar (tipo
'minhas cores são azul e cinza') que eu troco."* If the user gave a logo path or hex colors (now or
later, "minhas cores são X e Y"), use them and offer to persist them in the brand kit. At the END,
offer to save the brand kit so the next proposal is instant. One soft line, never a setup wizard.

## Step 3 — Write the proposal content (read `reference/estrutura-copy.md` AND `reference/anti-ia-escrita.md`)
Write the PT-BR copy like a real freelancer, not like AI: **no travessão "—"**, no AI tells — follow
`reference/anti-ia-escrita.md` and run its self-check before Step 5.
Build every section in the canonical order, client-centric, in Brazilian PT-BR:
capa → resumo executivo → contexto/diagnóstico (the client's pain FIRST) → solução →
escopo (incluso / não-incluso) → cronograma → investimento → (prova social só se fornecida) →
garantia → condições comerciais → próximo passo (single-focus CTA). Decide single price vs
3 níveis (good-better-best) per the reference. Keep it tight (5-8 pages of content). Frame
price as investimento/resultado, not custo. No placeholder survives this step.

## Step 4 — Payment conditions, and Pix ONLY if asked (read `reference/pix.md`)
Always write a clean **"Condições comerciais"** section (forma e prazo: à vista/parcelado, entrada
+ saldo, mensal). **Pix is opt-in and OFF by default** — most proposals don't embed one. Include the
Pix block ONLY if the user asks ("põe o Pix", "quero o QR pra entrada") or the brand kit has
`pix_incluir: sim`. If the user gave a price but didn't mention Pix, you MAY ask ONE quick yes/no
(*"Quer que eu inclua um Pix com QR pra ele pagar a entrada na hora, ou deixo só as condições de
pagamento?"*) — default to NO if they don't care. When Pix IS wanted and a key is available, write a
JSON config and run `node assets/pix.js` for the real copia-e-cola + QR SVG; validate the key type
(ask only if an 11-digit key is ambiguous CPF×celular); embed the QR SVG and keep the string for
chat/WhatsApp. No key / node down / not wanted → conditions section without Pix (delete the Pix block
from the template), honestly.

## Step 5 — Build the premium deck + render the PDF (read `reference/design-system.md` then `reference/render-pdf.md`)
The output is a **cinematic landscape DECK** (A4 landscape slides), not a plain document — this is what
makes it demo-worthy. Pick a **theme** for the client's sector (`reference/design-system.md`: meia-noite /
petróleo / esmeralda / vinho / grafite-claro, or the brand-kit colors), then clone
`assets/template-proposta.html` and fill it: two-tone display headlines, icon cards (use the inline
`<use href="#i-...">` icons, NEVER emoji), the big price callout, base64 logo, ghost watermark, and
(only if opted in) the Pix QR. Obey the anti-slop forbid list. **Delete optional slides you don't use**
(prova social, the Pix block) and ensure NO `{{TOKEN}}`/lorem survives. Write the self-contained HTML to
the archive folder, then detect a headless browser and render to PDF **in landscape** with the exact
command in `reference/render-pdf.md`. Narrate: *"Montando o deck... gerando o PDF..."*. No browser found →
deliver the HTML + the one-line Ctrl+P → Salvar como PDF instruction (it's self-contained, looks identical).

## Step 6 — Archive + WhatsApp + hand back (read `reference/dados-e-saida.md`)
Save to `.claude/propostas/<empresa-slug>-<AAAA-MM-DD>-proposta.{pdf,html}` (today's date;
create the folder; never overwrite — if a prior proposal for this empresa exists, bump to a new
file and note "essa é a 2ª/3ª versão" + what changed). Write the WhatsApp text to
`...-whatsapp.txt` AND show it in the chat in a copy-paste block: a personalized hook (anchored
on a real fact, never invented) + a clear CTA. Tell the user where the files are. Offer the
brand-kit save if not yet persisted. Re-run nudge: *"roda de novo pra cada cliente novo — o
brand kit fica salvo, então a próxima sai na hora."*

## Degraded mode
- **No headless browser:** deliver the self-contained HTML + the one-line Ctrl+P instruction.
  Never claim a PDF was generated if it wasn't.
- **No node:** skip the Pix QR/string, build the proposal with a generic "Condições comerciais"
  section, and tell the user the Pix automática needs node (it ships with o Claude Code).
- **No logo:** clean text-based cover (empresa + serviço + data) — still premium.
- **No Pix key:** payment-conditions section without Pix; offer to add a key to the brand kit.
- **Empty/garbage input:** one combined question; if refused, do not dead-end — build a clear
  template proposal for the stated service with sensible defaults and say which defaults you used.
Never fabricate data to fill a gap; cut the section or say it plainly.
