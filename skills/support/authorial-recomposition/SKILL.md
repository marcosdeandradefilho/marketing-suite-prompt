---
name: authorial-recomposition
description: Recompõe textos produzidos ou assistidos por qualquer LLM para restaurar voz autoral, reduzir regularidades estilísticas genéricas, preservar significado, evidências e precisão, e adequar o resultado ao gênero acadêmico, profissional ou literário. Use quando o usuário pedir naturalização editorial, restauração de voz, revisão de texto de IA, redução de padrões formulaicos, reescrita autoral ou adaptação a um corpus de referência.
---

# Authorial Recomposition

## Finalidade

Transformar um texto já existente em uma realização linguística mais autoral, específica e editorialmente consistente, independentemente do modelo que o tenha originado. O objetivo não é “enganar detector”, alterar proveniência ou falsificar autoria; é reconstruir forma, ritmo, progressão argumentativa e escolhas lexicais sem adulterar conteúdo verificável.

## Princípio central

**Recompor, não maquiar.**

Não faça simples troca de sinônimos. Não introduza erros artificiais, gírias aleatórias, hesitações falsas, ortografia defeituosa ou idiossincrasias inventadas. A reescrita deve ocorrer em múltiplas escalas: arquitetura, parágrafo, período, sintaxe, léxico e ritmo.

## Modos de operação

Escolha automaticamente um modo ou combine-os:

1. **AUTHORIAL_RESTORATION** — há textos genuínos do autor disponíveis; modele a voz e reescreva conforme padrões observáveis.
2. **LLM_PATTERN_REDUCTION** — não há corpus autoral; reduza regularidades formulaicas e aumente especificidade, variação funcional e densidade informacional.
3. **ACADEMIC_AUTHORIAL** — preserve terminologia, cautela epistêmica, citações, relações causais e escopo das afirmações.
4. **LITERARY_AUTHORIAL** — preserve imagem, tensão, ritmo, ambiguidade produtiva e coerência da voz narrativa.
5. **PROFESSIONAL_AUTHORIAL** — privilegie precisão, legibilidade, hierarquia informacional e adequação pragmática.

## Fluxo obrigatório

### Etapa 1 — Semantic Lock

Antes de reescrever, identifique o que não pode mudar:

- fatos, números, datas, nomes próprios e relações lógicas;
- citações diretas e referências bibliográficas;
- tese, posição argumentativa e grau de certeza;
- terminologia técnica necessária;
- requisitos formais pedidos pelo usuário;
- limites jurídicos, éticos ou institucionais presentes no texto.

Crie internamente um inventário de invariantes. Não mostre esse inventário salvo se solicitado.

### Etapa 2 — Diagnóstico de superfície

Procure sinais de escrita excessivamente formulaica. Use `references/style-signals.md` quando necessário. Não assuma que qualquer sinal prova origem por IA. Trate-os apenas como problemas editoriais potenciais.

Avalie especialmente:

- comprimento de frases excessivamente uniforme;
- repetição de estruturas sintáticas;
- excesso de enumerações em três itens;
- paralelismo automático;
- conectores usados mecanicamente;
- metadiscurso sem função (“é importante destacar que”);
- abstrações sem ancoragem;
- paráfrase circular;
- repetição de tese em cada parágrafo;
- conclusões que apenas recapitulam;
- adjetivos avaliativos sem evidência;
- transições excessivamente suaves;
- simetria artificial entre parágrafos;
- títulos e subtítulos excessivamente genéricos;
- falsa precisão ou referências não verificadas.

### Etapa 3 — Modelagem de voz

Se houver corpus do autor, extraia padrões reais, não caricaturas. Observe:

- distribuição do comprimento dos períodos;
- preferência por coordenação ou subordinação;
- posição de orações incidentais;
- densidade lexical e nível de nominalização;
- tipos de conectores realmente usados;
- relação entre conceito e exemplo;
- uso de primeira pessoa e marcação de agência;
- intensidade da modalização epistêmica;
- emprego de perguntas retóricas;
- pontuação expressiva;
- abertura e fechamento de parágrafos;
- repertório metafórico;
- grau de explicitação;
- tolerância a assimetria e elipse;
- modo de introduzir contraste e ressalva.

**Regra:** imite decisões autorais, não bordões superficiais.

Se houver menos de 500 palavras de corpus, use o perfil com cautela. Se houver 1.500+ palavras, considere o perfil suficientemente estável para orientar a reescrita. Não invente características ausentes.

### Etapa 4 — Reestruturação macro

Antes de editar frase por frase, verifique a arquitetura do texto:

- cada parágrafo precisa cumprir uma função distinguível;
- elimine redundância entre introdução, desenvolvimento e conclusão;
- reorganize argumentos quando a progressão estiver previsível ou repetitiva;
- una parágrafos que apenas fragmentam a mesma ideia;
- separe parágrafos que acumulam funções incompatíveis;
- prefira progressão semântica real a transições ornamentais.

### Etapa 5 — Reescrita meso e micro

Aplique transformações apenas quando melhorarem o texto:

- varie extensão de períodos por função retórica, não aleatoriamente;
- alterne sintaxe direta, subordinada, parentética e elíptica conforme o gênero;
- substitua abstrações por relações concretas ou exemplos quando o conteúdo permitir;
- converta enumerações previsíveis em prosa quando a enumeração não for necessária;
- corte metadiscurso vazio;
- preserve termos técnicos que carregam precisão;
- elimine sinônimos que mudem nuance conceitual;
- mantenha repetições deliberadas quando elas tiverem função retórica;
- preserve irregularidades autorais produtivas.

### Etapa 6 — Fricção intelectual

Textos excessivamente polidos podem perder pensamento. Reintroduza, quando o conteúdo justificar:

- ressalvas reais;
- tensões entre conceitos;
- limites de uma generalização;
- mudança de escala;
- contraste não perfeitamente simétrico;
- especificidade contextual;
- consequências concretas de uma ideia.

Nunca fabrique contradições ou incertezas inexistentes.

### Etapa 7 — Auditoria de fidelidade

Compare silenciosamente original e versão recomposta. Verifique:

1. nenhum fato foi alterado;
2. nenhuma fonte foi inventada;
3. nenhuma citação foi parafraseada como se continuasse direta;
4. o grau de certeza permanece equivalente;
5. a posição do autor não foi intensificada nem suavizada sem pedido;
6. termos técnicos permanecem corretos;
7. exemplos novos são claramente exemplos, não fatos alegados;
8. o texto não ficou apenas “mais diferente”: ficou melhor.

### Etapa 8 — Auditoria estilística

Leia novamente sem comparar com o original e pergunte:

- cada parágrafo poderia ter sido escrito pelo mesmo autor?
- há cadência repetitiva perceptível?
- há palavras de ligação substituindo relações lógicas reais?
- há frases que existem apenas para “soar bem”?
- o texto apresenta decisões estilísticas específicas em vez de neutralidade genérica?
- o nível de formalidade é estável?

Se necessário, faça uma segunda recomposição localizada.

## Regras específicas para texto acadêmico

Consulte `references/academic-mode.md` quando o texto for científico, ensaístico ou universitário.

Obrigatório:

- não alterar citações nem referências sem verificar a fonte;
- não criar DOI, página, autor ou ano;
- preservar distinções entre correlação, associação e causalidade;
- preservar modalidade: “sugere” não vira “demonstra”;
- não remover terminologia só para parecer mais simples;
- eliminar frases de enchimento que apenas anunciam o que virá;
- privilegiar densidade argumentativa e clareza conceitual.

## Regras para corpus autoral

Quando o usuário fornecer textos próprios:

1. trate-os como fonte estilística, não como conteúdo a ser copiado;
2. extraia padrões recorrentes em pelo menos três dimensões diferentes;
3. não reproduza sequências longas ou expressões raras de forma mecânica;
4. respeite diferenças de gênero: um artigo e uma crônica podem pertencer ao mesmo autor sem ter a mesma superfície;
5. priorize características estáveis entre gêneros.

## Ferramenta de perfil estilístico

Se execução de código estiver disponível e houver texto suficiente, use opcionalmente:

```bash
python scripts/style_profile.py arquivo.txt
```

O script mede indicadores descritivos simples. Esses indicadores não detectam autoria nem origem por IA; servem apenas como apoio editorial.

## Formato de saída

Por padrão, entregue somente o texto recomposto. Se o usuário pedir diagnóstico, forneça depois uma síntese objetiva das principais intervenções.

Quando a reescrita for extensa e houver risco de perda factual, prefira alterações conservadoras a transformações espetaculares.

## Critério de sucesso

O resultado deve:

- preservar integralmente o conteúdo verificável;
- soar específico ao gênero e ao autor quando houver corpus;
- reduzir regularidades formulaicas desnecessárias;
- apresentar variação sintática funcional;
- aumentar precisão e densidade informacional;
- manter naturalidade sem artificializar “imperfeições humanas”.

## Exemplos de acionamento

- “Reescreva este texto preservando minha voz.”
- “Retire os vícios de escrita de IA sem simplificar o argumento.”
- “Use meus artigos como corpus e recomponha este capítulo.”
- “Reduza a linguagem formulaica deste texto acadêmico.”
- “Naturalize a redação, mas preserve todas as referências e cautelas epistemológicas.”
- “Faça uma recomposição autoral profunda, não apenas troca de palavras.”
