# Critérios de ranqueamento

Pesos somam 100, cada critério pontua 0-5. Calcula a conta INTERNAMENTE e mostra ela só no apêndice
final do relatório ("Como cheguei nessa ordem") — **nunca dentro do cartão**. No cartão, o usuário vê
linguagem plana: "Por que ficou em 1º/2º/3º" + os dois termômetros (Procura · Trabalho pra montar). A
conta existe pra transparência de quem quiser auditar, não pra leigo tropeçar nela.

**Nota final** = soma de (peso × score/5) por critério.
**Rótulo:** ≥70 = SINAL FORTE · 45-69 = SINAL MÉDIO · <45 ou sem evidência viva = DADOS
INSUFICIENTES (não vira cartão; vai pra "O que descartei").

## Tabela

| Critério | Peso | 0 | 3 | 5 |
|---|---|---|---|---|
| Evidência de demanda | 25 | palpite, nada na busca | ≥3 URLs distintas/datadas/no-tema pedindo ou reclamando, OU 1 brief pago real | múltiplos briefs pagos + sinal de dinheiro forte + concorrente com clientes pagantes |
| Ticket em R$ | 20 | sem número rastreável | ticket real achado numa página | ticket alto e/ou recorrente, com link do preço |
| Brecha de concorrência no BR | 15 | BR já bem servido | tem concorrente, mas com buraco claro | fatura lá fora, fraco/caro/mal-localizado no BR (com as buscas mostradas) |
| Buildável por leigo no Claude Code | 15 | exige servidor/API paga/scraping logado/app store | precisa de ajuste mas roda local | entregável que o Claude Code cospe local (doc/script/conteúdo/análise) |
| Tempo até o 1º R$ | 10 | depende de muita coisa | dá pra começar a oferecer logo | oferta vendável já na próxima semana |
| Recorrência | 10 | one-shot puro | parte recorrente | receita mensal natural |
| Trava BR (defensibilidade) | 5 | nenhuma | uma trava (PT-BR ou Pix ou WhatsApp) | PT-BR + Pix + WhatsApp + LGPD = fosso contra gringo |

## Regras anti-gaming (obrigatórias)
1. Contagem de demanda ("10+ pedindo") SÓ vale com ≥3 URLs distintas, datadas, no-tema, enumeradas + citação de 1 linha cada. Não mostrou ≥3 → demanda **capa em 2**.
2. PROIBIDO "thread grande" / "tendência subindo" / "+5000%" sem um número/URL capturado nesta sessão.
3. Nenhum score de demanda ≥3 sem PELO MENOS 1 sinal de DINHEIRO (preço R$ real, alguém dizendo "tô pagando caro por", incumbente com clientes pagantes). Só reclamação, sem disposição a pagar, **capa em 3** — nunca 5.
4. A mesma fonte NÃO conta duas vezes (não pode valer em "demanda" e em "concorrência").
5. Timing é desempate SUAVE, não entra como score duro.
6. Cartão sem URL viva da sessão pra cada afirmação forte não é SINAL FORTE — no máximo MÉDIO, ou vai pra DADOS INSUFICIENTES.
7. **Triangulação do número-chave.** O ticket/preço do cartão nº 1 quer **2+ fontes independentes** que
   convirjam antes de ser afirmado como fato. Uma fonte só = hipótese, marca "ainda a confirmar", não
   crava. (Antes a skill repetia a MESMA fonte várias vezes e parecia robusto — não é.)
8. **Data em todo número.** Todo R$/preço/afirmação de demanda leva uma data quando der ("orçamento
   Workana, jun/2026"). Número sem data nem link, ou de página visivelmente velha (>~18 meses) sem
   aviso, **vira "estimativa"** — não conta como prova viva.
9. **Anti-sobrevivência.** Antes de chamar uma brecha de "dinheiro fácil", pergunta: quem JÁ TENTOU
   isso e quebrou/desistiu? Ver só os 3 concorrentes que sobraram superestima a oportunidade (os que
   morreram são invisíveis). Se achar sinal de tentativa fracassada, registra no "O que pode complicar".
10. **Teto quando o sinal de pagamento está bloqueado.** O sinal mais forte de demanda é o pedido pago
   aberto (Workana etc.). Se essa fonte não abriu nesta sessão e a demanda do cartão se apoia só em
   preço-de-serviço + dor, o cartão **não passa de SINAL MÉDIO** — por mais real que o preço seja, falta
   a prova de alguém pedindo a ferramenta exata. Diz isso no cartão e manda o usuário confirmar na mão.

## Ênfase por persona (o "número que importa" muda, a rubrica não)
- **A (do zero):** ranqueia por Ticket × Tempo-até-1º-R$ × Trava BR. Rejeita wrapper-de-ChatGPT que não passa no teste "e quando sair o próximo modelo?".
- **B (automatizar):** número-chave = horas/semana economizadas (+ clientes a mais). A pesquisa web pivota pro ângulo arbitragem/vira-produto.
- **C (PME):** número-chave = R$/mês economizado vs custo real do funcionário/processo (custo CLT ≈ salário-base + ~70-80% de encargos, puxado AO VIVO).

## Gate buildável-por-leigo (operacional)
- **REJEITA / penaliza:** servidor always-on; chave de API paga de terceiro; scraping atrás de login; publicar em app store; tratar dado pessoal em escala (exposição LGPD).
- **RECOMPENSA:** entregável que o Claude Code produz local — documento, script local, ferramenta single-file, conteúdo, análise.
- Cada cartão declara o escopo real no Claude Code pra o usuário saber no que tá se metendo.

## Já-foi-comido (freshness)
Antes de finalizar: a capacidade recomendada já virou feature grátis nativa de uma plataforma/modelo
grande? Se sim, pivota pra camada manual adjacente ou derruba o cartão.
