# Kishōtenketsu — estrutura de quatro atos sem conflito como motor

Técnica estrutural incorporada em 2026-08-07, a pedido do autor, para uso **a partir da
fase de lapidação** (skill 13). Não substitui a arquitetura aristotélica de causalidade
de Poe (`skills/10-arquitetura-da-narrativa/SKILL.md`) — soma-se a ela como lente
alternativa, útil sobretudo para contos que já nascem sem confronto direto entre forças
opostas e que a lapidação, aplicando só o modelo ocidental, tenderia a "corrigir" na
direção errada.

> [!important] Origem e legitimidade de uso
> Estrutura originada na poesia clássica chinesa (quadras Tang, *qǐ chéng zhuǎn hé* /
> 起承轉合), presente em narrativas chinesas, coreanas, vietnamitas e japonesas —
> molda o mangá, o anime e o dorama contemporâneos. Aplicar a técnica é apropriação
> legítima de método narrativo (mesmo estatuto de aplicar Aristóteles, Poe, Henry James
> ou Genette nesta oficina); **nunca** narrar cenário ou personagem do Extremo Oriente
> como pano de fundo exótico só para justificar o uso — a técnica se aplica a qualquer
> matéria brasileira, sem disfarce.

## Os quatro atos

| Ato | Nome | Função | Erro ao aplicar |
|---|---|---|---|
| **Ki** | Introdução | Constrói um mundo familiar — personagens, ambiente, rotina, sem pressa e sem perturbação | Plantar conflito aqui por hábito ocidental |
| **Shō** | Desenvolvimento | Expande o que o Ki abriu — aprofunda laços, amplia a ambientação, continua a mesma linha | Introduzir a reviravolta cedo demais |
| **Ten** | Virada | Elemento inesperado, revelação ou mudança de perspectiva — muitas vezes **sem relação direta** com os dois primeiros atos; pode mudar até o gênero da história | Explicar a virada; ligá-la cedo demais ao resto |
| **Ketsu** | Conclusão | Reconcilia o Ten com o que o Ki e o Shō estabeleceram — não resolve o Ten, harmoniza-o | Fechar tudo às explicações; reduzir o Ten a "assunto resolvido" |

Diferença estrutural chave em relação ao modelo ocidental: **o Ten não nasce de conflito
crescente** — nasce de contraste e mudança de perspectiva. Personagem oriental típico é
**responsivo** (reage, percebe, se transforma), não **proativo** (persegue um objetivo
contra obstáculos), o que Carrero já preparava com o conceito de personagem que se
revela por circunstância, não por declaração.

## Por que serve à doutrina desta oficina

1. **Compatibilidade direta com skill 13 §V (sentido irredutível).** Um Ketsu que
   reconcilia sem resolver é, estruturalmente, a mesma exigência de "nenhuma epifania
   final" — o kishōtenketsu já nasce sem a tentação da moral explícita que o modelo
   conflito-clímax-resolução empurra por hábito.
2. **Compatibilidade com skill 07 (elipse).** O Ten funciona melhor quando não é
   preparado — é a mesma lógica do "branco" de Proust e da elipse perturbadora: o
   melhor Ten é o que o leitor não viu vir porque a costura (skill 13 §4, "eco") só
   aparece depois, no Ketsu.
3. **Serve para os contos "de relação" do livro em curso.** Contos como "Calada!" ou
   "A Justa Medida" (ver `INDEX.md` de *Vísceras*) já são estruturalmente próximos do
   kishōtenketsu — não têm um antagonista, têm uma virada de percepção. Nomear a
   técnica evita "consertar" esses contos para caber num modelo de conflito que eles
   nunca tiveram.

## Como aplicar na lapidação (skill 13)

Adicionar como pergunta de diagnóstico **antes** da operação `1_abertura`:

```yaml
diagnostico_estrutural:
  pergunta: "este conto é movido por conflito crescente (aristotélico) ou por
    contraste/mudança de perspectiva (kishōtenketsu)? Um conto pode ser mais um
    do que o outro — raramente é 100% de um só."
  se_kishotenketsu:
    - "não force um clímax de confronto; localize o Ten (a virada de perspectiva) e
       teste se ele está genuinamente inesperado, não amarrado por causalidade"
    - "o Ketsu não precisa resolver o Ten — precisa reconciliar Ki+Shō com ele. Se o
       fecho 'explica' o Ten, é panfletarismo estrutural — mesma proibição de skill 13 §V"
    - "a operação '2_fecho' (cortar até doer) vale igual, mas o teste muda: não é 'o
       conflito se resolveu no ponto certo', é 'a reconciliação de perspectiva aconteceu
       no ponto certo'"
  registrar_em: "DOSSIÊ DE LAPIDAÇÃO — campo novo: modelo_estrutural (aristotelico |
    kishotenketsu | hibrido) + localização do Ten quando aplicável"
```

## Vocabulário operacional (evitar tradução forçada)

Não force os termos japoneses na prosa nem no dossiê de forma decorativa. Usar como
categoria de análise interna (como se usa "clímax" ou "peripécia"), nunca como enfeite
erudito no texto entregue ao leitor.

## Fontes consultadas (2026-08-07)

- [Kishōtenketsu Story Structure — Helping Writers Become Authors](https://www.helpingwritersbecomeauthors.com/kishotenketsu-story-structure/)
- [Kishotenketsu: The Secret Of Plotless Story Structure — Writers Write](https://www.writerswrite.co.za/kishotenketsu-the-secret-of-plotless-story-structure/)
- [Kishōtenketsu for Beginners — Mythic Scribes](https://mythicscribes.com/plot/kishotenketsu/)
- [Kishōtenketsu — Wikipedia](https://en.wikipedia.org/wiki/Kish%C5%8Dtenketsu)
- [Kishōtenketsu and Non-Western Story Structures — Nelson Literary Agency](https://nelsonagency.com/2022/01/kishotenketsu-and-non-western-story-structures/)
- [An Introduction To Kishōtenketsu, Contrast Over Conflict — Bang2Write](https://bang2write.com/2024/11/an-introduction-to-kishotenketsu-the-art-of-plot-contrast-over-conflict.html)
