# metodologia-briefing.md — the briefing fields + plain-language vocabulary (the moat)

> Internal reference (English). Everything you SAY to the user is plain PT-BR.
> Every fact here traces to a real source (see `fontes.md`). When WebFetch refreshes a
> source, prefer the fresh version. Do NOT pad with invented technique.

The single biggest upgrade you give a layperson: **force every briefing field to be filled.**
A blank field is where the generator falls back to generic, oversaturated, centered mush.
Fill each field with a FEW high-signal choices — not a wall of adjectives.

## The briefing fields (the art-director template)
A complete spec separates these, in this consistent, skimmable order
(use-case first sets the model's "mode" and polish level):

0. **Uso / deliverable** — ad, post, thumbnail, hero, logo, infográfico. State it first.
1. **Subject** — who/what, specific (not "a man" → "a tired delivery courier, 30s").
2. **Action** — what's happening.
3. **Setting** — where.
4. **Mood/tone** — the feeling.
5. **Palette** — color direction (see §Palette).
6. **Framing / shot size** (see §Framing) and **camera angle** (see §Angle).
7. **Lighting** (see §Lighting) and **depth of field** (see §Depth of field).
8. **Style / medium** (see §Style).
9. **Aspect ratio** (see §Aspect ratio by destination).
10. **Reference imagery** — if the user has one (optional).
11. **do-NOT / exclusions list** — author's checklist; gets TRANSLATED to positive phrasing
    for most generators (see `geradores.md`).
12. **Anti-AI-slop levers** (see §Anti-slop).

Sources: OpenAI cookbook prompting order (background/scene → subject → key details →
constraints + intended use); art-director creative-brief structure (Asana). [fontes.md #1, #2]

## §Framing — shot size (how much of the world you reveal)
Plain anchor for the user: "de quão longe tá a câmera e quanto da cena cabe".
Ladder: Extreme Wide (subject tiny in landscape) → Wide/Long (whole subject + environment)
→ Medium Wide → Medium → Medium Close-Up (chest up) → Close-Up (fills frame, e.g. a face)
→ Extreme Close-Up (one detail: an eye, a hand — tension/hyper-focus).
PT-BR: "plano aberto / plano geral / plano médio / close / close extremo". [fontes.md #3]

## §Angle — camera angle (how the viewer FEELS about the subject; separate from framing)
- Eye-level = neutro/equilibrado.
- Low-angle (de baixo) = poderoso, dominante, heroico.
- High-angle (de cima) = menor, vulnerável.
- Dutch (inclinado) = tensão, desconforto.
- Bird's-eye / top-down (de cima reto) = mapa, estratégico, "planta baixa".
Teaching move: pair the EMOTION the user wants with the angle term ("quero que fique
imponente" → ângulo baixo). [fontes.md #4]

## §Lighting — direction + hardness + color/time
- Golden hour = sol baixo, quente, suave, sombras longas.
- Soft light (luz suave/difusa) = sombras suaves, flattering (softbox, dia nublado, luz de janela).
- Hard light (luz dura) = sombras marcadas, alto contraste, drama.
- Backlight (contraluz) = luz por trás, separa o sujeito, brilha as bordas.
- Rim light = contorno de luz na borda do sujeito.
- Chiaroscuro = contraste extremo claro/escuro, dramático.
- Studio softbox = luz limpa de produto/retrato. Neon = brilho colorido artificial.
Teach as DIREÇÃO + DUREZA + COR/HORA. [fontes.md #8]

## §Depth of field — the highest-impact "looks professional" lever
- Shallow / shallow focus = só o sujeito nítido, fundo borrado (bokeh) — o look "retrato pro".
  PT-BR: "fundo desfocado/borrado".
- Deep / deep focus = tudo nítido da frente ao fundo — paisagem, produto, infográfico.
  PT-BR: "tudo em foco".
Flat all-in-focus snapshots read cheap/AI; naming DoF is a fast pro upgrade. [fontes.md #7]

## §Style / medium — name it explicitly, ONE at a time
Name the medium: foto / fotorrealista · pintura a óleo · aquarela · arte digital / render 3D ·
ilustração vetorial flat · pixel art · anime · isométrico · low poly.
**Rule: one complete style at a time** — stacking full styles dilutes each. Combine ONE style
with ONE lighting/material modifier, not three styles. For photoreal, include the literal word
"photorealistic" (or "real photograph / professional photography / iPhone photo") to engage the
photoreal mode. [fontes.md #9, gpt-image #11]
**Artist-name workaround:** many tools refuse "no estilo de [artista vivo]". Substitute by
MOVEMENT + MEDIUM + ERA + VIBE ("pôster mid-century, geométrico, paleta ocre fosca"). [fontes.md #10]

## §Palette — three precision levels
1. Mood/temperature: "quente", "fria", "fosca/dessaturada", "paleta natural".
2. Named palette: "teal e laranja", "tons pastel", "tons terrosos", cores nomeadas ("azul-marinho, ocre").
3. Brand hex / brand sheet for exact reproduction.
Naming a restrained palette ("paleta natural / tons foscos") is also an ANTI-SLOP lever against
default oversaturation. [fontes.md #11]

## §Aspect ratio by destination — choose BEFORE generating (it changes composition)
- 1:1 quadrado = universal, seguro em qualquer plataforma.
- 4:5 retrato = feed do Instagram, ocupa mais a tela do celular.
- 9:16 vertical = Story / Reels / TikTok / Shorts (única escolha pra tela cheia vertical).
- 16:9 paisagem = web/hero, YouTube, banner, cinematográfico.
- 3:2 / 2:3 = foto/print nativo.
Teaching point: a proporção faz parte do briefing, não é detalhe do fim — uma cena centralizada
pra 16:9 corta mal pra 9:16. Default social BR: 1:1 ou 4:5 pro feed, 9:16 pra Reels/Story. [fontes.md #17]

## §Anti-AI-slop — name the generic default and fight it
The tells of "cara de IA": cor super-saturada, pele plástica sem poros, simetria perfeita
demais, brilho chapado sem sombra real, vibe de banco de imagem. Cause: models default to
retouched training data.
Counter with IMPERFECTION + TEXTURE + DIRECTIONAL LIGHT + RESTRAINED COLOR:
"shot on 35mm film, visible skin pores, subtle film grain, natural asymmetric skin tone, soft
directional light with real shadow falloff, a few stray hairs, natural/muted color palette".
Principle (tool-agnostic): especificidade + direção de luz real + meio real + paleta contida.
Use deliberately, not as a magic word. [fontes.md #16]
Note: GPT Image IGNORES vague hype ("stunning", "masterpiece") and rewards concrete facts
("overcast daylight", "brushed aluminum"). So strip hype from the prompt. [evidencia #12]

## §Prompt length / signal discipline (cross-tool)
Signal beats filler — cut vague adjectives, keep concrete nouns. But length is NOT one number: it
branches by generator (Gemini/Nano Banana rewards a rich narrative paragraph; gpt-image rewards
structure and starting lean; Midjourney rewards concise ~30-60 words). Safe photoreal band ~30-75
words dense in nouns. The full expert structure, the ENGLISH-prompt rule, and the length-by-generator
branching live in `prompt-expert.md` — build the actual prompt from there. [fontes.md #18, #29]

## §Language of the prompt — ENGLISH (with a PT gloss)
Deliver the copy-paste prompt in ENGLISH: models are trained on English-majority captions, so English
gives higher adherence and is the only reliable language for technical photo/art terms. Add a short
PT-BR gloss so the layperson understands. In-image TEXT stays literal in PT, in quotes. Details +
sources in `prompt-expert.md` Rule 0. [fontes.md #27]

## What to actually say to the user
Translate every field into plain PT-BR with the anchors above. Don't dump the vocabulary list;
make the choices FOR them from their idea, show the briefing, and let them tweak. The value is
that nothing is left blank for the generator to guess.
