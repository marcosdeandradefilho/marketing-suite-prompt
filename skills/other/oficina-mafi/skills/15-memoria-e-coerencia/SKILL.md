---
name: mafi-memoria-e-coerencia
description: Ensina Claude a ler e escrever MEMORY.md, mantendo registro permanente de todas as obras MAFI em curso e concluidas, decisoes tecnicas, nomes usados, furos abertos e coerencia entre obras. Use ao abrir qualquer sessao, ao encerrar qualquer sessao produtiva, quando o comando /memoria for dado, quando o usuario perguntar o que ja foi escrito, e sempre antes de nomear personagem, escolher imagem ou repetir estrutura.
---

# 15 — Memória e Coerência

Sem este arquivo, a oficina recomeça do zero a cada conversa e contradiz a si mesma. Com
ele, MAFI tem obra — não textos avulsos.

## 1. Duas obrigações inegociáveis

```
ABERTURA DE SESSÃO → ler MEMORY.md antes de qualquer resposta
FIM DE SESSÃO      → escrever em MEMORY.md antes de encerrar
```

"Sessão produtiva" é qualquer troca que gerou: decisão de poética, nome, argumento,
planta, rascunho, burilamento, lapidação ou abandono.

## 2. Leitura — o que procurar, na ordem

```yaml
1_indice:    "existe obra relacionada ao pedido atual? retomar em vez de recomeçar"
2_lexico:    "o nome/imagem que eu ia usar já foi usado? é autoplágio ou eco deliberado?"
3_decisoes:  "há decisão de poética vigente que restringe esta obra?"
4_ficha:     "se a obra existe, ler ficha inteira antes de escrever uma linha"
5_furos:     "há furo transversal aberto que esta obra pode alimentar?"
6_diario:    "qual era o próximo passo declarado na última sessão?"
```

Se `MEMORY.md` estiver vazio, diga isso ao autor em uma linha e siga. Não invente
histórico.

## 3. Escrita — as cinco atualizações

Ao encerrar, atualize **nesta ordem**:

### 3.1 Índice de obras

```markdown
| # | Título | Forma | Estado | Palavras | Última sessão |
|---|--------|-------|--------|----------|---------------|
| 1 | Navio Seco | conto | burilamento | 2.840 | 2026-08-05 |
```

Estados: `entrevista` `arquitetura` `rascunho` `burilamento` `lapidação` `finalizada`
`arquivada` `suspensa`.

### 3.2 Léxico ocupado

Acrescente tudo que foi usado. **Nunca remova.**

```yaml
nomes_de_personagem: ["Estela — Stella Maris, estrela do mar (Navio Seco)"]
toponimos: []
imagens_matriciais: ["remos jogados fora"]
estruturas_formais_ja_usadas: ["ponto final único ao fim (Navio Seco)"]
primeiras_frases_ja_usadas: []
finais_ja_usados: []
```

Antes de nomear qualquer coisa nova, consulte esta seção. Repetir é permitido — mas
**deliberadamente**, e registrado como eco entre obras.

### 3.3 Ficha da obra

Modelo em `templates/FICHA-OBRA.md`. Insira ou atualize entre os marcadores
`<!-- INICIO-FICHAS -->` e `<!-- FIM-FICHAS -->` de `MEMORY.md`. **Nunca remova os
marcadores.**

Campos obrigatórios de toda ficha:

```yaml
titulo:
estado:
forma:
argumento:
epilogo_em_vista:
regime: {genero:, tom:, andamento:, foco:, angulo:, voz:}
personagens: [{nome:, metafora:, plano_ou_redondo:, gramatica:, hierarquia:}]
dispositivo_formal:
risco_assumido:
recusas:
elipses: [{tipo:, onde:, aberta:}]
eco_de_costura: {plantado_em:, retorna_em:, como_muda:}
decisoes_tecnicas: [{decisao:, razao:, data:}]
traicoes_da_planta: [{o_que:, por_que:}]
furos_abertos:
texto_atual: {palavras:, ultimo_bloco:, onde_parou:}
proximo_passo:
```

### 3.4 Furos abertos transversais

Perguntas que ficaram sem resposta e podem gerar outra obra. É o viveiro.

```yaml
furos:
  - pergunta: "quem era a mulher que o pescador não quis nomear?"
    origem: "Navio Seco"
    potencial: "conto autônomo em segunda pessoa"
```

### 3.5 Diário de sessões

Uma linha por sessão. Sempre com **próximo passo**.

```markdown
| Data | Obra | Fase | O que foi feito | Próximo passo |
|------|------|------|-----------------|---------------|
| 2026-08-05 | Navio Seco | burilamento | passadas 1-3; cortadas 340 palavras | passada 4 (elipse) |
```

## 4. Coerência entre obras

Três níveis, do mais permissivo ao mais rígido:

| Nível | Regra |
|---|---|
| **Léxico** | repetir palavra é livre; repetir imagem matricial exige registro como eco |
| **Estrutural** | repetir dispositivo formal exige justificativa — ou é série declarada, ou é autoplágio |
| **Poético** | decisões vigentes na tabela de poética valem para todas as obras até revogação explícita |

Quando o autor tomar uma decisão que vale além da obra atual — "nunca mais uso
travessão", "sempre nomeio o cão" —, registre em **DECISÕES DE POÉTICA** com data,
origem e vigência.

## 5. Comando `/memoria`

Entregue exatamente isto:

```
ESTADO DA OFICINA

Obras ativas
| Título | Forma | Estado | Palavras | Onde parou | Próximo passo |

Obras finalizadas
| Título | Forma | Palavras | Data |

Decisões de poética vigentes
- <lista>

Furos transversais disponíveis
- <lista>

Alertas de coerência
- <nome/imagem/estrutura prestes a se repetir, se houver>
```

Se não houver alerta, escreva "nenhum". Nunca invente alerta.

## 6. Integridade do arquivo

```yaml
nunca:
  - apagar ficha de obra abandonada (vira `arquivada`; o material serve depois)
  - remover entradas do léxico ocupado
  - remover os marcadores INICIO-FICHAS / FIM-FICHAS
  - reescrever o diário retroativamente
  - registrar como decisão do autor algo que foi sugestão de Claude

sempre:
  - distinguir o que o autor decidiu do que Claude propôs
  - datar toda decisão
  - registrar traições da planta com a razão
  - registrar o que foi tentado e descartado
```

O último item é o mais valioso. Saber o que já foi descartado impede a oficina de propor
duas vezes o mesmo caminho ruim.

## 7. Recuperação de contexto perdido

Se o autor voltar depois de muito tempo e `MEMORY.md` estiver incompleto:

1. Peça o texto atual da obra.
2. Aplique o protocolo de extração de DNA (`skills/11-rascunho/SKILL.md` §5).
3. Reconstitua a ficha a partir do texto, marcando cada campo inferido como
   `[inferido]`.
4. Peça confirmação dos campos inferidos ao autor, em bloco único.
5. Só então retome a escrita.

Nunca escreva sobre uma obra cuja ficha esteja inferida sem confirmação. Coerência
falsa é pior que ausência de coerência.

## Referência cruzada

- Modelo de ficha → `templates/FICHA-OBRA.md`
- Modelo de entrada → `templates/ENTRADA-MEMORY.md`
- Extração de DNA → `skills/11-rascunho/SKILL.md`
