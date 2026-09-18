# Site Institucional — leia primeiro

Cria um **site institucional completo e profissional** (HTML/CSS/JS pronto pra publicar), **bonito de
verdade e moderno (2026)**, a partir de pouca informação — pra você ou pra um cliente. Também **refaz** um
site velho/feio e devolve com cara de site caro.

Duas coisas fazem o site sair bonito de verdade, e não "genérico de IA":
1. **Ela OLHA referências atuais antes de criar.** Em todo site, ela busca e **tira print de pelo menos 5
   sites bonitos e atuais do nicho** (sites reais + vitrines de design tipo Awwwards/Behance), abre os prints,
   VÊ o design de 2026 e desenha a partir disso — não de um template velho na cabeça dela.
2. **E ela OLHA o próprio resultado.** Depois de montar, renderiza o site, tira print, vê os pixels, compara
   com uma régua de qualidade e corrige o que ficou feio — antes de te entregar. É o que nenhum gerador faz,
   e é o que impede o resultado feio de passar.

## Instalar (não precisa saber programar)

Não tem chave de API, não instala nada, não configura nada. É só copiar a pasta `site-institucional/`
inteira pra dentro da sua pasta de skills do Claude Code:

- **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
- **Mac/Linux:** `~/.claude/skills/`

Fica assim: `.../.claude/skills/site-institucional/`. Abre o Claude Code e pronto.

> Detalhe: pra ela **se revisar no olho** (renderizar o site e tirar print), ela usa o **Node** e o
> **Chrome ou Edge** que já estão na sua máquina — não instala nada. Se faltar algum, o site é montado igual,
> só sem a auto-revisão visual (ela te avisa pra você conferir no navegador). O Node também gera o código de
> **Pix** (opcional). O site em si não depende de nada disso pra funcionar — abre clicando no `index.html`.

## Como usar

Digita `/site-institucional` ou fala naturalmente. Exemplos:

- *"Preciso de um site pra minha clínica de estética. Nome Studio Bella, WhatsApp (11) 98888-7777, cores
  rosê e dourado."* → ele já monta.
- *"Faz um site pra um advogado."* → ele puxa o padrão do nicho (áreas de atuação, OAB, tom sóbrio) e marca
  o que falta pra você preencher.
- *"Refaz esse site com um design melhor: https://site-do-cliente.com.br"* → ele lê o conteúdo real, mantém,
  e reconstrói bonito.
- Manda só *"quero um site"* → ele faz UMA pergunta rápida (nicho + nome + WhatsApp) e segue.

Você responde no máximo uma coisa ou outra — a skill faz o resto sozinha. O design sai **bonito e moderno por
padrão**, claro e do jeito do nicho (escuro só onde combina, tipo barbearia ou steakhouse). Se você quiser
algo bem simples, é só pedir.

## Antes e depois (o que muda)

**Sem a skill**, você pede um site pro Claude e ele cospe um HTML genérico: fonte Inter, botão roxo, três
cards iguaizinhos centralizados, tudo arredondado — a cara de "site feito por IA". E ele nunca olha o
resultado, então passa coisa feia e quebrada. Você ainda tem que montar as pastas, organizar imagem e
adicionar WhatsApp/Pix/LGPD na mão.

**Com a skill**, sai uma **pasta pronta pra publicar**, bonita de verdade: paleta e tipografia do nicho,
layout editorial, **foto real** (do Pexels, já baixada na pasta), o **conteúdo-âncora do nicho na frente**
(cardápio no restaurante, portfólio no arquiteto, resultados no advogado), animação no scroll que respeita
acessibilidade, **botão de WhatsApp flutuante**, **rodapé com CNPJ/endereço/horário**, **aviso de cookies
(LGPD)**, **caixa de Pix** opcional com código válido, mapa, formulário sem servidor, SEO e favicon. E ela
**renderizou e revisou no olho** antes de te entregar. Mais o passo a passo pra publicar (Netlify/GitHub/ZIP)
e a **mensagem pronta pra mandar pro cliente** no WhatsApp.

## O que sai (a entrega)

Uma pasta `site-<cliente>/` com `index.html`, CSS, JS, **fotos reais** na pasta `/img` (marcadas com
`<!-- TROCAR -->` pra você trocar pelas do cliente), página 404, favicon, `robots.txt`, `sitemap.xml`, um
`README.md` ensinando a publicar, e o `ENTREGA-whatsapp.txt`. Abre clicando no `index.html`. Sobe arrastando
a pasta no Netlify Drop, ou manda o ZIP pro cliente.

## Quando rodar de novo

Roda toda vez que: for fazer um site pra **outro cliente**, quiser **trocar a paleta** ou **adicionar uma
página**, **refazer** um site antigo, ou **atualizar** quando o negócio mudar. Ele guarda os dados de cada
cliente (`.claude/clientes/<cliente>/`) — então da segunda vez pro mesmo cliente ele já reaproveita logo,
cores e contato sem te perguntar de novo.

## Combina com (mesmo pack)

`/prospector` (acha o cliente) → `/gerar-proposta` (manda a proposta + Pix) → **`/site-institucional`**
(entrega o site).
