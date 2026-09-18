# playbook-debugging.md — named techniques to drive a layer-1 fix

These are time-tested, attributed methods. Pick the one that fits; walk the person through it in
plain PT-BR. The point is to replace random patching with a method.

## 0. Stop digging FIRST (Law of Holes)
"If you find yourself in a hole, stop digging" (Law of Holes — Washington Post 1911 / Denis
Healey; en.wikipedia.org/wiki/Law_of_holes). Before generating ANY new code or change, halt —
especially if the person is flailing (changing things at random) or the project is mid-degradation.
Stopping alone leaves you in the hole, so pair it with a get-out plan: **revert to the last
running state OR isolate the broken slice.** This is step zero of every recovery.

## 1. Agans' 9 Indispensable Rules (the diagnostic backbone)
David J. Agans, *Debugging: The 9 Indispensable Rules* — exact names, in order
(embeddedartistry.com/blog/2017/09/06/debugging-9-indispensable-rules):
1. **Understand the System** — know what it's supposed to do.
2. **Make It Fail** — get a reliable repro before theorizing.
3. **Quit Thinking and Look** — STOP guessing/patching, read the real output/error first. *(The
   core destrava move.)*
4. **Divide and Conquer** — narrow where the failure lives (in code, or in history via bisect).
5. **Change One Thing at a Time** — one change per iteration, so a fix isn't masked by another
   edit. *(Stops panic-editing.)*
6. **Keep an Audit Trail** — write down what you tried and what happened (the hypothesis table
   below IS this).
7. **Check the Plug** — question assumptions: is it even running? right file? right version? saved?
8. **Get a Fresh View** — rubber-duck it, or describe it out loud / to someone else.
9. **If You Didn't Fix It, It Ain't Fixed** — re-run the repro and confirm it's actually gone; a
   bug that "disappeared" without a known cause isn't fixed.

## 2. Scientific / hypothesis-driven loop (the engine)
Andreas Zeller, *The Debugging Book* (debuggingbook.org/html/Intro_Debugging.html). Never jump
straight to a fix. Drive an explicit loop, tracked in a PT-BR table (which doubles as Agans rule 6,
the audit trail):

| Hipótese | O que eu espero ver SE ela for verdade | O que aconteceu | Confirma / Rejeita |
|---|---|---|---|

Observe → form a hypothesis → predict what you'd see if it's true → run the experiment → confirm or
reject → refine. Repeat until the hypothesis can't be narrowed further — that's the defect.

## 3. Reproduce first + Minimal Reproducible Example (MRE)
Agans rule 2 + the MRE/MCVE practice (en.wikipedia.org/wiki/Minimal_reproducible_example). Two
steps a non-programmer can do:
1. *"cola a mensagem de erro INTEIRA"* — the literal text, not a paraphrase.
2. *"faz quebrar de novo, do mesmo jeito"* — a reliable repro makes the cause visible and lets them
   ask for help effectively.
Then shrink to the smallest self-contained code+input+environment that still fails — and RE-RUN it
(you sometimes fix it by accident while minimizing).

## 4. Divide and conquer in TIME — `git bisect`
For "funcionava antes e quebrou" (a regression): binary-search history between a known-good and a
known-bad commit. O(log n) — about 7 tests for 100 commits. Can automate:
`git bisect run <script>` (exit 0 = good, 1-127 except 125 = bad).
(git-scm.com/docs/git-bisect)

## 5. Divide and conquer in INPUT — delta debugging
When the failing INPUT/file is big, halve it, re-test, keep only the half that still triggers the
failure, repeat toward the minimal trigger (ddmin — Andreas Zeller, 1999, Saarland; built to shrink
huge Mozilla bug-report HTML; handwiki.org/wiki/Delta_debugging). The input-side twin of git bisect.

## 6. Rubber-duck debugging (you are the duck)
Make the person narrate, line by line in plain PT-BR, what each part is SUPPOSED to do vs what it
actually does — the mismatch leaps out. It works because it offloads overloaded working memory and
forces sequential structure (Hunt & Thomas, *The Pragmatic Programmer*;
en.wikipedia.org/wiki/Rubber_duck_debugging). Perfect for non-programmers and a *confused* (not
exhausted) person. Ask: *"me explica como se eu não soubesse nada: o que essa parte deveria fazer?"*

## 7. 5 Whys — root cause (closing move)
After the immediate fix, ask *"por quê?"* ~5 times past the symptom to the underlying cause, so it
doesn't recur (Sakichi Toyoda / Toyota Production System;
en.wikipedia.org/wiki/Five_whys). Lightweight, no tools, fits the direct anti-guru tone. For
genuinely murky bugs, optionally enumerate candidate cause-buckets (input? environment?
dependency? logic? config?) before guessing.

## 8. Step away — incubation (when fatigue/loop is detected)
When you detect exhaustion or a thrashing loop, legitimize a low-stimulus break (coffee, walk,
sleep): the brain keeps working in the background (incubation effect — Brodt et al. 2018 riddle
study, reviewed at labvanced.com/content/research/en/blog/2024-11-incubation-effect-psychology).
It's an active strategy, not quitting. Don't push 5 more steps onto an already-fatigued person —
that deepens the blindness effects. (Tone handling: `ler-o-emocional.md`.)

---

### How these map into /destrava
- Flailing person → **0 (stop digging)** + **3 (quit thinking and look)**.
- Has a reproducible error → **2 (hypothesis table)** + **3/5 (reproduce + minimal case)**.
- "Worked before, broke now" → **4 (git bisect)**.
- Giant failing input/file → **5 (delta debugging)**.
- Confused but energetic → **6 (rubber duck)**.
- Just patched something → **1.9 (re-run the repro)** + **7 (5 Whys)** so it's actually fixed.
- Exhausted / looping → **8 (step away)**.
