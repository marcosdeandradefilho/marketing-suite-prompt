# severidade-e-veredito.md — the 🔴🟡🟢 rubric + verdict logic + honest limits

Severity is anchored to **OWASP Top 10 2021** (`owasp.org/Top10/2021/`) and **OWASP Top 10 for LLM
Applications 2025** (`genai.owasp.org`). Each finding shows: the traffic light, the plain-PT-BR
consequence, and the OWASP tie (for the curious — keep it small, never lead with jargon).

## 🔴 VERMELHO — corrige ANTES de publicar
A real, exploitable exposure. Any single unresolved red blocks the green light.
- **Segredo vivo commitado ou exposto** — real provider key/password in source, config, git history,
  or a client bundle. [A02 Cryptographic Failures] *"Tá valendo e tá à mostra — qualquer um usa."*
- **Chave de provedor pago no navegador** — OpenAI/Anthropic/Stripe/Gemini key reachable from
  client code or in a `NEXT_PUBLIC_`/`VITE_` var. [A02 + LLM10 Unbounded Consumption]
  *"Qualquer um abre o site, copia a chave e gasta dinheiro na tua conta."*
- **Banco aberto** — Supabase RLS off on a real table, `service_role` in client, Firebase rules
  `if true`. [A01 Broken Access Control + A05] *"Qualquer um lê (e escreve) a base inteira — inclui
  os dados dos teus clientes."*
- **Endpoint sensível sem autenticação** — admin/delete/user-data route with no auth. [A01/A07]
- **Injeção explorável óbvia** — string-concatenated SQL/shell with user input. [A03 Injection]
- **XSS — código que roda no navegador da vítima** — user input num sink de HTML (`innerHTML`,
  `dangerouslySetInnerHTML`, `v-html`, `document.write`, `insertAdjacentHTML`) ou a saída do modelo
  renderizada como HTML. [A03 Injection / CWE-79] *"alguém digita um código no teu campo e ele roda no
  navegador de quem visita — dá pra roubar o login da pessoa."*
- **Prompt injection com saída executada (cadeia LLM01+LLM05)** — texto do usuário colado nas instruções
  do modelo E a resposta dele cai num sink de HTML/`eval`/SQL. [LLM01 + LLM05] *"a pessoa manipula teu robô
  e o resultado vira código rodando no site."*
- **`DEBUG=True` / debugger em produção** — Flask/Werkzeug debugger or Django debug exposed. [A05]

## 🟡 AMARELO — dá pra publicar, mas arruma logo
Real weakness, not an open door today.
- CORS `*` (sem credencial sensível) / cabeçalhos de segurança ausentes. [A05]
- Erro detalhado / stack trace vazando pro cliente. [A05/A09]
- Dependência com CVE conhecido (`npm audit`/`pip-audit`). [A06 Vulnerable Components]
- Sem rate limit num endpoint que chama API paga / LLM. [LLM10] *"Se descobrirem, enchem de
  requisição e estouram tua conta."*
- **Prompt injection sozinho (LLM01)** — texto do usuário colado nas instruções do modelo, mas a saída
  NÃO vira HTML/código. [LLM01] *"dá pra fazer teu robô ignorar as regras ou cuspir o prompt secreto —
  manda o texto do usuário numa mensagem separada, não colado nas instruções."*
- PII do usuário indo pro modelo sem necessidade. [LLM02 Sensitive Info Disclosure]
- Token/segredo em `localStorage`; base de dados real commitada (CSV/SQL). [A02 + LGPD]
- Falta política de privacidade num app que coleta CPF/e-mail. [LGPD art. 46]

## 🟢 VERDE — boa prática já presente
`.env` gitignorado e não rastreado; segredo só no back-end; RLS ligado com policy; deps em dia;
sem segredo no histórico. Report these too — the user should SEE what they did right.

## ⚪ NÃO TENHO CERTEZA — confere
Low-entropy/generic matches, probable placeholders, keys in docs/examples, anything a source scan
can't resolve. Present for the user to confirm; never inflate into red, never silently drop.

## Verdict aggregation rules (apply exactly)
1. **Qualquer 🔴 não resolvido ⇒ veredito 🔴 "NÃO publica ainda".** Full stop. List the reds first.
2. **Zero 🔴, algum 🟡 ⇒ 🟡 "dá pra publicar, mas arruma logo"** — list the yellows with the fix.
3. **Zero 🔴/🟡 E o scan foi COMPLETO ⇒ 🟢 "não achei problema no que dá pra ver pelo código"** —
   still rendered WITH the limits block below.
4. **Scan INCOMPLETO ⇒ NUNCA 🟢 puro.** If git was absent, the run was truncated, or
   `npm audit`/`pip-audit` wasn't available, render **🟡/⚪ "só vi o que deu pra ver"** and list
   exactly what you could NOT check. *Couldn't look ≠ looked and it's clean.*
5. **Já publicado / já público no GitHub + segredo encontrado ⇒ 🔴 automático** + "gira a chave AGORA,
   antes de tudo" (the key is presumed compromised regardless of the working-tree fix).
6. A user-dismissed ⚪/false-positive only downgrades AFTER explicit confirmation, and the verdict
   notes it was the user who dismissed it.

## ALWAYS render this block next to the verdict — "O que essa varredura NÃO vê"
Never let a green light overstate coverage. Render in PT-BR, PLAIN TEXT (sem `>`, sem negrito):

```
O QUE EU NAO CONSEGUI CHECAR (importante):
Eu leio os arquivos do projeto, nao testo o app rodando nem o servidor. Entao eu NAO confirmo que:
- a trava de acesso (login/permissao) realmente bloqueia um pedido de verdade. Isso so testando o app no ar.
- o RLS do banco ta REALMENTE barrando, a nao ser que voce tenha deixado eu fazer o teste de leitura ao vivo no teu Supabase/Firebase (ai o que eu testei ta confirmado; o que nao testei continua sendo so suspeita).
- como o teu servidor/hospedagem responde (CORS, HTTPS, cabecalhos, portas abertas), a nao ser que voce tenha deixado eu fazer o teste na URL publicada (Estagio 2.6).
- permissoes de nuvem (bucket S3, regra de firewall do banco, IAM).
- nada disso e um certificado de seguranca nem de conformidade com a LGPD.
Pra essas coisas, o caminho e testar o app publicado e, se for dado sensivel em escala, falar com um profissional de seguranca.
```

Tie each line to its OWASP category internally (A01 access control, A05 misconfig, A07 auth, A10
SSRF, A09 logging) but DON'T dump that on the user. If the live web probe (Estágio 2.6) DID run, move
the items it confirmed out of this "não vê" list into the findings (they're now tested, not suspected).

## Report shape (write to `.claude/seguranca/relatorio-AAAA-MM-DD.md`, masked) — PLAIN TEXT
The user reads this file RAW in the editor, where markdown does NOT render. So the SAVED report uses
NO emoji, NO `**bold**`, NO `|` pipe tables, NO HTML. Severity is a TEXT TAG at line start, not a
colored circle: `[VERMELHO]` / `[AMARELO]` / `[VERDE]` / `[CONFERIR]`. (The 🔴🟡🟢⚪ in the reference
files are internal shorthand for YOU — they must NOT appear in the saved report or the user's chat.)
Use `#`/`##` headers, blank lines, numbered lists. Shape:
1. VEREDITO em 1 linha: `[VERMELHO] NÃO PUBLICA AINDA` / `[AMARELO] dá pra publicar, mas arruma logo` /
   `[VERDE] não achei problema no que dá pra ver` / `[CONFERIR] só vi parte` + quantos vermelhos/amarelos.
2. Pra resolver antes de publicar — cada achado COMEÇA com a tag, ex.: `[VERMELHO] Chave da OpenAI no
   código (server.js:11)` seguido de: o que é (PT-BR), por que dói, e o conserto. (A tag no começo de
   CADA achado, não só no veredito.)
3. Arrume logo — cada um `[AMARELO] ...` idem.
4. Confere — cada um `[CONFERIR] ...` (possíveis falsos positivos).
5. O que já tá certo — cada um `[VERDE] ...`.
6. O que essa varredura NÃO vê (o bloco acima, sempre).
7. Próximo passo — re-run nudge.

Secrets in the report are ALWAYS masked (`sk-ant-…AA`). If the project is a git repo, ensure
`.claude/seguranca/` is gitignored before writing, so the report itself never gets pushed.
