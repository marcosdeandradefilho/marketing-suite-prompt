# Authorial Recomposition

Skill agnóstica de modelo para recomposição autoral de textos produzidos ou assistidos por LLMs.

## O que ela faz

- restaura uma voz autoral quando há corpus de referência;
- reduz regularidades formulaicas e monotonia estrutural;
- reescreve em níveis macro, meso e micro;
- preserva fatos, citações, referências e modalidade epistêmica;
- oferece modo acadêmico, literário e profissional;
- inclui um perfilador estilístico descritivo opcional.

## O que ela não faz

- não detecta autoria por IA;
- não promete remover marca d'água, proveniência ou sinal estatístico;
- não otimiza texto para burlar detectores;
- não introduz erros artificiais para “parecer humano”.

## Instalação no Claude Code

### Pessoal

Copie a pasta inteira para:

```text
~/.claude/skills/authorial-recomposition/
```

O arquivo deve ficar em:

```text
~/.claude/skills/authorial-recomposition/SKILL.md
```

### Por projeto

Copie para:

```text
<seu-repositorio>/.claude/skills/authorial-recomposition/
```

## claude.ai

Compacte a pasta como ZIP e envie como Custom Skill em Settings > Features, quando o recurso estiver disponível no seu plano.

## Uso recomendado

Exemplos:

- “Use a skill de recomposição autoral neste capítulo.”
- “Aprenda minha voz a partir destes três artigos e reescreva este trecho.”
- “Reduza os padrões formulaicos, mas preserve rigor acadêmico.”
- “Faça uma recomposição profunda: estrutura, sintaxe, ritmo e léxico.”

## Estrutura

```text
authorial-recomposition/
├── SKILL.md
├── README.md
├── references/
│   ├── academic-mode.md
│   └── style-signals.md
├── scripts/
│   └── style_profile.py
└── templates/
    └── voice-profile.md
```

## Observação de compatibilidade

O formato segue a estrutura atual de Agent Skills: um diretório próprio com `SKILL.md` e frontmatter YAML contendo `name` e `description`, além de recursos opcionais.
