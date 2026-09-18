# contexto-md.md — the checkpoint file: template, rules, microcopy

The whole point: a checkpoint a layperson can trust, that a future session reloads, that stays
TINY. A bloated checkpoint defeats the purpose (you'd pay to re-read it every turn). Lean is the
feature.

## The fixed 5 sections (write exactly these headings, in this order)

```markdown
# Contexto da sessão — <projeto>
> Atualizado em AAAA-MM-DD · branch: <branch> · linhas: <n>/150

## Objetivo
<1-3 linhas: o que esse projeto/trabalho é e o que a gente quer que ele faça no fim.>

## Estado atual
<onde está AGORA. O que já funciona, o que já foi feito. Arquivos por CAMINHO, não conteúdo:
- `src/app.py` — tela principal, já roda
- `index.html:120` — formulário de contato, falta validar
Nunca cole o conteúdo dos arquivos aqui. Só o caminho + 1 linha do que tem nele.>

## Decisões tomadas
<as escolhas que NÃO se revisita sem motivo (as ~5 mais recentes/importantes). Ex:
- Banco: SQLite local (não Postgres) — é um app de 1 usuário
- Cor da marca: #1B998B — cliente aprovou
Isso é o que um /compact resumido perderia. É o ouro do checkpoint.>

## Becos sem saída
<o que JÁ se tentou e NÃO deu certo, pra não repetir amanhã. Ex:
- Tentei a lib X pra PDF — não roda no Windows, abandonei
- API Y exige cartão — fora de escopo
Se não tem nenhum, escreve "nenhum até agora".>

## Próximo passo
<UMA coisa concreta: o que fazer assim que reabrir. Ex:
- Validar o formulário de contato em index.html:120 e testar o envio
Se o usuário não declarou, pergunta uma vez; se ainda assim não souber: "(definir)".>
```

## The four rules that keep it valuable

1. **Pointers, not copies.** Reference files by path (`src/app.py:42`) and name decisions. NEVER
   paste file contents, code blocks of the project, logs, or command output. A checkpoint that
   pastes a 200-line file is worse than useless — it's the bloat you're trying to escape. The path
   lets the next session re-read the file ON DEMAND (and only if needed), instead of carrying it.

2. **Read before merge (never blind-overwrite).** If `.claude/context.md` already exists, READ it
   first. Then produce the new version by FOLDING IN what changed: keep decisions/dead-ends that are
   still true, update "Estado atual" and "Próximo passo", drop tasks that are now done. The user
   should never lose an earlier decision because a later save clobbered the file. When unsure whether
   an old line still holds, keep it and append the update — don't silently delete history.

3. **Self-prune to stay lean (~150 lines).** Cap the file at ~150 lines and "Decisões tomadas" at
   the ~5 most recent/load-bearing. If it's growing past that, REWRITE to critical-only (the goal is
   "smallest file that lets tomorrow's session continue correctly"), and move anything historical
   the user might still want into a one-line pointer ("histórico antigo: ver .claude/handoffs/"). The
   header line tracks `linhas: <n>/150` so the user (and you) can see it staying bounded.

4. **Stamp date + branch.** Top line carries `Atualizado em AAAA-MM-DD` and the current git branch.
   On reload, if the open branch differs from the stamped one, the skill flags it rather than mixing
   two branches' state. (Branch detection: read `gitBranch` from the transcript JSONL if available, or
   run `git rev-parse --abbrev-ref HEAD`; if it's not a git repo, omit the branch field.) Merge edge: if
   the PRIOR file stamped a branch but the project is no longer (or never was) a git repo, don't silently
   erase that line under rule 2 — keep `branch: <antiga> (sem git agora)` so no history is lost; don't
   invent a current branch.

## Gathering the state without dumping it
- Touched files this session: prefer what you actually edited/created in THIS conversation; if unsure,
  `Glob` recently-changed files or ask. Do NOT read every file in the project to "be thorough" — that
  burns the very tokens you're saving.
- Decisions: pull from the conversation (what was chosen and why). These are the highest-value lines.
- Dead-ends: anything tried-and-abandoned in the conversation.
- Next step: the user's stated next action; if absent, ONE question, then "(definir)".

## Microcopy (PT-BR, anti-guru — use these tones, not verbatim every time)
- Abertura: *"Vou salvar onde teu trabalho está num resumo enxuto — leitura local, não gasta tokens
  da tua janela."*
- Ao salvar por cima de um existente: *"Já tinha um checkpoint aqui — atualizei mantendo as decisões
  que ainda valem, não apaguei teu histórico."*
- Confirmação (1 linha por seção, não um muro): *"Salvo. Objetivo: <…>. Tá em: <…>. Próximo passo:
  <…>. Branch: <…>."*
- Branch divergente: *"Atenção: esse checkpoint foi salvo na branch `X`, tu tá na `Y` agora — confere
  se é isso mesmo antes de continuar."*
- Fechamento limpo: *"Pra fechar sem perder nada: dá `/clear` (custa ~0, não precisa de `/compact`).
  Reabriu nesse projeto, o Claude já carrega isso."*

## What NOT to write in the checkpoint
No secrets/keys/passwords/tokens (if you spot one in the state, replace with `<REDIGIDO>` and tell the
user). No pasted file bodies. No full command outputs. No motivational filler. No time estimates. No
invented progress percentages.
