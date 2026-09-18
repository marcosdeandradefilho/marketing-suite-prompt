# catalogo-ferramentas.md — o que é cada coisa e quando importa

Regra de uso: a skill recomenda só o que o PERFIL do usuário precisa (Step 4). Este catálogo
é a fonte do "por que importa" em linguagem de leigo e da divisão essencial vs opcional.

## A pegadinha-mestra (diga isso ao leigo, é o coração da skill)
O Claude Code **já está instalado e roda sozinho** — o instalador nativo dele **não precisa de
Node** (no Windows ele roda via PowerShell; no Mac/Linux nativo). Então *"tenho que instalar
Node pra usar o Claude Code?"* → **não, pra rodar o Claude Code não.**
MAS: Node e Python são o **motor que roda as FERRAMENTAS que o Claude constrói** pra você
(site, app, script de dados). Sem eles, o Claude escreve o código e a sua máquina não consegue
executar/testar. Por isso eles entram na lista — são pré-requisito dos seus PROJETOS, não do
Claude Code em si. Fonte: code.claude.com/docs/en/setup

## O que o próprio Claude Code precisa (já deve estar OK)
- **Sistema:** Windows 10 1809+/11, macOS 13.0+, Ubuntu 20.04+/Debian 10+/Alpine 3.19+, 4 GB RAM.
- **Git for Windows é OPCIONAL** pro Claude Code: com ele o Claude usa a "Bash tool" (Git Bash);
  sem ele usa a "PowerShell tool". Recomende instalar mesmo assim — muito tutorial assume bash.
- **WSL não é obrigatório** no Windows (só serve pra sandbox). Não assuste o leigo com WSL.
- Atualização: instalação nativa se atualiza sozinha; `claude update` força; `claude doctor` diagnostica.
- Fonte: code.claude.com/docs/en/setup ; code.claude.com/docs/en/terminal-guide

## Catálogo (essencial vs opcional)

### ESSENCIAIS (quase toda ferramenta usa pelo menos um)
- **Node.js (LTS)** — *"o motor que faz a maioria das ferramentas web/JS rodarem"*. Instale a
  linha **LTS** (não a "Current"). Checar: `node -v` (espere algo como `v24.x` ou `v22.x`) e
  `npm -v` (o npm vem junto). Sem ele, `npm`/`npx` não existem e a maioria das ferramentas com
  dependências quebra com *"npm não é reconhecido"*. Não fixe o número no texto — instale a LTS
  e leia o real com `node -v`. Fonte: nodejs.org/en/download
- **Python (3.11+)** — *"outro motor, mais usado pra dados, planilhas e automação"*. Checar:
  `py --version` no Windows (jeito canônico), `python3 --version` no Mac/Linux. Cobre dados,
  scripts, PDFs, scraping. No instalador do Windows, marcar **"Add python.exe to PATH"**.
  Fonte: python.org/downloads ; docs.python.org/3/using/windows.html
- **git** — *"o que guarda o histórico das suas mudanças; o Claude usa pra versionar e instalar
  coisas do GitHub"*. Checar: `git --version`. No Windows, o "Git for Windows" ainda traz o Bash
  que muitos tutoriais assumem. Fonte: git-scm.com/downloads

### OPCIONAIS DE SISTEMA (você instala UMA vez, vale pra todo projeto — entram no setup)
São binários de sistema, não bibliotecas de um projeto. Se faltam, o leigo trava no Windows
(instalação chata + PATH) — então vale resolver aqui, uma vez.
- **ffmpeg** — *"canivete suíço de vídeo e áudio: cortar, converter, extrair áudio, comprimir"*.
  Só pra quem mexe com VÍDEO/ÁUDIO. Checar: `ffmpeg -version`. Sem instalador oficial único no
  Windows (builds: gyan.dev / BtbN — ver `instalacao.md`). Fonte: ffmpeg.org/download.html
- **VS Code** — *"editor pra você VER os arquivos que o Claude cria"*. Recomendado, não
  obrigatório. Checar: `code --version`. Fonte: code.visualstudio.com
- **Visual C++ Build Tools (Windows)** — *"compilador C++ que ALGUNS pacotes precisam"*.
  Condicional: só quando um pacote npm tem "módulo nativo" (erro `gyp ERR! find VS`). Pesado
  (~vários GB) — **NÃO instalar por padrão**, só sob demanda. node-gyp também exige Python.
  Fonte: github.com/nodejs/node-gyp

### NÃO É TRABALHO DO SETUP — o Claude Code instala isso NA HORA DO BUILD
Estas são **bibliotecas de um projeto específico**. O setup só garante o MOTOR (Node/Python); a
biblioteca em si o executor instala quando escreve o código que precisa dela. **NUNCA pré-instale
nem liste como "falta".** Se o usuário perguntar, responda em 1 linha *"o Claude instala isso na
hora que construir"* e siga.
- **pandas / openpyxl** — só aparecem quando o usuário vai mexer com Excel/dados; o build roda
  `pip install pandas openpyxl` sozinho. (CSV simples nem precisa — cabe no módulo `csv` nativo.)
- **Pillow** — imagens em Python; o build instala se o script pedir.
- **pandoc** (+ motor LaTeX pra PDF) — conversão de documentos; o build resolve quando for gerar.
- **Navegador/Chromium do Playwright** — automação web; o build roda `npx playwright install
  chromium` no passo dele.
- **uv** — instalador de libs Python rápido; bom, mas não é fundação — o build pode adotar depois.
Por que separar isso: é EXATAMENTE aqui que a skill parecia redundante. Pré-adivinhar a lib do
projeto é trabalho do build, não do setup. O setup entrega o motor; o build entrega o resto.

## MAPA: tipo de trabalho → qual MOTOR garantir (não qual biblioteca)
A coluna que importa é "Fundação" — o runtime de sistema que o setup garante. As bibliotecas do
projeto (pandas, pandoc, Playwright…) NÃO entram aqui: o build instala na hora.
| O usuário quer… | Fundação (o setup garante) | Sistema, opcional | A biblioteca do projeto |
|---|---|---|---|
| **Sites e apps web** (React/Next/Vite, lojinha, sistema) | Node.js LTS + git | VS Code | o build instala (npm) |
| **Dados / planilhas** (Excel, CSV, relatórios) | Python + git | VS Code | o build instala (pandas/openpyxl) |
| **Documentos / textos** (PDF, Word, Markdown) | Python + git | VS Code | o build instala (pandoc + motor PDF) |
| **Vídeo e áudio** | ffmpeg (+ Node ou Python pra orquestrar) | — | o build instala (libs de mídia) |
| **Automação / integração** | Python OU Node + git | — | o build instala; MCP é mencionado, não instalado |
| **Só o básico / não sei** | Node OU Python (o mais provável) + git | — | decide na hora de construir |

> Sites estáticos (HTML/CSS/JS puro) rodam só com o navegador; Node entra quando aparece
> build/servidor local. Apps web modernos (Vite/Next) exigem Node. Fonte: ffmpeg.org ; docs pandas.

## Notas que evitam recomendar errado
- **Não fixe o major** no texto (Node 24 é LTS hoje, mas isso muda — Node 26 vira LTS em out/2026).
  Instale a linha LTS e mostre o número real com `node -v`. Alerte só se estiver abaixo de v20.
- Whisper local (transcrição) e modelos pesados **NÃO entram no setup base** — são grandes,
  exigem torch + ffmpeg + download de modelo. Marque "instalo só quando você for usar transcrição".
