# Modelo de relatório

Escreve o relatório nesta estrutura. **Duas regras de ouro:**

1. **Leigo entende de primeira.** Sem jargão. O leitor nunca programou e não é da área.
2. **O relatório é lido como TEXTO PURO, dentro do editor do Claude Code — o markdown NÃO é
   renderizado.** Então `**negrito**`, `*itálico*`, emoji e tabelas com `|` viram lixo visual na tela
   dele. NÃO use nenhum desses. O relatório tem que ficar limpo lido cru.

Escreve cada cartão no arquivo conforme clareia (incremental).

## O que NÃO usar (porque o usuário lê cru)
- ❌ `**negrito**` e `*itálico*` — viram asteriscos na tela. Não use. Destaque pela POSIÇÃO (linha
  própria, primeiro da lista), não por formatação.
- ❌ emoji (💰 🌡️ 📎 🥇 etc.) — viram quadradinhos/glifos estranhos. Zero emoji.
- ❌ tabela markdown com `|` — vira uma parede de pipes. Use lista de itens em linhas separadas.
- ❌ HTML (`<sub>`, `<br>`) — aparece literalmente. Nunca.
- ✅ PODE usar: títulos com `#`/`##` (esses o editor colore e ajudam), linhas em branco pra separar,
  listas numeradas simples (`1.` `2.`), e rótulos curtos no começo da linha seguidos de dois-pontos.

## Linguagem plana — OBRIGATÓRIO
Traduz TUDO. Termos PROIBIDOS no texto → use o substituto:

| NÃO escreva | Escreva assim |
|---|---|
| cunha / wedge | a brecha · o espaço que sobrou · o que ninguém ocupou ainda |
| incumbente | quem já domina o mercado · o concorrente já estabelecido |
| arbitragem | "você cobra o preço de quem é técnico, e o Claude Code faz o trabalho pesado" |
| MRR / receita recorrente | mensalidade (o que entra todo mês) |
| PME | pequeno negócio · pequena empresa |
| MEI / ME / EPP | MEI e pequenas empresas (explica "MEI = microempreendedor individual" 1×) |
| done-for-you / feita-pra-você | você entrega pronto, o cliente não mexe em nada |
| fake-door / porta falsa | (não use o conceito; peça uma oferta de verdade) |
| lock-in / fosso / defensibilidade | sua vantagem · o que te protege do concorrente |
| ROAS / CPA / CTR / pixel | só em relatório de gestor de tráfego, explicado 1× (ex.: "CPA = custo por cliente que chega") |
| RIPD / DPO | os documentos/responsável da LGPD |
| wrapper de ChatGPT / commodity | "qualquer IA faz isso sozinha, então não te protege de ninguém" |

## Tom — escreva como gente, não como IA
- Frase curta. Voz ativa. Uma ideia por frase.
- EVITA o travessão (—). Usa ponto, vírgula ou parênteses.
- EVITA a construção "não é X — é Y" e as frases-soco de três palavras ("Dinheiro alto, prova real,
  baixo esforço."). Soam a IA. Escreve direto: "essa é a melhor porque tem preço público e cliente pagando".
- Sem hype de guru, sem promessa de tempo, sem promessa de renda.

---

Estrutura do arquivo (segue esta ordem, em texto puro):

```
# Varredura de Mercado — DD/MM/AAAA

O que eu entendi: {1-2 frases, lente suave do que a pessoa pediu. Sem rótulo tipo "você é perfil C".}

Antes de ler: cada ideia tem quanto dá pra cobrar, quem paga e o primeiro passo. Onde aparece "(fonte N)" tem link de prova no fim do bloco. Onde está escrito "estimativa", é um chute com fundamento, e eu aviso quando é.


## Resumo rápido

{2-4 frases. A recomendação principal e UM número claro. Por que ela é a primeira, em palavras simples. Uma verdade útil que a pesquisa revelou. Fecha com: "Comece pela primeira."}


## As 3 melhores

Primeira. {título curto e claro}.
Quanto cobra: {R$ / horas-semana / R$-mês}.
Trabalho pra montar: {tranquilo / médio / pesado}, {meia linha do porquê}.
Por que ficou em primeiro: {motivo em palavras simples}.

Segunda. {…} {mesmas 3 linhas}

Terceira. {…} {mesmas 3 linhas}

{1 frase fechando: comecei pela primeira porque junta mais procura, mais dinheiro e mais facilidade.}


## Ideia 1. {Título curto, claro, sem jargão}

O que é: {1 frase explicando como pra um amigo leigo.}

Quanto dá pra cobrar: {ESTA é a linha mais importante, vem primeiro. Número concreto. Com fonte → faixa real + (fonte N). Sem preço público → "ainda é estimativa", a âncora usada, e "confirme antes de prometer".}

Quem paga: {público em palavra simples + a dor numa citação curta, se houver, com (fonte N).}

O que você monta: {entregável concreto, que roda no PC do leigo. Sem servidor ligado o tempo todo, sem ferramenta paga.}

Procura: {alta/média/baixa}. Trabalho pra montar: {tranquilo/médio/pesado}.

Por que ficou em primeiro: {1-2 frases conectando procura + dinheiro + facilidade. Responde direto "por que essa".}

Tem gente querendo: {a prova de demanda, em prosa limpa, com (fonte N) no fim das afirmações fortes. Demanda de verdade é gente PAGANDO (pedido pago, preço real, concorrente com cliente), não só gente reclamando.}

Quem já faz, e o que sobra pra você: {concorrentes + a brecha em palavras simples.}

Sua vantagem por ser do Brasil: {WhatsApp, Pix, português, estar perto — o que o concorrente de fora não tem.}

O que pode complicar: {honesto. Precisa de servidor? de advogado? é coisa que qualquer IA já faz? Risco real.}

Primeiro passo: {oferta de verdade, com preço de verdade, pra 5 pessoas reais do ramo. Nunca anunciar o que não existe.}

Fontes:
1. {nota curta}. {url}
2. {nota curta}. {url}


## Ideia 2. {…}
{mesma estrutura. Selo "Também apareceu:" pras 4ª-6ª, sem ranking de medalha.}


## Ideias que testei e descartei

{candidato}. {por que caiu, em 1 frase simples}. Pra checar você mesmo, busque: {query}.


## O que fazer agora

Se você escolher uma, rode a skill de busca de documentação pra ver como os concorrentes já resolveram, e aí mande o Claude Code construir.

Vale rodar de novo quando surgir concorrente novo de fora, mudar regra/Pix/LGPD, ou você entrar num ramo específico.

Se você me disser numa frase o que faz hoje, eu refaço a varredura focada nisso.


## Como cheguei nessa ordem

Isso aqui é só pra você conferir que a ordem não é chute. Pode pular. Cada ideia recebeu uma nota de 0 a 100.

Ideia 1, {título}: {nota} de 100. {o que puxou pra cima/baixo, 1 frase}.
Ideia 2, {título}: {nota} de 100. {…}.

A nota soma sete coisas, cada uma com um peso: procura (peso 25), quanto paga (20), brecha de concorrência (15), facilidade de fazer (15), rapidez pra começar (10), mensalidade (10) e vantagem por ser do Brasil (5).
```

---

## Regras de escrita (lembrete rápido)
- **Texto puro:** zero negrito, zero itálico, zero emoji, zero tabela `|`, zero HTML. O usuário lê cru.
- **Linguagem plana** (tabela de termos proibidos acima). Leigo entende de primeira ou não vale.
- **Link só no rodapé do cartão**, em "Fontes:" como lista numerada. No texto, a afirmação forte ganha um "(fonte N)" que aponta pra lista. NUNCA o link no meio da frase.
- **Dinheiro é a 1ª linha** de cada cartão (logo depois de "O que é"). Estimativa marcada "ainda é estimativa" + a âncora. Nunca mistura número com-fonte e estimado na mesma frase sem rótulo.
- **Cada número com fonte leva uma data quando possível** (ex.: "pedido aberto, junho/2026"). Número sem data nem link = vira "estimativa".
- **"Por que ficou em primeiro/segundo/terceiro"** é obrigatório em todo cartão.
- **A conta de pontos sai do corpo do cartão** e vira o bloco curto "Como cheguei nessa ordem" no fim — só o total + o motivo, sem despejar os 7 sub-números.
- "Número que importa": A = ticket R$; B = horas/semana economizadas; C = R$/mês economizado.
- Tom anti-guru e humano (seção "Tom" acima): frase curta, sem travessão, sem frase-soco, sem hype.
- Moeda: oferta/ticket sempre R$. Preço de fora só como US$, nunca `$` solto.
- 3 a 6 cartões reais valem mais que 6 inchados.
