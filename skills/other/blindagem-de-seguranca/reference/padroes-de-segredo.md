# padroes-de-segredo.md — the secret-detection engine

Patterns lifted **verbatim from the gitleaks master config** and verified against it this build
(`https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml`). Use these with
`Grep` (ripgrep regex). The whole point of this file is the moat: a generic "ask ChatGPT" does NOT
know the current 2026 key shapes (the OpenAI `T3BlbkFJ` infix, `sk-ant-api03-...AA`, fine-grained
`github_pat_`) nor the tuning that stops false alarms.

## How to scan (do this, not a naive grep)

1. Run a cheap **keyword pre-filter** first (the `keyword` column) to find candidate lines, then
   confirm with the full regex. This is how gitleaks stays fast.
2. Apply the **anti-false-alarm gate** (next section) to every hit BEFORE showing it.
3. **Redact** on output: show `prefix…last4` only. Never echo the full match.
4. **Never** call the provider to verify a key — a regex match is enough to act on.

## High-confidence provider patterns (a match here is real → 🔴 if live/committed)

| Provider | Keyword pre-filter | Regex (ripgrep) | Notes |
|---|---|---|---|
| OpenAI | `T3BlbkFJ` | `sk-(proj\|svcacct\|admin)-[A-Za-z0-9_-]{58,200}T3BlbkFJ[A-Za-z0-9_-]{58,200}` or legacy `sk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20}` | `T3BlbkFJ` infix is the cheap tell |
| Anthropic | `sk-ant-api03` | `sk-ant-api03-[a-zA-Z0-9_\-]{93}AA` | admin: `sk-ant-admin01-[a-zA-Z0-9_\-]{93}AA` |
| AWS access key | `AKIA` `ASIA` | `(A3T[A-Z0-9]\|AKIA\|ASIA\|ABIA\|ACCA)[A-Z2-7]{16}` | secret key is 40 base64 chars near it |
| Google / Gemini | `AIza` | `AIza[0-9A-Za-z_\-]{35}` | allowlist the docs demo `AIzaSyabcdefghijklmnopqrstuvwxyz1234567` |
| Stripe | `sk_live` `rk_live` | `(sk\|rk)_(test\|live\|prod)_[a-zA-Z0-9]{10,99}` | **`pk_live_`/`pk_test_` is PUBLIC by design → ⚪/note-only, NOT a leak** |
| GitHub PAT (classic) | `ghp_` | `ghp_[0-9a-zA-Z]{36}` | also `gho_`/`ghs_`/`ghr_` |
| GitHub PAT (fine-grained) | `github_pat_` | `github_pat_\w{82}` | |
| GitLab | `glpat-` | `glpat-[0-9a-zA-Z_\-]{20}` | |
| Slack bot | `xoxb` | `xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*` | also `xoxp-`/`xapp-`/`xoxe-` |
| SendGrid | `SG.` | `SG\.[a-zA-Z0-9_\-.]{22}\.[a-zA-Z0-9_\-.]{43}` | |
| Twilio | `SK` `AC` | `SK[0-9a-fA-F]{32}` / Account SID `AC[0-9a-fA-F]{32}` | |
| Mailgun | `key-` | `key-[0-9a-zA-Z]{32}` | |
| Private key | `PRIVATE KEY` | `-----BEGIN [A-Z ]*PRIVATE KEY-----` | RSA/EC/OPENSSH/PGP `.pem`/`.p12`/`.key` |
| JWT | `eyJ` | `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}` | decode payload — see Supabase below |
| DB connection string | `://` | `(postgres\|postgresql\|mysql\|mongodb(\+srv)?\|redis\|amqp)://[^\s:@]+:[^\s:@]+@` | flags only when it carries `user:password@` |

### Supabase (decode, don't guess)
Both `anon` and `service_role` keys are `eyJ...` JWTs — you CANNOT tell them apart by prefix. Decode
the payload (base64 the middle segment) and read `"role"`:
- `"role":"anon"` → public by design (meant for the browser) → **note-only**, BUT pair it with the
  RLS check in `deteccao.md` (an anon key is only safe if RLS is ON).
- `"role":"service_role"` → **🔴 always** — this key bypasses RLS entirely; it must NEVER be in
  client code or committed.
- New-format keys: `sb_publishable_...` (public, note-only) and `sb_secret_...` (🔴). Detect
  `sb_secret_` prefix loosely (`sb_secret_[A-Za-z0-9_-]{20,}`) — flag HIGH on the prefix alone;
  don't assert an exact length (post-dates gitleaks rules; medium confidence on the bound).

### BR providers (lock-in — gringo scanner ignora)
| Provider | Pre-filter | Regex / signal |
|---|---|---|
| Mercado Pago | `APP_USR` `TEST-` | access token `APP_USR-[0-9]{10,}-[0-9a-zA-Z\-]{20,}` (and `TEST-...`) |
| Meta / WhatsApp Cloud API | `EAA` | long-lived token `EAA[A-Za-z0-9]{20,}` |
| PagSeguro / Asaas | `token` `$aact` | Asaas `\$aact_[A-Za-z0-9_=\-]{20,}`; PagSeguro token = 32-hex near `pagseguro`/`token` |
| Pix key in text | `pix` `chave` | CPF/CNPJ/email/phone/random-key string labeled as a Pix key in source/config |

## The generic catch-all (powerful AND noisy — only ship it WITH the gate)
gitleaks `generic-api-key` requires a **variable-name keyword** + assignment + a high-entropy value:

```
(?i)(access[_-]?(key\|token)\|api[_-]?key\|auth[_-]?token\|client[_-]?secret\|secret[_-]?key\|password\|passwd\|token\|credential)["' ]*[:=]\s*["']([0-9A-Za-z._\-+/=]{16,80})["']
```

It will NOT fire on an arbitrary quoted string (no key-like name = no match). It DOES get noisy on
real assignments, so it is **invalid without all of these**:

### Anti-false-alarm gate (mandatory on the generic pattern AND a sanity pass on all)
- **Entropy ≥ 3.5** on the captured value (Shannon over the chars). Low-entropy → drop.
- **Stopwords / placeholders → drop:** `your-api-key`, `your_key_here`, `xxxx`, `changeme`,
  `example`, `placeholder`, `test`, `1234...`, `aaaa...`, `000000...`, `sk-xxxx`, `sk-1234`,
  the AWS docs key `AKIAIOSFODNN7EXAMPLE`, the Google demo key above.
- **Skip env LOOKUPS, not literals:** `process.env.OPENAI_KEY`, `import.meta.env.X`,
  `os.environ["X"]`, `os.getenv(...)`, `${{ secrets.X }}`, `config('X')` — these READ a secret,
  they don't contain one. Never flag them.
- **Path-aware:** in `*.example`, `*.sample`, `*.md`, `*.mdx`, `/docs/`, `/test`, `__tests__`,
  `/fixtures/` treat a match as a **probable example → ⚪ "confere se é real"**, not 🔴 — UNLESS it
  matches a high-confidence provider pattern above (a real `sk-ant-api03-...` in a README IS a leak).
- **Public-by-design allowlist (note-only, never 🔴):** Stripe `pk_`, Supabase `anon`/`sb_publishable_`,
  Firebase `apiKey` in the public web config (Firebase web keys are not secrets — the protection is
  the security rules, see `deteccao.md`), any value the user confirms is a placeholder.

## False-positive INTERACTION (not just the regex)
When a hit lands in docs/example/test paths or matches a known demo value, present it as
*"isso parece exemplo — é uma chave de verdade ou só de exemplo?"* and let the user confirm or
dismiss. Record dismissals so they don't re-fire in the same run. NEVER silently delete a match,
and NEVER silently suppress a high-confidence provider hit just because it's in a `.md`.

## What this engine canNOT catch (be honest in the verdict)
Encrypted/encoded secrets, secrets fetched at runtime from a remote config, secrets only in the
deployed host's env panel (good — that's where they belong), obfuscated/minified bundles, and
binaries you can't read. Listed in the "NÃO vê" block of `severidade-e-veredito.md`.
