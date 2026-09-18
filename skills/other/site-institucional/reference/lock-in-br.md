# lock-in-br.md — the Brazil-specific elements that a foreign template never has

These are first-class, not afterthoughts. They are also the strongest trust + conversion signals for a
local BR business. Sources: BR design articles, ANPD 2026 cookie guidance, BCB Pix/EMV, Google Maps embed.

## Floating WhatsApp button (the #1 BR conversion CTA, esp. mobile)
Link format: `https://wa.me/55DDDNUMERO?text=<URL-encoded message>`. Pre-fill a context message and
URL-encode it (`%20` etc.).
```html
<a class="wa-float" href="https://wa.me/5511999999999?text=Ol%C3%A1!%20Vim%20pelo%20site%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es."
   target="_blank" rel="noopener" aria-label="Falar no WhatsApp">
  <!-- inline SVG WhatsApp glyph (currentColor) --></a>
```
```css
.wa-float{ position:fixed; right:1.25rem; bottom:1.25rem; width:56px; height:56px; border-radius:50%;
  background:#25D366; display:grid; place-items:center; color:#fff; z-index:60; box-shadow:0 8px 24px rgba(0,0,0,.18); }
@media (prefers-reduced-motion: no-preference){ .wa-float{ animation: wa-pulse 2.4s ease-out infinite; } }
@keyframes wa-pulse{ 0%{box-shadow:0 0 0 0 rgba(37,211,102,.5)} 100%{box-shadow:0 0 0 18px rgba(37,211,102,0)} }
```
Every section CTA ("Fale no WhatsApp", "Agende", "Peça um orçamento") points to the same wa.me link, ideally
with a section-specific `text=` (e.g. "...sobre o tratamento X"). If the WhatsApp number is unknown → leave
`55DDDNUMERO` with a `<!-- TROCAR: WhatsApp -->` and tell the user.

## BR footer (must include)
Razão social + **CNPJ** · endereço completo · **horário de funcionamento** · telefone/WhatsApp clicável ·
e-mail · links de redes (Instagram) · "Política de Privacidade" + "Termos" links · (Google Maps embed often
sits here or in Contato). The footer is also where many BR sites keep the cookie notice. Unknown fields →
`<!-- TROCAR: CNPJ -->` markers, never invented.

## LGPD cookie banner (pure JS, no library, localStorage)
ANPD 2026 wants a two-level banner with an easy "Rejeitar todos" alongside "Aceitar". Pragmatic zero-config
minimum = a dismissible bottom bar: short PT-BR text + **Aceitar** + **Recusar** + a link to the Política de
Privacidade, choice persisted in `localStorage`.
```html
<div id="cookie-bar" hidden role="dialog" aria-label="Aviso de cookies">
  <p>Usamos cookies para melhorar sua experiência. <a href="/politica-de-privacidade.html">Política de Privacidade</a></p>
  <div><button id="cookie-reject" type="button">Recusar</button><button id="cookie-accept" type="button">Aceitar</button></div>
</div>
<script>
  const bar=document.getElementById('cookie-bar');
  if(!localStorage.getItem('cookie-consent')) bar.hidden=false;
  const set=v=>{localStorage.setItem('cookie-consent',v); bar.hidden=true;};
  cookie-accept.onclick=()=>set('accept'); cookie-reject.onclick=()=>set('reject');
</script>
```
Always generate a matching `politica-de-privacidade.html` page (template PT-BR; tell the user to have it
reviewed). Don't claim legal compliance — say it's a base.

## Pix copia-e-cola box (OPT-IN, OFF by default)
Include ONLY if the user asks (or brand kit `pix_incluir: sim`). **Reuse the bundled `assets/pix.js`** — do
NOT hand-write a Pix string (a wrong CRC = a dead code). It's deterministic, Node-stdlib-only, zero-config.

Invoke at BUILD time (the generated site embeds a STATIC string + SVG QR — works offline, no JS/network):
```bash
echo '{"key":"<chave>","keyType":"email|cpf|cnpj|phone|evp|auto","name":"NOME ATE 25","city":"CIDADE","amount":150.00,"txid":"***"}' | node assets/pix.js
# → {"brcode":"...6304XXXX","keyType":"...","ambiguous":false,"svg":"<svg ...>","svgOk":true}
```
- `amount` optional (omit = valor aberto). `ambiguous:true` (11-digit key) → ask "CPF ou celular?" and re-run
  with explicit `keyType`. `svgOk:false` → use the copia-e-cola string alone (still valid).
- CRC = CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF, no final XOR) over the full payload incl. `6304`.
  Canonical `123456789 → 29B1`. Render: merchant name + monospace textarea with the brcode + a "Copiar código
  Pix" button (`navigator.clipboard.writeText` + "Copiado!" feedback) + the inline SVG QR.
- `node` unavailable → never fake it; offer the box without QR or skip it and tell the user.

## Google Maps (keyless)
Use the share-iframe ("Compartilhar → Incorporar um mapa" gives `<iframe src=...>`) — no API key, keeps the
buyer zero-config. Accept either a Maps share/embed URL OR a plain address from the user. Wrap with a reserved
aspect-ratio to avoid CLS. The official Maps Embed API needs a key → don't use it.

## Contact form WITHOUT a backend (and it must WORK)
On submit, build a `wa.me` link with the fields URL-encoded into `text=` (Nome/Telefone/Mensagem) and
`window.open` it; fall back to `mailto:` with subject/body. Default = WhatsApp submit (most local niches);
mailto secondary. Anti-slop: the form must have **required-field indicators, JS validation, error states,
ARIA labels, keyboard nav, `:focus-visible`** — not a fake form.
```js
form.addEventListener('submit', e=>{ e.preventDefault();
  if(!form.checkValidity()){ form.reportValidity(); return; }
  const t=`Nome: ${nome.value}%0ATelefone: ${tel.value}%0AMensagem: ${msg.value}`;
  window.open(`https://wa.me/5511999999999?text=${t}`,'_blank','noopener');
});
```
Optional opt-in: a Formspree/FormSubmit endpoint for inbox delivery — never the default (needs signup).

## JSON-LD LocalBusiness (pt-BR) — in `<head>`
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"LocalBusiness","name":"<Nome>","inLanguage":"pt-BR",
  "url":"<canonical>","telephone":"+5511999999999","image":"<og-image url>",
  "address":{"@type":"PostalAddress","streetAddress":"<rua, nº>","addressLocality":"<cidade>",
    "addressRegion":"<UF>","postalCode":"<CEP>","addressCountry":"BR"},
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","..."],"opens":"09:00","closes":"18:00"}],
  "priceRange":"$$" }
</script>
```
Use the most specific subtype when it fits (Dentist, HealthAndBeautyBusiness, LegalService, Restaurant,
AccountingService, etc.). One JSON-LD block per physical location. CNPJ is not a schema field — keep it in
the footer text. (The `$$` priceRange is a schema literal, not a price shown to the user — never surface a
bare `$` in user-facing copy.)

## Trust seals by niche
Clínica estética → ANVISA/biossegurança · dentista → CRO · médico → CRM · advogado → OAB · contador → CRC ·
academia/personal → CREF · arquiteto → CAU · construtora/engenharia → CREA · imobiliária/corretor → CRECI.
Show the registration number where the niche expects it (footer and/or Sobre).

## WhatsApp delivery message (gere sempre → `ENTREGA-whatsapp.txt` + bloco no chat)
Keep consistent with skill 07. 4 parts: (1) saudação + nome do cliente; (2) gancho 1-2 linhas ancorado num
fato REAL (nunca inventado); (3) uma linha "segue o site / o link"; (4) UM CTA. Tone: curto, humano, PT-BR
direto, no máximo 1 emoji, nunca com cara de template. Ex.:
```
Oi, [Cliente]! Terminei o site da [Empresa].
Deixei tudo pronto pra rodar no celular e com o botão de WhatsApp já apontando pro seu número.
Segue o link pra você ver: [URL]
Me diz o que achou que eu ajusto o que precisar.
```
