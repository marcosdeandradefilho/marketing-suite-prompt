# blueprint.md — coarse-placement vocabulary + the ASCII text planta (render FALLBACK)

> The PRIMARY deliverable is now the RENDERED rascunho (an image) — see `rascunho-visual.md`.
> This file holds two things: (1) the coarse-placement VOCABULARY that both the rascunho staging
> and the prompt share, and (2) the small ASCII "planta de posições" you deliver as the DEGRADED
> FALLBACK when the render can't run (no Node/Chrome). The ASCII planta serves the human (to look
> at, approve, edit); the placement also goes into the prompt as coarse words. It is NOT a precise
> spatial spec. Read this when you build the prompt placement, or when you need the render fallback.

## The honest limit — read this first, never oversell
Text-to-image models are genuinely WEAK at literal relational placement. Peer-reviewed work
(ECCV 2024, "Getting it Right", arxiv.org/abs/2404.01197) found spatial relationships are
under-represented in training captions and models distinguish "on the left" vs "on the right"
at roughly RANDOM CHANCE (~49-52% accuracy). [fontes.md #13]

Consequences for how you build and sell the blueprint:
- **Prefer COARSE placement** (terços, cantos, fundo/meio/frente, ~% do quadro) over fine
  coordinates. Never write "exatamente 12% da esquerda".
- **Keep the count of independently-placed elements LOW** (2-4). More than that and the model
  drops or merges them.
- **Treat layout as a STRONG SUGGESTION**, not a guarantee. Tell the user: se a posição sair
  trocada, é UMA edição ("move o copo pra esquerda, mantém o resto"), não re-rodar do zero.
- An ASCII/box sketch helps the HUMAN reason and approve; the model parses it only loosely —
  so the placement also goes into the prompt as words.

## The coarse coordinate vocabulary (shared by human + model)
Use the rule-of-thirds grid + depth planes as a common language:
- Horizontal: terço da esquerda / centro / terço da direita.
- Vertical: terço de cima / meio / terço de baixo.
- Corners: canto superior direito, canto inferior esquerdo, etc.
- Depth planes: **primeiro plano (frente) / plano médio (meio) / fundo**. Naming the three
  depth planes is exactly what stops the model from flattening everything into centered mush.
- Size: rough share of the frame ("~40% do quadro", "pequeno no canto", "domina a cena").
[fontes.md #5, #12; gpt-image #10 endorses calling out placement when layout matters]

## How to build the ASCII planta (the render FALLBACK)
Use this when `rascunho-visual.md`'s render is unavailable, OR whenever a quick labeled list helps
the user reason. The SAME depth-plane thinking drives the rendered rascunho — see `rascunho-visual.md`
for the perspective-first staging.
1. List the elements (2-4 main ones). For each: position (grid + plane) + rough size + 1-line look.
2. Draw a small ASCII box sketch ONLY when it clarifies — a simple frame with labeled boxes:

```
┌─────────────────────────────┐
│  "TEXTO" (terço de cima)     │   ← headline, fonte bold, alto contraste
│                             │
│        [SUJEITO]            │   ← centro, ~45% do quadro, primeiro plano
│        plano médio          │
│  ~~~~~~ FUNDO ~~~~~~~~~~~~~  │   ← estádio/paisagem, fundo, desfocado
└─────────────────────────────┘
   formato: 9:16 (story)
```

   Keep the box small and labeled in PT-BR. The sketch is for the user to APPROVE/EDIT.
3. Translate the same placement into the prompt as coarse words (see `geradores.md` — for
   complex layouts, a short labeled list parses better than one dense sentence).

## How the user USES the plan (say this explicitly)
- The primary aid is the **rendered rascunho (PNG)**: the user ATTACHES it to the generator as a
  composition/palette reference AND pastes the prompt (see `rascunho-visual.md` + `geradores.md`).
  The ASCII planta is the fallback the user reads on screen when no image was rendered.
- Either way, the user pastes the **PROMPT** into the generator — the ASCII box itself is a
  planning/approval aid, not something to paste (pasting raw ASCII isn't a reliable technique).
- The plan exists so the user can SEE the composition before spending a generation, change what's
  wrong for free, and so the placement is already baked into the prompt as coarse words.

## Composition rules worth encoding (plain anchors)
- Rule of thirds: key elements on the grid lines/intersections ("sujeito no terço esquerdo").
- Leading lines: estradas/rios/caminhos que guiam o olho até o sujeito.
- Framing-within-frame: porta/janela/galhos ao redor do sujeito pra profundidade.
- Layering: nomear frente + meio + fundo. [fontes.md #5]

Always end the planta with the honest line to the user: *"Isso é o mapa da imagem. A posição é
uma sugestão forte — se o gerador trocar algo de lugar, pede pra ele mover só aquilo e manter o
resto, em vez de gerar tudo de novo (assim você não gasta outra geração)."*
