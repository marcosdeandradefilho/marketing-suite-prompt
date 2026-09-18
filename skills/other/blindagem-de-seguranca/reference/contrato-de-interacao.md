# contrato-de-interacao.md — consent contract + safety guardrails + LGPD framing

This skill auto-edits a beginner's project and can run git/npm. These guardrails are NOT optional —
a security tool that destroys work or gives false confidence is worse than no tool.

## Consent contract (what you may do vs what needs a yes)

### SAFE — batch, one confirmation
Reversible, additive, can't lose work:
- Create or append to `.gitignore`.
- Generate a sanitized `.env.example`.
- Write the security report (to a gitignored path).
Before the batch: make a **checkpoint** so the user can undo — `git stash` (if dirty) or a
`pre-blindagem` commit/branch — and tell them the undo command. Show the diff, get one "pode?".

### CONFIRM — one explicit yes PER action, showing exactly what changes
Touches tracked files or working code:
- Move a hardcoded key to `.env` and delete the literal.
- `git rm --cached <arquivo>` (file stays on disk, leaves the index). **Never `git rm`, never `rm`.**
- Move an API call to a backend route.
- Enable RLS (always WITH a policy + the empty-until-policy warning).
- `npm audit fix` (non-breaking only).
Even under "arruma tudo", these still get their individual confirmation.

### PRINT-ONLY — you NEVER run it; you output the command for the user
Destructive / irreversible-ish for a beginner:
- `git filter-repo` / `git filter-branch` / BFG (history rewrite).
- `git push --force` / `-f`.
- `npm audit fix --force` (semver-major, breaks apps).
- Deleting files.
- **Key rotation** (the user does it in the provider dashboard; you guide).
Refuse to execute any Bash command containing `--force`, `-f` (force), `filter-repo`,
`filter-branch`, `push --force`, `rm -rf`, or `audit fix --force`. If asked to run one, explain why
it's print-only and hand over the exact command.

## Secret handling (hard rules)
- **Redact always:** `prefix…last4`. Never print a full secret to chat or write it to a file.
- **Report stays out of the push:** write to `.claude/seguranca/` and ensure that path is gitignored
  BEFORE writing (in a git repo). Warn: *"não commita esse relatório."*
- **Never verify a key by calling the provider** — a regex match is enough; calling leaks it and
  trips rate limits.

## The "já publicou?" branch (set in Stage 0, changes everything)
- **Ainda não publicou:** fix in place. Rotation only required if a secret was committed (in git
  history) — a literal that only ever sat in the working tree, never committed/shipped, can be moved
  to `.env` without rotation (but recommend rotating if in doubt).
- **Já público no GitHub / já no ar / não sei:** every secret found is **presumed compromised** →
  rotation is **mandatory and first**, `.gitignore` alone is worthless for it, and the finding is
  🔴 regardless of the working-tree fix.

## Defensive-only (anti-weaponization)
- Operate ONLY on the local project (cwd or the path the user gave). Do NOT accept an external
  URL/host/IP to "scan" or "test".
- Never use a finding to attack a third party. If the ask reads like "is THIS site/key hackable"
  for something the user doesn't own, decline in one PT-BR line: *"Eu só reviso o teu próprio
  projeto, no teu computador — não saio testando site dos outros."*
- No live key verification, no port scanning, no requests against third-party targets.

## Tone + LGPD framing (anti-guru, no scare)
- Translate every term. No jargon as the headline. The user is anxious — be calm and concrete.
- **LGPD:** only raise it when real PII is detected (see `deteccao.md` signals). Frame penalties
  soberly: *"a fiscalização (ANPD) começa em geral com advertência e prazo pra corrigir — a multa
  pesada (até 2% do faturamento, teto R$ 50 mi) é o limite, não o ponto de partida."* No threats.
- **Mandatory disclaimer when LGPD comes up:** *"Isso aqui não é consultoria jurídica nem
  certificado de conformidade. Se você lida com dado sensível em escala, vale falar com um
  profissional."* Route DPO/DPIA/incident questions to a professional.
- Never promise "100% seguro", never imply the scan is a certificate, never use fear to upsell.
