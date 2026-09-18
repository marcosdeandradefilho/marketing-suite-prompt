# fontes.md — provenance + the WebFetch freshness targets

> The reference layer's claims trace here. These are also the URLs to (optionally) WebFetch at
> Step 2 to confirm current model names / new tricks. If a fetch is blocked or fails, proceed on
> the baked-in reference and tell the user you used the built-in guide.

## WebFetch freshness targets (Step 2 — try these first, in this order)
The two that matter most for "what's valid today" are the official prompt guides:
1. **OpenAI / GPT Image prompting guide** —
   https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
2. **OpenAI API image guide (sizes/quality/failure modes)** —
   https://developers.openai.com/api/docs/guides/image-generation
3. **ChatGPT Images (consumer, model branding/ratio picker)** —
   https://help.openai.com/en/articles/11084440-images-in-chatgpt
4. **Google / Gemini image generation docs (model IDs, ratios, fusion)** —
   https://ai.google.dev/gemini-api/docs/image-generation
5. **Google blog — Nano Banana Pro prompting tips** —
   https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/
6. **Google developers blog — Gemini 2.5 Flash Image prompting** —
   https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/

If model NAMES differ from `geradores.md`, trust the fetched page and use the fresh name.

## Per-generator technique sources
- GPT Image: prompt order, sentences-vs-keywords, text-in-quotes/ALL-CAPS/spell-out, verbatim
  marketing copy, no-negative-field→positive constraints, reference images + index pattern,
  placement, photoreal trigger, iterate-change-one-thing, ad-as-creative-brief →
  https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- GPT Image: sizes (1024²/1536×1024/1024×1536/auto), quality levels, documented failure modes →
  https://developers.openai.com/api/docs/guides/image-generation
- GPT Image: ratio in prompt or UI picker; model branding gpt-image-2 / ChatGPT Images 2.0 →
  https://help.openai.com/en/articles/11084440-images-in-chatgpt
- Nano Banana: model IDs (gemini-2.5-flash-image / gemini-3.1-flash-image / gemini-3-pro-image),
  narrative-prose rule, aspect-ratio list + extremes + resolutions, 14-image fusion, semantic
  negatives, grounding/thinking → https://ai.google.dev/gemini-api/docs/image-generation
- Nano Banana: photorealistic + text templates, force-preserve-ratio on edits, hyper-specific +
  intent, character re-anchor →
  https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/
- Nano Banana: structure checklist, multilingual/PT text caveat, Pro for text →
  https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/
- Nano Banana: API free tier doesn't generate images (429/limit 0); free quota is the consumer
  Gemini app → https://ai.google.dev/gemini-api/docs/rate-limits

## Sketch-as-reference sources (the rascunho)
These back `rascunho-visual.md` + the attach/ratio notes in `geradores.md`. Sources: GPT Image, Nano
Banana, princípios de composição-referência. OFFICIAL = doc do fornecedor;
os head-to-head de "que forma de rascunho" não são cravados por nenhum fornecedor (princípio, não lei).
- **#19 — OpenAI: sketch→render é oficial + reference images + edit até 16 imagens.** "Sketch-to-render
  workflows are great for turning rough drawings into photorealistic concepts while keeping the
  original intent. Treat the prompt like a spec: preserve layout and perspective, then add realism."
  → https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide +
  https://developers.openai.com/api/reference/resources/images/methods/edit (OFFICIAL)
- **#20 — Google: "napkin sketch as the structure" + fusão multi-imagem por PAPEL.** Rascunho tosco
  serve como estrutura; nomear o papel em palavras é o que isola composição de estilo. →
  https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana +
  https://ai.google.dev/gemini-api/docs/image-generation (OFFICIAL)
- **#21 — gpt-image: placement é steer, não trava; viés de corte no 1024²; paleta/estilo por PALAVRA.**
  "the model may have difficulty placing elements precisely in structured or layout-sensitive
  compositions." Tamanhos nativos 1024²/1536×1024/1024×1536. →
  https://developers.openai.com/api/docs/guides/image-generation +
  https://community.openai.com/t/gpt-image-1-bias-towards-cropping-with-1024x1024-aspect-ratio/1318395 (OFFICIAL + fórum)
- **#22 — Texto no rascunho VAZA como texto embolado; linha forte é calcada.** "erase or mask any
  handwritten text in your input image before generation"; scribble card: linhas fortes "obey the
  condition image more". → https://community.openai.com/t/misspellings-or-grabled-text-in-generated-illustrations/1135230 +
  https://huggingface.co/xinsir/controlnet-scribble-sdxl-1.0 (fórum OpenAI + model card)
- **#23 — Bloco de cor chapado empurra a paleta (mecanismo treinado).** T2I-Adapter "color" = paleta
  espacial por downsample 8×8 → "conditioning on color palettes". Nudge, não trava-hex. →
  https://huggingface.co/TencentARC/t2iadapter_color_sd14v1 (OFFICIAL model card)
- **#24 — Nano Banana renderiza texto muito bem (por isso rótulo no rascunho é risco).** "advanced
  text rendering". → https://ai.google.dev/gemini-api/docs/image-generation +
  https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/ (OFFICIAL)
- **#25 — Casar a proporção antes de gerar; gpt-image não faz 16:9/9:16 nativo, Nano Banana faz.**
  → https://developers.openai.com/api/docs/guides/image-generation +
  https://ai.google.dev/gemini-api/docs/image-generation + https://editorialge.com/controlnet-composition-guide/ (OFFICIAL + guia)
- **#26 — Multi-imagem: GPT edit até 16; Nano Banana mistura até 14 refs por papel.** Referir cada
  imagem por índice/papel. → https://developers.openai.com/api/reference/resources/images/methods/edit +
  https://ai.google.dev/gemini-api/docs/image-generation (OFFICIAL)
- Princípio de conditioning (por que massa chapada > line-art; profundidade/segmentação = onde-o-quê):
  ControlNet → https://arxiv.org/abs/2302.05543 ; guia de composição → https://editorialge.com/controlnet-composition-guide/

## Prompt-engine sources (o prompt)
Backam `prompt-expert.md` + o roteamento/coaching em `geradores.md`. OFICIAL = fornecedor;
ESPECIALISTA = tester/benchmark credível; nenhum fornecedor crava "forma ideal" — princípio, não lei.
- **#27 — Prompt em INGLÊS rende mais; exceção = texto-na-imagem em PT.** Dados de treino/captions são
  majoritariamente inglês; termos técnicos de foto só confiáveis em inglês; texto renderizado precisa da
  string literal no idioma alvo. → OpenAI cookbook (aspas/CAPS/soletrar) + benchmarks de idioma +
  Google (multilíngue com erros admitidos). https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide ·
  https://ijonis.com/en/does-prompt-language-matter-llm-output · https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/ (OFICIAL+ESPECIALISTA)
- **#28 — Estrutura canônica + template fotorreal oficial.** OpenAI: "background/scene → subject → key
  details → constraints"; Google: "[Subject]+[Action]+[Location]+[Composition]+[Style]" e o template
  "A photorealistic [shot] of [subject]... illuminated by [lighting]... captured with [camera/lens]". →
  https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide ·
  https://ai.google.dev/gemini-api/docs/image-generation · https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/ (OFICIAL)
- **#29 — Tamanho ramifica por gerador (não há número único).** Gemini: prosa rica ganha ("more detail =
  more control"); gpt-image: estrutura > volume, começa enxuto e itera 1 mudança; Midjourney: conciso
  (~30-60 palavras). Faixa segura ~30-75 palavras. → docs acima + https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics (snippet) + https://artsmart.ai/blog/ai-image-prompts-photorealistic/ (OFICIAL+ESPECIALISTA)
- **#30 — Câmera/lente ajudam como GATILHO de estilo (não óptica literal).** "shot on 85mm f/1.8, shallow
  depth of field, bokeh"; "35mm film". → OpenAI cookbook + https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana (OFICIAL)
- **#31 — Anti-"cara de IA": textura de pele/material, grão/RAW/film stock, luz direcional real,
  imperfeição/assimetria, paleta contida.** OpenAI: "real skin texture... no heavy retouching"; Google:
  material nomeado ("navy blue tweed"). → cookbook + cloud.google.com guide + https://artsmart.ai/blog/ai-image-prompts-photorealistic/ (OFICIAL+ESPECIALISTA)
- **#32 — Negativo por gerador.** gpt-image/Gemini SEM campo negativo → constraint positivo ("empty
  street, no traffic"); Midjourney `--no` (lê palavra-por-palavra: nunca "--no modern clothing"). →
  cookbook + ai.google.dev + https://docs.midjourney.com/hc/en-us/articles/32173351982093-No (snippet) (OFICIAL)
- **#33 — Rosto que COLA: foto frontal chapada em cena 3/4 dramática força o modelo a inventar
  sombra/ângulo; conserto = trava de identidade + RE-ILUMINAR pela cena + foto melhor (3-6, ângulo
  casado ~15-30°, ≥1024px, luz de dia).** gpt-image (1.5) hoje segura melhor rosto de 1 foto real que
  Nano Banana Pro (o clichê inverso é sobre personagem gerado+repetido). → teste https://aiblewmymind.substack.com/p/nano-banana-2-vs-gpt-images-2 ·
  relight https://chasejarvis.com/blog/how-to-re-light-an-image-with-nano-banana-pro/ · foto https://kirkify.io/blog/ai-image-quality-factors-face-swaps · https://pict.ai/blog/how-to-put-your-face-in-ai-generated-images/ · relight oficial https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/ (ESPECIALISTA+OFICIAL; amostra pequena, campo muda rápido — validar ao vivo)
- **#34 — Sem foto: "character DNA block" fixo, colado VERBATIM (parafrasear = drift); nenhum gerador
  trava rosto só com texto/seed.** OpenAI admite dificuldade de personagem recorrente. → https://developers.openai.com/api/docs/guides/image-generation · https://miraflow.ai/blog/consistent-ai-characters-multiple-images-step-by-step (OFICIAL+ESPECIALISTA)
- **#35 — Valor do helper: GRANDE em rosto/produto/texto/layout/multi-ref; PEQUENO em cena simples
  (o ChatGPT auto-expande pedido casual — confirmado oficial p/ DALL·E 3).** → https://community.openai.com/t/api-image-generation-in-dall-e-3-changes-my-original-prompt-without-my-permission/476355 · https://nightjar.so/blog/prompt-patterns-realistic-ai-product-photos (OFICIAL+ESPECIALISTA)

## Methodology sources (generator-agnostic vocabulary)
- Creative-brief field structure → https://asana.com/resources/how-write-creative-brief-examples-template
- Framing / shot sizes → https://www.first.edu/blog/film-video-industry/the-6-basic-framing-shots-for-filmmaking/
- Camera angle + composition rules → https://leonardo.ai/news/ai-image-prompts
- Focal-length feel (loose interpretation caveat) → https://fstoppers.com/gear/what-focal-length-should-use-portrait-photography-616568
- Depth of field → https://blinksandbuttons.net/what-camera-setting-controls-depth-of-field/
- Lighting glossary → https://www.iphotography.com/blog/glossary-of-photography-lighting-terms/
- Style/medium + one-style-at-a-time → https://leonardo.ai/news/ai-art-styles
- Style-reference workaround + constant-vs-changing → https://www.aiforthat.io/blog/consistent-ai-art-style-guide/
- Palette levels, negative-prompt methodology, prompt-length discipline → https://letsenhance.io/blog/article/ai-text-prompt-guide/
- Anti-AI-slop tells + counters → https://lifehackedai.com/articles/why-ai-images-look-fake/
- Aspect ratio by destination (social sizes) → https://blog.hootsuite.com/social-media-image-sizes-guide/
- **Spatial-placement limit (~49-52%, ≈ chance)** → https://arxiv.org/abs/2404.01197 (ECCV 2024)

## "Why first try matters" evidence (use attributed, never as a hard number)
- Tier-1 anchor: Google cut free Nano Banana Pro from 3→2 images/day, "high demand", and warned
  "limits may change frequently" → https://www.engadget.com/ai/google-limits-free-nano-banana-pro-image-generation-usage-due-to-high-demand-223442929.html
- Reported: free quota shrinking + failed/unsaved generations still burn a slot (attribute, don't
  quote a hard count) → https://blog.laozhang.ai/en/posts/nano-banana-2-limits-daily-quotas-guide

## Competitor gap (the moat vs existing tools)
- imageprompt.org = single "Magic Enhance" box, no blueprint, no per-generator tuning, EN-first →
  https://imageprompt.org/image-prompt-generator
- Prompt databases (PromptHero, The Prompt Index) = static copy-paste libraries, no live docs, no
  per-idea tuning → https://www.thepromptindex.com/image-database.php
- Gap this skill fills: natively PT-BR, builds a blueprint, tunes to documented per-generator
  tricks, and (optionally) pulls the CURRENT guide at run time.

## DO-NOT (anti-bluff)
- Do NOT name Adobe Firefly as "the one that reliably refunds" (contradicted by user reports).
- Do NOT state hard free-quota numbers or per-image prices as fact — they churn; attribute or omit.
- Do NOT pin any "fully paywalled" claim to a specific date for a third generator — out of scope.
