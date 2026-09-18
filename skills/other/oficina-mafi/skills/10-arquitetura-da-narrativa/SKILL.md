---
name: mafi-arquitetura-da-narrativa
description: Ensina Claude a arquitetar a narrativa MAFI com robustez tecnica total — imaginar, inventar e selecionar (Henry James), esboco, argumento aristotelico, comeco-meio-fim, consequencia e causalidade de Poe, e a planta baixa completa da obra antes de qualquer rascunho. Use apos a entrevista, sempre que o comando /arquitetar for dado, quando o usuario tiver briefing pronto e quiser plano, e quando um texto em andamento precisar de replanejamento estrutural.
---

# 10 — Arquitetura da Narrativa

Aqui a história deixa de ser impulso e ganha planta baixa. Nada de rascunho antes
disto. Nada de improviso depois disto — exceto quando o personagem exigir, e ele vai
exigir.

## 1. A sequência de Henry James

Turguêniev contou a James como nascia o quadro ficcional: quase sempre começava com a
**visão de uma ou mais pessoas**, que pairavam diante do romancista, solicitando-o,
interessando-o justamente como eram e pelo que eram. Ele as via como disponíveis,
expostas ao acaso e às complicações da existência. Via-as com nitidez — e então tinha
de encontrar-lhes as relações adequadas, aquelas em que mais se revelassem.

Daí os três verbos:

```
IMAGINAR  →  INVENTAR  →  SELECIONAR
```

### IMAGINAR

Imaginar o conflito. Tomar as primeiras anotações. Fazer rascunhos. As frases não
prestam; cortar; insistir; duvidar. Detalhar roupas, jeito de caminhar, cenas. **Nada
deve ser descartado.** Um passo de cada vez.

Faulkner sobre *Enquanto agonizo*: "Simplesmente imaginei um grupo de pessoas e as
sujeitei às catástrofes universais da natureza que são as inundações e o fogo, com um
motivo natural que desse sentido ao seu desenvolvimento. Escrever uma história é apenas
uma questão de ir construindo esse momento."

### INVENTAR

Procurar novas intrigas. Envolver outras pessoas. Questionar a relação entre os
personagens. Escrever tudo que se imagina, sem pouso e sem parada, sem definições.
Esboçar diálogos, acrescentar, rasgar. Inventar cenas novas.

### SELECIONAR

Cortar palavras e cenas. Melhorar diálogos. Optar por silêncios e elipses. **Na seleção
está um dos segredos.** Não se leva ao texto conclusivo tudo o que se escreveu. Tudo e
tudo é *antes*; agora, cuidado.

## 2. Começo, meio e fim (Aristóteles)

> **Começo** é aquilo que, em si, não se segue necessariamente a outra coisa, mas depois
> do que existe outra coisa à qual ele estará unido.
> **Meio** é o que se segue a outra coisa e após o que vem outra coisa.
> **Fim** é o que acontece depois de alguma coisa e depois do que não há mais nada.

Aplicação prática: qualquer texto bom se divide assim. Divida um texto de Clarice, de
Vilela, de Kadaré, e a divisão aparece limpa. Faça isso com o seu.

**Advertência:** terminar um texto tem sido um tormento e exige disciplina. Não é
incomum encontrar escritores consagrados que não sabem terminar.

## 3. Consequência e causalidade (Poe)

Poe nega a inspiração: só tendo o **epílogo constantemente em vista** é possível dar ao
enredo o aspecto indispensável de consequência ou causalidade, fazendo com que os
incidentes — e especialmente o tom — tendam ao desenvolvimento da intenção.

```
epílogo em vista → consequência + causalidade + tom → DESENVOLVIMENTO (= enredo)
```

**Regra MAFI:** você não precisa saber tudo. Precisa saber o **fim** e o **tom**. O meio
se descobre escrevendo.

## 4. Da manchete ao argumento — o método completo

### Passo 1 — o furo inicial

Uma manchete, sem ler a matéria:

> "Mulher tenta suicídio no mar e é salva por pescadores"

Pergunta de James: quem é essa mulher, o que fez, o que faz? Qual é o rosto ainda
envolto em sombras?

### Passo 2 — dois textos paralelos

Trabalhe sempre com **dois documentos**:

- um que revela a história
- um que desvenda o personagem (biografia breve, ainda que de linhas contadas)

O segundo destrava a criação. Quase nada dele vai ao texto.

### Passo 3 — o interrogatório

Cada decisão vira pergunta; cada pergunta é respondida por escrito. Modelo:

```
Onde ocorreu? Praia solitária ou não? Barcos?
Ela toma o barco ou entra a pé?
Dois pescadores ou três? Quem são?
Diálogo ou silêncio? Externo ou interno?
É levada para casa, ou tratada na casa de um pescador e depois segue sozinha?
Quem chega ao anoitecer? A polícia? Com que papel?
No dia seguinte, quem lê a notícia — e onde, e com que gesto?
```

Enquanto houver perguntas, elas devem ser feitas. **Nem todas para o leitor; para
registro do autor.**

### Passo 4 — o argumento

O argumento nunca detalha. Resume o objeto da história. Aristóteles resumindo a
*Odisseia* — sem nome de personagem, sem peças soltas:

> Um homem solitário vagueia, durante anos, em terras estrangeiras, pois Posidon o
> impede de voltar; em casa, os pretendentes de sua esposa lhe devoram os bens e ameaçam
> a vida de seu filho; quando, finalmente, se dá o regresso, ele revela a alguns sua
> identidade, ataca e destrói os inimigos, salvando-se.

Argumento resultante do exemplo:

> Uma mulher tenta o suicídio, joga-se no mar depois de breve passeio de barco. É
> socorrida e salva por pescadores. Intimada pela polícia, por motivos ainda sem
> clareza, não pode comparecer à delegacia porque é convocada pelo marido a levar os
> filhos ao colégio. Ao ler os jornais do dia seguinte, ele sabe que a mulher tentou o
> suicídio.

**Critérios de um bom argumento MAFI:**

- [ ] Cabe em 4–6 linhas
- [ ] Não nomeia personagens
- [ ] Não explica motivos ("por motivos ainda sem clareza" é a formulação exemplar)
- [ ] Contém ao menos uma inversão de expectativa
- [ ] Termina num gesto, não numa conclusão

## 5. A planta baixa

Depois do argumento, monte a planta completa. Use `templates/PLANTA-BAIXA.md`.
Estrutura mínima:

```yaml
identificacao:
  titulo_provisorio:
  forma:                 # fragmento | conto | novela | romance
  extensao_alvo:

regime:
  genero_dominante:      # ver skill 09
  tom:
  andamento_base:
  foco_narrativo:        # ver skill 03
  regime_de_voz:         # ver skill 02, §8
  angulo:                # fechado | aberto — ver skill 05

argumento: |
  <4 a 6 linhas>

epilogo_em_vista: |
  <o fim, mesmo que mude depois — Poe exige>

personagens:
  centrais:      [{nome:, metafora_do_nome:, plano_ou_redondo:, gramatica:}]
  secundarios:   []
  ilustrativos:  []
  hierarquia_de_apresentacao: []   # ordem de entrada e por quê

blocos:
  - n: 1
    funcao_no_todo:
    cena_ou_cenario:
    quem_ve:
    andamento:
    furos_abertos: []
    furos_fechados: []
  # repetir

costura_interna:
  eco_plantado:          # a "pequena frase de Vinteuil" desta obra
  onde_planta:
  onde_retorna:
  como_volta_mudado:

elipses_planejadas:
  - tipo:                # fato | motivo | qualidade | tempo | nome | sentido
    onde:
    permanece_aberta:    # sim | não

riscos_assumidos: []     # ver skill 14
recusas: []              # o que esta obra se proíbe de ser
```

## 6. Regra de ouro da arquitetura

A planta baixa **não é contrato**. É armamento. Autran Dourado, Osman Lins e Flaubert
faziam planta baixa e a traíam quando o personagem exigiu. O que não se pode é traí-la
por preguiça.

Toda traição de planta é registrada em `MEMORY.md` com a razão. Sem exceção.

## 7. Antes de liberar para rascunho

- [ ] O argumento cabe em 6 linhas e não explica motivos?
- [ ] O epílogo está em vista?
- [ ] Cada personagem central tem nome com justificativa metafórica?
- [ ] A hierarquia de apresentação está definida?
- [ ] O eco de costura interna está plantado e datado?
- [ ] As elipses estão planejadas por tipo?
- [ ] O gênero dominante e as irrupções estão declarados?
- [ ] Existe uma recusa explícita — a versão fácil que fica proibida?
- [ ] Tudo isso foi gravado em `MEMORY.md`?

Só então: `skills/11-rascunho/SKILL.md`.

## Referência cruzada

- Furos e seleção → `skills/07-elipse-e-bordado/SKILL.md`
- Nome e apresentação → `skills/04-personagem/SKILL.md`
- Regime de gênero → `skills/09-genero-tom-andamento/SKILL.md`
- Registro → `skills/15-memoria-e-coerencia/SKILL.md`
