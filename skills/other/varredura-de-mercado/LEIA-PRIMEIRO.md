# Varredura de Mercado — como instalar e usar

**O que essa skill faz:** você fala o que quer ("quero ganhar dinheiro com Claude Code", "sou
gestor de tráfego e quero automatizar meu trabalho", "tenho uma clínica e quero cortar custo") — ou
nem sabe ainda — e ela faz uma pesquisa de verdade na internet e te devolve um relatório com 3 a 6
oportunidades **reais, com link de prova**, ranqueadas, e o primeiro passo concreto pra cada uma.
Nada de ideia genérica de ChatGPT: cada oportunidade vem com a evidência de que funciona.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `varredura-de-mercado` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. Não tem chave de API, não instala nada, não configura nada.

> Skill instalada no usuário funciona em **qualquer projeto** que você abrir no Claude Code.

---

## Usar

Abre o Claude Code e faz **uma** das duas coisas:

- Digita o comando: **`/varredura-de-mercado`**
- Ou simplesmente fala, em português normal:
  - *"quero ganhar dinheiro com Claude Code, o que eu faço?"*
  - *"sou corretor de imóveis, dá pra automatizar meu trabalho?"*
  - *"tenho uma clínica com 3 funcionários, onde corto custo com IA?"*
  - *"não sei o que fazer, me dá ideias de ferramenta pra construir"*

Ela pode fazer **1 pergunta** rápida pra mirar certo, e aí roda a pesquisa (leva um tempinho — ela
vai te contando o que tá fazendo). No fim, o relatório aparece na tela **e** fica salvo em
`.claude/varreduras/` dentro do seu projeto, pra você reler depois.

---

## Detalhes que importam

- **Funciona no PRO** (US$20/mês). Ela é desenhada pra caber no limite do PRO; no MAX roda mais folgado.
- **Roda de novo quando quiser.** O mercado muda — toda vez que você entra num nicho novo ou quer reavaliar, roda outra vez. Ela mostra "o que mudou desde a última".
- **Não inventa.** Se a busca na web estiver fora do ar ou bloqueada, ela te avisa em vez de chutar. Todo número de R$ e toda empresa citada vem de uma busca real, com link.

---

## Depois da varredura

Escolheu uma oportunidade? O próximo passo dentro do pack é a skill **Busca de Documentação**
(`/busca-documentacao`) pra ver como os concorrentes já resolveram — e aí mandar o **Claude Code**
construir.
