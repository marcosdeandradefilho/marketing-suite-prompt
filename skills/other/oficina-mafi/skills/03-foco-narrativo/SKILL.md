---
name: mafi-foco-narrativo
description: Ensina Claude a escolher e operar o foco narrativo de uma obra MAFI — eu ficcional, eu confessional, alter ego, terceira pessoa, alter ego em terceira, segunda pessoa — e a distinguir com rigor foco narrativo de ponto de vista. Use ao decidir quem conta a historia e como conta, ao trocar de foco no meio de um texto, ao diagnosticar distanciamento excessivo ou exposicao indevida do autor, e sempre que o usuario perguntar se escreve em primeira ou terceira pessoa.
---

# 03 — Foco Narrativo

## Definição que resolve metade dos problemas

> **Foco narrativo** é a técnica de enfoque: por onde caminha a observação do narrador
> oculto ou dos personagens. Pertence ao autor.
>
> **Ponto de vista** é a ideologia do personagem: o que ele considera básico sobre os
> assuntos e sobre os outros. Pertence ao personagem.

Confundir os dois produz textos em que todos pensam igual. Um narrador pode dar foco a
um personagem cujo ponto de vista ele detesta — e é aí que a narrativa fica rica.

## Os seis regimes

### 1. Eu ficcional

Primeira pessoa. O `eu` é do personagem, nunca do autor. Não é confissão: é máscara
construída.

- **Ganho:** intimidade brutal. Conversa ao pé do ouvido, de cozinha. Dolorosa e afetiva.
- **Risco:** o autor se assustar e recuar. Escritores medrosos não chegam longe.
- **Marca de qualidade:** o personagem se expõe por completo, o autor não.

Abertura típica — o personagem se dá a ver por inventário material, não por declaração:

> Desempregado há dois meses. Sapato furado, camisa puída. Dinheiro ralo no bolso.

Note: nenhuma palavra sobre o que sente. Só o que tem e o que falta.

### 2. Eu confessional

O `eu` é do autor, conscientemente. Ele se joga inteiro, em julgamento — julgando e
sendo julgado. Não é autobiografia: a autobiografia não admite imaginação; o
confessional admite, e a declara.

- **Quando MAFI usa:** raramente, e sempre com a fratura exposta ("teço, neste papel,
  um passado real, às vezes").
- **Perigo:** vira diário. Se não houver invenção declarada, não é literatura.

### 3. Alter ego

Autor com outro nome e às vezes outras características. Entre o ficcional e o
confessional — quase sempre reúne os dois. Conta os fatos da própria vida e inventa
por cima, alterando nomes e situações.

Modelos: Carlos de Melo (José Lins do Rego), Sal Paradise (Kerouac), Nick Adams
(Hemingway).

Momento mais alto do procedimento — quando o alter ego se estranha:

> Parecia que era outra pessoa que eu criara de repente. [...] Era como se eu me
> sentisse um estranho para mim mesmo.

**Uso MAFI:** o alter ego é a forma privilegiada quando a matéria é herança, pai,
formação, origem. Nomeie o alter ego com metáfora (skill 04) — nunca com apelido do
autor.

### 4. Terceira pessoa

Guarda distância. Deixa o leitor mais solto, menos dentro do texto. Retira do autor a
sensação de exposição.

Atenção: mesmo em terceira pessoa, uma expressão pode denunciar o indireto livre e
puxar o personagem para dentro da frase — e essa oscilação é desejável.

### 5. Alter ego em terceira pessoa

Um personagem representativo do autor, tratado como `ele`. Não é confessional, mas
sugere realidade de forma consciente. Os fatos são fictícios; as revelações,
concretas.

- **Ganho:** permite reflexão pessoal sem custo de exposição.
- **Modelo:** Filipe, de Maximiano Campos; Nick Adams, de Hemingway.

### 6. Segunda pessoa

Raríssima. Sofisticação e requinte. O criador conversa com a criatura, ou um personagem
conversa com outro, ou a morte conversa com a personagem.

> Teresa, muita gente dirá que não existes. Mas eu sei que existes, eu, que há anos te
> observo e muitas vezes te detenho de passagem e te desmascaro.

> Ana Paúcha acorda. Deixa a tua casa antes que ressurja o sol. A lua está morta.
> Ninguém te verá partir.

- **Ganho:** intimidade absoluta, tom de coro grego, imperativo do destino.
- **Custo:** desgaste do leitor. Exige concentração enorme.
- **Regra MAFI:** raríssimo em texto inteiro. Excelente em **irrupções** — um bloco em
  segunda pessoa dentro de um conto em terceira produz vertigem. Marque a entrada e a
  saída com mudança de andamento, nunca com aviso.

## Matriz de escolha

| Se a matéria é... | Regime indicado | Por quê |
|---|---|---|
| ferida do próprio autor, com invenção | alter ego | protege e revela ao mesmo tempo |
| consciência em colapso, tempo curto | eu ficcional | proximidade insuportável é o efeito |
| coletividade, várias existências | terceira + indireto livre | permite circular sem trocar de capítulo |
| destino, fatalidade, voz que ordena | segunda pessoa (bloco) | o imperativo faz o leitor obedecer junto |
| balanço de vida, ajuste de contas | eu confessional | só se o autor aceitar o julgamento |
| infância, herança, formação | alter ego em terceira | distância suficiente para ver |

## Mudança de foco dentro da obra

Permitida e desejável em MAFI. Duas condições:

1. A mudança acontece **numa fronteira de cena ou de bloco**, nunca no meio de um
   movimento emocional.
2. A mudança **muda também o andamento** — se o foco troca e o ritmo continua igual, o
   leitor lê como erro.

Modelo de arquitetura polifônica: *Pedro Páramo*, onde as vozes circulam e nem sempre é
possível dizer quem fala; *Os sinos da agonia*, onde monólogos se entrecruzam até
formarem uma voz só.

## Erro clássico a evitar

Achar que a primeira pessoa expõe o autor. Não expõe. Romances em primeira pessoa não
são romances confessionais: trazem apenas o **eu ficcional**, criado e elaborado para
se confirmar na pele do narrador.

Se o autor hesitar por medo, registre a hesitação em `MEMORY.md` e proponha o alter ego
como ponte. Nunca decida por ele.

## Registro obrigatório

Ao fixar o foco, escreva em `MEMORY.md`:

```yaml
foco_narrativo: <eu ficcional | eu confessional | alter ego | terceira | alter ego em terceira | segunda>
ponto_de_vista_dominante: <de quem é a ideologia que organiza o mundo do texto>
pontos_de_vista_conflitantes: [<personagens que discordam e como>]
irrupcoes_permitidas: [<blocos onde o foco muda, e por quê>]
```

## Referência cruzada

- Vozes entrecruzadas e indireto livre → `skills/02-voz-narrativa/SKILL.md`
- Iluminação recíproca de personagens → `skills/04-personagem/SKILL.md`
- Monólogo, solilóquio, fluxo → `skills/06-dialogos-e-vozes/SKILL.md`
