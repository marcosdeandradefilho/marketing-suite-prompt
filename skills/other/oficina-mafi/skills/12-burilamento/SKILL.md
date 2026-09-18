---
name: mafi-burilamento
description: Ensina Claude a burilar texto MAFI por camadas — investigar em vez de corrigir, aplicar as seis passadas (voz, personagem, cena, elipse, pulsacao, som), emitir laudo tecnico de qualquer texto pronto e reescrever preservando a voz do autor. Use quando o comando /burilar ou /diagnosticar for dado, quando o usuario colar texto proprio pedindo melhoria, quando um rascunho precisar de lapidacao intermediaria, e sempre que for preciso justificar tecnicamente cada alteracao.
---

# 12 — Burilamento

Passagem da **intuição** à **técnica**. Aqui os defeitos aparecem e pedem
**investigação**, não conserto.

> Investigar a frase significa descobrir as suas possibilidades, os defeitos, a
> precisão. Aquilo que está sendo escrito e o que precisa ser escrito.

E a lei que protege o autor: **as sugestões não são imposições.** Numa oficina nada se
impõe. Tudo é colocado em debate. O que parece ruim pode ter função e efeito.

## 1. As seis passadas

Uma passada por vez, do texto inteiro. **Nunca misture passadas** — misturar produz
correção genérica e destrói a voz.

```
PASSADA 1 — VOZ        quem escreve cada frase?
PASSADA 2 — PERSONAGEM cada um tem gramática própria?
PASSADA 3 — CENA       é cena ou cenário? começa e termina onde?
PASSADA 4 — ELIPSE     o que sai? o que fica aberto?
PASSADA 5 — PULSAÇÃO   função e efeito de cada escolha
PASSADA 6 — SOM        rima, eco, aliteração, respiração
```

### Passada 1 — Voz

Para cada parágrafo:

- [ ] Isto é do autor ou do personagem? Se do autor, devolva ao personagem.
- [ ] Há explicação de sentimento? Substitua por gesto ou circunstância.
- [ ] Há marcação de diálogo automática? Remova; devolva só as necessárias.
- [ ] O narrador oculto está à frente ou atrás do personagem? Deve estar atrás.
- [ ] Alguma frase soaria igual em qualquer livro? Reescreva.

### Passada 2 — Personagem

- [ ] Pontuação distinta por personagem?
- [ ] Tempo verbal distinto por personagem?
- [ ] Léxico distinto (registro, campo semântico, tiques)?
- [ ] Algum personagem foi descrito pelo narrador em vez de por outro personagem?
- [ ] Há visão contraditória sobre o central (Teoria da Iluminação)?
- [ ] O nome ainda se justifica metaforicamente após o texto ter crescido?

### Passada 3 — Cena

- [ ] Cada bloco é cena (personagem ativo) ou cenário (fixo)?
- [ ] Há cenário se fingindo de cena?
- [ ] A cena começa no gesto, não na chegada?
- [ ] A cena termina uma batida antes do desejado?
- [ ] O ângulo é consistente com o gênero?

### Passada 4 — Elipse

- [ ] O que pode sair sem que o leitor trave?
- [ ] Algum motivo está explicado? Reabra o furo.
- [ ] Alguma qualidade está nomeada (a doença, a soma, a ofensa)? Retire o nome.
- [ ] Os saltos de tempo estão feitos por verbo, não por advérbio?
- [ ] O furo de sentido está intacto?

### Passada 5 — Pulsação

Aplique o teste de função e efeito (skill 08) a cada recurso marcante. Monte a tabela:

| Recurso | Onde | Função | Efeito | Veredito |
|---|---|---|---|---|
| repetição de "pés" | §3 | comunicação subterrânea entre A e B | identifica cada voz | mantém |
| ponto e vírgula em série | §7 | sincopa a privação | urgência acumulada | mantém |
| adjetivo "sombria" | §2 | — | — | **corta** |

Recurso sem função e efeito declarados **sai**. Sem exceção.

### Passada 6 — Som

- [ ] Rima acidental próxima? (`apaixonou / chorou`) → remover, salvo golpe de eloquência
- [ ] Rima distante e imperfeita? (`paixão / ilusão`) → pode ficar, dá peso
- [ ] Aliteração involuntária? → distanciar ou assumir
- [ ] Eco de vogal recorrente? → é lamentação deliberada ou acidente?
- [ ] Leia em voz alta: onde a respiração falha, a pontuação está errada.

## 2. Investigar ≠ corrigir

Modelo de raciocínio correto, sobre `A moça se apaixonava por um rapaz louro`:

```
Observação:  o imperfeito "apaixonava" parece deslocado; torna a frase falsa.
Investigação: qual é a natureza do imperfeito? Proust — ele relaciona não só as
              palavras, mas toda a vida das pessoas. Aqui a paixão é um evento, não
              uma vida.
Alternativas: (a) "se apaixonou" — perfeito, preciso, definitivo
              (b) manter, se a personagem for de paixões contínuas e indistintas
Decisão:      (a), porque o texto seguinte trata de UMA paixão.
Consequência: "e chorou" agora atropela. Testar "." e testar "chorava".
```

**Sempre apresente ao autor no mínimo duas alternativas com consequências.** Nunca
apenas a versão "corrigida".

## 3. Tabela de operações canônicas

| Sintoma | Operação | Justificativa |
|---|---|---|
| conjunção "e" em excesso | testar substituição por ponto, depois devolver uma ou duas | conjunções fazem curva e dão leveza; pontos pesam |
| palavra que vaga na frase | deslocar para o fim | adensa a informação |
| `sabia que era` + `sabia` | cortar o primeiro | redundância que não é reiteração |
| `mas nunca mais ia voltar` | `nunca mais voltaria` | condicional resolve; evita `mas`+`mais` |
| símile ("como Julieta") | cortar, ou converter em metáfora plena ("uma Julieta") | símile reduz o texto a comparação |
| dois verbos no mesmo tempo criando monotonia | variar tempo com razão declarada | monotonia cede a andamento mais rico |
| artigo indefinido em personagem denso | retirar | densidade psicológica dispensa indefinição |
| artigo indefinido em personagem oscilante | manter | o indefinido define o caráter |
| adjetivo que não muda a leitura | cortar | adjetivo de conforto |
| parágrafo final que conclui | cortar inteiro | fecha o furo de sentido |

## 4. Laudo técnico (`/diagnosticar`)

Quando o autor cola um texto e quer diagnóstico, entregue neste formato exato:

```
LAUDO — <título>
forma: <fragmento|conto|novela|romance>   palavras: <n>

1. VOZ
   diagnóstico: <2 a 4 linhas>
   evidência: "<trecho curto>"
   nota: <0-10>

2. PERSONAGEM
   ...

3. CENA E CENÁRIO
   ...

4. ELIPSE E ECONOMIA
   ...

5. PULSAÇÃO (tom, andamento, efeito, função, ritmo)
   ...

6. GÊNERO E EXTENSÃO
   ...

7. INVENÇÃO E RISCO
   ...

SÍNTESE
o que já é forte: <3 itens, específicos>
o que está impedindo o texto de subir: <o único problema estrutural>
três operações de maior retorno:
  1. <operação> → <ganho esperado>
  2.
  3.
o que NÃO mexer: <o que é assinatura do autor e deve ser preservado>
```

**Regra de honestidade:** nunca abra o laudo com elogio de cortesia. Nunca dê nota 9+
sem evidência. Se o texto for fraco, diga onde cavar — não onde polir.

## 5. Reescrita preservando a voz

Ao reescrever texto do autor:

```yaml
preservar_sempre:
  - tiques sintáticos recorrentes (são reiteração, não vício)
  - léxico pessoal e regionalismo por aproximação
  - pontuação idiossincrática atribuída a personagem
  - imagens matriciais do autor (ver CLAUDE.md §2)
  - aspereza deliberada

pode_alterar:
  - rima acidental
  - explicação de sentimento
  - marcação automática de diálogo
  - símile de repertório
  - adjetivo de conforto
  - parágrafo conclusivo

nunca_fazer:
  - "melhorar" a fala do personagem
  - uniformizar a pontuação entre personagens
  - substituir palavra rara por palavra comum sem razão de personagem
  - acrescentar transição onde havia elipse
```

## 6. Entrega do burilamento

```
VERSÃO BURILADA
<texto limpo, sem marcações>

---
DIÁRIO DE OPERAÇÕES
| # | trecho original | operação | função/efeito | alternativa não adotada |

O QUE FICOU DE PROPÓSITO
<lista das "imperfeições" mantidas, com razão técnica>

AINDA EM ABERTO
<o que precisa de decisão do autor>
```

O bloco "o que ficou de propósito" é o que distingue burilamento de correção. Sem ele,
o autor não sabe se você entendeu a voz dele.

## 7. Quando parar de burilar

Não existe texto perfeito nem definitivo. Mesmo um pequeno texto tem inesgotáveis
redações. Pare quando:

- [ ] Três passadas completas foram feitas
- [ ] Todo recurso tem função e efeito declarados
- [ ] Nenhuma alternativa testada melhorou o resultado
- [ ] O autor reconhece a própria voz no texto

Então: `skills/13-lapidacao-nobel/SKILL.md`.

## 8. Leitura crítica (soma às seis passadas, não substitui)

Antes ou depois das seis passadas técnicas, aplique também os três pressupostos
críticos permanentes do autor — Dalcastagné, Hutcheon, Culler — descritos em
`referencias/criticos-de-referencia.md`. Perguntas: quem fala e quem é falado
(Dalcastagné); a autoconsciência formal serve ao efeito ou é gratuita (Hutcheon); há
convenção naturalizada ou camada cultural relevante (Culler, com ressalva sobre o que
ele é e não é autoridade). Todo achado dessa leitura vira pergunta ao autor — nunca
correção silenciosa.

## Referência cruzada

- Investigação da frase → `skills/02-voz-narrativa/SKILL.md` §5
- Função e efeito → `skills/08-pulsacao-narrativa/SKILL.md`
- Padrões proibidos → `referencias/protocolo-antisimulacro.md`
- Pressupostos críticos permanentes → `referencias/criticos-de-referencia.md`
