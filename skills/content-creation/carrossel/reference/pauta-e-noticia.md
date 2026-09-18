# pauta-e-noticia.md — ideation, live-news, format variants, policy

Three things live here: how to generate post ideas from just a niche, how to build a news/timely
carousel from a verified fact, and the format + policy cautions. (Sources: pathsocial content pillars,
pingback pauta-mining, sproutsocial newsjacking, TRE-PR/PUCRS fact-checking, IG/X authenticity policy,
maquinadepost carousel format, 2026.)

## A) Niche ideation — "não sei o que postar, me dá ideias"
Minimal entry: the user gives only a niche (e.g. "nutricionista"). Don't invent the audience — if it's
ambiguous, ask ONE short sub-niche question ("foco em emagrecimento, materno-infantil ou clínico?"). If
unanswered, assume the most common sub-niche and say so.

**Step 1 — map the pain (4-6 real dores):** question-mining — the o-que / como / por-que / quanto /
vale-a-pena questions + the niche's objections and myths. With web: anchor in Google autocomplete /
AnswerThePublic / competitor comments / Reclame Aqui. Without web: derive from knowledge and mark
confidence as such. Real pains come from real sources, not imagination.

**Step 2 — cross with the 6 categories** (so you don't ship 7 ideas of the same type):
EDUCATIVO (ensina algo acionável) · AUTORIDADE/PROVA (mito-vs-verdade, erro comum, prova de domínio) ·
INSPIRACIONAL (mudança de mentalidade, antes/depois) · BASTIDOR (como eu faço / processo real) ·
POLÊMICO/OPINIÃO (contraria o senso comum do nicho) · ENGAJAMENTO (pergunta/checklist que faz salvar).

**Step 3 — output 5-10 pautas**, each with 3 fields: **(a) ângulo** in one sentence (what the post
argues), **(b) categoria**, **(c) por que performa** (which pain/trigger — salvável, polêmico,
contraintuitivo, útil na hora). Vary the category across the list; include ≥1 polêmico and ≥1
que-gera-salvamento. Never a generic "5 dicas de X" without a point of view.

**Step 4 — prioritize:** mark the 2-3 strongest (prefer contraintuitivo + salvável + dor frequente).
Let the user pick, or pick the strongest and say which.

**Step 5 — turn the pick into a brief** for the copy stage (do NOT write hooks here — that's
copy-craft.md): `{ tema, ângulo, categoria, público, dor_atacada, promessa_do_carrossel,
fatos_verificados[] (vazio se não for notícia), tom }`.

### Worked examples (molde de FORMATO, não garantia de viralização)
- **Nutricionista (emagrecimento):** "Você não engorda por comer à noite, engorda pelo total do dia"
  (polêmico/autoridade — derruba mito, gera comentário+salvamento) · "O que eu peço num rodízio (e não
  é dieta)" (bastidor — aplicável na hora) · "3 alimentos 'fit' com mais açúcar que refrigerante"
  (educativo — contraintuitivo, alto salvamento).
- **Social media / tráfego:** "Seguidor não paga boleto: por que métrica de vaidade enganou seu
  cliente" (polêmico) · "O briefing de 5 perguntas que evita 90% do retrabalho" (bastidor/autoridade —
  salvável por outros social medias) · "Quanto cobrar quando tá começando (e como justificar)"
  (autoridade — dúvida campeã do iniciante).
- **Advogado (trabalhista):** "Foi demitido? 3 coisas pra fazer nas primeiras 48h" (educativo — útil,
  urgente) · "Aquele acordo 'amigável' que te faz perder dinheiro" (autoridade/polêmico). **Nuance:**
  área jurídica/saúde exige cautela — nunca prometer "você vai ganhar"; sempre "depende do caso,
  procure um profissional".

## B) Live-news path — only when the content depends on a current external fact
Trigger: "notícia de hoje sobre X", "fazer carrossel sobre [fato recente]", "reagir a [acontecimento]".
1. **WebSearch** the topic with a recency term (mês/ano atual). Find the news AND credible-source
   candidates (veículo grande, fonte oficial, empresa que anunciou).
2. **WebFetch 1-2 CREDIBLE sources** (prefer primary/official over third-party repercussão). Never
   write from a search snippet alone.
3. **Extract the verifiable core:** (a) the FACT in one sentence, (b) the DATE of the fact/publication,
   (c) WHO said/announced it (identified source), (d) the URL. Check the date — reposting an old story
   as current is the most common fraud; if the date doesn't match "de hoje", warn the user.
4. **Separate fact from interpretation:** verified facts → `fatos_verificados[]`; reading/forecast/
   opinion → marked OPINIÃO in the brief, never as fact.
5. **Pick an angle** (see below) and build the brief: `{ tema, fato_verificado, data, fonte_nome,
   fonte_url, ângulo, categoria, o_que_é_opinião }`.
6. The copy stage MUST attribute the source ("segundo [veículo], em [data]") when stating the fact, and
   mark opinion as opinion. Suggest putting the source on the last slide or in the legenda.

**News angles:** EXPLAINER ("o que mudou e o que significa pra você" — safest, salvável) · HOT TAKE
("minha leitura sobre X" — engaja, MUST be labeled opinion + anchored to the real fact) · O QUE NINGUÉM
FALOU ("o ângulo que ficou de fora") · TIMELINE ("como chegamos até aqui" — needs verified dates).

**Relevance + timing:** only proceed if the news genuinely connects to the niche; forced relevance or a
sensitive topic/tragedy = refuse or confirm (backlash risk). News has a short window (best within
hours) — say so without manufacturing urgency, and never trade fact-checking for speed.

## C) Accuracy guardrails (hard rules)
- NEVER invent a stat, number, date, quote or source name. Not verified → not a fact.
- Every asserted fact in a news carousel needs an identified source + date; without it, it's explicit
  "comentário/opinião", not an assertion.
- Always check the date (old-news-as-current is the #1 fraud). Prefer primary/official sources.
- On delivery, TELL the user which source was used (nome + URL + data) and what couldn't be verified.
- If a claim looks viral/dubious, flag it and suggest checking a fact-checking agency before posting.
- If the user pastes a "fact" as true → don't amplify; ask for a source or mark it as opinion.
- **Web down → the news path CANNOT run:** say "web indisponível, não invento fato"; offer an evergreen
  carousel on the same theme (no current claim) or ask the user to paste the source/fact to rewrite.

## D) Format variants (pick one, tell the user which)
- **A — THREAD:** 1 tweet per slide, narrative order (numeração 1/ 2/ opcional). Use: educativo,
  marketing, negócios. (This is the default for a "how-to" or list carousel.)
- **B — COMPILAÇÃO:** vários prints de tweets independentes sobre 1 tema. Use: humor/cultura pop.
- **C — FRASE DE EFEITO:** tweet único em destaque + slides de desdobramento. Use: mindset/empreendedorismo.
- Slides: Instagram allows 2-20; practical range 3-10; **6-8 favors screen time**. Same size on ALL
  slides. Dark "Dim" is the most common premium look; light also fine. Slide 1 = o gancho que decide o arrasto.

## E) Policy & impersonation cautions (warn the user; refuse the abusive case)
- **Impersonation:** Instagram forbids passing yourself off as a real person. A fake print attributed
  to a real person/brand to deceive or defame can get the post/account removed and carries legal risk
  in BR. The verified badge is OFF by default for this reason. WARN before generating a tweet
  attributed to a real existing person.
- **Parody must be labeled:** to imitate a public figure, the safe pattern (X rule) is clear "paródia /
  fake / sátira" labeling — never present it as a real statement.
- **Misleading content:** a "real-looking" tweet with a false factual claim can be flagged by checkers
  and have its reach cut. Don't fabricate data/events.
- **Política/eleitoral (BR):** fake political tweets carry elevated platform + regulatory risk —
  recommend not generating them.
- The safe lane is **your own voice / a fictional persona / clearly-labeled paródia** — that's almost
  always what the user actually wants, and it's what this skill produces by default.
