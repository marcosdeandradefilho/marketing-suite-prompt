# roteiro.md — como o vídeo não sai genérico

O que faz um canal dark crescer não é a ferramenta, é o ROTEIRO e o PACKAGING. Um vídeo de IA
fracassa por defeitos concretos: voz monótona, b-roll desconexo, roteiro genérico, thumb ruim,
título sem curiosidade, ritmo constante. Cada regra abaixo ataca um desses.

## §pauta — medir a demanda antes de produzir (Stage 1)

Ninguém no mercado de "canal dark" mede pauta; todo mundo só produz. Isto é o primeiro
diferencial da skill.

Quando o usuário NÃO traz tema, a skill SUGERE: acha canais parecidos que estouraram e os temas
que bombaram (`scripts/pauta.py` — método e apresentação em `canal.md`). O que está abaixo é o
outro caminho: o usuário JÁ traz um tema e a skill mede a demanda DELE antes de produzir.

1. Autocomplete real do YouTube (WebFetch, sem chave, testado ao vivo HTTP 200):
   `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=pt-BR&q=<termo>`
   → 10 a 30 variações reais que as pessoas digitam.
2. Pra cada variação: `yt-dlp --flat-playlist "ytsearch15:<termo>"`, depois metadata nos 3
   melhores (`view_count`, `upload_date`, `channel_follower_count`).
3. Dois números por vídeo: views/dia desde a publicação, e o multiplicador de outlier
   (views do vídeo ÷ inscritos do canal). Multiplicador ≥3 = o tema puxa além da base do canal.
4. BARRA DE APROVAÇÃO: precisa de ≥1 vídeo com multiplicador ≥3 publicado nos últimos 12 meses.
   Sem isso, diga "esse tema não tem demanda medida" e ofereça os 3 termos vizinhos melhores.
5. Cacheie em disco. Não martele o endpoint (o yt-dlp toma 429 e "confirme que não é robô"
   depois de ~12 chamadas seguidas — a busca de metadata aguenta, a de legenda não).

## §packaging — título e thumb ANTES do roteiro (Stage 3)

Inversão em relação ao fluxo n8n concorrente, que faz título/thumb no fim. Documento vazado
atribuído à MrBeast Production, verbatim: "THIS IS WHY YOU MUST KNOW THE TITLE AND THUMBNAILS
OF THE VIDEOS YOU ARE MAKING!" (https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/
— documento vazado, não oficial; não cite pro usuário como doutrina).

Padrão MEDIDO em 160 vídeos de canal dark PT-BR (yt-dlp, 2026-07): 55–60 caracteres de título
(mediana 58), 46% com número, só 6% com interrogação, 49% com 2+ palavras em CAIXA ALTA, 31%
usando o separador "|". Palavras que mais aparecem: mistérios, ninguém, contou, relatos, reais,
fatos, inexplicáveis. Gere 10 títulos nesse padrão + 3 conceitos de thumb, e o usuário escolhe
1 + 1. Depois o roteiro é escrito pra PAGAR aquela promessa; se não paga, muda o título.

## §roteiro — blocos com função declarada (Stage 4)

Não é "escreva um roteiro sobre X". É um JSON de blocos, cada um com função. Duração alvo v1:
10 a 14 min de áudio (mediana do nicho em PT-BR é 36,9 min, mas v1 fica menor por custo de voz
e render; o `_estado`/plano já aguenta ir além).

Piso de 8 minutos é DURO: mid-roll (anúncio no meio) só existe a partir daí. Verbatim:
"On monetized videos that are 8 minutes or longer, you can turn on ads during the middle of the
video (known as mid-rolls)" (https://support.google.com/youtube/answer/6175006).

Blocos obrigatórios:
- 0:00–0:30 GANCHO. Entrega literalmente o que a thumb prometeu. PROIBIDO: "neste vídeo",
  "hoje eu vou", "antes de começar", "se inscreva", "bem-vindo". O YouTube mede esse intervalo
  sozinho: "Intro tells you what percentage of your audience still watched your video after the
  first 30 seconds" (https://support.google.com/youtube/answer/9314415).
- 0:30–1:00 PROMESSA + LOOP ABERTO (uma pergunta que só fecha lá na frente).
- 1:00–3:00 PAYOFF RÁPIDO, muita troca de cena.
- ~3:00 RE-ENGAJAMENTO 1. ~6:00 RE-ENGAJAMENTO 2 (memo MrBeast: "Once you have someone for 6
  minutes they are super invested").
- daí em diante: blocos de 3–4 min, cada um fechando um mini-loop e abrindo o próximo.
- FECHO curto: loop fechado + a tese do usuário. Sem recap longo, sem pedido arrastado de inscrição.

VALIDADOR but/therefore (Trey Parker, verbatim: "What should happen between every beat is the
word therefore or but"): entre dois blocos tem que caber "mas" ou "portanto", nunca "e aí"/"além
disso"/"também". Se só couber conector aditivo, o roteiro é uma lista, não uma história —
reescreva. Dá pra checar por regex de conector nas junções.

CAMPO OBRIGATÓRIO DE ÂNGULO: a tese do usuário (Stage 2) aparece, com as palavras dele, em ≥2
blocos. Sem tese, não gere (é requisito da política, ver `politica-youtube.md`).

## §thumb — a miniatura (Stage 11)

A miniatura tem referência própria: `thumbnail.md` (os 2 arquétipos, as 11 leis medidas, as 7
fórmulas de copy, os 7 layouts, o passo OBRIGATÓRIO de reduzir a foto pra 1280px antes de
renderizar, o render `--multi` e o pacote de prompt pro ChatGPT). Regra-mãe: decida o ARQUÉTIPO
antes do layout — A (a imagem manda: 0–4 palavras, às vezes zero) ou B (o texto manda: 5–9
palavras em 3–5 linhas). NÃO existe teto universal de 4 palavras. Texto GRANDE, contraste
extremo (scrim + vinheta + stroke 3px que mantém o acento limpo), UMA cor de acento fixa no
canal (#f2c230 amarelo ou #e8804f brasa) caindo na PUNCHLINE, manchete à ESQUERDA, canto
inferior direito livre, no máximo UMA marca de anotação (seta/círculo). O `{{TITULO}}` é COPY
com fórmula, não o título do vídeo repetido.

## §loop — por que roda de novo (recorrência)

Depois do vídeo publicado, o usuário volta e roda a skill no mesmo canal. Pergunte:
- os timestamps onde a RETENÇÃO RELATIVA do YouTube Studio ficou abaixo da média;
- o CTR do vídeo.
Mapeie esses timestamps nos blocos salvos e reescreva o próximo roteiro atacando aqueles pontos.
Use SÓ o número oficial que existe (CTR): "Half of all channels and videos on YouTube have an
impressions CTR that can range between 2% and 10%" (https://support.google.com/youtube/answer/7628154).
NUNCA cite benchmark de retenção percentual — não existe número oficial, os que circulam são de
fornecedor de analytics e se contradizem.

ANTI-TEMPLATE entre vídeos: varie paleta, ritmo de corte, tipo de transição e proporção
clipe/Ken-Burns entre execuções (registre em `_historico.json`). Repetir o mesmo molde é o
exemplo LITERAL de spam na política ("the exact same background music and repetitive AI
generated imagery across many videos, with each video reading out an AI-generated script",
https://support.google.com/youtube/answer/2801973).
