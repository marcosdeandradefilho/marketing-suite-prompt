# windows.md — os pega-ratão do ffmpeg no Windows (já resolvidos nos scripts)

Todos foram reproduzidos numa máquina real e resolvidos DENTRO dos scripts. Este doc é pra
você diagnosticar se um render falhar, não pra reimplementar. Se um passo quebrar, ache o
sintoma aqui e conserte só a causa.

## 1. Lista de concat gravada errado (arquivo de 0 bytes, erro sobre 'file')
Sintoma: `montar.py` falha com "Impossible to open 'cena ...'" ou "unknown keyword '<BOM>file'".
Causa: no Windows, `Set-Content` grava ANSI (CP1252, quebra acento) e `Out-File -Encoding utf8`
grava COM BOM (o ffmpeg lê `<BOM>file` como keyword). Resolvido: `comum.escreve_lista_concat`
grava os bytes em UTF-8 SEM BOM, com nome RELATIVO, e o concat roda com `cwd` na pasta das cenas.
NUNCA gere a lista de concat pelo PowerShell.

## 2. Caminho do Windows dentro do filtro subtitles
Sintoma: erro que ENGANA — "Unable to parse original_size option value" (uma opção que ninguém
escreveu). Causa: os `:` de `C:\pasta` viram separador de opção do filtro. Resolvido: `cena.py`
roda o ffmpeg com `cwd` na pasta da legenda (02-legenda) e usa NOME RELATIVO (`cena-01.ass`).
Também: a legenda tem que estar SEM BOM (`legenda.py` grava sem BOM), senão o libass come os
acentos e "ação/você" viram caixinhas.

## 3. Fonte trocada em silêncio
Sintoma: o vídeo sai com uma fonte genérica, sem erro nenhum. Causa: o libass procura a fonte no
sistema; não achando, cai numa genérica calado. Resolvido: `cena.py` copia o `Anton-Regular.ttf`
(vem em `assets/fontes/`) pra `02-legenda/fontes/` e passa `fontsdir=fontes` no filtro. Se a
pasta de fontes ficar vazia, a legenda sai feia — confira que a fonte foi copiada.

## 4. concat -c copy corrompe SEM erro se as cenas forem diferentes
Sintoma: duração final errada, exit code 0, sem warning. Causa: `concat -c copy` exige streams
idênticos. Resolvido: `cena.py` normaliza TODA cena pra 1920x1080, 30fps, yuv420p e
`video_track_timescale 30000` — todas idênticas. Nunca alimente o concat com clipe cru.
Doc do concat, verbatim: "All files must have the same streams (same codecs, same time base, etc.)".

## 5. MP4 interrompido no meio fica ilegível
Sintoma: matou o render e o arquivo não abre ("moov atom not found"). Por isso o render é POR
CENA (cada cena é curta): se cair, as cenas prontas continuam válidas e você refaz só a que
faltou (`cena.py --bloco N`). O `+faststart` (moov na frente) é o último passo, em `montar.py`.

## 6. zoompan (Ken Burns) que nunca termina
Sintoma: o encode da foto trava e enche o disco. Causa: `-loop 1` + `zoompan d=300` gera frames
infinitos. Resolvido: `cena.py` usa `zoompan d=1` + `-t <dur>` + upscale antes (`scale=8000`)
pra não tremer. Nunca use `d` grande com `-loop 1`.

## 7. ffprobe com vírgula no locale pt-BR
Sintoma: durações 1000x erradas, o gate de duração aprova/reprova errado. Causa: em pt-BR o
ffprobe pode devolver "660,123". Resolvido: `comum.dur`/`sonda` fazem `.replace(",", ".")`.

## 8. Outros limites
- Caminho do projeto: MAX_PATH 260 chars; pasta em `C:\videos\<slug>` (curto, ASCII). Espaço e
  acento no caminho quebram os filtros — o Stage 0 propõe mover.
- Linha de comando do cmd tem teto de 8.191 chars: montagem de N clipes SEMPRE pela lista de
  concat, nunca com N `-i`. Os scripts já fazem assim.
- `drawtext font=Arial` derruba o ffmpeg no Windows (access violation). Por isso TODO texto vai
  pelo `.ass`/libass, nunca por `drawtext`.
- `yt-dlp` toma 429/"confirme que não é robô" depois de ~12 downloads seguidos. A busca de
  metadata (`--flat-playlist`) aguenta; não faça a pauta baixar legenda de concorrente em massa.
