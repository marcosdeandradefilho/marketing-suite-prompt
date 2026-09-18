# Carrossel — leia primeiro

Cria carrossel pro Instagram no estilo **print de tweet** (foto, nome, @ e o texto) — com a copy
escrita pra prender do primeiro ao último slide, sem cara de texto de IA — e entrega os slides em PNG
prontos pra postar. O segredo aqui é a **escrita**: o layout é simples, mas a copy é de copywriter.

## O que ela faz
- Você manda um tema ("carrossel sobre X") **ou** só o seu nicho ("sou nutri, não sei o que postar") e
  ela te dá pautas e escreve.
- Escreve a copy inteira (gancho, slides, CTA, legenda + 5 ganchos pra testar) e **te mostra pra você
  aprovar ANTES de gerar qualquer imagem**. Você ajusta o que quiser. Só depois ela gera os PNGs.
- Faz **vários de uma vez** (em lote) — manda 4 temas, aprova as copys, ela renderiza tudo.
- Quando o tema é **notícia/atualidade**, ela pesquisa na web, confere a fonte e a data, e te diz de
  onde tirou — não inventa fato.
- Pode usar **sua foto de perfil e seu @** no card. Se não mandar, ela usa um avatar de iniciais.

## Como instalar (não precisa saber programar)
Copia a pasta `carrossel/` inteira pra dentro da pasta de skills do Claude Code:
- **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
- **Mac/Linux:** `~/.claude/skills/`

Fica assim: `.../.claude/skills/carrossel/SKILL.md`. Abre o Claude Code e pronto.

**Sem chave de API, não instala nada, não configura nada.** As imagens são geradas pelo próprio
navegador que já vem no seu computador (Microsoft Edge no Windows). Zero mensalidade extra além do
Claude Code que você já tem.

## Como usar
Digita `/carrossel` ou fala natural:
- *"cria um carrossel sobre [tema], meu @ é @seuperfil"*
- *"sou [seu nicho] e não sei o que postar hoje, me dá ideias"*
- *"faz 3 carrosséis sobre [tema] pro meu cliente"*
- *"carrossel sobre a notícia de hoje sobre [assunto]"*

Pode mandar sua foto de perfil junto (o caminho do arquivo) que ela usa no card.

## Sem a skill vs com a skill
- **Sem a skill:** você pede "carrossel sobre IA" e o Claude devolve um texto motivacional genérico,
  cheio de "No mundo de hoje…" e emoji em toda linha, já joga imagem sem te perguntar, e quase nunca
  vira um PNG pronto pra postar.
- **Com a skill:** a copy é ancorada num gancho de verdade, sem cara de IA, você **aprova antes**,
  e sai um carrossel de prints de tweet em PNG 1080x1350 prontos pro feed — vários de uma vez se quiser.

## Quando rodar de novo
Toda semana, pra outro tema, pra outro cliente, ou pra testar outro dos 5 ganchos que ela te deu. Cada
run é conteúdo novo — não é o mesmo post reimpresso.

## Depois do carrossel
- `/briefing-de-imagem` — se quiser uma capa ilustrada ou uma arte avulsa.
- `/reels` — pra transformar o tema num vídeo.

## Um aviso honesto
Ela **não** faz print de tweet falso atribuído a uma pessoa real pra enganar — isso quebra regra do
Instagram e dá problema. O selo verificado vem desligado por padrão. O caminho certo é a sua própria
voz, um personagem fictício, ou uma paródia claramente marcada — que é o que ela faz.
