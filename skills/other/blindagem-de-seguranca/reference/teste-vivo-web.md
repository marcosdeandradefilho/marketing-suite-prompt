# teste-vivo-web.md — live, read-only, opt-in probe of the user's OWN published URL (Stage 2.6)

A file scan SUSPECTS; one read-only GET of the user's own live URL CONFIRMS. This turns "you have a key
in .env (might be fine)" into "your key is live in the browser right now, rotate it." Highest value:
confirming a client-side leak is actually shipped, and grading the real response headers.

## The four hard safety rules (never break — same model as the DB probe)
1. **Own URL only.** Only a URL that belongs to the USER'S project (their deployment/preview). NEVER a
   URL the user typed to "check if someone else's site is hackable." If it's not theirs, decline in one
   PT-BR line. This is a self-check, identical posture to running securityheaders.com on your own site.
2. **Opt-in.** Ask before any network request. *"Teu projeto já tá no ar? Posso fazer uns testes de
   LEITURA na URL dele? Não ataco nada — só abro as páginas e olho o que tá exposto."*
3. **Read-only GET, no attack.** GET only. One request per path. NO fuzzing, NO attack payloads, NO
   auth/password guessing, NO POST/PUT/DELETE, NO volume. Observe status/headers/body, report, stop.
4. **Confirm, don't exploit.** If a path leaks, you REPORT it (status + that it's reachable). You never
   download/dump data at scale, never pivot, never use a finding to go further.

If the user declines, every URL-level item STAYS a suspicion in the "o que essa varredura NÃO vê" block.

## What to GET (in order; stop early if the user only wants a quick look)

1. **Secret actually in the served JS bundle (the #1 confirmation).** Fetch the main served JS (the
   `<script src>` from the HTML, e.g. `/assets/index-*.js`) and grep it for real key shapes: `sk-`,
   `sk-ant-`, `AIza`, `eyJ` (JWT), `service_role`, `AKIA`, `xox` (Slack). A hit = the leak is LIVE and
   exploitable, not theoretical → 🔴 CONFIRMADO "gira a chave AGORA". Mask the hit in the report (prefix…last4).
2. **Missing security response headers** (read the response headers of the main GET). Report which are
   absent and the plain consequence:
   - **Content-Security-Policy** — sem ela, um XSS tem campo livre. (defesa contra injeção)
   - **Strict-Transport-Security (HSTS)** — força HTTPS. (só vale servida por HTTPS)
   - **X-Frame-Options** (`DENY`/`SAMEORIGIN`) — sem ela, outro site põe o teu num iframe e engana o usuário (clickjacking).
   - **X-Content-Type-Options: nosniff** — impede o navegador de executar um arquivo como script.
   - **Referrer-Policy** — evita vazar a URL/dados no header de referência.
   Missing headers are 🟡 (boa prática ausente), not 🔴. Frame as "dá pra publicar, mas adiciona esses".
3. **Source maps served in prod** — GET `<bundle>.js.map` (or look for `//# sourceMappingURL=` in the JS).
   If the `.map` returns 200, o código-fonte original tá público → 🟡.
4. **Exposed sensitive paths** — GET each, report only the status (200 = exposto): `/.env`,
   `/.git/config` (e `/.git/HEAD`), `/config.json`, `/config.js`, `/.env.local`, `/.env.production`,
   `/.DS_Store`. Also GET a directory path and look for an "Index of /" autoindex (directory listing). A
   200 on `/.env` or `/.git/config` = 🔴 (qualquer um baixa teus segredos / teu código).
5. **HTTP vs HTTPS** — GET `http://<host>`: redireciona pra `https://` (301/302)? Se servir conteúdo em
   HTTP puro sem redirect = tráfego interceptável → 🟡.

## Degraded / errors
- URL unreachable / DNS fail / timeout: say so plainly, keep the items as suspicion, don't retry at volume.
- WebFetch blocked in the environment: note the probe couldn't run; the items stay in the "não vê" block.
- A 401/403 on a path is fine (it's protected) — only a 200 with real content is a finding.

## After the probe
Move every CONFIRMED item out of the "o que essa varredura NÃO vê" block into a real finding (now tested,
not suspected). What you did NOT probe stays listed as a gap. Never let a partial probe read as "tudo ok".
