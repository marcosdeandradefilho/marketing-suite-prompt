# recuperacao-de-escopo.md — layer-2/3 recovery paths (each with an acceptance criterion)

When the trava isn't a single error but "o código virou bagunça" or "o escopo explodiu," the fix is
to RE-CUT, not to keep patching. Each path below has an **acceptance criterion written as an
observable result** — what must be true for that path to be "done." Pick 2-3 distinct ones for the
report (see `caminhos-de-saida.md`). Critical distinction: **cut accidental complexity, never cut
the scope** — the tool still has to do the 30 things it needs to do; you're removing the messy HOW,
not the WHAT.

## 1. Pare de cavar + volta pro último estado que rodava
Law of Holes (en.wikipedia.org/wiki/Law_of_holes). Stop adding; get back to solid ground.
**Aceite:** nenhuma mudança/feature nova é tentada até (a) o projeto estar de volta num estado que
roda OU (b) a fatia quebrada estar isolada do resto.

## 2. Essencial vs acidental — corta só o acidental
Brooks, "No Silver Bullet" (en.wikipedia.org/wiki/No_Silver_Bullet). Essential complexity = the
problem itself (irreducible). Accidental complexity = the messy way it got built (reducible).
**Aceite:** cada peça travada está marcada `essencial` ou `acidental`, e SÓ as acidentais entram no
corte; o escopo (o que a ferramenta precisa fazer) fica intacto.

## 3. Corta o especulativo — YAGNI "presumido culpado"
"You Aren't Gonna Need It" (martinfowler.com/bliki/Yagni.html). Generic layers/flags/abstractions
built "for the future" with no current user are the usual bloat.
**Aceite:** toda abstração/flag/camada genérica que sobrou tem pelo menos UM consumidor concreto no
escopo atual; o resto é deletado ou revertido.

## 4. Fatia fina — Must-have-only (MoSCoW)
Vertical slicing + MoSCoW Must/Should/Could/Won't
(mountaingoatsoftware.com/blog/using-vertical-slicing-and-estimation-to-make-business-decisions-at-adobe).
**Aceite:** existe exatamente UMA próxima fatia que roda ponta-a-ponta; tudo marcado Should/Could/
Won't saiu do escopo atual. Define a meta em uma frase + listas IN/OUT explícitas.

## 5. Esqueleto que anda (walking skeleton)
A minimal end-to-end path that runs, before depth
(mattblodgett.com/2020/09/start-with-walking-skeleton.html). Great for an empty/near-empty project
or one that sprawled before anything worked.
**Aceite:** um único comando/fluxo produz um resultado real ponta-a-ponta (mesmo feio, hardcoded,
com dado falso); profundidade só DEPOIS que o esqueleto roda.

## 6. Refatora o módulo quebrado — NÃO recomeça o projeto
Joel Spolsky, "Things You Should Never Do, Part I" — never rewrite from scratch
(joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i). The instinct to "começar do zero"
is almost always wrong: that messy old code is full of accumulated bugfixes.
**Guardrail (diz pro usuário):** *"código não enferruja — o que parece bagunça costuma ser bugfix
acumulado que você vai jogar fora e ter que reaprender na marra."*
**Aceite pra sequer CONSIDERAR rewrite:** o usuário consegue (a) nomear o arquivo/módulo culpado E
(b) confirmar que existe um ponto de revert limpo. Sem os dois, refatora o módulo, não o projeto.

## 7. Estrangula, não explode (Strangler Fig)
If one module is rotten, replace it incrementally behind the flow that already works
(martinfowler.com/bliki/StranglerFigApplication.html).
**Aceite:** a cada passo o projeto ainda roda; a peça velha só sai depois que a substituta fina
passa no mesmo teste.

## 8. Enxuga o que a IA inflou
A 2026 analysis suggests that more capable LLMs tend to generate MORE bloated, coupled code, and
that code *volume* itself correlates with structural decay — so `"funciona"` is not proof of clean
(arxiv.org/html/2605.02741; treat as an indicative finding, not a hard law). Aim at the files where
the AI wrote a lot, a God Class / Long Method, or stdlib logic reimplemented by hand.
**Aceite:** a versão simplificada (a) passa no MESMO teste E (b) é mais curta / tem menos
responsabilidades por unidade.

## 9. Tira o sunk cost da decisão continuar-vs-abandonar
Sunk-cost fallacy applied to code
(arjancodes.com/blog/avoiding-the-sunk-cost-fallacy-in-software-development). Reframing question:
*"Se você começasse HOJE do zero, faria esse pedaço assim?"*
**Aceite:** a escolha (continuar/cortar/refazer só o pedaço) é justificada só por trabalho restante
+ valor futuro, NUNCA por "já investi muito tempo nisso."

## 10. Troca a abordagem manual pela ferramenta-padrão (pesquisa a saída)
The trava is "tô fazendo isso na mão / do meu jeito e não sai" when there's a standard, ready-made way.
Reinventing parsing, dates, money math, auth, file formats (XML/CSV/JSON), HTTP, etc. by hand is the
classic accidental-complexity trap — the way out is to STOP hand-rolling and use the standard tool, and
to look up how others already do it. This is the research path (SKILL rule 8): run a real search this
session for "the normal way to do X" / a library / an open-source example, VERIFY it exists, and hand
the user a one-line anchor to paste ("cola isso no Google ou pro Claude: ..."). For a deep prior-art
sweep, point them to `/busca-documentacao`.
**Aceite:** a parte feita na mão é trocada pela forma padrão (biblioteca/ferramenta nativa), confirmada
real nesta sessão, E o resultado certo aparece (ex.: "quando você rodar, o total bate com os itens").

---

### Choosing among these for the report
- Sprawl / "explodiu o escopo" → 1 + 4 (or 5 if nothing runs yet).
- "Virou bagunça" but it runs → 2 + 3 + 8.
- "Quero recomeçar do zero" → 6 (+ 9 to kill the sunk-cost pull).
- Rotten module inside a working app → 7.
- **Doing-it-by-hand / wrong approach when a standard tool exists** → 10 (the research path) + 2.
Always state acceptance as something the person can SEE ("quando você rodar X, sai Y"), never as a
recipe. Note: "voltar pro último estado que rodava" is a synthesized practice (composed from Law of
Holes + Strangler Fig + sunk-cost), not a single attributed doctrine — present it as practice, not
gospel.
