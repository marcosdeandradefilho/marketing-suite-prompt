# guard-rails.md — input guards, refusals, policy-rewrites, Portuguese text (read at Step 0)

> These exist because a polished prompt that the generator REFUSES burns the user's scarce
> quota — and because the skill must behave on empty/garbage/abuse input. Handle these BEFORE
> any clarifier. All user-facing text is plain PT-BR, anti-guru, no lecture.

## 1. Empty / garbage / non-descriptive input
Triggers: empty, whitespace, a single word ("logo", "imagem", "arte"), an emoji, or a wall of
unrelated text. Do NOT fire the 3 clarifiers blindly on this.
Action: ask ONE open question and **STOP — wait for the reply**:
> *"Descreve em 1-2 frases o que tu quer ver na imagem: o quê, onde, e pra quê vai usar."*
That single question is the WHOLE response. Do NOT produce a briefing, a planta, or a prompt,
do NOT fabricate an example "to show how it works", and do NOT Write any file on empty input —
there is nothing to brief yet. Only proceed to the clarifiers once the user replies with a
minimally describable subject. Never dead-end and never refuse for "lack of detail" — pull the
detail out with the one question.

## 2. NSFW / abusive / harmful
Triggers: sexual/explicit content, sexualization of real people or minors, graphic
violence/gore, hate, harassment, or clearly illegal imagery.
Action: decline plainly, write NO file, do not lecture:
> *"Isso eu não monto. Manda outra ideia que eu te ajudo a fechar o prompt."*
One short line on why is fine; no moralizing paragraph.

## 3. Real people / celebrities / brands / logos / trademarks / living artists
Why it matters: generators routinely REFUSE named celebrities, real private individuals,
trademarked logos/characters, and "in the style of [living artist]" — and a refusal still costs
the user a generation. So rewrite BEFORE producing the prompt.
Rewrite rules:
- **Named celebrity / real person** → a generic person matching the visual description
  ("um homem de ~40 anos, barba grisalha, terno azul"), not the name. If it's the USER's own
  face/subject they want in the image, that's a legit reference-image job — coach the photo and write
  the identity-lock + RELIGHT prompt (see `geradores.md` routing/coaching + `prompt-expert.md`), so the
  face INTEGRATES instead of looking pasted.
- **Brand / logo / trademark** → either "uma marca fictícia chamada X" or describe the VISUAL
  STYLE (cores, tipografia) without reproducing the mark.
- **Trademarked character** (Mickey, Pikachu, club crests, etc.) → describe an original
  character with similar vibe, or a generic version ("um camisa de time de futebol genérica,
  listras pretas e brancas" instead of a real club crest).
- **"No estilo de [artista vivo]"** → translate to MOVEMENT + MEDIUM + ERA + VIBE
  ("pôster mid-century geométrico, paleta ocre"). [metodologia #10]
Always tell the user in ONE line what you swapped and why:
> *"Troquei [nome] por uma descrição parecida — gerador costuma recusar nome real/marca e isso
> queima uma geração à toa. Se você tem a foto/logo, dá pra subir como referência no gerador."*
Note: a generic "camisa de um time" / "um estádio de futebol" is fine — only the SPECIFIC
trademarked crest/badge/logo needs the swap.

## 4. Portuguese / accented text inside the image
In-image text in PT is a known failure spot — accents (ç, ã, õ, á) and long phrases misspell
often, and Nano Banana docs explicitly warn multilingual text "may make grammar mistakes".
[nano-banana #6, metodologia #15]
When the briefing has in-image text:
1. Put the EXACT words in QUOTES in the prompt (verbatim render).
2. Keep it SHORT — prefer 2-5 word phrases over sentences.
3. Specify font category + high contrast ("fonte bold sem serifa, texto branco sobre fundo
   escuro") for legibility.
4. Warn the user plainly:
   > *"Texto com acento (ç, ã, á) às vezes sai embolado. Deixei a frase curta e entre aspas pra
   > acertar melhor — confere letra por letra quando gerar, e se sair errado peça pra ele
   > corrigir só o texto."*
5. For text-heavy images, recommend Nano Banana **Pro** (best at legible text). [nano-banana #5]

## 5. The general anti-bluff stance
Never claim a generator does something that isn't in `geradores.md` / the fetched docs. If the
user asks about a generator you have no documented info on, say you'll apply the cross-generator
best practices (they transfer well) and that they should check that tool's own quirks. Don't
invent model names or limits.
