# deteccao.md — scan scope + per-archetype checks + LGPD signals

## Scan-scope algorithm (run before reading anything)

1. **Resolve target:** the path the user gave, else cwd.
2. **Detect archetype(s)** from marker files: `package.json` (Node/JS), `requirements.txt`/
   `pyproject.toml`/`manage.py` (Python/Django/Flask), `index.html` with no build (static site),
   `wp-config.php`/`wp-content/` (WordPress), `composer.json` (PHP/Laravel), `*.csproj`/
   `appsettings.json` (.NET), `docker-compose.yml`/`Dockerfile` (Docker), `supabase/` or
   `@supabase/supabase-js` in deps (Supabase), `firebase.json`/`firebaseConfig` (Firebase).
   **Monorepo** (multiple `package.json`/`requirements.txt` in subfolders) → scan each sub-app, or
   ask which one if there are many.
3. **Build the include set** — source + config by extension: `.js .jsx .ts .tsx .vue .svelte .py
   .rb .php .go .java .cs .env* .json .yml .yaml .toml .ini .config .properties .html .sql .ipynb`
   plus dotfiles `.npmrc .pypirc .netrc` and CI `.github/workflows/*.yml`.
4. **Hard ignore set** (never scan — noise and huge): `node_modules/ vendor/ .git/ dist/ build/
   .next/ out/ .nuxt/ .venv/ __pycache__/ coverage/ *.min.js *.min.css *.map` lockfiles
   (`package-lock.json yarn.lock pnpm-lock.yaml poetry.lock`), media/binaries
   (`*.png *.jpg *.gif *.mp4 *.pdf *.zip *.woff*`), and **`.claude/`** (your own internals + other
   pack skills' generated artifacts). Use ripgrep's defaults (it already skips `.gitignore`d paths
   and binaries) plus these globs.
5. **Soft cap:** if the include set is huge (e.g. thousands of files), scan source + config first,
   git history second, and WARN that you truncated; offer to continue on a subfolder.

## Config-file secret locations (beyond .env — this is what stops a FALSE GREEN)
Scan these with the patterns in `padroes-de-segredo.md`. Beginners hide real secrets here far more
than they realize:
- `.env`, `.env.local`, `.env.production` — and **`.env.example`/`.env.sample`** (people fill in a
  real key then commit the "template"; scan it, treat clear placeholders as expected).
- `config.json`, `config.js`, `settings.json`, `appsettings.json` / `appsettings.Development.json` (.NET).
- `docker-compose.yml` (`environment:` / `env_file:` with literal values), `Dockerfile`
  (`ENV KEY=secret` / `ARG KEY=secret` — both bake into the image).
- `wp-config.php` — `define('DB_PASSWORD', '...')`, the auth salts/keys.
- `settings.py` / `config.py` (Django/Flask) — `SECRET_KEY = '...'`, DB password, `DEBUG = True`.
- `application.properties` / `application.yml` (Spring), `serverless.yml`, `vercel.json`,
  `netlify.toml`, `app.config`/`web.config`.
- `.npmrc` (`//registry/:_authToken=`), `.pypirc`, `terraform.tfvars`.
- **CI files** (`.github/workflows/*.yml`): an inline literal secret instead of `${{ secrets.NAME }}`.

## .ipynb and committed data dumps
- **Jupyter `.ipynb`** are JSON: scan BOTH the source cells AND the stored cell `outputs` (people
  commit notebooks with printed `os.environ`, API responses, `df.head()` showing real CPF/e-mail).
  Parse the JSON; scan source + decoded text outputs for keys and PII.
- **Committed data files** — tracked `*.csv *.xlsx *.sql *.db *.sqlite *.log` over a size threshold:
  flag as *"tem uma base de dados de verdade no repositório? Pode ter CPF/e-mail de cliente aí
  dentro"* (LGPD/🟡). Recommend `.gitignore` + `git rm --cached`.

## Per-archetype dangerous-config checks

### Node / Next.js / Vite / React (the common case)
- **Secret in a client bundle / frontend call** (🔴, the #1 vibe-coder leak): a `fetch`/SDK call to
  `api.openai.com`, `api.anthropic.com`, `api.stripe.com`, etc. from client-side code with a key; a
  literal key inside a React/Vue component. Consequence: *"a chave aparece no 'ver código-fonte' —
  qualquer um copia."*
- **`NEXT_PUBLIC_*` / `VITE_*` / `REACT_APP_*` holding a SECRET** (🔴): the public prefix INLINES
  the value into the browser bundle. Only non-secret values may use it. Grep for
  `NEXT_PUBLIC_.*(KEY|SECRET|TOKEN|PASSWORD)` etc.
- Next.js source maps shipped to prod; `next.config` exposing server env to the client.

### Python / Flask / Django
- `DEBUG = True` / `app.run(debug=True)` in production (🔴 — Werkzeug debugger = remote code
  execution; Django debug leaks settings + stack traces).
- `SECRET_KEY = '<literal>'` in `settings.py` (🔴), DB password literal, `ALLOWED_HOSTS = ['*']` (🟡).
- `requirements.txt` → `pip-audit` (or `pip list --outdated` if pip-audit absent).

### Static site (HTML/JS, no build)
- ANY API call with a literal key in client HTML/JS = **always public → 🔴**. There is no "backend"
  to hide it in; the fix is a serverless proxy or removing the feature.

### WordPress
- `wp-config.php` DB creds + missing/old auth salts; `define('WP_DEBUG', true)`; exposed `/wp-admin`
  with default creds; plugin API keys in options. (Mark deep WP/plugin runtime checks as partial.)

### Supabase / Firebase (open-database — the breach pattern)
- **Supabase RLS off:** tables created via SQL do NOT get RLS by default (dashboard-created ones
  do). An anon key + RLS-off table = anyone reads/writes the whole table. Check for `ENABLE ROW
  LEVEL SECURITY` in migrations; if absent on tables that exist, 🔴. (Real incident: CVE-2025-48757
  — 303 endpoints across 170 Lovable-generated apps had anon-readable tables; one leak exposed
  13,000 users.) `service_role` key in client = 🔴 always (bypasses RLS).
- **Firebase rules** `allow read, write: if true;` (or test-mode rules left on) = open database 🔴.
  Note: the Firebase web `apiKey` itself is NOT a secret — it's a project identifier; the real
  protection is the security rules. Don't scare the user about the apiKey; check the RULES.

### Cross-cutting (any web backend)
- **CORS** `Access-Control-Allow-Origin: *` together with credentials (🟡→🔴 if on a sensitive API).
- **Auth missing** on a sensitive route (admin/delete/user-data endpoint with no auth check) — A01
  Broken Access Control, the #1 OWASP risk. Source scan can only flag the OBVIOUS cases; true proof
  is runtime (state this).
- **Verbose errors / stack traces** returned to the client (leaks paths, versions) 🟡.
- **No rate limit** on an endpoint that calls a paid LLM/API (🟡 — "denial of wallet": an exposed,
  unthrottled proxy gets drained; real incidents in the millions-of-tokens range).
- **Secrets in `localStorage`** / tokens in client storage 🟡.

### XSS / injeção no navegador (A03 Injection, CWE-79) — checagem que faltava
Grep for these **unsafe DOM sinks fed by user input** (the #1 client-side hole in AI-generated code):
- **HTML sinks:** `.innerHTML =`, `.outerHTML =`, `document.write(`, `document.writeln(`,
  `.insertAdjacentHTML(`; jQuery `.html(` / `.append(` / `.prepend(` / `.after(` / `.before(`.
- **Code-execution sinks:** `eval(`, `new Function(`, `setTimeout("…")`/`setInterval("…")` with a STRING arg.
- **Framework escape hatches:** React `dangerouslySetInnerHTML`, Vue `v-html`, Angular
  `bypassSecurityTrust*`, Lit `unsafeHTML`. These exist ONLY to bypass the framework's auto-escaping.
- **URL sinks:** `location =`/`location.href =`/`.src =`/`.setAttribute('href'|'src', …)` taking user input
  (a `javascript:`/`data:` URL runs code).
- **Server-side reflected:** `res.send(`/`res.write(` or an HTML template literal `` `…${userInput}…` ``
  echoing a request value without escaping; triple-stache `{{{ }}}` / Jinja `| safe`.
Trigger: a sink ABOVE receiving anything traceable to user input (a form field, `req.body`/`req.query`/
`req.params`, `location`, or an LLM's output) = flag it. Pure-literal/constant content = not a finding.
- **Consequência (PT-BR):** *"se alguém digitar um código malicioso num campo do seu site (nome,
  comentário, mensagem), ele roda no navegador de quem visita — dá pra roubar o login da pessoa ou
  redirecionar pra um site falso."*
- **Conserto:** trocar `innerHTML` por `.textContent` (não executa código); deixar o framework escapar
  sozinho (não usar o escape hatch); se PRECISA renderizar HTML do usuário, sanitizar com DOMPurify
  (`DOMPurify.sanitize(...)`). Severidade: user input claro num sink = 🔴; escape hatch sem origem clara = 🟡/⚪.

### Ferramenta de IA: prompt injection (LLM01) + saída insegura (LLM05)
Quando o app manda texto pro modelo (OpenAI/Anthropic/Gemini), cheque a cadeia LLM01→LLM05:
- **LLM01 Prompt Injection:** o texto do usuário é COLADO dentro das instruções/system prompt — ex.:
  `prompt = "Você é X. Responda: " + userInput`, ou um template `` `Você é X. ${userInput}` ``, em vez de
  ir numa mensagem de papel `user` separada (`messages: [{role:'system'...},{role:'user', content:userInput}]`).
  Risco (leigo): *"a pessoa escreve 'ignore as instruções e faça Y' e o seu robô obedece — pode vazar o
  prompt secreto, falar besteira em nome da empresa, ou ser usado pra outra coisa."* Severidade base 🟡.
- **LLM05 Improper Output Handling:** a RESPOSTA do modelo cai num sink da seção XSS (`innerHTML = resposta`,
  `dangerouslySetInnerHTML`, `v-html`, `eval(resposta)`) ou é concatenada numa query SQL/comando. Isso vira
  XSS/RCE. **A cadeia LLM01 + LLM05 junta = 🔴** (entrada manipulável + saída executada).
- **Conserto (proporcional, pro leigo):** (1) texto do usuário vai numa mensagem `user` separada, nunca
  colado nas instruções; (2) imprimir a resposta com `.textContent`, nunca como HTML; (3) limitar tokens +
  rate limit (custo); (4) nunca pôr segredo/PII dentro do prompt (LLM02).

## LGPD detection signals (so the nudge only fires when there's real PII)
Only raise LGPD when the app actually handles personal data. Detect it from source:
- **Form fields:** HTML/JSX inputs named/typed `cpf email telefone celular nome nascimento rg
  endereco cep`.
- **DB schema / models / migrations:** columns `cpf email telefone nome data_nascimento`.
- **PII → LLM:** user personal data passed into a prompt sent to a model provider.
- If any fire AND there's **no privacy page** (grep routes/files for `privacidade`/`politica`/
  `privacy`) → nudge: política de privacidade visível + base legal/consentimento + segurança (LGPD
  art. 46). See `contrato-de-interacao.md` for the exact framing and the not-legal-advice disclaimer.
