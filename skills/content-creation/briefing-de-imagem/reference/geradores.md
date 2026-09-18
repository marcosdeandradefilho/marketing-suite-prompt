# geradores.md — documented per-generator tricks + the ONE-prompt design

> Every trick here traces to official docs (see `fontes.md`). Model names change — when
> WebFetch refreshes the guides, prefer the fresh names. If the web is down, use these and
> tell the user "na data da última atualização do guia". NEVER invent a behavior.

## Current model names (as of the last guide update — confirm via WebFetch when possible)
- **ChatGPT / OpenAI:** current model is **gpt-image-2**; in the ChatGPT app it's branded
  **"ChatGPT Images" (Images 2.0, all tiers)**. Older "DALL·E" / "4o image generation"
  branding is legacy. Techniques below are stable across the gpt-image family. [gpt-image #16]
- **Nano Banana (Google/Gemini)** is an umbrella for THREE models:
  - **Nano Banana** = `gemini-2.5-flash-image` (low-latency).
  - **Nano Banana 2** = `gemini-3.1-flash-image` (newest fast/high-volume).
  - **Nano Banana Pro** = `gemini-3-pro-image` (pro assets, "Thinking", high-fidelity TEXT).
  All Nano Banana output carries a SynthID watermark. [nano-banana #1]
  - **For text-heavy images, recommend Nano Banana Pro** (best at legible text). [nano-banana #5]

## Generator ROUTING by job (the layperson doesn't know this — route for them) [fontes.md #33, #35]
Do NOT treat the generators as interchangeable. Recommend by what the image NEEDS. Always frame as a
suggestion + "vale testar nos dois", never an absolute (this field moves fast).
- **The user's real FACE in a scene (identity):** default **ChatGPT / gpt-image** — 2025-26 hands-on
  tests show it preserves a real person's face from a SINGLE photo better than Nano Banana (the old
  "Nano Banana = king of consistency" line is about generating+repeating a character, not a real
  selfie). **Nano Banana Pro** is the alternative IF the user sends 3–6 photos and wants strong
  scene relight/compositing. Midjourney omni-ref = stylized character, not a faithful selfie. [fontes.md #33]
- **Text INSIDE the image (logo, headline, price):** **Nano Banana Pro** (best legible text), + the
  PT-accent caveat. [nano-banana #5]
- **True 16:9 / 9:16 (wallpaper, YouTube, Story):** **Nano Banana / Gemini** (gpt-image crops to 3:2/2:3).
- **Product / commercial (lens+light+material control):** either; gpt-image follows structured prompts
  well, Gemini rewards rich narrative. Both fine.
- **Multi-reference by role** (object vs style vs character): Gemini mixes up to 14 refs by role
  (≤6 objects / ≤5 characters / ≤3 style); gpt-image edit takes up to 16. [fontes.md #26, #35]
Say it in one plain line, e.g.: *"Pro teu caso (teu rosto na cena), vai de ChatGPT — hoje ele segura
melhor o rosto de uma foto. Se quiser 16:9 exato de wallpaper, o Nano Banana faz; o ChatGPT corta."*

## Reference-photo COACHING (when the user wants their face/subject) — this matters MORE than the prompt
The #1 cause of a "pasted" face is a bad reference photo, not a bad prompt: a flat, front-lit document
selfie dropped into a dramatic 3/4 scene forces the model to invent shadows/geometry it never saw.
[fontes.md #33] Coach the user BEFORE they generate:
- **Send 3–6 photos, not one** — different angles, including at least one at the SAME ~3/4 angle as the
  target pose (within ~15–30° of it).
- **Sharp and big:** ≥1024px, ideally ~2000px; face fills a good part of the frame.
- **Neutral daylight, no heavy filter/beauty mode;** include hair, neck and shoulders for context.
- **Avoid:** only the flat frontal white-background document photo, sunglasses, deep shadows, motion blur.
- If they only have the flat document photo, say plainly it may look pasted, and that matching the angle
  + the prompt's RELIGHT lines (see `prompt-expert.md`) is what rescues it.

## The shared spine (works for BOTH — this is the core of the ONE prompt)
Both engines reward the SAME structure, so the core prompt is generator-agnostic:
1. Write **narrative prose, not a keyword list.** Google states this explicitly as the #1 rule;
   GPT Image is format-agnostic but also works great with clear sentences. [nano-banana #2, gpt-image #2]
2. **Consistent order:** use-case → subject → action → setting → style → lighting →
   framing/composition → coarse placement → palette → anti-slop → (photoreal trigger if photo)
   → aspect ratio in prose. [gpt-image #1, nano-banana #3/#4]
3. **In-image text:** put the EXACT words in **QUOTES** — quotes flip the model from "describe"
   to "render verbatim" (the single most impactful text habit). Keep text SHORT (1 word or 2-5
   words render far more reliably than sentences). Specify font category + high contrast.
   [gpt-image #3, nano-banana #5, metodologia #15]
4. **Aspect ratio in plain prose** in the core prompt ("formato vertical 9:16", "imagem
   quadrada 1:1") — this is what carries across both chat UIs. [gpt-image #6, nano-banana #7]
5. **Exclusions as POSITIVE phrasing**, not "no X". Neither engine wants a "no cars" list in
   natural language; say the positive ("uma rua deserta, sem trânsito"). [gpt-image #7, nano-banana #10]
6. **Photoreal trigger:** include the literal word "photorealistic" / "real photograph" for
   photo looks. Camera/lens specs are interpreted LOOSELY — use them for high-level look, not
   exact simulation. [gpt-image #11, metodologia #6]

## GPT Image (ChatGPT) — documented specifics
- **Text fidelity:** for tricky words/brand names, SPELL THEM OUT letter-by-letter and/or use
  ALL CAPS; for marketing copy demand "EXACT, verbatim, no extra characters" and "appears once,
  perfectly legible". Use medium/high quality for small/dense text. [gpt-image #3, #4, #14]
- **Aspect ratio:** in the ChatGPT app you can TYPE the ratio in the prompt OR use the
  aspect-ratio picker in the UI; you can also regenerate an existing image in a new ratio. (API
  sizes: 1024×1024 square, 1536×1024 landscape, 1024×1536 portrait, "auto".) [gpt-image #5, #6]
- **No negative-prompt field:** state exclusions/invariants as positive constraints inside the
  prompt ("no watermark", "fundo branco liso", "do not add new elements or text"). [gpt-image #7]
- **Reference images:** accepts uploads; describe the change, or reference each input by index +
  description ("Image 1: produto... Image 2: estilo..." → "aplica o estilo da 2 na 1"). Supports
  sketch→render. [gpt-image #8, #9]
- **Documented failure modes:** precise text placement, character consistency across gens, exact
  layout placement, latency on complex prompts. Mitigation = strict constraints + iterate. [gpt-image #13]

## Nano Banana (Gemini) — documented specifics
- **Narrative prose is the rule.** Official photorealistic template (fill in the blanks):
  "A photorealistic [shot type] of [subject], [action/expression], set in [environment].
  The scene is illuminated by [lighting], creating a [mood] atmosphere. Captured with a
  [camera/lens], emphasizing [textures/details]. The image should be in a [aspect ratio] format."
  [nano-banana #4]
- **Text template:** 'Create a [image type] for [brand/concept] with the text "[text]" in a
  [font style]. The design should be [style], with a [color scheme].' Pro model for high-fidelity
  text. Caveat: small text + multilingual (Portuguese) "may make grammar mistakes / misspell" —
  keep text short, quote it, iterate, verify letter-by-letter. [nano-banana #5, #6]
- **Aspect ratio:** in the API it's a parameter (`aspectRatio`), but in the chat UI state it in
  prose. Supported ratios: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, plus extremes
  1:4, 4:1, 1:8, 8:1. On EDITS it preserves the input ratio; to force it: "Do not change the
  input aspect ratio." [nano-banana #7, #8]
- **Reference images / fusion:** upload and describe the change; multi-image fusion up to 14
  reference images in one output. [nano-banana #9]
- **Negatives = semantic:** describe the scene positively; for complex scenes give step-by-step
  build order (fundo → meio → frente). [nano-banana #10]
- **Iterate conversationally:** "mantém tudo igual, muda só a expressão"; if a character drifts
  over many edits, start a new chat re-anchoring with a text description. [nano-banana #12]
- **Free-quota gotcha (tell the user if they mention the API):** the Gemini **API** free tier
  does NOT generate images (429 / limit 0) — image gen needs a billing-enabled project. The free
  ~quota lives in the **consumer Gemini app (gemini.google.com)**, a separate system. So "usar de
  graça" = o app Gemini, não a API. [nano-banana #13]

## Attaching the rascunho (+ the user's photo) — how to word it (Step 5)
The rascunho is attached as a COMPOSITION reference, not copied literally. Both engines support
sketch→render and multi-image reference; what does the work is NAMING each image's ROLE in words.
- **Sketch→render is official on both.** OpenAI: "Sketch-to-render workflows are great for turning
  rough drawings into photorealistic concepts while keeping the original intent. Treat the prompt
  like a spec: preserve layout and perspective, then add realism." Google's worked example uses a
  "napkin sketch as the structure." So a rough blocking is enough. [fontes.md #19, #20]
- **Multi-image:** GPT Image's edit endpoint takes up to 16 images; Nano Banana mixes up to 14
  reference images (roles: objects/characters/style). Refer to each by index/role. [fontes.md #19, #26]
- **The wording to give the user** (composition-only, keep palette, ignore the crude style, and —
  critical — render NO text from the sketch, since both models render text eagerly and a baked label
  would leak): e.g.
  > *"Imagem 1 = rascunho: usa SÓ como referência de composição/enquadramento e posição. Não copie o
  > traço, as linhas nem as cores achatadas do rascunho, e NÃO escreva nenhum texto que aparecer nele.
  > Mantém a paleta [tons X]. Renderiza como [estilo/descrição]."*
- **Only add "Imagem 2 = foto" when there's a real subject to preserve** (the user's face, a real
  product/logo): *"Imagem 2 = foto: é essa pessoa — mantém o rosto exato E RE-ILUMINA ele pela luz da
  cena (temperatura de cor, exposição e grão), pra não ficar colado."* (The identity-lock + relight
  language lives in `prompt-expert.md` — it's what stops the pasted look.) If the scene has no personal
  photo (generic product/scene), attach ONLY the rascunho — do not invent a second image.
- **Attach flow:** ChatGPT = ícone de clipe (desktop) / botão + (celular); Gemini app = botão de
  anexar. Both accept PNG + JPG. The user's real photo carries the FACE/subject; the rascunho carries
  the layout. [fontes.md #19, #26]

## Aspect-ratio caveat by generator (Step 5 — put in the note, and pick the render size)
- **ChatGPT / gpt-image outputs only 1:1 (1024²), 3:2 (1536×1024), 2:3 (1024×1536) natively** — it
  does NOT produce true 16:9 or 9:16 (it crops/approximates), and it has a documented crop bias
  toward 1024² that lops heads/legs. Keep the subject off the extreme edges. [fontes.md #21, #25]
- **Nano Banana / Gemini does true 16:9 and 9:16** (plus 1:1, 4:5, 3:2, 2:3, 21:9, extremes). On
  EDITS it preserves the input ratio unless you say "não muda a proporção". [nano-banana #7]
- **So:** for a wallpaper/YouTube (16:9) or Story/Reels (9:16), render the rascunho at that true
  ratio and tell the user: no Nano Banana sai na proporção exata; no ChatGPT o mais perto é 3:2/2:3
  e pode cortar. For 1:1 / 4:5 both are fine.

## The "ajuste por gerador" note (Step 5 — out of band, NOT in the core prompt)
After the core prompt, append a short PT-BR note so the one prompt serves both:
- **ChatGPT:** cole o prompt; se quiser travar a proporção, use também o seletor de proporção da
  interface. Pra texto, peça "texto nítido, exatamente como escrito".
- **Nano Banana / Gemini:** cole o prompt no app Gemini (gemini.google.com); pra imagem com muito
  texto, prefira o modelo Pro. Pra editar, peça a mudança e diga "não muda a proporção".

## The iterate-don't-reroll tip (both engines document this)
Change ONE thing at a time; on edits say "muda só X, mantém todo o resto igual" and RESTATE what
to keep, to prevent drift. This is the documented way to fix a close-but-wrong image without
burning another fresh generation. [gpt-image #12, nano-banana #12]
