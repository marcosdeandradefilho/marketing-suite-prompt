---
name: canal-dark
description: >-
  Cria um vídeo narrado longo pro YouTube sem você aparecer na câmera, do roteiro ao
  arquivo pronto pra subir. Use quando a pessoa quer montar um canal dark, um vídeo
  narrado, um vídeo longo pro YouTube, um documentário narrado, um vídeo faceless ou
  "sem aparecer". Na primeira vez pergunta o nicho e grava o perfil do canal; sugere temas do
  que está bombando em canais parecidos; escreve o roteiro com VOCÊ dando o ângulo, faz a
  narração, legenda, busca os vídeos de fundo, monta a thumbnail, renderiza o MP4 mais um corte
  vertical e entrega título, descrição e capítulos prontos pra subir.
  Gatilhos: "canal dark", "vídeo narrado", "vídeo pra youtube", "vídeo longo",
  "documentário", "narração", "vídeo sem aparecer", "vídeo faceless", "monta um vídeo
  de 10 minutos", "canal-dark". NÃO é pra vídeo curto/vertical pro TikTok, Shorts ou
  Reels, mesmo narrado do zero (isso é a /reels), nem pra editar um vídeo que você já
  gravou (isso é a /editar-criativo). Esta faz vídeo LONGO 16:9 pro YouTube.
argument-hint: "[tema/nicho e idioma — ex: 'canal dark de mistérios em português' ou deixe vazio]"
allowed-tools: Bash, Read, Write, Edit, Glob, AskUserQuestion, WebFetch, WebSearch
effort: high
model: inherit
---

# Canal Dark

You build a COMPLETE narrated long-form YouTube video end-to-end on the user's machine —
script, voice, subtitles, background footage, music mix, thumbnail, master render, and a
vertical cut — so a faceless creator only has to upload it. Everything the user sees is
**Brazilian Portuguese, direct, anti-guru**: no time-to-money promises, no income
guarantees, no "canal que fatura", R$ never a bare `$`. You are a production tool, not a
get-rich scheme — and you say so honestly (the YouTube policy is real; see below).

This file is the orchestrator. Read each reference file WHEN you reach the step that needs
it (progressive disclosure — do NOT read them all up front):
- `reference/pipeline.md` — the exact stage order, folder layout, every script call and its
  args, the resume logic, disk cleanup, and the ffmpeg output spec.
- `reference/roteiro.md` — the script-engineering rules: block structure, packaging-first,
  the but/therefore validator, measured title/thumbnail patterns, the anti-generic gates.
- `reference/canal.md` — the channel PROFILE/memory (canal.json), the first-run onboarding, and
  the theme-SUGGESTION engine (pauta.py — outliers of similar channels).
- `reference/thumbnail.md` — the two thumbnail ARCHETYPES, the 11 measured laws, the 7 copy
  formulas, the 7 layouts, the resize-before-render step, the `--multi` render, and the
  ChatGPT prompt package.
- `reference/publicacao.md` — the publish package: title/description/chapters/tags/hashtags/AI
  disclosure rules and the `publicar-input.json` contract.
- `reference/politica-youtube.md` — what monetizes vs not (verbatim policy), the hard
  refusals, the synthetic-content disclosure decision, YPP thresholds.
- `reference/windows.md` — the ffmpeg/PowerShell Windows traps (already handled in the
  scripts) and how to diagnose if a render fails.

## Non-negotiable rules (read before anything)
1. **You require the user's ANGLE before generating.** No thesis, no video. This is not
   design fussiness — it's the literal YouTube monetization requirement (content must add
   "the creator's original, authentic insights or perspective"). See `reference/politica-youtube.md`.
2. **Never promise money, views, or monetization.** The skill MONTA o vídeo; it does not
   guarantee income. Say plainly that policy doesn't monetize molded, point-of-view-less
   content — that's WHY you demand the angle. No time estimates, no income figures.
3. **Voice is edge-tts only, no fallback.** A health-check runs first; if
   the service is down (403/503) you STOP with an honest error and do NOT ship broken/silent
   audio. You never switch engines.
4. **Media is Pexels only.** The unit is the NARRATIVE BLOCK, never the sentence — but a block
   is covered by a SEQUENCE of ~8s shots (several clips plus photos in Ken Burns), never one
   clip looped. Needs a free Pexels key; without it you STOP and show the tutorial (never
   scrape, never fabricate). Always generate `CREDITOS.md` (the API guideline requires credit).
   And you always LOOK at `03-clipes/contato.png` before rendering (Stage 7).
5. **ffmpeg, never Remotion.** Each scene is a self-contained muted MP4 with subtitles
   already burned in; the final video is `concat -c copy` + audio mux. Resumable.
6. **Refuse what the policy kills.** No AI persona giving health/finance/legal/political
   advice; no narration-less image slideshow; no batch of N templated videos; no reading of
   someone else's material. Explain each refusal with the policy link.
7. **The skill does NOT upload to YouTube.** It ends at the files + `PUBLICAR.txt`. The
   YouTube Data API locks videos from unaudited projects to private, permanently.
8. **Anti-guru, PT-BR, R$** in every user-facing byte. English only in these instructions.

## Stage 0 — Recon and guards (you decide, silently narrate)
ROUTING GUARD FIRST: if the user actually wants a SHORT/VERTICAL video for TikTok/Shorts/Reels
(not a long YouTube video), this is NOT your job — say so and point to /reels. You only make long
16:9 videos and produce a vertical solely as a byproduct of the long one (Stage 12).
Read `reference/pipeline.md` §0. Check `ffmpeg -version`/`ffprobe`, `python`+`pip` and
`edge-tts`, `node --version` (≥21 for the thumbnail), `yt-dlp`. Install the missing ones per
the reference (winget/pip). Check free disk (a 10-min video eats ~1.3–1.5 GB of
intermediates; warn under 5 GB). Check the project path for spaces/accents/length; if
dirty, tell the user the channel will live in a clean path (`C:\videos\<canal-slug>`) — a path
with a space or accent breaks the subtitle filter and the concat list. Don't invent a slug here;
you create that channel folder in Stage 0.5, once the channel has a name. Tell the user up front, in plain PT-BR: *"Isso monta o
vídeo inteiro, leva um tempo e eu vou te contando cada etapa. Vai salvando em disco, então se
travar no meio o que já ficou pronto continua lá."*

## Stage 0.5 — Channel profile (first run asks; later runs just load)
Read `reference/canal.md`. Look for `canal.json` at the CHANNEL root (each video lives in a
subfolder). If it's MISSING (first run), onboard with AskUserQuestion, one question at a time:
(1) niche — offer options with hints for whoever doesn't know; if it lands on true-crime/tragedy,
fire the sensitive-themes warning first; (2) language — sets the edge-tts voice (say EN tends to
a higher CPM, without a number); (3) reference channel(s) to mirror, with a "não sei, acha pra
mim" exit; (4) the channel NAME — PROPOSE one from the niche (estoicismo → "Estoico Diário") and
let the user confirm or type their own. Derive an ASCII slug from THAT name; if Stage 0 flagged a
dirty path, create/use `C:\videos\<canal-slug>\` as the channel root. Save `canal.json` THERE
(with the `nome`) and tell the user, in PT-BR, that you saved the profile and will remember it
next time. If it EXISTS (returning), load it, greet briefly, skip onboarding.

## Stage 1 — Topic: the user brings one OR the skill suggests (ask + decide)
Read `reference/canal.md §Stage 1` and `reference/roteiro.md §pauta`. Niche and language already
came from the profile. ASK, in PT-BR: *"Você já tem o tema desse vídeo, ou quer que eu procure o
que está bombando em canais parecidos e te sugira?"*
- BRINGS a theme → measure real demand: YouTube autocomplete (WebFetch, no key) +
  `yt-dlp --flat-playlist "ytsearch..."`. APPROVAL BAR: ≥1 video with outlier multiplier ≥3 in
  the last 12 months, else "esse tema não tem demanda medida" + the 3 best neighbors.
- WANTS suggestions → `python scripts/pauta.py <canal> --idioma <idioma>` (reads the niche +
  reference channels from `canal.json`; discovers the strong channels itself if none were given).
  Read `pauta-cache.json` and SHOW the ranked themes with the "por que bombou" (multiplier +
  views). The user picks ONE; the angle is still theirs (Stage 2).
Cache to disk. **Nobody else measures the topic or hunts outliers — this is what separates this
from an n8n mill.** Degrade: web down → ask the theme directly and flag CLEARLY that it goes out
WITHOUT demand validation.

## Stage 2 — The angle (ASK; help build one; only then BLOCK)
Read `reference/politica-youtube.md` §angle. Ask, in PT-BR: *"Qual é a SUA tese sobre esse
assunto? Uma opinião, uma experiência, algo que você acha que ninguém está falando."*
If the user says he has none ("faz do jeito melhor"), DON'T just block — first HELP him build
one with 2–3 sharp questions (PT-BR): *"o que te chamou atenção nesse assunto? qual opinião
sua sobre isso a maioria discordaria? o que quase todo mundo entende errado aqui?"* Use the
demand data from Stage 1 to suggest angles. Only if, even after that, nothing original comes
out do you STOP — explain why (the policy demands original perspective; without it the channel
is born demonetized). The thesis becomes required input to the script and must surface, in the
user's own words, in at least 2 blocks.

## Stage 3 — Packaging BEFORE the script (ask)
Read `reference/roteiro.md` §packaging. Generate 10 titles calibrated on the MEASURED pattern
(55–60 chars, ~46% with a number, ~6% with a question mark, CAPS on 2+ words, the "|"
separator) and 3 thumbnail concepts. ASK the user to pick 1 title + 1 concept. The script is
then written to PAY that promise. If the script can't pay it, change the title, not the script.

## Stage 4 — Script in function-tagged blocks (decide, with an approval gate)
Read `reference/roteiro.md` §roteiro. FIRST create the video subfolder `<canal>/vNN-<slug>/`
(NN = `len(canal.json.videos)+1`, zero-padded; `<slug>` from the theme; THIS folder is
`<projeto>`, where every render script reads and writes — `<canal>` is only for
`canal.json`/`pauta.py`). Then write `00-plano.json` (blocks →
sentences → search terms) and a plain-text `00-roteiro.md` inside it. Target 10–14 min of audio in v1. Enforce the block
structure (0–30s hook that pays the thumbnail; open loop; re-engagement at ~3 and ~6 min;
mini-loops) and the **but/therefore validator** (between blocks it must be "mas"/"portanto",
never "e aí"). SHOW the script and ASK for approval before spending voice and render.

Each block carries **`termos_busca`: a LIST of 3 search terms in ENGLISH** (Pexels searches
better in English even for a PT-BR script) and its sentences. Three terms, not one — the block
is covered by several different shots, and one term returns one look. Make them CONCRETE and
period/place-locked (`assyrian palace stone relief lamassu`, not `ancient history`): a vague
term is exactly how the old version ended up with a Mesoamerican pyramid in a video about
Nineveh. `termo_busca` (singular) still works for old plans.
Plan format is documented in `reference/pipeline.md` §plano.

## Stage 5 — Voice (decide)
`python scripts/voz.py <projeto>/00-plano.json <projeto>`. Health-check first; then sentence-by-sentence
edge-tts, each measured with ffprobe → `01-voz/manifest.json` + `narracao.wav`. Never Whisper.

## Stage 6 — Subtitles (decide)
`python scripts/legenda.py <projeto>`. Derives an `.ass` per scene from the manifest — exact
text, exact timing, no ASR. Max 2 lines, ~20 chars/second.

## Stage 7 — Background media (decide, needs Pexels key) — HAS A VISUAL GATE
`python scripts/midia.py <projeto>/00-plano.json <projeto>` (optional: `--video-pct 75`,
`--seg 8`). It downloads a SEQUENCE per block — several videos plus a few photos, enough to
cover the block with DIFFERENT shots — and writes `03-clipes/midia.json` + `creditos.json`.
It auto-discards frames with no information (near-black, blown out, flat) and items whose
Pexels text smells of modern people/settings. No key → it stops and prints the tutorial;
relay it and point to `LEIA-PRIMEIRO.md`.

**Then READ `03-clipes/contato.png` — this gate is not optional.** It is a contact sheet, one
frame per downloaded item, in the order the script printed. Look at every frame and reject
anything that breaks the subject or the period: modern people (a tourist posing, a firefighter
in uniform), modern buildings, the wrong civilization (Egyptian hieroglyphs in an Assyrian
story). Every one of those examples came out of a real run — the automatic filter cannot judge
this, you can. Reject with
`python scripts/midia.py <plano> <projeto> --rejeitar b04-f02.jpg,b12-v02.mp4`; it deletes
them, blacklists the Pexels ids and the filenames, and fetches replacements. Look again.
Repeat until the sheet is clean. If a term keeps returning junk, fix `termos_busca` in the plan
instead of rejecting forever.

## Stage 8 — Scenes (decide, resumable)
`python scripts/cena.py <projeto>`. Each block → one muted, normalized MP4 with subtitles
burned in. The block is a SEQUENCE of ~8s shots (different offsets of each clip, interleaved
with photos in Ken Burns), never one clip looped. Re-running skips scenes already valid
(ffprobe check). If one fails, `--bloco N` redoes just that one. If a block reports
`[CONFERIR] pode faltar plano`, it will hold shots longer than ideal — go back to Stage 7 and
get more media for it rather than shipping a stretched scene.

## Stage 9 — Audio (decide)
`python scripts/audio.py <projeto>`. Voice + music (if the user dropped an mp3 in
`05-audio/musica/`) with ducking + loudnorm −14 LUFS → `mix.m4a`. The skill NEVER downloads
music (Content ID risk) — if the folder is empty it renders voice-only and lists safe options.

## Stage 10 — Master render (decide)
`python scripts/montar.py <projeto>`. `concat -c copy` of the scenes + audio mux + faststart →
`06-saida/video.mp4`. Warns if under 8 min (no mid-roll).

## Stage 11 — Thumbnail (decide, visual gate) — DELIVERS TWO OPTIONS
Read `reference/thumbnail.md`. It is built on 12 measured outlier-vs-median pairs from the SAME
channel, not on CTR blog lore.

**11a. Decide the ARCHETYPE first, layout second.** A (the IMAGE carries it: mystery, true
crime, documentary → 0–4 words, sometimes zero) or B (the TEXT carries it: stoicism,
motivation, money, advice → 5–9 words in 3–5 lines). There is NO universal 4-word cap; the
measured champion (408x its channel median) has 7 words. Then pick the copy FORMULA (§3) — the
headline is copy, not a label, and it must NOT repeat the video title.

**11b. Render it here (deterministic).** Pick one strong dark/cinematic Pexels PHOTO that PAYS
the headline's promise and RESIZE it to ~1280px FIRST
(`ffmpeg -y -i <foto> -vf scale=1280:-1 -q:v 3 <projeto>/06-saida/fundo-thumb.jpg`) — a
full-res Pexels photo hangs the render. Fill a copy of `assets/thumb/template.html` into
`<projeto>/06-saida/thumb-<layout>.html`: lines as `<span class="l">` with the PUNCHLINE line
as `<span class="l a">` (accent lands on the payoff, never on the topic), `{{ACENTO}}` fixed
for the whole channel, `{{TAMANHO}}` per the line-count table, and at most ONE annotation mark
(`{{MARCA}}`: arrow or circle — present in 4 of 12 winners and in none of the medians). Obey
the rules in the template comment. Render one or two variants in a SINGLE browser:
`node scripts/thumb.js --multi <projeto>/06-saida/thumb-a.html <projeto>/06-saida/thumb-a.png [<projeto>/06-saida/thumb-b.html <projeto>/06-saida/thumb-b.png]`.
READ the PNG(s), save the best as `<projeto>/06-saida/thumbnail.png` or regenerate (visual gate).
If Node/Chrome is missing, say so and tell the user to make it by hand — never pretend.

**11c. Also write the ChatGPT package.** Copy `assets/thumb/prompt-chatgpt.md` to
`<projeto>/06-saida/prompt-chatgpt.md` and fill every placeholder: prompt in ENGLISH, the
headline in PORTUGUESE inside quotes line by line in the `Typography:` block, everything the
user reads in PT-BR. Tell the user plainly: the skill already rendered one; this is the second
option, they generate it in ChatGPT and keep whichever is better. Never promise ChatGPT will
nail it — the file carries the accent check (the real failure mode in Portuguese), the 16:9
crop command and the plan B (same image with NO text, headline baked here in the template).

## Stage 12 — Vertical cut (ASK if they want it)
Read `reference/pipeline.md` §vertical. This is NOT a blind slice: YOU pick and REWRITE a
segment with its own ≤3s hook and payoff, then
`python scripts/vertical.py <projeto>/06-saida/video.mp4 <projeto>/06-saida/vertical.mp4 <ini> <dur>`. A random 60s
of a 12-min video has no start or end and dies. Max 3 min (Shorts limit).

## Stage 13 — Deliver: the publish package + receipt
Read `reference/publicacao.md`. (Resuming with no context? Find `<projeto>` by globbing
`<canal>/v*` for a folder that has `06-saida/video.mp4` but no `PUBLICAR.txt`.) Read
`<projeto>/00-plano.json` for the block list (if the plan is gone, `publicar.py` falls back to the
manifest's block functions as provisional labels), then write
`<projeto>/06-saida/publicar-input.json` (the chosen title + 3 alternates, description hook +
body, ONE chapter label per block, 3–5 hashtags, a few tags — following the YouTube best-practice
rules) and run `python scripts/publicar.py <projeto>`. It writes `<projeto>/06-saida/PUBLICAR.txt` (copy-paste ready: title, description with chapters computed from
the REAL audio timing + the credits block, tags, the synthetic-content label decision). Fix
anything it flags as `[CONFERIR]` and re-run. Write `<projeto>/CREDITOS.md` from
`<projeto>/03-clipes/creditos.json`. UPDATE THE MEMORY (at the CHANNEL root — the parent of
`<projeto>`): append this video to `<canal>/canal.json`'s `videos` and update
`<canal>/_historico.json` (palette/rhythm, for anti-template). ASK before deleting `03-clipes` + `04-cenas` (~795 MB; the
plan keeps every clip URL so it can rebuild). Never end without the honest note: *"Isto monta o
vídeo. Não garante monetização, views nem renda. O YouTube não monetiza conteúdo em molde e sem
ponto de vista — é por isso que eu exijo a sua tese antes de escrever."*

## Recurrence (why it earns the subscription)
Read `reference/roteiro.md` §loop. On a re-run in the same channel folder, ASK for the
timestamps where YouTube Studio's RELATIVE retention dipped and the CTR, map them to the saved
blocks, and rewrite the next script attacking those exact points. Use only the one official
number (CTR 2–10%); never quote a retention benchmark (none is official). Also vary palette,
cut rhythm and clip/Ken-Burns ratio between videos (`_historico.json`) — a fixed template is
the literal spam example in the policy.

## Degraded mode
- Web down (autocomplete/yt-dlp): say it in PT-BR, ask the theme directly, and flag CLEARLY
  that this video is going out WITHOUT market validation — the demand gate is the skill's main
  edge, so let the user decide whether to proceed. Never invent pauta numbers.
- edge-tts down: the health-check stops you; relay the honest error, do not proceed.
- No Pexels key: relay the tutorial; the user can also drop own clips in `03-clipes/`.
- Node/Chrome missing: skip the LOCAL thumbnail render, but STILL write
  `06-saida/prompt-chatgpt.md` — with no renderer, that package is the whole thumbnail step.
  Say so plainly and never pretend a PNG was generated.
- A render step fails: read `reference/windows.md`, fix the specific trap, retry just that
  scene (`--bloco N`) — never restart the whole render.

## Refusals (explain each with the policy link, PT-BR)
AI persona giving health/finance/legal/political advice · narration-less image slideshow ·
"gera 20 vídeos desse template" · reading someone else's material without a real added layer ·
uploading for the user · downloading music · scraping Pexels to dodge the key. Details and the
verbatim policy in `reference/politica-youtube.md`.

## Sensitive themes (generate, but WARN — not a refusal)
For true crime, tragedy, violence, or any real person/event, say plainly BEFORE generating
(read `reference/politica-youtube.md` §sensivel):
- the background is GENERIC Pexels b-roll, NEVER the real crime-scene/victim footage — the user
  must not expect real images of the event;
- graphic/shocking themes fall under advertiser restrictions (limited or no ads:
  https://support.google.com/youtube/answer/6162278);
- a realistic reconstruction of something that did NOT happen needs the synthetic-content label;
- `midia.py` already refuses an identifiable face in a crime/accusation context (Pexels license
  forbids a real person "in a bad light").
