# Página de Vendas — leia primeiro

Cria uma **página de vendas completa e de alta conversão** (HTML/CSS/JS pronto pra publicar), com **copy
profissional** e **design premium**, a partir de um briefing curto. Antes de montar, ela te mostra a **copy e
as cores pra você aprovar**. Serve pra vender curso, mentoria, serviço, software, ou pra captar leads. Também
**refaz** uma página de vendas velha e devolve com cara de página cara.

## Instalar (não precisa saber programar)

Não tem chave de API, não instala nada, não configura nada. É só copiar a pasta `pagina-de-vendas/` inteira pra
dentro da sua pasta de skills do Claude Code:

- **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
- **Mac/Linux:** `~/.claude/skills/`

Fica assim: `.../.claude/skills/pagina-de-vendas/`. Abre o Claude Code e pronto.

> Único detalhe: a caixa de **Pix** (opcional, só se você pedir) e o **preview pra conferir o visual** usam coisas
> que já vêm no Claude Code (Node + o navegador Edge/Chrome que você já tem). Se faltar, a página é gerada do
> mesmo jeito, só esses dois extras que não rodam.

## Como usar

Digita `/pagina-de-vendas` ou fala naturalmente. Exemplos:

- *"Cria uma página de vendas pro meu curso de confeitaria, R$197, pra quem quer fazer e vender doce em casa."* →
  ela propõe a copy e as cores, você aprova, e ela monta a página.
- *"Faz uma landing pra captar leads de uma aula gratuita."* → ela monta uma página de captura (sem preço, o
  foco é o formulário).
- *"Refaz essa página de vendas com um design melhor: https://..."* → ela lê o que já existe, mantém a oferta
  real, e reconstrói bonito.
- Manda só *"quero uma página de vendas"* → ela faz UMA pergunta rápida (o que vende, pra quem, preço, objetivo)
  e segue.

**Como funciona o jogo:** primeiro ela te mostra a copy (título, oferta, garantia) e a paleta de cores. Você
aprova ou ajusta. Só depois ela monta a página inteira, **gera um preview pra ela mesma conferir o visual**, e
refaz o que ficou genérico até a página ficar realmente boa.

## Antes e depois (o que muda)

**Sem a skill**, você pede uma página de vendas pro Claude e ele cospe um HTML genérico: fonte Inter, botão roxo,
título centralizado com dois botões, três cards iguais, texto com cara de IA (cheio de travessão), preço antes de
construir valor, sem LGPD, sem Pix, sem preview do WhatsApp. E você ainda corre o risco de escrever uma promessa
de renda que **derruba o seu anúncio no Meta**.

**Com a skill**, sai uma **página pronta pra vender**: copy de copywriter de verdade (sem cara de IA), design
premium (tipografia editorial, paleta com um acento só, efeitos de scroll com acessibilidade), **a oferta vem
antes do preço**, ancoragem honesta, garantia certa, **botão de checkout** pra colar o link da Hotmart/Kiwify,
**Pix opcional**, **aviso de cookies e formulário no jeito da LGPD**, **card de preview pro WhatsApp (Open Graph)**
e **barra de compra fixa no celular**. Tudo já passado por um pente-fino contra "cara de IA", contra design
genérico, e contra promessa de renda / escassez falsa que dá problema com a lei e com o Meta.

## O que sai (a entrega)

Uma pasta `pagina-<produto>/` com `index.html` (a página), `politica-de-privacidade.html`, CSS, JS, imagens
(placeholders marcados com `<!-- TROCAR -->`), favicon, OG image, e um `README.md` ensinando a publicar e a colar
o link do checkout e o Pixel da Meta. Abre clicando no `index.html`. Sobe arrastando a pasta no Netlify Drop, ou
cola no editor de página da Hotmart/Kiwify.

## Quando rodar de novo

Roda toda vez que: for vender **outro produto**, quiser a **versão fria pro Meta Ads** (a quente e a fria são
páginas diferentes), **trocar a oferta ou o preço** quando o lote virar, **refazer** uma página antiga, ou
**atualizar a prova social**. Ela guarda as suas cores/fonte (`.claude/clientes/<produto>/`), então da segunda
vez já reaproveita sem te perguntar de novo.

## Combina com (mesmo pack)

**`/pagina-de-vendas`** (converte) → `/mcp-meta` (roda o anúncio que aponta pra essa página).
Pro site da empresa (não de vendas), use a `/site-institucional`.
