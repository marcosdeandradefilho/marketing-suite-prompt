# pipeline.md — a ordem técnica, os arquivos, e cada chamada de script

Tudo roda LOCAL, com ffmpeg. Nada de Remotion (medido: ffmpeg é ~23x mais rápido pra
long-form, e o Remotion tem trava de licença acima de 3 funcionários). Cada CENA é um
arquivo pronto e conferível, então o trabalho é retomável e a montagem final é instantânea.

## §0 — Recon e ambiente (Stage 0 do SKILL.md)

Confira e instale o que faltar (narre em PT-BR, sem jargão de ferramenta):
- `ffmpeg -version` e `ffprobe -version`. Faltando → `winget install Gyan.FFmpeg` (Windows,
  build FULL), `brew install ffmpeg` (Mac), `apt install ffmpeg` (Linux). A variável PATH só
  aparece num terminal NOVO — se acabou de instalar, o passo seguinte pode não achar; avise.
  [VERMELHO] Nunca empacote o ffmpeg.exe dentro da skill: o build do Gyan é GPLv3 e embarcar
  o binário herda obrigação de código-fonte. A skill INSTALA via winget, não redistribui.
- `python --version` (3.9 a 3.13) e `pip`. Depois `pip install edge-tts` (versão pinada, ver
  requirements). No Windows use `py -3` se `python` não existir.
- `node --version` (≥21, só pro thumbnail — usa fetch/WebSocket globais).
- `yt-dlp --version` (pauta). Já é dependência de outras skills do pack.
- Disco: um vídeo de 10 min gera ~1,5–2 GB de intermediários. A pasta `03-clipes` engordou
  ~2,5x na v1.3.0 (o bloco agora baixa vários clipes + fotos em vez de um clipe só): medido
  ~35 MB por bloco. Abaixo de 6 GB livres, avise e pergunte.
- Caminho do projeto: se tiver espaço, acento ou passar de ~180 chars, PROPONHA mover pra
  `C:\videos\<slug>`. Caminho sujo quebra o filtro de legenda e a lista de concat (ver
  `windows.md`). O slug do projeto é ASCII, minúsculo, com hífen.

## §plano — o contrato de dados (`00-plano.json`)

Tudo gira em torno deste arquivo. Você (o Claude) escreve ele no Stage 4.

```json
{
  "titulo": "O caso que o FBI fechou por 40 anos",
  "idioma": "pt-BR",
  "voz": "pt-BR-AntonioNeural",
  "tese": "a frase do usuário, verbatim",
  "blocos": [
    {
      "id": 1,
      "funcao": "gancho",
      "termos_busca": [
        "dark abandoned archive room cinematic",
        "dusty shelves old documents low light",
        "single lamp empty corridor night"
      ],
      "frases": [
        {"texto": "Primeira frase falada."},
        {"texto": "Segunda frase."}
      ]
    }
  ]
}
```

Regras do plano:
- `termos_busca`: **TRÊS termos em INGLÊS por bloco** (o acervo do Pexels responde muito melhor
  em inglês, mesmo com roteiro em PT-BR). Três porque o bloco é coberto por vários planos
  diferentes e um termo só devolve sempre a mesma cara. Termo CONCRETO e preso à época/lugar
  (`assyrian palace stone relief lamassu`, não `ancient history`) — termo vago foi exatamente
  como a versão antiga colocou pirâmide mesoamericana num vídeo sobre Nínive. Continua sendo
  por BLOCO, nunca por frase. (`termo_busca` no singular ainda funciona, pra plano antigo.)
- Uma `frase` = uma cartela de fala = uma unidade de tempo medida. Frase curta legenda melhor.
- `voz`: `pt-BR-AntonioNeural` (masc.) ou `pt-BR-FranciscaNeural` (fem.). Escolha pela cara
  do canal; deixe o usuário trocar.

## §fluxo — a ordem dos scripts (cada um lê o disco, escreve o disco)

Rode nesta ordem. Cada script é idempotente: rodar de novo pula o que já está pronto e válido.

```
<canal>/             pasta do CANAL: canal.json, _historico.json, pexels-key.txt, pauta-cache.json
                     (o perfil/memória e a sugestão de tema — ver canal.md)
  <projeto>/         uma subpasta POR VÍDEO (v01-..., v02-...). É o <projeto> que os scripts recebem.
    00-plano.json    você escreve (Stage 4)
    00-roteiro.md    você escreve, texto puro (Stage 4)
    01-voz/          voz.py    -> b{BB}-f{FF}.wav, narracao.wav, manifest.json
    02-legenda/      legenda.py-> cena-{BB}.ass  (+ fontes/ copiada por cena.py)
    03-clipes/       midia.py  -> b{BB}-v{NN}.mp4 + b{BB}-f{NN}.jpg (varios por bloco),
                     midia.json (o plano de midia), creditos.json, contato.png (o gate visual)
    04-cenas/        cena.py   -> cena-{BB}.mp4  (mudo, legenda queimada)
    05-audio/        audio.py  -> mix.m4a   (musica/ é onde o usuário põe mp3, opcional)
    06-saida/        montar.py -> video.mp4 ; thumb.js -> thumbnail.png ; vertical.py -> vertical.mp4
                     publicar-input.json (você escreve) -> publicar.py -> PUBLICAR.txt
    CREDITOS.md      você escreve a partir de 03-clipes/creditos.json
```
A chave `pexels-key.txt` pode ficar na RAIZ do canal (serve todos os vídeos) ou dentro do
vídeo — o midia.py acha nos dois lugares (e no env `PEXELS_API_KEY`).

Chamadas (a partir da pasta da skill; `<projeto>` é o caminho absoluto da pasta do vídeo):
0. (Stage 1, sugestão de tema — opcional) `python scripts/pauta.py <canal> --idioma <idioma>`. Ver canal.md.
1. `python scripts/voz.py <projeto>/00-plano.json <projeto>`
2. `python scripts/legenda.py <projeto>`
3. `python scripts/midia.py <projeto>/00-plano.json <projeto>` [`--video-pct 75` `--seg 8`]
   -> depois LEIA `03-clipes/contato.png` e reprove o que nao combina:
   `python scripts/midia.py <projeto>/00-plano.json <projeto> --rejeitar b04-f02.jpg,b12-v02.mp4`
4. `python scripts/cena.py <projeto>` (ou `--bloco N` pra refazer uma só)
5. `python scripts/audio.py <projeto>`
6. `python scripts/montar.py <projeto>`
7. (Stage 11, thumbnail) decida o arquétipo, reduza a foto (`ffmpeg -i <foto> -vf scale=1280:-1 -q:v 3 <foto-sm.jpg>`),
   preencha o template e `node scripts/thumb.js --multi <a.html> <a.png> [<b.html> <b.png>]`.
   Depois copie `assets/thumb/prompt-chatgpt.md` pra `<projeto>/06-saida/prompt-chatgpt.md` e
   preencha (a 2ª opção de thumb, gerada no ChatGPT). Ver thumbnail.md.
8. `python scripts/vertical.py <projeto>/06-saida/video.mp4 <projeto>/06-saida/vertical.mp4 <ini> <dur>`
9. (Stage 13) você escreve `<projeto>/06-saida/publicar-input.json` e roda `python scripts/publicar.py <projeto>`. Ver publicacao.md.

## §resume — retomada (o checkpoint nativo do Claude Code NÃO cobre isto)

O checkpoint do Claude Code só desfaz edições de arquivo feitas pelas ferramentas dele; NADA
que o ffmpeg criou é rastreado. Então o estado é o próprio disco:
- `voz.py` pula frase cujo `.wav` já existe e mede > 0,05s.
- `cena.py` pula cena cujo MP4 já abre e bate a duração esperada (tolerância 0,15s).
- `midia.py` completa o bloco até cobrir a duração dele; bloco já coberto sai como cache.
  `--rejeitar` apaga o arquivo, bane o id e o NOME no `rejeitados.json` e busca outro.
Se um passo cair, rode o mesmo comando de novo: ele continua de onde parou.

## §ffmpeg — a especificação de saída pro YouTube

Os scripts já usam estes parâmetros (em `comum.py`, `V_ARGS`/`A_ARGS`). Vêm da doc oficial de
upload, verbatim: "H.264", "High Profile", "2 consecutive B frames", "Closed GOP. GOP of half
the frame rate", "AAC-LC", "Sample rate: 48kHz", "MP4 with moov atom at the front (Fast Start)"
(https://support.google.com/youtube/answer/1722171).
[CONFERIR] O encoder AAC nativo do ffmpeg satura em ~256 kbps; não alcança os 384 kbps que o
YouTube recomenda. Escrevemos 256k e não mentimos que é 384. Áudio sempre estéreo 48kHz.

## §vertical — o corte 9:16

Master é 1080p, então cortar 9:16 viraria upscale. `vertical.py` usa fundo desfocado (o próprio
frame borrado atrás + o vídeo centralizado por cima), mantendo a legenda já queimada legível.
[VERMELHO] O corte NÃO é um pedaço aleatório: você escolhe e REESCREVE o trecho com gancho
próprio de até 3s. Política de Shorts não paga "compilations with no original content added"
(https://support.google.com/youtube/answer/12504220). Limite: 3 min, 1080p.

## §disco — limpeza

Depois de entregar, pergunte se pode apagar `03-clipes` + `04-cenas` (~1,3 GB por vídeo de
13 min: ~35 MB de mídia por bloco + as cenas renderizadas). O plano guarda a URL de cada clipe (`creditos.json`), então dá pra rebaixar
sem perder nada. `06-saida` (o que interessa) fica.
