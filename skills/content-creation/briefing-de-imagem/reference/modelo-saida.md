# modelo-saida.md — the artifact format to Write + what to show in chat (Step 6)

> Write ONE small file. Show the final prompt inline in chat too. All PT-BR, anti-guru.
> No quota/price NUMBERS anywhere. No hype. The prompt goes in a fenced code block so the
> user can copy it in one tap.

## Output path
`.claude/briefings-imagem/AAAA-MM-DD-<slug>.md` (today's date; `<slug>` = 3-5 kebab words from
the idea). Create the folder if it doesn't exist. Before writing, Glob the folder for a prior
briefing on a similar idea; if found, Read it and add a short "o que mudou / variação nova"
note instead of reprinting from scratch.

## File template (fill it; keep it tight)

```markdown
# Briefing de imagem — <título curto da ideia>
data: AAAA-MM-DD · destino: <feed 1:1 / story 9:16 / wallpaper 16:9 / etc>

## 1. Briefing visual
- **Uso:** <post / anúncio / thumbnail / wallpaper / logo ...>
- **Assunto:** <quem/o quê, específico>
- **Ação/cena:** <o que acontece, onde>
- **Estilo:** <foto realista / ilustração / 3D ...>  ·  **Clima:** <sério / divertido ...>
- **Luz:** <golden hour / luz suave / contraluz ...>
- **Enquadramento:** <plano aberto / close ...>  ·  **Ângulo/câmera:** <de baixo / atrás por cima / nível dos olhos>
- **Profundidade:** <fundo desfocado / tudo em foco>
- **Paleta:** <tons quentes / teal e laranja / paleta natural ...>
- **Proporção:** <1:1 / 4:5 / 9:16 / 16:9>
- **Texto na imagem:** <"PALAVRAS EXATAS" + fonte/contraste, ou "sem texto"> (vai no prompt, nunca no rascunho)
- **Evitar:** <o que NÃO quer — traduzido em positivo no prompt>

## 2. Rascunho visual
- **Arquivo:** `AAAA-MM-DD-<slug>.png` (anexa esse no gerador junto com sua foto)
- **Legenda (o quadro não tem texto de propósito):** <o degradê X é o céu; a silhueta escura na
  frente é <sujeito>; o bloco Y no fundo é <elemento>; ...> — cada cor/posição = um elemento.
- **Câmera:** <de lado / atrás por cima / aérea / contra-plongée> — o rascunho está montado nessa
  perspectiva; a câmera exata está no prompt.

> A posição é uma sugestão forte, não milímetro. Se o gerador trocar algo de lugar, peça pra ele
> mover só aquilo e manter o resto — assim você não gasta outra geração. O rascunho marca ONDE e
> QUÃO GRANDE fica cada coisa; a forma e o rosto reais vêm do prompt + da sua foto.

(Se não deu pra renderizar o PNG aqui: no lugar do arquivo, entra a planta em texto — e diga isso.)

## 3. Prompt pronto (EN) — cola no gerador
O prompt vai em INGLÊS (o gerador obedece melhor). Texto que aparece DENTRO da imagem fica literal em
PT entre "aspas". Estrutura de 10 campos (ver `prompt-expert.md`), denso em substantivos, ~30–75 palavras.

​```
<English expert prompt: photorealistic [shot] of [subject], [action], [setting]. [light] [camera/lens].
[anti-slop texture] [palette] [composition + camera angle]. [positive constraints]. [aspect ratio].
— se tem rosto: + identity-lock + RELIGHT lines; se não tem foto mas tem pessoa: + character DNA block;
— texto na imagem: "PALAVRAS EXATAS EM PT">
​```

## 4. O que o prompt diz (PT)
<2–4 linhas explicando em português o que cada parte faz, pra você entender e editar. Ex.: "pedi foto
realista, câmera baixa heroica, luz do fogo iluminando teu rosto, paleta teal/laranja, pele com poros
(pra não ficar 'cara de IA'), e mandei manter teu rosto exato e re-iluminar ele pela cena.">

## 5. Qual gerador usar (pro SEU caso)
<roteamento por trabalho, 1-2 linhas. Ex.: "Teu rosto na cena → ChatGPT (hoje segura melhor o rosto de
foto). Wallpaper 16:9 exato → Nano Banana/Gemini (o ChatGPT corta pra 3:2). Texto na imagem → Nano
Banana Pro.">

## 6. Como anexar + integrar o rosto
- **Rascunho (Imagem 1):** *"usa SÓ como composição/enquadramento; não copia o traço nem as cores, e não
  escreve nenhum texto que aparecer nele; mantém a paleta [X]."*
- **Sua foto (Imagem 2) — só se tem rosto/produto real:** *"é essa pessoa: mantém o rosto exato E
  RE-ILUMINA ele pela luz da cena (temperatura de cor, exposição, grão), com sombras reais — pra não
  ficar colado."* Sem foto pessoal (cena genérica): anexa só o rascunho.
- **Foto de referência (se é seu rosto):** manda 3–6 fotos nítidas, uma no MESMO ângulo da pose (ex.: 3/4),
  luz de dia, sem filtro — NÃO só a foto de documento frontal (é o que faz o rosto colar).

**Ajuste por gerador:** <ChatGPT: 1:1/3:2/2:3 nativo (16:9 corta) · Nano Banana/Gemini: 16:9/9:16 real, Pro pra texto, "não muda a proporção" em edição>

**Se sair quase certo:** não gera tudo de novo. Pede pra mudar SÓ o errado ("keep the face identical,
change only X" / "muda só X, mantém o resto"). Cota grátis é curta e cada tentativa do zero gasta um slot.
```

## What to show in chat (besides the file) — ALWAYS, every run
- The 1-line soft read-back at the top (Step 1).
- The **rascunho**: the PNG path they can open + the **legend** keying the label-free image (or, in
  degraded mode, the ASCII planta + the honest "não deu pra renderizar aqui" line).
- The **English prompt** inline in a fenced code block (so they copy without opening the file).
- The **PT gloss** ("o que o prompt diz") under it, so a layperson gets it.
- **Qual gerador usar** (routing for their job) + **como anexar + integrar o rosto** (attach + relight +,
  if a face, the reference-photo coaching) + the "ajuste por gerador" + the "se sair quase certo" tip.
- One line: where the file (+ PNG) was saved + that they can reabrir/editar.
- The handoff line (Step 7).

**Re-run / variação:** even when a prior briefing exists and this is a variation, you STILL render a
fresh rascunho + show the legend + the full prompt inline in chat. Add a short "o que mudou" note, but
NEVER reduce the turn to only "salvei a variação" — the user must be able to see the new rascunho and
copy the new prompt without opening a file.

## Tone lints before you finish (self-check)
- Output is PT-BR end to end. No bare `$` (only R$ / US$ if money ever appears — it usually won't).
- No time estimate, no income/views promise, no hype adjective ("incrível", "impressionante").
- No hardcoded quota/price number. The quota line is qualitative only.
- Every model name you stated is from `geradores.md` or a fresh WebFetch — not invented.
- The blueprint never promises precise placement.
