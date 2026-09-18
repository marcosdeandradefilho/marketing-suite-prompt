# teste-vivo-banco.md — live, read-only, defensive probe of the user's OWN database

This turns "I SUSPECT your DB is open" (static read of code) into "I CONFIRMED it: I pulled N rows
from your table just now with the public key — anyone can." It's the highest-value check in the
whole skill, and the safest possible version of it, IF you obey every rule here.

## When this runs
ONLY when the static scan (`deteccao.md`) found a **Supabase** or **Firebase** project AND you have
the project's own URL + public key from its config. For generic SQL (Postgres/MySQL/Mongo) you do
NOT connect — those stay static (see bottom).

## The four hard rules (never break)
1. **Own project only.** Use ONLY the URL + key found in THIS project's own config (`.env`, client
   init). NEVER a URL/host the user types or that points anywhere else. This is the user testing
   their own system — defensive, not an attack. (Reinforces the defensive-only rule in `contrato-de-interacao.md`.)
2. **Opt-in.** Make a real network call only after the user says yes. Ask in PT-BR:
   *"Achei teu Supabase no projeto. Posso fazer um teste de LEITURA nele agora pra confirmar se a
   base tá aberta? Não escrevo nem apago nada — só tento ler, no TEU banco."* (AskUserQuestion, sim/não).
3. **Read-only.** ONLY HTTP `GET` (a safe method per RFC 9110 — it cannot modify data). NEVER send
   `POST`/`PATCH`/`DELETE`/`PUT`. Use `limit=1` to stay light. Never run a destructive or write probe.
4. **Public key only — decode first.** Decode the JWT/key and probe ONLY with an `anon` /
   `sb_publishable_` key. **NEVER probe with `service_role` / `sb_secret_`** — it bypasses RLS (would
   falsely read as "open") AND transmitting a secret key is itself dangerous. If the ONLY key you
   found is a `service_role`, do NOT probe — that key being in the project is already a 🔴 finding.

## Transport (important for a correct verdict)
Make the GET with a **raw HTTP client via Bash** — `curl` (Mac/Linux) or `curl.exe` /
`Invoke-WebRequest` (Windows) — NOT WebFetch. The verdict hinges on the EXACT body (`[]` vs rows)
and the EXACT status (401 vs 403); WebFetch upgrades/paraphrases responses through a small model and
can mangle that distinction. Read the verbatim status line + body. `Bash` is already in `allowed-tools`,
so no extra permission prompt. Keep it to ONE request per table (`limit=1` / `shallow=true`).

## Supabase live probe (PostgREST)
Endpoint + headers (confirmed vs Supabase docs):
```
GET https://<project-ref>.supabase.co/rest/v1/            # OpenAPI root — lists anon-reachable tables
GET https://<project-ref>.supabase.co/rest/v1/<tabela>?select=*&limit=1
Headers:  apikey: <anon_key>
          Authorization: Bearer <anon_key>
```
Find `<project-ref>` + anon key in `SUPABASE_URL` / `VITE_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_URL`
+ the matching `*_ANON_KEY`, or the `createClient(url, key)` call in code. Get table names from the
OpenAPI root, or fall back to table names found in code/migrations.

**Interpret the BODY, not the status — all three cases return HTTP 200:**
- Body has **rows** (`[{...}, ...]`) → **RLS OFF / world-readable → 🔴 CONFIRMED.** Anyone with the
  public key reads this table.
- Body is **`[]`** (empty array) → RLS is ON and blocking the anon role → **safe** for that table.
- Body is an **error object** (e.g. `{"message":"...","code":"..."}`) → blocked/no access → safe.

**Redact the data.** If a table returns rows, report the COUNT and table name, NEVER the row
contents (they likely hold real client PII — CPF/e-mail). Say *"consegui ler N registros da tabela
`clientes` SEM login"* — never paste the rows into chat or the report.

## Firebase live probe
- **Realtime Database:** `GET https://<db>.firebaseio.com/.json?shallow=true`
  → `200` + a JSON object of keys = **open → 🔴 CONFIRMED**; `401 {"error":"Permission denied"}` =
  locked (safe). `shallow=true` returns only top-level keys, so you don't pull the whole DB.
- **Firestore:** `GET https://firestore.googleapis.com/v1/projects/<id>/databases/(default)/documents/<colecao>`
  → `200` + documents = **open → 🔴**; **`403` PERMISSION_DENIED** = locked (note: Firestore uses
  403, RTDB uses 401). Get `databaseURL`/`projectId` from the firebase config in the project.

## What CONFIRMED changes in the verdict
- A static "suspeito que o RLS tá off" becomes a 🔴 **comprovado**, with the count of rows you read.
- Update the limits block accordingly: when the live probe RAN, say *"testei teu banco ao vivo
  (só leitura) e confirmei isto"* for the tables you tested. When it did NOT run (user declined, or
  not Supabase/Firebase), the RLS/open-DB question STAYS a suspicion and remains listed in
  "o que NÃO vê" — never silently upgrade an untested DB to safe.
- **The fix is the same** (`correcao-e-rotacao.md`): enable RLS + ship a policy (Supabase) / lock the
  rules (Firebase). After a confirmed-open DB with PII, that's the top 🔴 — fix before publishing,
  and treat the data as already exposed.

## Generic SQL / Mongo — STAYS static (do NOT connect)
A normal app's Postgres/MySQL/Mongo is usually NOT exposed to the internet, and a zero-config skill
has no driver to connect (installing one breaks zero-config). So for these:
- Flag an exposed **connection string with a password** in config (🔴 if committed).
- Flag a DB port that looks publicly bound (e.g. Mongo `27017` open with no auth — historic
  mass-breach pattern) and point the user to the host's **firewall / network rules** — do NOT try to
  connect to it.
- Say plainly in the limits block that you checked the connection config, not the live DB, for these.
