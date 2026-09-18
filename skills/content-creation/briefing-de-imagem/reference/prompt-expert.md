# prompt-expert.md — the expert prompt engine (English prompt + PT gloss). Read at Step 5.

> This is the moat of the PROMPT (the rascunho is the moat of the composition). A layperson can't
> write an expert English photo prompt or the identity/relight language — this file encodes it.
> Everything here traces to official docs + credible experts (see `fontes.md` #27–#34).

## Rule 0 — deliver the prompt in ENGLISH, explain it in PT-BR
All evidence converges: image models are trained on English-majority captions, so an English prompt
gives higher adherence and is the ONLY reliable language for technical photo/art terms (lens,
lighting, color grade) and for text rendering. [fontes.md #27]
- **The copy-paste prompt block is in ENGLISH.**
- Right below it, give a **2–4 line PT-BR "o que o prompt diz"** gloss so the layperson understands
  and can edit — "inglês pra máquina, português pra você".
- **EXCEPTION — text that appears INSIDE the image:** keep that literal string in the user's language
  (PT), in "quotes", even inside the English prompt. Warn that accents (ç/ã/õ) may misspell; keep it
  short; suggest checking letter-by-letter. [fontes.md #27, geradores.md text rules]

## The 10-field expert structure (canonical order — fill densely with concrete nouns)
Synthesis of the official OpenAI + Google + Midjourney templates. [fontes.md #28, #29]
1. **Shot + realism trigger** — "A photorealistic [close-up / wide / full-body] [real photograph / candid photo / iPhone photo]".
2. **Subject** — who/what, specific: age, build, hair, clothing in a NAMED material ("navy blue tweed", not "suit").
3. **Action / expression** — what they do, expression ("relaxed, unposed" / "firm, heroic").
4. **Environment / setting** — concrete place.
5. **Light** — directional and real: "golden hour backlight", "Rembrandt lighting", "rim light", "soft window light", "firelight key from lower-left".
6. **Camera + lens** — style trigger, not literal optics: "shot on an 85mm lens, shallow depth of field, bokeh" / "35mm film, eye-level". [fontes.md #30]
7. **Texture / materials (ANTI-SLOP)** — "visible skin pores, natural imperfections, slight asymmetry, fabric weave, subtle film grain, RAW, no heavy retouching". [fontes.md #31]
8. **Palette / color grading** — restrained: "muted teal and orange", "1980s color film", named film stock ("Kodak Gold 200").
9. **Composition / framing** — angle (eye-level / low hero / aerial) + aspect ratio in prose.
10. **Constraints (negatives — BY ENGINE)** — gpt-image & Gemini have NO negative field → write the clean scene POSITIVELY ("an empty street with no traffic", "no glamorization"). Only Midjourney has `--no` (and it reads word-by-word — never "--no modern clothing"). [fontes.md #32]

Keep it dense in concrete NOUNS, not vague adjectives ("beautiful", "amazing" are ignored).

## Length — branch by the target generator (there is NO single number) [fontes.md #29]
- **Gemini / Nano Banana:** a rich NARRATIVE paragraph wins — "more detail = more control" (official).
- **gpt-image (ChatGPT):** structured beats messy; start lean and refine one change at a time. More
  text only helps if it's structure, not adjective spam.
- **Midjourney:** concise wins (~30–60 words), no adjective spam; the default aesthetic fills the rest.
- **Safe universal band for photoreal:** ~30–75 words dense in concrete nouns.
Write ONE English prompt in flowing prose (serves gpt-image + Gemini). If the user is on Midjourney,
add a short "encurta pro MJ" note rather than rewriting the core.

## The 5 anti-"AI slop" levers (bake into field 7) [fontes.md #31]
1. Skin/material texture: "visible pores, wrinkles, fabric weave, worn materials".
2. Film realism: "subtle film grain", "RAW photo", a named film stock.
3. Real directional light (field 5): golden hour / Rembrandt / rim — never flat.
4. Deliberate imperfection: "slight asymmetry, unposed, candid, natural skin".
5. Restrained palette: "muted", "no glamorization", "no heavy retouching".
The enemy is sterile perfection (plastic skin, oversaturation, symmetry). Strip hype words — gpt-image
ignores "stunning/masterpiece" and rewards concrete facts ("overcast daylight", "brushed aluminum").

## FACE FROM A PHOTO — identity lock + RELIGHT (this kills the "pasted" look) [fontes.md #33]
When the user attaches their own face/subject, the single biggest failure is a face that looks pasted
(a flat frontal photo dropped into a dramatic scene). Two things fix it — put BOTH in the prompt:
1. **Identity lock:** "the same person from the attached photo — keep the exact face, bone structure,
   skin tone and features; do not restyle or beautify the face."
2. **RELIGHT by the scene (the antidote):** "relight the face to match the scene — [firelight] key from
   [direction], matching the scene's color temperature, exposure, white balance and film grain, with
   physically-plausible contact shadows and ambient bounce, so the person truly belongs in the scene."
Also match ANGLE: if the scene is 3/4, the person should be described at 3/4 (and the user should send a
3/4 photo — see the photo coaching in `geradores.md`). Iterate small: "keep the face identical, change
only the lighting/angle". The reference PHOTO quality matters MORE than the prompt — always coach it.

## NO FACE PHOTO — the "character DNA block" [fontes.md #34]
When there's no reference photo but the image has a person/character, WRITE the identity so it isn't
generic mush. Build a fixed DNA block and (if they'll make more images) tell them to paste it VERBATIM
each time — paraphrasing causes drift; no generator locks a face from text/seed alone.
DNA block fields: apparent age + gender · skin tone/ethnicity · hair (color, length, texture) · beard ·
eye color + face shape · one distinctive trait · expression · default outfit (named materials).
Example: "a man in his early 30s, warm olive skin, short dark wavy hair, full trimmed beard, brown eyes,
oval face with strong jaw, calm confident expression, wearing dark worn leather armor".

## Google's official photoreal template (fill the blanks, in English) [fontes.md #28]
"A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is
illuminated by [lighting], creating a [mood] atmosphere. Captured with a [camera/lens], emphasizing
[textures/details]. [aspect ratio] format." — good scaffold for gpt-image + Gemini.

## Before → after (calibration)
- **Leigo:** "eu num dragão botando fogo num castelo" (PT, vago).
- **Expert (EN, what the skill delivers):** "A photorealistic cinematic wide shot of the man from the
  attached photos riding a colossal black dragon with vast membranous wings, breathing a jet of orange
  fire onto a burning stone castle below, a panicked army beneath. Low heroic angle, the rider large in
  the left third. Key light is the warm firelight relighting his face from below-right, matching its
  color temperature; cold blue-purple storm sky behind as rim light. Muted teal-and-orange cinematic
  grade. Real skin pores, subtle film grain, physically-plausible shadows, no heavy retouching. Keep his
  exact face and features from the photos; relight them to match the fire. Landscape 16:9."
Note the deltas the layperson would never add: English, camera/light, anti-slop texture, identity lock +
relight, restrained palette, positive constraints.

## Assembly checklist (Step 5)
- [ ] Prompt is in ENGLISH, flowing prose, ~30–75 words dense in nouns.
- [ ] In-image text (if any) kept literal in PT, in "quotes", with the accent warning.
- [ ] If a face photo: identity-lock + RELIGHT lines present; angle matched.
- [ ] If no photo but a person: character DNA block present.
- [ ] Anti-slop (field 7) + real light (field 5) + camera/lens (field 6) present.
- [ ] Negatives written positively (or `--no` only if Midjourney).
- [ ] A 2–4 line PT-BR gloss under the English block.
