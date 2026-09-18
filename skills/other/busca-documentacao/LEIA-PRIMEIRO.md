# Busca de Documentação — como instalar e usar

**O que essa skill faz:** você fala o que vai construir ("um gerenciador de senhas", "um app de
notas", "um emissor de nota fiscal") e ela lê a **documentação real** de várias ferramentas
parecidas que já existem — README do GitHub, changelog, issues, página de preço — e te devolve um
resumo com: as features que todo mundo do nicho tem, padrões de UX, ideias de arquitetura pra
reusar, as armadilhas conhecidas (tirada das reclamações reais) e como essas ferramentas cobram.
É o passo de **inspiração técnica** antes de você mandar o Claude Code construir — pra você não
reinventar a roda.

---

## Sem a skill x Com a skill

- **Sem a skill:** você pergunta pro Claude "como os concorrentes do meu app de notas funcionam?" e
  ele responde de memória — pode citar ferramenta que mudou, feature que não existe mais, preço
  desatualizado, e nenhum link pra conferir.
- **Com a skill:** ela vai na internet, abre a documentação de verdade, conta em quantas das N
  ferramentas cada feature aparece (com o número na frente pra você conferir), pega armadilha real
  de issue do GitHub, e marca o que não conseguiu ler em vez de inventar. Tudo com link.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `busca-documentacao` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. Não tem chave de API, não instala nada, não configura nada.

> Skill instalada no usuário funciona em **qualquer projeto** que você abrir no Claude Code.

---

## Usar

Abre o Claude Code e faz **uma** das duas coisas:

- Digita o comando: **`/busca-documentacao`**
- Ou simplesmente fala, em português normal:
  - *"vou construir um app de notas, como os parecidos já resolvem isso?"*
  - *"pesquisa a documentação de gerenciadores de senha antes de eu começar"*
  - *"o que já existe pra emitir nota fiscal e como funciona?"*
  - *"não quero reinventar a roda no meu CRM — vê os concorrentes"*

Se você já conhece 1 ou 2 ferramentas parecidas, cola o nome — ela usa como ponto de partida. Se
quiser focar num ângulo (UX, técnico ou como cobram), é só falar. A pesquisa leva um tempinho (ela
vai te contando o que tá fazendo). No fim o resumo aparece na tela **e** fica salvo em
`.claude/pesquisas/` dentro do seu projeto.

---

## Detalhes que importam

- **Funciona no PRO** (US$20/mês). É desenhada pra caber no limite do PRO; no MAX roda mais folgado.
- **Não inventa.** Lê documentação de verdade. Se uma página estiver bloqueada (Cloudflare, login) ou
  a busca cair, ela te avisa e marca "não consegui ler" — em vez de chutar uma feature que não existe.
- **Roda de novo a cada projeto.** As ferramentas do nicho lançam versão, mudam preço e às vezes
  morrem — uma pesquisa salva fica velha rápido. Na segunda vez ela mostra "o que mudou desde a última".
- **Power-up opcional (não precisa):** se você pesquisa muito e o GitHub começar a limitar as buscas,
  dá pra configurar um `GITHUB_TOKEN` gratuito pra soltar o limite. **Não é obrigatório** — a skill
  funciona zero-config sem token nenhum.

---

## Depois da pesquisa

Agora você sabe COMO o nicho já resolve o problema. O próximo passo é mandar o **Claude Code** construir
— com a pesquisa em mãos, ele já parte do que funciona lá fora. A skill ainda te entrega um bloco
**"Brief pra construir"** pronto pra copiar e colar.
