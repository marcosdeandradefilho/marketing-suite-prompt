# canal.md — a memória do canal e a sugestão de tema

Um canal dark não é UM vídeo — é uma esteira. Na primeira vez a skill pergunta quem é o
canal e GRAVA isso; nas próximas ela já sabe e vai direto ao ponto. E quando o usuário não
tem tema, ela vai atrás do que está estourando em canais parecidos e sugere.

## A pasta do canal (uma pasta por canal, um vídeo por subpasta)

```
C:\videos\<canal-slug>\
  canal.json          <- o PERFIL do canal (a memória). Fica na RAIZ do canal.
  _historico.json     <- o que ja foi feito (anti-template + retencao); ver roteiro.md §loop
  pexels-key.txt      <- a chave do Pexels (serve todos os videos do canal)
  pauta-cache.json    <- ultima sugestao de tema (pauta.py)
  v01-<slug>\         <- UM video (aqui dentro moram 00-plano.json, 01-voz, ... 06-saida)
  v02-<slug>\
```

O `<projeto>` que os outros scripts recebem é a subpasta do VÍDEO (`v01-...`), não a raiz do
canal. A raiz do canal guarda só o perfil, o histórico, a chave e o cache de pauta.

## canal.json — o perfil (a memória)

```json
{
  "nome": "Estoico Diario",
  "slug": "estoico-diario",
  "nicho": "estoicismo e filosofia pratica",
  "idioma": "pt-BR",
  "voz": "pt-BR-AntonioNeural",
  "canais_referencia": ["https://www.youtube.com/@DailyStoic"],
  "estilo": "reflexivo, cinematografico, tom calmo",
  "criado_em": "2026-07-24",
  "videos": []
}
```

`videos` é preenchido no Stage 13 a cada vídeo entregue: `{slug, titulo, tema, data}`.

## Stage 0.5 — Perfil (primeira vez pergunta; depois só carrega)

Procure `canal.json` na raiz da pasta do canal.

- **NÃO existe (primeira vez):** faça o onboarding com AskUserQuestion, UMA pergunta por vez:
  1. **Nicho.** Ofereça opções com dica (quem não sabe, escolhe daqui): `estoicismo / filosofia`,
     `curiosidades e fatos`, `motivação e mentalidade`, `histórias de terror / creepypasta`,
     `mistérios e casos reais`, `história`, `ciência e espaço`, `Outro`. Se cair em terror/true
     crime/tragédia, dispare o aviso de temas sensíveis (ver `politica-youtube.md §sensivel`)
     ANTES de seguir.
  2. **Idioma.** `Português (Brasil)`, `Inglês`, `Espanhol`. Diga em PT que canal em inglês
     costuma ter CPM maior, sem citar número. O idioma define a voz (mapa abaixo).
  3. **Canal(is) de referência pra se espelhar.** Texto livre (link ou @) → vai pro campo
     `canais_referencia` do perfil. Ofereça a saída "não sei, acha pra mim" — aí deixe
     `canais_referencia` vazio e o pauta.py acha os canais fortes do nicho sozinho (o `--canais`
     é só um override manual opcional, o padrão é ler do `canal.json`).
  4. **Nome do canal.** PROPONHA um nome a partir do nicho (estoicismo → "Estoico Diário") e deixe
     o usuário confirmar ou trocar. Vira o `nome` do `canal.json` e o slug ASCII da pasta do canal.
  Salve o `canal.json` na RAIZ do canal e diga, em PT-BR, que gravou o perfil e já vai saber depois.
- **Existe (voltou):** carregue e cumprimente curto em PT-BR ("Canal de estoísmo em PT, voz
  Antonio — bora o próximo?"). Pule o onboarding. Deixe o usuário trocar algo se quiser.

## Mapa idioma → voz (edge-tts, sem chave)

- `pt-BR` → `pt-BR-AntonioNeural` (masc., padrão) ou `pt-BR-FranciscaNeural` (fem.)
- `en-US` → `en-US-ChristopherNeural` (masc.) ou `en-US-AriaNeural` (fem.)
- `es-ES` → `es-ES-AlvaroNeural` · `es-MX` → `es-MX-JorgeNeural`

O padrão do pt-BR é o Antonio. O usuário pode trocar por uma voz paga
depois — isso é assunto de aula, a skill não força.

## Stage 1 — Tema: o usuário traz OU a skill sugere

Pergunte em PT-BR: *"Você já tem o tema desse vídeo, ou quer que eu procure o que está
bombando em canais parecidos e te sugira?"*

- **Traz o tema:** meça a demanda como sempre (autocomplete + outlier — ver `roteiro.md §pauta`).
- **Quer sugestão:** rode `python scripts/pauta.py <canal_dir> --idioma <idioma>` (ele lê o
  nicho e os canais de referência do `canal.json`; sem canais, descobre os fortes do nicho
  sozinho). Leia `pauta-cache.json` e MOSTRE ao usuário os temas ranqueados, cada um com o
  "por que bombou" (o multiplicador e as views). O usuário escolhe UM. Só depois disso a skill
  produz.

### Como o pauta.py acha o que estourou (método, verificado — dossiê pesquisa-temas.md)

1. Busca o nicho no YouTube (`ytsearch`) → vídeos fortes + os canais que aparecem.
2. Pega os canais mais fortes (ou os de referência do perfil).
3. Lista os uploads recentes de cada um (`--flat-playlist`, barato) e acha OUTLIER:
   **views ≥ 3× a MEDIANA do canal** (mediana, não média — um viral só não distorce).
   Faixas do vidIQ: <2x fraco, 2–5x bom, 5–10x forte, >10x viral.
4. Junta, ranqueia por multiplicador, tira repetido.

### A regra de ouro: achar demanda ≠ copiar

O pauta.py entrega o TEMA e por que ele puxou — NUNCA "copie este vídeo". O ângulo é sempre do
usuário (Stage 2). A política do YouTube (support.google.com/youtube/answer/1311392) tira a
monetização de conteúdo "reused/inauthentic" que reaproveita sem comentário original — e a
punição vale pro canal inteiro. Sugerir tema é competir num assunto provado; refazer o vídeo
do outro é o que derruba o canal.

### Cuidado de robô e degradação

- yt-dlp toma 429 ("confirme que não é robô") depois de ~12 chamadas seguidas. O pauta.py faz
  poucas (1 busca + até 5 canais). Não rode em loop; ele cacheia em `pauta-cache.json`.
- Se a web cair / vier 429 / o nicho não tiver base: o `pauta-cache.json` sai com `temas`
  vazio e um `aviso`. Aí peça o tema direto ao usuário e AVISE que o vídeo vai SEM validação de
  demanda (o portão de demanda é a maior vantagem da skill; deixe o usuário decidir seguir).
