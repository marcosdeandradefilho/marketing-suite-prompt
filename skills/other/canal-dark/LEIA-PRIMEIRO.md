# Canal Dark — leia primeiro

Esta skill monta um vídeo narrado longo pro YouTube do começo ao fim, sem você aparecer na
câmera. Você dá o tema e a SUA opinião sobre ele; ela escreve o roteiro, faz a narração, a
legenda sincronizada, busca os vídeos de fundo, monta a miniatura e renderiza o MP4 pronto,
mais um corte vertical pro Shorts. Você só sobe no YouTube.

## O que ela faz por você (antes e depois)

Sem a skill: você pede um roteiro pro Claude, ele te dá um texto, e o trabalho pesado continua
todo na sua mão (gravar voz, achar clipe, cortar, legendar, montar, fazer thumb).

Com a skill: sai uma pasta com o vídeo montado (`06-saida/video.mp4`), o corte vertical, a
miniatura, o `PUBLICAR.txt` com título, descrição, capítulos e créditos prontos pra colar, e o
`CREDITOS.md`. Você arrasta o vídeo no YouTube Studio, cola os textos e publica.

## As imagens de fundo trocam sozinhas dentro do bloco

Cada trecho do vídeo é montado como uma sequência de planos de uns 8 segundos, não como um
clipe só rodando em loop. A skill baixa vários vídeos e algumas fotos por trecho, e mistura
os dois (mais ou menos 75% vídeo, 25% foto — dá pra mudar). Foto nunca entra parada: sempre
com zoom ou travelling, alternando o movimento pra duas seguidas não ficarem iguais.

Antes de renderizar, a skill monta uma folha de contato com um quadro de cada arquivo baixado
e OLHA um por um, jogando fora o que não combina com o assunto (gente moderna, prédio moderno,
civilização errada) e buscando outro no lugar. Se você achar que sobrou alguma imagem ruim, é
só falar qual e ela troca.

## A miniatura vem em DUAS opções

A skill monta a miniatura aqui na sua máquina (`06-saida/thumbnail.png`) e, junto, escreve um
`06-saida/prompt-chatgpt.md`: um prompt pronto pra você copiar e colar no ChatGPT e gerar a
mesma miniatura lá. Aí você compara as duas e fica com a melhor.

Existe porque o ChatGPT hoje escreve texto dentro da imagem muito melhor do que escrevia, e
monta cena que foto de banco de imagem não tem. O que ele ainda erra é ACENTO em português
(til, cedilha, acento agudo). Por isso o arquivo já vem com o passo de conferir letra por
letra e com o plano B: pedir a imagem sem texto no ChatGPT e deixar a skill escrever a
manchete por cima, que aqui o texto sai certo sempre.

O desenho da miniatura não é chute: as regras vieram de uma medição de vídeos que estouraram
comparados com os vídeos medianos do MESMO canal, pra isolar o que fez a diferença.

## Honestidade primeiro (importante)

- Esta skill NÃO é como as outras do pack no quesito "não configura nada". Ela precisa de UMA
  coisa sua: uma chave gratuita do Pexels (o banco de vídeos de fundo). É de graça, sem cartão,
  leva 2 minutos, e o passo a passo está aqui embaixo.
- Ela instala sozinha o que precisa (o ffmpeg pra montar o vídeo e o edge-tts pra voz) na
  primeira vez.
- Ela NÃO sobe o vídeo no YouTube por você (o YouTube trava vídeo enviado por robô não
  auditado). Ela deixa tudo pronto e você arrasta no Studio — é um clique e publica na hora.
- Ela NÃO promete que você vai ganhar dinheiro, nem quantas views vai ter. O YouTube não
  monetiza vídeo feito em molde, sem a sua opinião dentro. É por isso que a skill EXIGE a sua
  tese antes de escrever qualquer coisa. Ela monta o vídeo bem feito; o resto é o mercado.
- A voz usa o edge-tts (a voz do "ler em voz alta" do Edge). É grátis e natural, mas é um
  serviço que às vezes sai do ar. Se sair no momento em que você for gerar, a skill avisa com
  todas as letras e você tenta mais tarde — ela não entrega um vídeo com áudio quebrado.

## Como instalar a skill

Copie a pasta `canal-dark` inteira pra dentro da sua pasta de skills do Claude Code:

- Windows: `C:\Users\SEU-NOME\.claude\skills\`
- Mac/Linux: `~/.claude/skills/`

No Windows a skill foi testada; no Mac/Linux a montagem e a legenda funcionam igual, mas a voz
e a miniatura não foram testadas fora do Windows — se algo não sair, me avise.

## Como pegar a chave do Pexels (2 minutos, de graça)

1. Abra `https://www.pexels.com/api/` no navegador.
2. Clique em "Get Started" e faça login (ou crie a conta, é grátis).
3. Diga pra que é (pode ser "vídeos pro meu canal") e aceite os termos.
4. A chave (uma linha de letras e números) aparece na hora.
5. Copie essa chave e cole num arquivo de texto chamado `pexels-key.txt` dentro da pasta do seu
   projeto de vídeo. Só a chave, nada mais.

Pronto. A skill acha a chave sozinha a partir daí. (Se preferir, dá pra pôr numa variável de
ambiente `PEXELS_API_KEY` — mas o arquivo é o jeito mais simples.)

## Como usar

Digite `/canal-dark` ou fale naturalmente:
- "cria um canal dark de mistérios em português"
- "monta um vídeo narrado de 12 minutos sobre o Império Romano"
- "faz um vídeo pro youtube sem eu aparecer sobre casos não resolvidos"

Na primeira vez ela pergunta sobre o seu canal (o nicho, o idioma, algum canal pra se espelhar)
e guarda isso — nas próximas já sabe. Depois ela te pergunta o tema; se você não tiver um, ela
procura o que está bombando em canais parecidos e te sugere, e você escolhe. Aí pede a SUA tese,
te mostra títulos e ideias de miniatura pra escolher, e o roteiro pra aprovar ANTES de gastar
tempo montando. No fim, além do vídeo, ela te entrega título, descrição e capítulos prontos pra
colar no YouTube.

## Por que rodar de novo

A cada vídeo novo. E tem um motivo mais esperto: depois que um vídeo seu roda, você volta com os
pontos onde as pessoas largaram o vídeo (a retenção do YouTube Studio) e o CTR, e a skill
reescreve o próximo roteiro atacando exatamente aqueles pontos. Ela também varia o visual entre
os vídeos de propósito — repetir o mesmo molde é o que derruba canal dark.

## Depois

Vídeo pronto e no ar? Um trecho bom vira Short (a skill faz o corte vertical). Pra divulgar,
`/carrossel` monta um post pro Instagram sobre o tema do vídeo.
