# Briefing de Imagem — como instalar e usar

**O que essa skill faz:** você descreve do seu jeito a imagem que quer ("um cavalo com asas
usando uma camisa de time em cima de um estádio", "um post de promoção de hambúrguer", "eu em cima
de um dragão botando fogo num castelo, pra wallpaper") e ela te devolve **três coisas prontas pra
você levar pro gerador de imagem** (ChatGPT, Nano Banana, Gemini, o que você usar):

1. **Briefing visual** — todos os detalhes definidos (enquadramento, luz, cor, estilo, proporção).
2. **Rascunho visual (imagem PNG)** — ela DESENHA e RENDERIZA um rascunho da composição (onde fica
   cada coisa, a paleta, o clima, a câmera) numa imagem de verdade, pra você **anexar no gerador**
   junto com a sua foto e qualquer outra referência. É o esboço que guia o gerador a montar a cena.
3. **O prompt pronto (em inglês) + explicação em português** — o gerador obedece melhor em inglês, então
   ela escreve o prompt nível especialista em inglês e te explica em PT o que cada parte faz. Você só
   copia e cola.
4. **O manual de acerto** — QUAL gerador usar pra cada caso (rosto, texto, wallpaper 16:9), como anexar o
   rascunho + a sua foto, e — quando é o **seu rosto** — como fazer ele INTEGRAR na cena (não ficar
   "colado") e que foto mandar. É aqui que mora o valor que você não conseguiria fazer sozinho.

A ideia é simples: a cota grátis dos geradores é curta e **cada tentativa errada gasta um slot**.
Essa skill faz você chegar lá com a imagem já rascunhada, o prompt de especialista e o gerador certo.

---

## Antes x depois (o que muda)

- **Sem a skill:** você digita "faz uma imagem de um hambúrguer pra promoção" no gerador, sai
  uma foto genérica, sem o texto certo, na proporção errada pro feed — e você re-roda 6, 8 vezes
  até a cota do dia acabar.
- **Com a skill:** ela te entrega o briefing (close no hambúrguer, luz quente, fundo desfocado,
  formato 4:5 pro feed), um **rascunho em imagem** da composição pra você anexar no gerador, e um
  prompt único afinado nas boas práticas atuais do ChatGPT **e** do Nano Banana. Você anexa o
  rascunho, cola o prompt e geralmente acerta na primeira.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `briefing-de-imagem` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. **Não tem chave de API, não instala nada, não configura nada.**

> Skill instalada no usuário funciona em **qualquer projeto** que você abrir no Claude Code.

---

## Usar

Abre o Claude Code e faz **uma** das duas coisas:

- Digita o comando: **`/briefing-de-imagem`**
- Ou simplesmente fala, em português normal:
  - *"quero criar uma imagem de um cavalo com asas em cima de um estádio"*
  - *"me ajuda a fazer o prompt de uma thumbnail de YouTube sobre investimento"*
  - *"preciso de uma arte de promoção pro feed, um hambúrguer com o texto COMBO R$ 25"*
  - *"minha imagem sempre sai errada, me ajuda a descrever direito"*

Ela pode fazer 2-3 perguntas rápidas (onde vai usar, se tem texto na imagem, que estilo), e aí
te entrega o briefing + o rascunho em imagem + o prompt. O resultado aparece na tela **e** fica
salvo em `.claude/briefings-imagem/` dentro do seu projeto (o `.png` do rascunho e o `.md` com
tudo), pra você reusar depois.

> Pra renderizar o rascunho em imagem, a skill usa um navegador que você já tem (Chrome ou Edge) e
> o Node. Se não tiver, ela avisa e entrega a planta em texto no lugar — o resto funciona igual.

---

## Detalhes que importam

- **Funciona no PRO** (US$20/mês). Não depende de internet pra funcionar: ela tem o guia dos
  geradores embutido. Quando a internet está disponível, ela dá uma olhada na documentação atual
  pra usar os truques mais recentes (os geradores mudam de versão direto).
- **Roda de novo a cada imagem nova.** Cada post, anúncio ou thumbnail é uma rodada. E como a doc
  dos geradores muda, o prompt sempre sai no padrão atual — coisa que um modelo de prompt fixo
  (template estático) não faz.
- **Não inventa.** Os truques de cada gerador vêm da documentação oficial, não de chute. Se a
  internet estiver fora, ela te avisa e usa o guia embutido.
- **Ela NÃO gera a imagem FINAL** — ela monta o briefing, RENDERIZA um rascunho da composição e
  escreve o prompt. Quem gera a imagem pronta é o ChatGPT / Nano Banana / o gerador que você já usa.
  Por isso ela é segura e não gasta sua cota: o trabalho pesado de acertar a descrição acontece aqui,
  antes.

---

## Uma coisa só pra deixar claro

O **rascunho** é um **mapa da composição**, não a arte pronta e nem um desenho milimétrico. Ele
marca ONDE e QUÃO GRANDE fica cada coisa, a paleta e a câmera — a **forma e o rosto de verdade vêm
do prompt e da sua foto** (que você anexa junto). Os geradores ainda erram posição ("põe à esquerda"
às vezes vira à direita), então trate a posição como sugestão forte: se sair algo trocado de lugar,
peça pro gerador **mover só aquilo** em vez de gerar tudo de novo — assim você não gasta outra geração.
