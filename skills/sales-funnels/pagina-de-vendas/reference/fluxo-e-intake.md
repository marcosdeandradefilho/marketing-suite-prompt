# fluxo-e-intake.md — the conversation-first flow, intake, brand reuse, audience temperature

The flagship is conversation-first ON PURPOSE: a sales page is the user's brand voice and money on the
line, so you show the copy + colors and get a go-ahead BEFORE building. That is the opposite of the
"minimal questions, just build" model of the other skills, and it is deliberate. Still: ask the FEW
load-bearing things in ONE consolidated question, infer the rest, never a long form.

## Intake fields
**Load-bearing (block the build until these exist, inferred or asked):**
- **produto / oferta** — what is being sold (curso, mentoria, serviço, software, ebook, comunidade).
- **público-alvo** — who buys (the more specific, the better the copy: "dono de barbearia", not "empresários").
- **preço** — R$ (and whether there's a real "de R$X por R$Y" anchor, and parcelamento).
- **objetivo da página** — venda direta (checkout) / captura de lead (formulário) / agendamento (high-ticket).

**Inferred (state assumptions in the read-back; the user corrects):**
- dor central, transformação prometida, mecanismo único, bônus, prova social disponível, garantia,
  urgência real, tom (mais sóbrio vs mais direto).

## The minimal-question model
- Brief is clear → ONE soft read-back line ("Entendi: página pra vender [X] pra [público], a R$[Y], com
  objetivo de [checkout/lead]. Vou propor a copy e as cores.") then proceed.
- Load-bearing field missing → ONE `AskUserQuestion` with fixed options + a free-text rider. Suggested
  question (combine into one screen, never sequential forms):
  - "O que você vende?" (curso/infoproduto · serviço/freela · mentoria/consultoria · software/SaaS · outro)
  - "Objetivo da página?" (vender direto no checkout · captar lead/inscrição · agendar conversa/call)
  - "Faixa de preço?" (até R$97 · R$98–497 · R$498–1.997 · R$1.998+ · captura grátis)
  - free-text rider: "Me conta em 1-2 linhas o produto, pra quem é, e se você já tem depoimentos/cores."
- Empty / zero-arg → run that same question; NEVER dead-end. If the user refuses to specify, build a clear
  TEMPLATE page for a generic offer in their stated category, with sensible defaults, and say which defaults
  you used + where to swap them.

## Brand reuse (recurrence — read these silently before asking anything)
`Glob` for, in order, and Read the first that exists:
- `.claude/clientes/<slug>/brand.md` (the site skill / this skill persist here)
- `.claude/brand-kit-freelancer.md` (the proposta skill)
- `.claude/brand.md` (a full brand kit: palette hex, fonts, logo path, voice). **If one exists, you
  already have the palette + fonts + logo — do NOT re-ask. Reuse and SAY you reused it** ("Peguei as
  cores e a fonte da marca que você já tem."). This keeps content and page visually consistent.
On a re-run for the same product/client, do NOT reprint byte-identical: surface "o que mudei desde a última
versão" (nova oferta, novo preço, versão fria pro Meta). Persist back to `brand.md` at the end (Step 5).

## Audience temperature (quente vs frio) — this changes the whole copy
Ask (or infer from the brief) which traffic the page receives. It flips the structure (see
`copy-estrutura.md` §awareness):
- **LISTA QUENTE / warm** (grupo de WhatsApp, e-mail da própria lista, quem já te conhece): nível 3-4 de
  consciência. Skip the IA-101 explaining; open with the **mecanismo único + oferta**, lighter pain, lots
  of trust ("você já me conhece"). Lead de Oferta ou Promessa. Shorter.
- **TRÁFEGO FRIO / Meta Ads** (anúncio, desconhecido): nível 1-2. Much more **pain agitation at the top**,
  name the problem before the product, build authority from zero, more proof, more objection-killing.
  Lead Problema-Solução, Segredo ou História. Longer. **This version must pass `compliance-br.md` hard**
  (Meta bans the ad on income claims / fake scarcity).
Default to the temperature the brief implies; mention you can generate the OTHER version on a re-run (one
product → two pages is a real, honest recurrence reason). Do NOT try to serve both in one page (Schwartz's
fatal error: "genérica pra todos, específica pra ninguém").

## Capture / opt-in pages (objetivo = lead)
If the goal is lead capture (not a direct sale): shorter structure, no price/offer/value-stack block; the
hero promise points at a free thing (aula gratuita, ebook, diagnóstico, lista de espera); the CTA IS the
form (nome + e-mail/WhatsApp, with the LGPD separated-consent rule from `compliance-br.md`); add a one-line
"o que você recebe" + light proof. Keep the premium design bar identical.

## Rebuild path (a URL or "refaz essa página")
Read this when Step 0 detects REBUILD.
- WebFetch the URL with a targeted extraction prompt: pull the headline, every offer/bônus, the price and
  any anchor, the guarantee, all proof/depoimentos VERBATIM, the checkout link, contato. On a cross-host
  redirect, re-call once with the redirect URL.
- KEEP all the real copy/offer/price/proof. You are upgrading the DESIGN and tightening the COPY, not
  inventing a new offer. Improve weak headlines/objection-handling, but never fabricate proof or change the
  price without asking.
- Fetch blocked/empty/JS-only → ask the user to paste the page text (or the offer details); NEVER scrape
  elsewhere or invent the offer. Colors/fonts usually aren't extractable → propose from the product, say so.

## Progress narration (multi-step)
Up front: *"Isto tem duas partes. Primeiro eu te mostro a copy e as cores pra você aprovar. Depois eu monto
a página inteira e te mostro como ficou. Vou te contando no caminho."* Between steps, plain PT-BR, never raw
tool names ("Montando o hero... agora a parte da oferta... gerando o preview pra eu conferir o visual...").
Write files incrementally so an interruption leaves a usable partial page.
