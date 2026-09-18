# correcao-e-rotacao.md — how to FIX each finding (safely) + key rotation

Worst-first. Every command's safety class (auto / confirm / print-only) is in
`contrato-de-interacao.md` — respect it. The golden rule: **a key that was ever committed or
shipped to the browser is COMPROMISED — moving it to `.env` does not un-leak it; it must be ROTATED.**

## The leaked-secret incident order (teach this, in order)
1. **Gira a chave AGORA** (revoke + reissue in the provider dashboard) — do this FIRST. Bots scan
   public GitHub and harvest keys within minutes (real cases: AWS creds → 500+ crypto-mining EC2
   instances in ~20 min / $72k; a frontend Gemini key → ~$60k in 13h).
2. **Põe um limite de gasto** no provedor (cap the damage).
3. **Tira do código** → move pra variável de ambiente (`.env`), e DELETA o valor literal.
4. **Confere a cobrança/uso** no painel — vê se já abusaram.
5. **Limpa o histórico do git** (só se foi commitado) — passo SECUNDÁRIO, e **print-only** (o usuário
   roda). Nunca substitui a rotação.

> Tell the user plainly: *"Só apagar o arquivo ou tirar do último commit NÃO resolve — a chave
> continua no histórico E provavelmente já foi varrida por robô. Por isso a regra é girar a chave."*

## Fix: secret hardcoded in code → environment variable
- Create/append `.gitignore` (see canonical list below). Create `.env` with the key; replace the
  literal in code with the env lookup:
  - Node: `process.env.OPENAI_KEY` (+ `dotenv` if not a framework that auto-loads).
  - Python: `os.environ["OPENAI_KEY"]` / `os.getenv(...)` (+ `python-dotenv`).
  - Vite: only `import.meta.env.VITE_*` for **non-secret** values; secrets go server-side.
  - Next.js: server-only env (no `NEXT_PUBLIC_`); read it in a Route Handler / Server Action.
- **Delete the literal** — NEVER leave `process.env.KEY || 'sk-...'` (that re-leaks it).
- **Verify** `.env` is gitignored AND not already tracked: `git ls-files --error-unmatch .env`
  (if tracked → `git rm --cached .env`, a confirm-class action).
- Generate a sanitized **`.env.example`** (same keys, blank values) so collaborators have a template.

## Fix: secret reaching the browser → move the call to a backend
A paid-API key can NEVER live in client code. Proxy it:
- Next.js → an API Route / Route Handler (`app/api/.../route.ts`) that holds the key server-side.
- Vite/React SPA → a small serverless function (Vercel/Netlify function, Supabase Edge Function).
- Static site → a serverless proxy, or drop the feature. There is no safe way to call a paid API
  with a secret from pure client HTML.
Then **rotate** the old key (it already shipped).

## Fix: open Supabase / Firebase
- **Supabase:** enable RLS AND ship at least one policy together:
  ```sql
  ALTER TABLE public.<tabela> ENABLE ROW LEVEL SECURITY;
  CREATE POLICY "dono lê o próprio" ON public.<tabela>
    FOR SELECT USING (auth.uid() = user_id);
  ```
  **Warn:** *"Depois de ligar o RLS, a tabela fica VAZIA até existir uma policy — isso é esperado,
  não é bug. Por isso a gente liga as duas coisas juntas."* A `service_role` key in client → remove
  it and rotate.
- **Firebase:** replace `allow read, write: if true;` with auth-scoped rules. The web `apiKey` is
  not a secret — the protection IS the rules.

## Fix: dependency vulnerabilities
- `npm audit --omit=dev` to see; `npm audit fix` (non-breaking) may run with a lockfile present.
  **`npm audit fix --force` is PRINT-ONLY** — it does semver-major bumps that can break the app.
- Python: `pip-audit` (print the upgrade commands; let the user run them).
- If the tool isn't installed, say so and skip — don't fail the run.

## Fix: git history cleanup (PRINT-ONLY — you never run this)
Output the steps; the user runs them. Always after rotation, never instead of it.
```
# instale o git-filter-repo e rode (REESCREVE o histórico — combine com quem trabalha no repo):
git filter-repo --path .env --invert-paths      # remove o arquivo de TODO o histórico
git push --force                                  # você roda isso, com cuidado
```
Warn: rewrites every commit hash, breaks collaborators (they must re-clone, not merge), and the key
is STILL compromised → rotate. For most beginners with a solo repo, "girei a chave + tirei do código
+ daqui pra frente fica no `.env`" já é suficiente; history rewrite é opcional.

## Canonical `.gitignore` essentials (github/gitignore Node baseline + secrets)
```
.env
.env.*
!.env.example
node_modules/
.venv/
__pycache__/
*.pem
*.key
*.p12
credentials.json
service-account*.json
.npmrc
.DS_Store
dist/
build/
.vercel
```

## Host env vars (where the secret SHOULD live in production)
- **Vercel:** Project → Settings → Environment Variables (Production/Preview/Development).
- **Netlify:** Site settings → Environment variables.
- **Railway:** project Variables tab.
Set the key there, NOT in the repo. Build-time vs runtime: framework-public vars are build-time and
end up in the bundle — only non-secrets.

## Key rotation playbooks (PRINT-ONLY / guided — you never type the new key)
General rule for any provider not listed: *"entra no painel do provedor, revoga a chave antiga, gera
uma nova, põe limite de gasto, atualiza o `.env` / as variáveis do host, confere a cobrança."*

| Provedor | Revoga / gira | Limite de gasto | Painel |
|---|---|---|---|
| **OpenAI** | Cria a NOVA primeiro → troca no app → revoga a antiga (evita downtime) | Settings → Limits (usage/budget) | platform.openai.com/api-keys |
| **Anthropic** | API Keys → revoke + create | Plan & Billing → spend limit | console.anthropic.com |
| **Stripe** | "Roll key" (janela de transição até 12h, old+new valem) | — | dashboard.stripe.com/apikeys |
| **Supabase** | Migra pros novos `sb_secret_`/`sb_publishable_`. **NÃO** gire o JWT secret legado por impulso: isso **invalida TODAS as chaves e reinicia o projeto** (Supabase docs). RLS é o conserto real de uma `anon` key. | — | Project → Settings → API |
| **Google / Gemini** | Regenera a chave + adiciona restrição de API e de aplicativo | Quotas/billing | console.cloud.google.com |
| **AWS** | **Desativa primeiro** (`update-access-key --status Inactive`, preserva CloudTrail) → depois deleta → cria nova IAM. Chave ROOT é o pior caso: delete e nunca recrie (IAM não limita o root) | Budgets/alarms | console IAM |
| **GitHub PAT** | Settings → Developer settings → Tokens → revoke + regenerate | — | github.com/settings/tokens |
| **Mercado Pago / Meta-WhatsApp / PagSeguro / Asaas** | Painel do provedor → revoga o access token → gera novo → atualiza `.env` → confere cobrança | painel do provedor | painel BR do provedor |

**Never** auto-execute any of these. **Never** hold or paste the new key — the user types it into
their own `.env` / host panel.
