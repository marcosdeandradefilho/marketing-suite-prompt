# Fontes e queries

## Princípio
WebSearch's backend is US-localized. FORCE PT-BR + "no Brasil" + `site:.com.br` on every
demand/competition query; pin `allowed_domains` to .com.br/reclameaqui.com.br/gov.br where
supported. English ONLY in the arbitrage tier (T4).

## O que dá pra buscar de verdade (2 probes ao vivo, jun/2026)
NEM tudo está bloqueado, mas tem fonte que oscila. Dois testes reais nesta data deram resultados
DIFERENTES pro Workana, então a regra honesta é: trata marketplace como APOSTA, não como certeza.

- **FETCHÁVEL e confiável (traz R$ real) — usa estes como espinha dorsal do ticket:**
  - **Tabelas de honorários / preço de serviço** (ex.: ledware, ohub e similares) — páginas que listam
    "quanto cobrar por X em 2026" com faixas em R$ e data. Fetcharam limpo e deram o ticket com link.
    Pra serviço B2B (contador, advogado, agência) é a MELHOR fonte de preço.
  - **Google Play BR** — texto das avaliações (minera as de 2-3 estrelas = comprador travado por 1 falha).
  - **Páginas públicas de preço** de concorrente BR e gringo (quando publicam o plano).
- **APOSTA — tenta um fetch rápido, mas NÃO conte com ele (oscila):**
  - **Workana** (`workana.com/jobs`) / **GetNinjas** — QUANDO abrem, mostram orçamento em R$ + data +
    nº de propostas = ouro ("gente PAGANDO por X"). MAS no 2º probe o Workana voltou só a casca (lista
    de projetos carrega por JavaScript depois) e o GetNinjas deu 404. Então: gasta NO MÁXIMO 1 fetch
    nisso; se vier casca/challenge, cai pro snippet `site:workana.com KEYWORD orçamento` e manda o
    usuário conferir na mão. NUNCA cravar um número de pedido pago que você não LEU de verdade.
- **BLOQUEADO de verdade — NÃO finja que leu, snippet do Google / trata como manual:**
  - **Reclame Aqui** — app (SPA) atrás de Cloudflare; os NÚMEROS de reputação carregam por XHR e NÃO
    aparecem no HTML. Lê só o snippet; nunca afirme "índice X" ao vivo.
  - **Hotmart/Kiwify** — dá pra ver QUAIS produtos e o preço, mas a "temperatura"/volume de vendas NÃO
    é público. Nunca invente volume de vendas.
  - **App Store da Apple** — gateada por bot; usa as paradas via busca, não fetch direto.
- **Regra:** se um fetch voltar com challenge/SPA-shell/login (fetch-integrity gate), cai pro snippet
  via `site:` e marca a fonte como "verificar manualmente". Bloqueado nunca vira "não tem demanda".

## Tiers (BR-first)
- **T1 ticket/intenção (PAGAMENTO real):** Workana via WebFetch (orçamento R$ + data); `site:99freelas.com.br` pt KEYWORD orçamento (snippet); GetNinjas; productized-service catalog/menu pages; Hotmart/Kiwify public sales pages (preço, NÃO volume); "procuro freelancer KEYWORD" em grupos.
- **T2 dor:** reviews 1-3 estrelas de apps BR no Google Play (texto fetchável); Reclame Aqui SÓ via snippet do Google (números não renderizam); comentários no YouTube; `site:reddit.com/r/MEI` (via cache do Google); fóruns BR.
- **T3 dinheiro comprovado:** páginas públicas Hotmart/Kiwify; relatos de faturamento (sempre "relato não auditado").
- **T4 arbitragem (EN):** ProductHunt, G2, Capterra, Indie Hackers, app stores US — produto que fatura + preço real.
- **T5 timing:** Exame, Startupi, TechCrunch (funding/launch datados); gov.br / Banco Central (regra/Pix datada).

## Query templates (PT-BR)
- **Dor:** `"KEYWORD" "perco tempo" OR "odeio fazer" site:.com.br`, `KEYWORD reclame aqui`, `KEYWORD review 1 estrela`.
- **Ticket:** `quanto cobrar por KEYWORD brasil`, `KEYWORD freelancer orçamento R$`.
- **Concorrência BR:** `KEYWORD brasil preço R$`, `KEYWORD app brasil`, `site:.com.br KEYWORD`.
- **Arbitragem (EN):** `KEYWORD tool pricing`, `best KEYWORD software`, `site:producthunt.com KEYWORD`.
- **BR-absence confirm:** `KEYWORD brasil`, `KEYWORD pt-br`, busca na app-store BR.

## BLOCKLIST (scam-saturated — never query these)
ganhar dinheiro fácil · renda extra · trabalhe em casa · tarefas pagas · app que paga · dinheiro
rápido · make money online · passive income · get rich.

## ALLOWLIST reframe (professional / business pain)
profissão + "perco tempo com" / "odeio fazer" / "quanto cobrar por" / "planilha" / "relatório" /
"cobrança" / "follow-up"; incumbent-app + "reclame aqui" / "review 1 estrela".

## Reliability notes (do not depend on)
- **Google Trends / pytrends / Keywords Everywhere / AnswerThePublic:** rate-limited/paid/gated — do NOT depend on for "trend" claims.
- **Reddit API:** forbids commercial/automated reads — read only via Google cache, keep dependency low (most BR pain is on Facebook groups / Reclame Aqui / app reviews anyway).
