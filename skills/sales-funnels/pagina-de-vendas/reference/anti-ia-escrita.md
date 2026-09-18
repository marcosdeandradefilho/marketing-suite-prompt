# anti-ia-escrita.md — write copy that nobody can tell was AI-written

Goal: nobody reading the page can tell an AI wrote it. This applies
to EVERY Brazilian-Portuguese string on the page (headline, body, bullets, FAQ, CTA, P.S.) and any chat copy
the user might paste. Run the self-check (bottom of this file) BEFORE the render loop, every build.

## Regra nº1 — PROIBIDO o travessão "—" como pausa
The em-dash "—" is the #1 AI tell in Brazil. Almost nobody types "—" in real copy. **NEVER use "—" or "–".**
Rewrite with a period, comma, parentheses, or the words "e"/"que"/"só que"/"aí".
- ❌ "A skill — que economiza horas — é simples" → ✅ "A skill economiza horas. E é simples."
- ❌ "Sem mensalidade — você paga uma vez" → ✅ "Sem mensalidade. Você paga uma vez."
Grep the final HTML for `—` and `–`; if either appears, fix it before delivering.

## The 15 tells of "cara de IA" (forbid; each with the antidote)
1. **Travessão "—" em excesso** (tell #1). Max 0, never as a rhythmic pause.
2. **Ritmo uniforme** (every sentence the same length) → mix a 3-word sentence with a 25-word one. "Funciona.
   Você descreve o que quer, aperta enter, e ele monta enquanto você toma um café."
3. **Parágrafos que começam igual** ("O método... O método... O método...") → vary the openings.
4. **Vocabulário neutro-previsível** (blacklist): inovador, eficiente, otimizado, potencializar, elevar,
   robusto, transformar (hype sense), "solução completa", "de forma simples e prática", "no mundo de hoje",
   "cada vez mais", descomplicar, alavancar, impulsionar, excelência, expertise, sinergia, holístico,
   "divisor de águas", "próximo nível". → swap for a plain, concrete word (melhorar, fazer render, deixar
   pronto, resolver, vender mais).
5. **Generalização vazia** (diversos, inúmeros, "vários aspectos", "especialistas dizem") → replace with a
   number/name/case. "Diversos alunos criaram ferramentas" → "Um aluno fez um leitor de boleto numa tarde."
6. **Adjetivo de elogio sem prova colada** ("inovador" solto) → "faz em 2 min o que você fazia em 2 horas".
7. **Aberturas-clichê:** "Imagine que...", "No mundo acelerado de hoje...", "E se eu te dissesse...", "Você já
   parou pra pensar..." → open with a fact, a number, or a dry question.
8. **Frase espelhada** "não só X, mas também Y" / "não é A, é B" + **tricolon perfeito** (três itens em ritmo
   igual: "rápido, fácil e eficiente") → break the symmetry; use 2 or 4, or vary the rhythm.
9. **Conectores formais empilhados:** "além disso", "no entanto", "vale ressaltar", "portanto", "em suma",
   "dessa forma", "ademais", "outrossim" → max 1 per section; prefer "e", "mas", "só que", "aí", "então",
   "porque", "por isso".
10. **Polido até zerar imperfeição** → keep a short sentence, a direct question to the reader, light slang.
11. **Emoji as decoration / in bullets / in the nav** → none on the page (a single one in a WhatsApp message
    is the max, only if it fits).
12. **Negrito e dois-pontos dramáticos em excesso** → bold only what truly matters (price, deadline, the one
    promise). Not every other phrase.
13. **Genérico em vez de concreto** ("soluções personalizadas") → a specific detail of THIS case ("anúncio no
    raio de 3km na hora do almoço").
14. **EN tells if any English leaks:** leverage, utilize, robust, seamless, synergy, comprehensive, delve,
    embark, tapestry, vibrant, "in today's fast-paced world".
15. **Tudo soando perfeito demais** → real copy has a human edge. Own a flaw, ask a question, use a contraction.

## Voice to SEEK (so the output isn't "correct but soulless")
Direct, no throat-clearing. Scannable. Tell it like a story. Prove what you claim. Own your flaws (fits
anti-guru). Ask the reader direct questions. Natural contractions ("pra", "tá", "dá pra", "a gente"). Formal
enough for a real offer, but unmistakably a person wrote it. See `exemplo-pagina-completa.md` for the gabarito.

## Mandatory self-check (run BEFORE the render loop, every build)
1. **Grep the final HTML for "—" and "–". Any hit → rewrite.**
2. Scan for the blacklist words (§4) and the stacked connectors (§9). Found → swap for a plain word.
3. Any perfect tricolon or mirror sentence? Break it.
4. Are all sentences ~the same length? Vary them (add a short punch, merge two into a long one).
5. Any cliché opening (§7) or empty generalization (§5)? Replace with a fact/number/concrete scene.
6. Any income promise, hype adjective, or fake-scarcity phrasing? Cut it (also see `compliance-br.md`).
7. Final filter: *"Isso ainda parece algo que uma pessoa escreveria?"* If not, rewrite that line.
Only when all 7 pass is the copy human enough to ship.
