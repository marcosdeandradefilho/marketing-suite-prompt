# compliance-br.md — keep the page legal, the ad account alive, and the tone anti-guru

Read at Step 1, BEFORE
writing any copy or offer. This is not legal advice; it's the guardrail that keeps the user out of trouble and
keeps a Meta Ads account from being banned (the Fase-2 channel that funds the launch). When the user asks for
something risky, decline THAT part in one sober PT-BR line and build the honest version.

## Rule 1 — NO income / earnings claims (the page-killer)
NEVER promise the buyer will make money, get rich, "ganhe R$X por mês", "renda garantida", "viva disso",
"primeiro salário em N dias", "ROI garantido". This is exactly what Meta Ads, the CDC, and the anti-guru
positioning all punish. It also breaks Hotmart/Kiwify policy (renda garantida is grounds for takedown).
- ✅ Allowed: the cost of the ALTERNATIVE, framed as the SELLER's price, never the buyer's earnings.
  "Um dev cobra R$2.000+ por uma ferramenta dessas" (a real market cost) is fine. "Você vai faturar R$2.000"
  is BANNED.
- ✅ Allowed: capability and outcome of the PRODUCT ("você sai com a primeira ferramenta rodando"), not a
  financial promise about the buyer's life.
- If the user insists on an income claim: decline it plainly, explain it can ban the ad + violate the CDC, and
  offer the capability/alternative-cost framing instead.

## Rule 2 — Never invent proof (fatal + illegal)
No fabricated testimonials, faces, names, results, ratings, "alunos", logos, or "antes e depois". Proof appears
ONLY if the user provides it. Unknown → marked `<!-- TROCAR: depoimento real -->` placeholder + initials avatar.
A fabricated "antes e depois" or fake result is publicidade enganosa (CDC art. 37) and a Meta/Hotmart takedown.

## Rule 3 — "De R$X por R$Y" must be a REAL price
A struck-through anchor price ("de R$497") is only honest if R$497 is a price actually charged (now, or after
the lote really rises). A fabricated "de" is publicidade enganosa (CDC art. 37). Same for "valor total R$ X.XXX":
only use a stacked total if every item's value is DEFENSIBLE (real alternative cost / real future price). An
inflated fake total corrodes trust and causes refunds. When unsure, anchor on the alternative cost, not a total.

## Rule 4 — Urgency/scarcity must be REAL (FTC dark pattern + CDC art. 37)
The single test: if the customer verified the claim, would it be true? FORBIDDEN: a countdown that resets on
reload; "2 vagas" with 200; a weekly "flash 24h"; a permanent "últimas vagas". ALLOWED: a real lote cap; a price
that genuinely rises on a real date; launch bônus that actually expire. Max 1 scarcity surface per page. If the
user wants a fake timer, decline and use the real lote→cheio frame.

## Rule 5 — Stats stay OFF the page
The research benchmarks ("+45% cliques", "+266%", "+121%", "+300% valor percebido", "charm pricing +24%") guide
YOUR build decisions only. NEVER print them as claims on the generated page ("aumente suas vendas em 45%") —
that's an unproven third-party number presented as a promise, a guru tell, and potentially misleading. If the
user wants a statistic on the page, it must be THEIR own audited number with a source, or it doesn't go up.

## Rule 6 — LGPD on the form (separate the purposes — ANPD granularity)
A form that collects nome/e-mail/WhatsApp must:
- **Separate consents.** One purpose = product delivery (sending the access) is execution of contract (Art. 7,V),
  so that's an obligatory "Concordo com a Política de Privacidade". A SEPARATE, OPTIONAL checkbox handles
  marketing: "Quero receber novidades por e-mail/WhatsApp (você pode sair quando quiser)". **Access to the
  product can NOT be conditioned on accepting marketing.** WhatsApp ativo needs its own explicit opt-in.
- Checkboxes are **NOT pre-checked**; the Política link is clickable.
- Microcopy near the form: "Pedimos só nome e e-mail pra te enviar o acesso."
- Ship a base `politica-de-privacidade.html` listing: the data collected, the legal basis PER purpose, the
  retention, the user's rights + a contact channel (encarregado/e-mail), per Arts. 9, 18, 41. Mark the
  controller fields `<!-- TROCAR: razão social / CNPJ / e-mail do encarregado -->`.

## Rule 7 — Cookie banner (LGPD/ANPD)
On first visit: a clear banner with **3 visible buttons** (Aceitar / Recusar / Configurar — "Recusar" as easy as
"Aceitar"), the choice stored (localStorage), a Política link reachable afterward. Don't drop non-essential
tags/pixels before consent. (Keep it lightweight; the Meta Pixel slot fires per the user's consent setup.)

## Rule 8 — Decreto 7.962/2013 (e-commerce) footer
The page (or its footer) shows: **razão social, CNPJ, endereço, características essenciais do produto, preço
detalhado** (with the parcela). For an infoproduto, deliver access via login during the 7-day window (not a
permanent download) to preserve the direito de arrependimento. Mark these as `<!-- TROCAR: ... -->` if unknown;
never invent a CNPJ.

## Rule 9 — Guarantee honesty (CDC art. 49)
The 7-day window is a LEGAL right (compra online), not a generous gift. Present it honestly and, to make it a
real conversion lever, stretch it past the floor (14-30 dias). Transparency line: "Os 7 dias são por lei, é seu
direito. Eu estico pra [N] porque confio no que entrego." Never a fake/hard-to-claim guarantee.

## Rule 10 — Platform & ad-policy quick traps (so the page isn't taken down)
- **Meta Ads:** no income claims, no fake scarcity, no "antes e depois" of body/health/wealth, no "você"
  personal-attribute targeting language ("você está endividado?"), a working privacy policy + cookie consent,
  no misleading before/after. A landing that violates policy can flag the whole ad account.
- **Hotmart/Kiwify/Eduzz:** no renda garantida, no fake testimonials, a real guarantee, clear product
  description and price. Keep the checkout link to the real platform.
- **Health/finance/legal niches:** extra caution; no cure/return guarantees; recommend a professional-disclaimer
  line. If the offer itself is a cure-all or get-rich scheme, decline to build it.

## How this shows up in the flow
At Step 1c set the frame: pick the honest anchor, confirm zero income claims, set the real guarantee days, set
the real urgency (or none). At Step 2 the proposed copy already obeys these. At Step 4 the render-loop self-check
greps for income/hype/fake-scarcity phrasing and for any printed stat, and the form/banner/footer are verified.
