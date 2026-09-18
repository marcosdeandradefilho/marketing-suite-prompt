# pix.md — Pix copia-e-cola + QR real na proposta (zero config)

> The proposal closes faster when the client can pay the deposit on the spot. We generate a REAL
> static Pix "copia e cola" (BR Code / EMV MPM) with a valid CRC16 + a QR image — via the bundled
> `assets/pix.js` (Node stdlib + bundled `assets/qrcode.js`, MIT). No pip, no npm, no API key.
> **Verified 2026-06:** CRC-16/CCITT-FALSE matches the canonical check value (`"123456789"` →
> `29B1`); the payload re-parses field-by-field; the QR SVG renders.

## When to generate Pix
**Pix is OPT-IN and OFF by default** — most commercial proposals don't embed one. Generate it ONLY when
ALL are true: the user ASKED for it (or the brand kit has `pix_incluir: sim`) AND there's a **price** AND
a **Pix key** available AND a deposit/payment makes sense. If the user gave a price but didn't mention
Pix, you may ask ONE quick yes/no; default NO. Otherwise (the default) build a clean "Condições
comerciais" section WITHOUT Pix and delete the `.pay-pix` block from the template. When Pix IS wanted,
the copia-e-cola string is the GUARANTEED payment path (Pix apps accept pasting it); the QR is polish.

## How to run it
1. Decide the amount: usually the **entrada/sinal** (e.g. 50% or a fixed deposit), not always the
   full value. You may also generate an **open-value** Pix (omit `amount`) so the client types it.
2. Write a JSON config and pipe it to the script via Bash:
```bash
echo '{"key":"<chave>","keyType":"<cpf|cnpj|email|phone|evp|auto>","name":"<nome recebedor>","city":"<cidade>","amount":750,"txid":"PROPOSTA"}' | node "<skill>/assets/pix.js"
```
   On Windows the same works through the Bash tool; if you must use PowerShell, write the JSON to a
   temp file and do `Get-Content cfg.json | node pix.js`.
3. The script prints one line of JSON:
   `{ "brcode": "...", "keyType": "...", "ambiguous": false, "svg": "<svg .../>", "svgOk": true }`
   - `brcode` → the **copia-e-cola** string. Show it in chat + WhatsApp, and print it (small,
     monospace, selectable) under the QR in the PDF so the client can paste it.
   - `svg` → drop directly into the HTML where the QR should appear (it's a self-contained `<svg>`).
   - `ambiguous: true` → the key was 11 digits and could be a CPF or a celular. Ask the user which
     (one quick question) and re-run with the explicit `keyType`.
   - `svgOk: false` → the QR lib didn't load; still use the copia-e-cola string (it works alone).

## Pix key — validate & normalize (so the QR isn't dead)
The key goes RAW into the payload (no dots/dashes). `pix.js` normalizes, but verify the type:
- **CPF:** 11 digits. **CNPJ:** 14 digits. (Both: strip formatting.)
- **E-mail:** as typed, lowercased.
- **Telefone:** must be international `+55DDDNNNNNNNNN`. `pix.js` prepends `+55`.
- **EVP / chave aleatória:** 36-char UUID with hyphens.
- **Ambiguity:** 11 digits is BOTH a CPF and a DDD+celular. Don't guess silently — if `auto`
  returns `ambiguous`, ask: *"Essa chave Pix é seu CPF ou seu celular?"* and re-run with the type.
A wrong type = a QR that fails when scanned, which is worse than no QR. Be sure before shipping.

## EMV BR Code field map (what `pix.js` builds — for reference/debug)
TLV = ID(2) + LENGTH(2, zero-padded) + VALUE. Static Pix:
| ID | Campo | Valor |
|----|-------|-------|
| 00 | Payload Format Indicator | `01` |
| 26 | Merchant Account Info | subcampo `00`=`br.gov.bcb.pix` + `01`=chave (+ opcional `02`=info) |
| 52 | Merchant Category Code | `0000` (genérico) |
| 53 | Moeda | `986` (BRL, ISO 4217) |
| 54 | Valor | decimal com PONTO, 2 casas (`750.00`); omitido = valor aberto |
| 58 | País | `BR` |
| 59 | Nome do recebedor | ≤25 chars, MAIÚSCULAS, ASCII sem acento |
| 60 | Cidade | ≤15 chars, MAIÚSCULAS, ASCII sem acento |
| 62 | Additional Data | subcampo `05`=txid (`***` se não houver) |
| 63 | CRC16 | 4 hex MAIÚSCULOS — CRC-16/CCITT-FALSE (poly `0x1021`, init `0xFFFF`) sobre tudo incluindo `6304` |

`pix.js` já cuida de acento/maiúscula/limite. Name/city longos são truncados, não rejeitados.

## Condições comerciais (norma BR — escreva esta seção)
- **"Condições de pagamento" = quando/como** (à vista, parcelado, entrada + parcelas, prazo).
  **"Formas/meios" = canal** (Pix, boleto, cartão, transferência). Liste os dois com clareza.
- Padrões comuns: à vista no Pix com desconto; entrada (ex: 50%) + saldo na entrega; parcelado em
  cartão; mensal pra serviços recorrentes (ex: gestão de tráfego R$ X/mês).
- Inclua a **validade da proposta** ("válida por 15 dias") e o que acontece ao aprovar.
- Mantenha **simples** — confusão de pagamento é dos maiores matadores de fechamento no fim do funil.
- **Não** dê conselho jurídico/tributário. Se o serviço esbarrar em limite de MEI ou regra fiscal,
  uma linha sóbria ("confirme o enquadramento com seu contador") — sem afirmar classificação legal.
- **Regra incerta:** "Pix parcelado/Pix Garantido" estava em definição na pesquisa — **não cite
  como disponível**. Use parcelamento por cartão/entrada+saldo, que são consolidados.

## Degradação
- **Sem chave Pix:** seção "Condições comerciais" sem Pix (entrada+saldo, cartão, etc.) + ofereça
  salvar uma chave no brand kit pra próxima.
- **Sem node:** não dá pra gerar o BR Code com CRC confiável — pule o Pix automático, escreva as
  condições genéricas e avise: *"o Pix automático precisa do node (vem com o Claude Code)"*. **Nunca
  escreva um código Pix 'na mão'** — um CRC errado gera um código que não funciona.
- **`svgOk:false`:** use só a string copia-e-cola (funciona sozinha); não force um QR quebrado.

## Fontes
- tabnews.com.br/usrbinenv/entendendo-o-payload-do-pix-copia-e-cola — campos TLV, regras de 59/60/54.
- github.com/klimadev/gerador-pix — estrutura do campo 26 / GUI / chave.
- askpython.com/python/examples/crc-16-bit-manual-calculation — CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF).
- spcbrasil.com.br/blog/condicoes-de-pagamento — condições × formas de pagamento (norma BR).
