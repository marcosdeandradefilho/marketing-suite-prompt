---
name: mafi-rascunho
description: Ensina Claude a materializar o impulso em rascunho MAFI — escrever tudo e tudo sem julgar, nunca confiar na memoria, produzir texto bruto com voz ja afinada — e a continuar textos interrompidos preservando voz, pulso e decisoes anteriores. Use quando o comando /rascunhar ou /continuar for dado, quando a planta baixa estiver pronta, quando o usuario colar um texto inacabado pedindo sequencia, e sempre que for preciso produzir prosa nova em vez de analisa-la.
---

# 11 — Rascunho

Fase do **impulso materializado**. Aqui não se julga: escreve-se.

> Uma oração pensada é muito diferente da oração escrita. Tem outro ritmo, outra
> montagem. As palavras precisam estar diante dos olhos.
> Gore Vidal: *a frase que soa na mente muda quando aparece no papel. Então começo a
> cutucá-la com a caneta, descobrindo novos significados.*

**Nunca confiar na memória.** História se materializa.

## 1. Preparação (5 minutos, obrigatória)

Antes de escrever uma linha:

```
1. Ler a ficha da obra em MEMORY.md
2. Ler a planta baixa: regime, foco, tom, andamento, ângulo
3. Ler as gramáticas dos personagens que entram neste bloco
4. Reler a última frase escrita (se houver) em voz alta
5. Declarar internamente: "quem escreve este bloco é ___" (personagem, não autor)
```

Se algum item faltar, volte à skill 10. Rascunhar sem planta produz texto genérico.

## 2. Regras do rascunho

| Faça | Não faça |
|---|---|
| Escreva o bloco inteiro sem parar | Não corrija enquanto escreve |
| Deixe frases feias passarem | Não use `[...]` nem "descrever depois" |
| Escreva demais e corte depois | Não escreva de menos por medo |
| Marque dúvidas com `{{?}}` | Não interrompa para pesquisar |
| Mantenha a gramática do personagem | Não melhore a fala dele |
| Escreva a cena que dá medo | Não pule para a cena seguinte |

O medo é diagnóstico: a cena que assusta é a cena que importa. Clarice: *é preciso não
ter medo de criar.*

## 3. Como abrir um texto MAFI

A abertura é a armadilha. Cinco padrões testados — escolha um e comprometa-se:

```yaml
1_de_chofre:
   modelo: Charles Bovary jogado no palco-sala
   uso: personagem que não terá chance de se explicar nunca
   forma: gesto público que o expõe, sem uma palavra de caracterização

2_por_degraus:
   modelo: "uma moça" → "a moça" → "a srta." → "Emma" → "a sra. Bovary"
   uso: personagem dissimulado, que o leitor só terá inteiro no fim
   forma: escada de artigos e nomes ao longo do texto

3_voz_que_ja_comecou:
   modelo: "Vim a Comala porque me disseram que aqui vivia meu pai"
   uso: obra polifônica; o leitor entra numa conversa em curso
   forma: primeira frase com informação de terceiros, não do narrador

4_cenario_como_profecia:
   modelo: o pó sobre as folhas em Adeus às armas
   uso: quando o desfecho precisa estar no ar desde o início
   forma: material, sem adjetivo de opinião, fechando em ausência

5_inventario_material:
   modelo: "Desempregado há dois meses. Sapato furado, camisa puída."
   uso: primeira pessoa; intimidade imediata
   forma: o que se tem e o que falta; nada do que se sente
```

**Proibido abrir com:** clima meteorológico decorativo, despertar do personagem,
pergunta retórica, citação, definição abstrata, "havia" existencial.

## 4. Escrita do corpo — laço operacional

Para cada bloco da planta:

```
a. Localize o pulso: qual é o estado do personagem neste bloco?
b. Escolha o andamento que o traduz (ou o contraria, com razão).
c. Escreva a cena inteira, começando no gesto e terminando uma batida cedo.
d. Não explique nada. Se explicou, deixe — vai sair no burilamento.
e. Marque com {{?}} tudo que precisou inventar fora da planta.
f. Passe ao bloco seguinte sem reler.
```

Reler enquanto escreve mata o impulso. Releitura é fase seguinte.

## 5. `/continuar` — retomar texto interrompido

Protocolo de continuidade, executado **antes** de escrever qualquer palavra nova:

```yaml
1_leitura:
   - ler MEMORY.md (ficha da obra)
   - ler o texto existente INTEIRO, não só o final

2_extracao_de_dna:
   voz:        "quem escreve? narrador oculto colado a quem?"
   pontuacao:  "que sinais dominam? de quem são?"
   tempo:      "perfeito, imperfeito, presente? há mistura? onde?"
   lexico:     "campos semânticos recorrentes; nível de registro"
   andamento:  "orações por período; extensão média do parágrafo"
   tiques:     "construções que se repetem — são reiteração"
   furos:      "o que foi aberto e não fechado"
   ecos:       "o que foi plantado e ainda não voltou"

3_declaracao:
   "escreva para si o DNA em 6 linhas antes de continuar"

4_juncao:
   - a primeira frase nova NÃO deve chamar atenção
   - continue no meio do movimento, não no começo de um novo
   - use um dos tiques identificados na terceira ou quarta frase, para selar

5_verificacao:
   - cubra a linha de junção e leia dez linhas antes e dez depois
   - se der para adivinhar onde a máquina entrou, refaça
```

**Se o texto existente contradiz a planta baixa, o texto ganha.** Atualize a planta e
registre a mudança.

## 6. Ferramentas de desbloqueio

Quando o rascunho travar, aplique uma destas, nesta ordem:

1. **Pergunta ao personagem.** Escreva a pergunta e deixe que ele responda em primeira
   pessoa, fora do texto. Aproveite duas palavras da resposta.
2. **Mudança de foco temporária.** Escreva a mesma cena pelos olhos de outro personagem.
   Você não vai usar — mas vai saber o que falta.
3. **Cenário puro.** Descreva o lugar sem ninguém, por dez linhas. O personagem volta
   sozinho.
4. **Regra de Calvino.** Dê-se um exercício de escola: "descrever uma girafa",
   "descrever um céu estrelado". Encha um caderno; extraia a matéria depois.
5. **Corte o parágrafo travado.** Quase sempre ele estava explicando algo.

## 7. Entrega do rascunho

Antes de entregar: grave (crie ou atualize) `Desktop\MARCOS_ESCRITOR\obras\<slug-do-
titulo>.md` com o texto corrido de todos os blocos escritos até aqui — nunca deixe o
texto existir só na resposta do turno. Releia o arquivo em disco a cada nova sessão
sobre a obra: se o autor editou manualmente, é o texto dele que vale, e a diferença
entra em pauta antes de continuar (ver `CLAUDE.md` §6, decisão do autor de 2026-08-06).

Ao terminar, entregue ao autor:

```
TEXTO
<o rascunho corrido, sem comentários dentro>

---
NOTAS DE RASCUNHO
bloco_alterado_em_relacao_a_planta: <o que mudou e por quê>
duvidas: <lista dos {{?}}>
furos_abertos: <quais>
onde_eu_expliquei_demais: <autodiagnóstico honesto, 2 a 3 pontos>
proximo_passo_sugerido: /burilar
```

O autodiagnóstico é obrigatório. Rascunho entregue como se fosse final é a forma mais
comum de sabotar a obra.

## 8. Quantas vezes reescrever

Hemingway reescreveu o final de *Adeus às armas* trinta e nove vezes no manuscrito e
modificou-o trinta vezes nas provas. Carrero reescreveu *Viagem no ventre da baleia*
cinco vezes.

Os novos autores só veem o publicado. Não sabem o esforço, as noites insones, os dias
sacrificados.

**Norma MAFI:** nenhum texto vai ao autor como final antes de três passagens completas.

## Referência cruzada

- Investigação frase a frase → `skills/12-burilamento/SKILL.md`
- Voz e gramática de personagem → `skills/02-voz-narrativa/SKILL.md`, `skills/04-personagem/SKILL.md`
- Onde cortar → `skills/07-elipse-e-bordado/SKILL.md`
- Registro da sessão → `skills/15-memoria-e-coerencia/SKILL.md`
