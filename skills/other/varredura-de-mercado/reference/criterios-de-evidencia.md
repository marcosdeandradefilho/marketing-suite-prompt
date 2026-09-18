# Critérios de evidência (anti-bluff)

Este é o arquivo que protege a credibilidade do produto. As regras NÃO são aspiracionais — são
verificadas no passo de auto-verificação obrigatório antes de escrever o relatório.

## Banido (rígido)
- Nome de empresa inventado.
- Faturamento / MRR inventado.
- "estudos mostram" / "pesquisas indicam" sem URL real desta sessão.
- QUALQUER cifra gringa de arbitragem hardcoded. Acha a cifra AO VIVO a cada run — nunca de memória.
- R$ não rastreável a uma página fetchada → obrigatório rotular `estimado (base AAAA)` + raciocínio.

## Notação de moeda (regra única)
- A **oferta/ticket que você recomenda é SEMPRE em R$.**
- Preço de produto gringo (arbitragem) pode aparecer como **`US$`** (ex.: `US$19/mês`) — nunca um `$` solto.
- Proibido `$` isolado como unidade (ex.: `$5`, `$80k`). Só `R$` e `US$` são permitidos no texto.

## Relato não auditado
Todo número de faturamento/contrato auto-reportado leva o selo **"relato não auditado"**. NÃO
hardcode caso nomeado como verdade — verifica ao vivo e marca. Casos que sobreviveram ao fact-check
da pesquisa (usar SÓ com o selo, e só se reconfirmados ao vivo na sessão):
- Guilherme ~R$60k em 2 meses (agentes de IA, atendimento/qualificação).
- ChatADV / Paulo Dantas ~R$160k/mês (micro-SaaS jurídico no WhatsApp) — UM caso, não dois, não R$200k.
- Tintim ~R$500k MRR (rastreio de vendas no WhatsApp) — não R$1M.
- VetGPT / AiVets "mais de 1.000 veterinários" — não 10.000.

## Passo de auto-verificação (obrigatório, antes de escrever)
Relê CADA cartão. Pra cada URL/empresa/R$: foi mesmo retornado por um WebSearch/WebFetch NESTA
sessão? Se não veio da sessão → rebaixa pra "estimativa" ou move pra DADOS INSUFICIENTES. Mantém a
conta "buscas tentadas vs. buscas que voltaram dado usável".

Dois lints finais antes de emitir:
1. **Moeda:** todo `$` no texto é parte de `R$` ou `US$`. Nenhum `$` solto (ex.: `$19/mês` → `US$19/mês`).
2. **URL:** cada link de produto nomeado resolve PRO produto daquele nome — sem URL duplicada apontando pra outro produto, sem slug quebrado.

## Fetch-integrity gate
Página com "Just a moment" / `cf-challenge` / "Enable JavaScript" / formulário de login / menos de 3
valores R$ numéricos → DESCARTA, nunca resume. Vai pra DADOS INSUFICIENTES. Bloqueado ≠ sem demanda.

## Exemplo REJEITADO (não fazer)
> "Oportunidade: bot de agendamento pra dentistas. Existe o DentalAI nos EUA faturando US$80k/mês,
> sem nada igual no Brasil. Ticket R$2.000/mês."

Rejeitado: DentalAI / US$80k não veio de busca (inventado); "sem nada igual no Brasil" afirmado sem
busca BR; R$2.000 sem fonte. **Três bluffs num cartão só** — é exatamente isso que mata a confiança.

## Exemplo ACEITO
> "Oportunidade: agente de WhatsApp de triagem pra clínicas pequenas. **Dor:** 14 reclamações no
> Reclame Aqui sobre demora no atendimento do [incumbente] [link] — 3 citadas abaixo. **Lá fora:**
> [ProductHunt link] cobra US$X. **No BR:** não achei concorrente forte com WhatsApp nativo (busquei
> "triagem clínica brasil", site:.com.br, app-store BR). **Ticket:** serviço similar anunciado a
> R$197/mês [link Kiwify]. Nenhum relato de faturamento usado."

Cada afirmação forte carrega a fonte da sessão. Onde não dá pra provar, ele DIZ que não dá.
