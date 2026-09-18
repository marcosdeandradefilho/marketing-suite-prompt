# design-system.md — o deck premium (o que faz a proposta encantar)

> The output is a **cinematic landscape DECK** (A4 landscape slides), one idea per slide — the format
> agency commercial proposals use, not a plain A4 document. The whole point: someone seeing it should
> think "eu quero isso". Grounded in agency references (sixtythirtyten.co,
> designyourway.net, uxpin, din-studio, Anthropic PPTX skill design guide, Proposify design). RGB
> screen/print-at-home, not offset CMYK. The skeleton lives in `assets/template-proposta.html`.

## Formato
- **A4 paisagem** (297×210mm), uma `.slide` por página, `page-break-after:always`. Renderiza em paisagem
  (ver `reference/render-pdf.md`). Tela-primeiro (abre no celular/PC, manda no WhatsApp), mas imprime limpo.
- ~9 slides: capa · resumo · diagnóstico · solução · escopo · cronograma · investimento · garantia+condições · CTA.
  (prova social só se houver; ver `reference/estrutura-copy.md`.)

## Temas curados (escolha pelo SETOR do cliente; ou use o brand kit)
Cada tema é um conjunto de tokens já calibrado (fundo, acento, glow). Setar via `data-theme` no `<html>`.
Tema escuro é o default premium (as melhores referências de proposta são dark + 1 acento). Use **grafite-claro**
quando o cliente/segmento pedir algo claro e sóbrio (advocacia tradicional, saúde conservadora, governo).

| Tema (`data-theme`) | Cara | Acento | Bom pra |
|---|---|---|---|
| `meia-noite` (default) | preto-azulado + glow laranja | `#ff6a2b` | tráfego, marketing, geral, gastronomia, fitness |
| `petroleo` | petróleo profundo + ciano | `#3fb6c9` | tech, SaaS, dados, serviços digitais |
| `esmeralda` | verde profundo + verde claro | `#36c98a` | saúde, estética, wellness, sustentável, finanças "novas" |
| `vinho` | bordô escuro + rosa | `#e0457a` | beleza, moda, lifestyle, eventos |
| `grafite-claro` | off-white + azul | `#2563eb` | advocacia, contábil, B2B conservador, governo, quando pedirem claro |

Se o brand kit tem `cor_dominante/secundaria/acento`, sobrescreva os tokens `--bg/--bg-2/--accent` direto no `:root`
(o `--glow` = o acento com ~50% alpha; o `--on-accent` = cor de texto que contrasta com o acento, geralmente escura).
Regra dura: **máximo 1 acento por proposta** + neutros. Nunca 2 acentos competindo.

## Vocabulário editorial (o que dá a cara de agência — está embutido no template)
1. **Capa cinematográfica:** fundo full-bleed do tema + um **glow** (radial) e um **arco/ring** brilhante no canto +
   **título DISPLAY gigante bicolor** ("Proposta de" em cinza claro / "[Serviço]" no gradiente do acento) + badge do
   ano + marca do freelancer + meta (preparada por / data / validade) + **watermark gigante** ao fundo.
2. **Título bicolor (two-tone):** toda seção tem headline grande com UMA palavra no acento (`.acc`) e o resto em
   branco/tinta. É o truque visual nº1 das referências. Ex: "O **desafio** de [cliente]", "O **investimento**".
3. **Kicker + régua:** label curto em maiúsculas espaçadas na cor do acento, acima do título, + uma régua curta do acento.
4. **Watermark fantasma:** palavra gigante (a marca do freelancer ou 1 palavra-chave) em contorno (`-webkit-text-stroke`)
   baixíssima opacidade, atrás do conteúdo. Dá profundidade sem poluir.
5. **Cards com ícone:** itens (dores, pilares da solução, "incluído no valor") em cards com **ícone num quadrado com
   gradiente do acento + glow**. **Ícones = SVG inline** (`<use href="#i-...">`), NUNCA emoji. Ícones disponíveis no
   template: target, chart, bolt, check, shield, rocket, monitor, edit, megaphone, users, calendar, arrow.
6. **Número da seção grande:** `02`...`08` no canto, e números gigantes no cronograma (gradiente do acento).
7. **Callout de preço:** o valor em fonte **enorme** com gradiente do acento (`.price-big`) — o bloco mais importante,
   inconfundível. Preço único → hero + faixa "incluído no valor" (3 itens) pra não deixar a slide vazia. Ou 3 níveis
   (good-better-best) com o do meio marcado `.tier.reco`.
8. **CTA de fechamento:** slide só com o headline grande + 1 botão em gradiente com glow + contato. Foco único.

## Tipografia
- Fontes **seguras cross-OS** (sem instalar nada): stack `'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif`
  (Segoe no Windows, Helvetica no Mac — ambas limpas e modernas). Para um ar mais editorial/serifado, troque o corpo
  por `Georgia, 'Times New Roman', serif`. Duas famílias no máximo.
- Display da capa ~74pt; título de seção ~46pt; lead 16pt; corpo 13pt (line-height 1.6); legendas 9-11pt.
- Tamanhos em **pt** (estável na impressão, não px). Medida de corpo ~50em (texto não cruza a slide inteira).

## Cor — 60-30-10 + contraste
- **60%** fundo do tema (dominante) · **30%** estrutura (cards/painéis/secundária) · **10%** acento (preço, CTA, ícones,
  1 palavra do título). A escassez do acento é o que faz ele gritar "aja aqui".
- **WCAG AA:** corpo precisa de 4.5:1. Nos temas escuros, texto é `--ink` (quase branco) sobre fundo escuro = folgado.
  Nunca ponha corpo pequeno em cima do acento saturado (só texto bold/curto com `--on-accent`).

## Forbid list — anti-AI-slop (NON-NEGOTIABLE)
- ❌ **Gradiente roxo/violeta "de IA".** O glow do tema é a cor do ACENTO (laranja/ciano/verde/etc.), aplicado com
  intenção (capa, botão), nunca um degradê roxo aleatório. (Glow intencional do tema ✅; degradê arco-íris/roxo ❌.)
- ❌ **Tudo centralizado.** Conteúdo é alinhado à esquerda (editorial). Centralizar só capa/CTA/callout curto.
- ❌ **Emoji como ícone.** Use os SVGs inline. Emoji em documento profissional mata a credibilidade.
- ❌ **Fonte Inter/Poppins/Montserrat como "default genérico".** Use as stacks de sistema acima.
- ❌ **Cantos arredondados gigantes em tudo** + sombras exageradas. Raio comedido (8-14pt), sombra só no glow do acento.
- ❌ **Foto de banco genérica** (aperto de mão, gráfico subindo). Sem foto é melhor que clichê. (Logo do cliente/freela ✅.)
- ❌ **5+ cores / arco-íris.** 1 acento + neutros.
- ❌ **Parede de texto** numa slide. Uma ideia por slide; o resto vira card/callout/bullet.
- ❌ **Repetir o layout idêntico** slide após slide — alterna split/cards/timeline/hero pra dar ritmo.

## CSS de impressão (já no template; respeitado pelo motor headless)
- `@page { size: A4 landscape; margin:0 }` + margens internas no `.slide`.
- `-webkit-print-color-adjust: exact; print-color-adjust: exact;` no `body` — **força os fundos escuros a imprimirem**
  (sem isso a capa dark sai branca). Essencial pros temas escuros.
- `page-break-after:always` por slide; imagens/logo em **base64** (headless ignora `url()` externo).

## Fontes
- sixtythirtyten.co/blog/60-30-10-rule-complete-guide — 60-30-10 + hex + WCAG.
- designyourway.net/blog/best-fonts-for-professional-documents — stacks de sistema cross-OS.
- uxpin.com/studio/blog/optimal-line-length-for-readability — medida ~66 CPL.
- din-studio.com/7-best-colors-for-branding — psicologia de cor por setor (base da tabela de temas).
- Anthropic PPTX skill design guide (via snyk.io top-skills) — temas curados com hex, callouts grandes, "nunca linha de acento sob título de IA", não repetir layout.
- firecrawl.dev/blog/best-claude-code-skills & proposify.com/blog/proposal-design-best-practices — anti-slop + design que converte.
