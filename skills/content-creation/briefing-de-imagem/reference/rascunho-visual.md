# rascunho-visual.md — render the composition sketch (the "rascunho") the user attaches

> The rascunho is a rough, LABEL-FREE composition sketch you RENDER to a PNG (SVG → PNG via a
> headless Chrome/Edge, no npm). The user attaches it to their generator as a COMPOSITION +
> PALETTE + FRAMING reference. Read this at Step 4. It replaces the ASCII planta as the primary
> deliverable; the ASCII planta in `blueprint.md` is now the DEGRADED FALLBACK when render fails.

## What the rascunho is (and is NOT) — say this honestly
- It IS: a rough blocking that fixes **composition** (where the masses sit), **framing / aspect
  ratio**, **camera/perspective**, and **palette + light direction**. That is what image models
  reliably read from a reference image.
- It is NOT: the final art, and NOT an accurate drawing of the subject. The subject's true FORM
  and (crucially) the user's FACE come from the **prompt** + the user's **real reference photo**,
  never from this sketch. Tell the user this in one plain line so they don't judge the rascunho as
  a finished image.
- You RENDER a rough sketch; you never generate the FINAL image. (Non-negotiable rule #1.)

## Why this exact form — grounded in the generators' own docs
- **Sketch → render is officially supported.** OpenAI: "Sketch-to-render workflows are great for
  turning rough drawings into photorealistic concepts while keeping the original intent. Treat the
  prompt like a spec: preserve layout and perspective, then add realism." Google's example uses a
  "napkin sketch as the structure." So a ROUGH blocking is explicitly enough — clean line art is
  NOT required. [fontes.md #19, #20]
- **Big flat MASSES, not line art.** Strong/clean lines get traced literally (the output looks
  like your crude doodle); filled silhouettes/greybox masses read as "where the big shapes sit"
  and leave the model free to render. Keep detail LOW — over-detail gets copied; tiny/faint shapes
  get ignored. [fontes.md #21, #22]
- **Color transfers by INSTRUCTION, not automatically.** Flat color blocks NUDGE the palette and
  its placement, but the reliable lever is also naming the palette in the prompt. Fill each mass
  with the intended palette color AND write the palette in the prompt. [fontes.md #21, #23]
- **NO text inside the sketch.** Models render text eagerly and baked-in labels come out as
  garbled text in the final image. Keep the rendered sketch 100% label-free; the labels live in
  the chat LEGEND and in the prompt. [fontes.md #22, #24]
- **Match the target aspect ratio**, and keep the subject off the extreme edges (gpt-image has a
  documented crop bias). [fontes.md #21, #25]

## PERSPECTIVE FIRST — the anti-bias rule (do this before drawing anything)
A sketch must NEVER default to a flat side-on "2D platformer" view just because it's easy to draw.
That biases the generator toward the easy shot. Instead:

1. **Decide the camera from the briefing** (framing + angle + what's near/far): e.g. over-the-
   shoulder behind the subject, low hero angle looking up, high aerial looking down, front 3/4
   banking into a turn, eye-level side. The camera is the FIRST decision.
2. **Express that camera with depth, not with a flat profile.** The tools you have:
   - **Depth planes:** foreground (big, often CROPPED by the frame, darkest) / midground /
     background (small, near the horizon, lower contrast). Naming the three planes is what stops
     the model from flattening everything.
   - **Relative size = distance:** the same castle is huge if near, a thumbnail on the horizon if
     far. Size, not just left/right, carries depth.
   - **Overlap / occlusion:** a near mass overlaps a far one — the single strongest depth cue.
   - **Horizon line height:** high horizon = looking down (aerial); low horizon = looking up (hero).
3. **Stage the masses for THAT camera.** Example, same scene, two cameras:
   - *Side, eye-level:* subject silhouette in the left third, target block in the right third, both
     on a low horizon — a lateral composition.
   - *Behind / aerial:* subject's back + wings BIG and cropped in the foreground framing the shot,
     the target tiny on a high horizon dead ahead, action receding INTO the frame.
   Both are the same kit (planes + size + overlap + palette + light) — only the staging changes.
4. **The prompt is the authority on camera.** Write the exact angle in the prompt ("câmera baixa
   heroica" / "vista de trás por cima do ombro, castelo pequeno ao longe"). The rascunho is
   attached as "reference only," so the generator builds the perspective from the words and treats
   the sketch as a loose guide — never locked into the sketch's geometry. This is what keeps the
   skill broad and unbiased.

## The masses (keep it to 3–6)
For each element from the planta: pick its **plane** (frente/meio/fundo), **rough size** (% of the
frame), **position** (thirds/corners), and a **flat fill** in the palette. Then draw it as ONE
bold silhouette/mass — no fine internal detail. Simple geometric subjects (castle, buildings,
horizon, sun, bottle, phone, car) render as clean recognizable silhouettes; complex organic
subjects (a person, an animal, a creature) render as a SIMPLE evocative silhouette — accept that
it's rough, because its real form comes from the prompt + photo. Do not chase realism in SVG.

## The SVG kit (build the HTML, then render it)
Write a minimal HTML file whose body is a single `<svg viewBox="0 0 W H">` at the target ratio
(W×H in the ratio the user will actually request — see ratios below). Building blocks:
- **Background = sky/atmosphere in the palette:** a `<linearGradient>` fill (e.g. cool storm
  blue→purple top, warmer near the horizon). This carries the palette.
- **Light source:** a soft `<radialGradient>` ellipse (warm if firelight/sunset) placed where the
  key light is, under a Gaussian-blur `<filter>` — this is the "luz principal" and gives mood.
- **Ground/horizon plane:** a rect or gradient from the horizon down; darker near the camera.
- **Masses:** `<path>`/`<polygon>`/`<rect>` filled flat in palette colors; foreground darkest,
  background lighter/greyer. Use overlap for depth.
- **Motion/energy (fire, light beam, spray):** a tapering `<polygon>` with a gradient, softly
  blurred; add a brighter inner core.
- **Rim light:** a faint warm blurred shape on the lit edge of the foreground mass.
- **Cinematic vignette:** a full-frame `<radialGradient>` transparent→black at the corners.
- **NO `<text>` anywhere.** Lightning/atmosphere may be faint strokes (they're mood, not elements).

Keep it a RECIPE, not a fixed template — adapt shapes/colors/planes to the scene and camera.

## Aspect ratio — render at what the user will actually request
- **1:1** → 1080×1080. **4:5** → 1024×1280. **9:16** → 720×1280. **16:9** → 1280×720.
  **3:2** → 1280×854. **2:3** → 854×1280.
- **Caveat that matters:** ChatGPT / gpt-image only outputs **1:1, 3:2, 2:3** natively — it does
  NOT do true 16:9 / 9:16 (it crops/approximates). **Nano Banana / Gemini does true 16:9 and 9:16.**
  So if the user wants 16:9 (wallpaper, YouTube) or 9:16 (Story/Reels): render the rascunho at that
  true ratio AND, in the prompt note, tell them to use Nano Banana for the exact ratio, or accept
  ChatGPT's closest (3:2 / 2:3) with a crop. Put this in the "ajuste por gerador" note. [fontes.md #25]

## Render it (Bash) — then CHECK it worked
1. Write the sketch HTML to the artifact folder, e.g.
   `.claude/briefings-imagem/AAAA-MM-DD-<slug>.rascunho.html`.
2. Run the renderer (it drives an installed Chrome/Edge via CDP — no npm, no API key):
   ```
   node "<caminho-desta-skill>/assets/rascunho.js" "<...>.rascunho.html" "<...>.png" <W> <H>
   ```
   `<caminho-desta-skill>` = this skill's own folder (where SKILL.md lives). W/H are the CSS size
   from the ratio table above (output PNG is 2× = crisp).
3. **Success** = stdout prints `WROTE <out> <w>x<h>` and the PNG exists. Tell the user the PNG path.
4. **You cannot see the PNG while running as the skill in a normal session** — that's fine; you
   built it deterministically from the planta. (When YOU are iterating on the technique with vision
   available, render → open the PNG → fix → re-render, like the site skill's visual loop.)

## Degraded fallback — never fake a PNG
If `node` is missing (`node -v` fails), no Chrome/Edge is found (the script prints `ERR no
Chrome/Edge`), Node is <21, or the render errors/timeouts:
- Do NOT claim a rascunho image exists. Say plainly: *"Não consegui gerar o rascunho em imagem
  aqui (faltou o Node/navegador headless), então vai a planta em texto — serve do mesmo jeito pra
  você aprovar a composição."*
- Deliver the **ASCII planta** from `blueprint.md` as the fallback, plus the full prompt.
- Optionally tell them how to enable it (install Node) if they want the image next time.

## The LEGEND (always show, because the sketch has no labels)
After a successful render, show a short PT-BR legend keying each region to a plain color/position,
so the human understands the label-free image. Example:
> *No rascunho: o degradê azul-arroxeado é o céu de tempestade; a silhueta escura grande na frente
> é você no dragão; o cone laranja atravessando é o fogo (a luz principal); o bloco cinza-pedra
> pequeno lá no fundo é o castelo. As posições são um mapa, não milímetro.*

Then hand off to the prompt + the "como anexar o rascunho" note (in `modelo-saida.md` /
`geradores.md`): the user attaches the PNG (and their real photo) and NAMES the roles in words.
