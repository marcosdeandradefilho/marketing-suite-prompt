<!--
  Molde do pacote "gera a thumb no ChatGPT". O SKILL.md copia este arquivo pra
  <projeto>/06-saida/prompt-chatgpt.md preenchendo os placeholders.

  Placeholders:
    {{TITULO_VIDEO}}  titulo do video (so pra pessoa se situar)
    {{ARQUETIPO}}     "A (a imagem manda)" ou "B (o texto manda)"
    {{CENA}}          descricao da cena em INGLES, densa em substantivo
    {{SUJEITO}}       o assunto unico da imagem, em INGLES
    {{LINHAS}}        as linhas da manchete em PT-BR, uma por item, formato:
                      - Line 1: exact text "ENVERGONHE" ... (ver molde abaixo)
    {{ACENTO_EN}}     nome da cor de acento em ingles (ex: "saturated golden yellow")
    {{MARCA_EN}}      a marca de anotacao em ingles, ou a linha inteira apagada
    {{TEXTO_PT}}      a manchete inteira em PT, pra pessoa conferir letra por letra
  Regra: o PROMPT vai em INGLES (o gerador obedece melhor), o TEXTO DA THUMB vai em
  PORTUGUES entre aspas. Tudo que a pessoa le, em PT-BR.
-->

# Gerar esta thumbnail no ChatGPT

Video: {{TITULO_VIDEO}}
Arquetipo: {{ARQUETIPO}}

A skill ja gerou a thumb aqui do lado (thumbnail.png). Este arquivo e a SEGUNDA opcao:
cola o bloco abaixo no ChatGPT, gera la, e compara com a que saiu aqui. Fica com a melhor.

Por que existe: o ChatGPT hoje escreve texto dentro da imagem muito melhor do que escrevia,
e resolve cena que foto de banco de imagem nao tem. O que ele nao faz e garantir acento em
portugues. Por isso tem o passo de conferencia embaixo.

--------------------------------------------------------------------------------
O PROMPT (copia daqui ate a linha de baixo e cola no ChatGPT)
--------------------------------------------------------------------------------

Create a YouTube thumbnail. Aspect ratio 16:9, landscape, 1280x720.

Scene: {{CENA}}
Single subject: {{SUJEITO}}. One subject only. Nothing else competing for attention.

Composition:
- Subject placed on a rule-of-thirds line, never dead center.
- Text block occupies the opposite half of the frame.
- Keep the bottom-right corner completely empty (YouTube prints the duration badge there).
- Keep a 5% safe margin on all sides. Nothing important touches the edge.

Lighting and palette: dark, cinematic, high contrast. Deep near-black background,
one warm key light on the subject. Maximum 3 colors in the whole image.

Typography:
{{LINHAS}}
- All headline text in UPPERCASE, bold condensed sans-serif, very heavy weight, tight
  tracking, thin black outline plus a soft dark shadow so it stays readable over the photo.
- The headline must occupy 50 to 70 percent of the frame height.
- Render the text EXACTLY as written between the quotes, character by character, including
  every Portuguese accent mark (a-tilde, c-cedilla, e-circumflex, a-acute). Do not translate,
  do not rephrase, do not fix, do not shorten.
{{MARCA_EN}}

Do not include: any other text anywhere in the image, no watermark, no logo, no signature,
no caption, no subtitle, no UI elements, no borders or card corners, no purple gradient,
no collage of several scenes, no text touching or crossing the frame edge.

Style: photographic, realistic, filmic grain, natural imperfection. Not a 3D render,
not a vector illustration, not stock-photo clean.

--------------------------------------------------------------------------------
CONFERE ISTO QUANDO A IMAGEM VOLTAR (nesta ordem)
--------------------------------------------------------------------------------

1. ACENTO. Le a manchete letra por letra e compara com esta:
   {{TEXTO_PT}}
   E o erro mais comum. Til que virou traco, cedilha que sumiu, letra trocada no meio da
   palavra. Se errou, responde no mesmo chat: corrige so a palavra errada, uma de cada vez.
   Errou duas vezes seguidas, vai pro plano B la embaixo.

2. TEXTO CORTADO. Nenhuma letra pode encostar na borda. Se cortou, responde:
   "Keep all text fully inside the frame with padding on all sides."

3. CANTO INFERIOR DIREITO. Tem que estar vazio. E onde o YouTube carimba a duracao.

4. PROPORCAO. Se nao veio 16:9, corta sem perder qualidade:
   ffmpeg -i entrada.png -vf "crop=iw:iw*9/16" -y thumbnail.png

5. TESTE DOS 160px. Diminui a imagem ate ficar do tamanho de uma unha de dedo. Se nao der
   pra ler a manchete e reconhecer o assunto, o problema nao e a imagem: e palavra demais
   ou assunto demais. Corta e gera de novo.

--------------------------------------------------------------------------------
PLANO B (quando o acento nao para de errar, ou o ChatGPT recusa a cena)
--------------------------------------------------------------------------------

Pede a MESMA imagem sem nenhum texto:

  Same image, but with no text at all. Leave the left half clean and dark, with nothing
  written on it.

Salva o PNG e me avisa. Eu asso a manchete por cima no template daqui, que controla o texto
no pixel e nunca erra acento. Voce fica com a cena do ChatGPT e o texto certo.

Se a recusa for por causa de pessoa real: nao insista. Descreve a pessoa em vez de nomear
("a man in his nineties in a dark suit, investor") ou usa uma foto real de imprensa como
fundo e pede so o tratamento.
