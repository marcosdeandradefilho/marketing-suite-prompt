# fluxo-e-consentimento.md — relatório, perfil, consentimento, snapshot, microcopy

## Tom (vale pra tudo que o usuário vê)
PT-BR direto, anti-guru. Sem estimativa de tempo, sem "incrível!", sem promessa. Todo termo
técnico traduzido na hora: Node = *"motor que roda várias ferramentas"*; Python = *"outro motor,
mais pra dados e automação"*; git = *"guarda o histórico das suas mudanças"*; PATH = *"a lista de
onde o sistema procura programas"*; gerenciador de pacote = *"a lojinha de programas por comando"*.

## Pergunta de perfil (Step 4) — AskUserQuestion, 1 só, multiSelect
O perfil escolhe o **MOTOR** (Node / Python / ffmpeg), NÃO as bibliotecas do projeto — essas o
build instala na hora. Header curto *"O que construir"*. Pergunta *"O que você quer construir?
(pode marcar mais de um)"*. 4 opções fixas (o "Other" automático cobre o resto, ex. automação):
1. **Sites e apps web** — *páginas, sistemas, lojinha* → Node.js
2. **Dados, planilhas e documentos** — *Excel/CSV, relatórios, PDF* → Python
3. **Vídeo e áudio** — *cortar, converter, legendar* → ffmpeg
4. **Só o básico / não sei ainda** — *deixa o essencial pronto e a gente decide depois* → essencial

Vazio / pulou / "não sei" → **básico** (essencial só), nunca trava. Mapear via tabela de tipo de
trabalho em `catalogo-ferramentas.md`. Não despejar o catálogo inteiro — só o do perfil.

## Relatório de varredura (Step 5) — ordem fixa, anti-susto
```
Dei uma olhada no teu PC. Vou do que é boa notícia pro que falta.

✅ JÁ TEM
- Claude Code  (v2.x)        ← o principal já tá rodando
- git          (2.53)
- winget                     (a lojinha de programas do Windows)

➕ FALTA (só pro que você escolheu: [perfil])
- Node.js  — motor que roda sites e apps web. Sem ele, "npm não é reconhecido".
- ffmpeg   — corta e junta vídeo/áudio. Sem ele, nada de vídeo roda.
(As peças específicas do teu projeto, tipo bibliotecas, não entram aqui — o Claude
 instala sozinho quando for construir. Aqui eu cuido só do motor.)

♻️ DESATUALIZADO
- (nada relevante)  ← só listar se a versão velha realmente atrapalha

➡️ O QUE VOCÊ JÁ CONSEGUE FAZER HOJE
- Abrir o Claude Code em qualquer pasta e pedir pra ele criar/editar arquivos e textos.
(assim que instalar o Node, você também consegue rodar sites e apps.)
```
Regras: essencial primeiro; cada FALTA tem 1 linha de "por quê" em linguagem de leigo; NUNCA
mostrar o dump cru do scan nem nomes de ferramenta interna (Bash, PowerShell). Sempre fechar com
"o que já consegue hoje" (early-success = âncora anti-reembolso).

## Consentimento na instalação (Step 6) — uma de cada vez

Antes do primeiro s/n, mostre o **plano** (ordem de dependência + aviso de reabrir o terminal):
```
Pra deixar pronto pro que você escolheu, é isto, nesta ordem (instalo um de cada vez, sempre te
perguntando antes):
  1. winget   — a lojinha de programas do Windows (instala o resto sem download manual)
  2. git      — guarda o histórico; no Windows ainda traz o terminal "bash" que muito tutorial usa
  3. Node.js  — motor que roda sites e apps web
  4. ffmpeg   — corta e junta vídeo/áudio
Aviso: depois de cada instalação, é normal o programa ainda não ser reconhecido na mesma janela —
aí a gente reabre o terminal e eu confiro. Começo pelo 1? (s/n)
```
Depois, padrão por item:
```
Vou rodar:  winget install -e --id OpenJS.NodeJS.LTS --scope user --accept-package-agreements --accept-source-agreements
Isso instala o Node (motor que várias ferramentas usam). Posso? (s/n)
```
→ só roda no "sim" → valida com smoke-test (ver `instalacao.md`) → confirma:
```
Pronto. node -e "console.log(1+1)" deu 2. ✓  (se não reconhecer, reabre o terminal e eu re-checo)
```
**Consentimento reforçado** (pipe-to-shell, PATH, ExecutionPolicy, `--allowerasing`):
```
Esse passo baixa um script da internet (URL oficial: https://...) e roda no seu PC.
É o jeito oficial de instalar o [X]. Quer que eu rode? (s/n)
```
Nunca em lote. Nunca silencioso. Só escopo User/CurrentUser, nunca Machine/global.

## Dois caminhos nomeados (casos extremos)
- **CAMINHO A — máquina limpa (quase nada instalado):** ordem dura → 1) confirmar que o Claude
  Code abre e o login está feito (já que ela está rodando, está); 2) checar/instalar o gerenciador
  de pacote (winget/brew) — se ausente, rodar a escada de fallback de `instalacao.md` ANTES de tudo;
  3) git cedo (no Windows, instalar git troca o shell que o Claude usa — avise); 4) o runtime do
  perfil (Node/Python); 5) reabrir o terminal; 6) validar com smoke-test. Termine com 1 coisa
  funcionando.
- **CAMINHO B — tudo OK:** detecta, confirma as versões, diz "teu PC já tá pronto pra [perfil]",
  lista o que ele já consegue fazer hoje, e **ENCERRA sem instalar nada**. Não invente o que instalar.

## Setup "correto" do Claude Code (Step 7) — PILAR #2, não rodapé
Esse é o segundo motivo da skill existir: por padrão o Claude Code pede permissão em quase toda
ação, e o leigo não sabe o que clicar (ou cansa e desiste). Configurar isso uma vez é o maior
alívio do dia 1. Benefício em 1 linha pro usuário: *"isso faz o Claude editar arquivo sem te pedir
Enter toda hora — mas ainda confirma comando de terminal — e protege teu .env de ser lido."*
Escreva (só após "sim") em `~/.claude/settings.json` (escopo USER = vale em todo projeto futuro):
```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "deny": ["Read(./.env)", "Read(**/.env)", "Read(**/.env.*)", "Read(./secrets/**)"]
  }
}
```
- `acceptEdits` = *"o Claude edita arquivos sem te pedir Enter toda vez, mas AINDA pede
  confirmação em comando de terminal"*. **Nunca** `bypassPermissions` (pularia toda confirmação —
  proibido pelo método). **Nunca** configurar `/compact`.
- O `deny` protege `.env`/segredos de serem lidos. Pode adicionar uma allowlist de comandos comuns
  por projeto depois (`.claude/settings.json`), mas no setup base do USER, menos é mais.
- **MCP:** mencione em 1 linha — *"MCP é como você pluga ferramentas externas (ex.: Meta Ads) lá na
  frente; você não precisa de nada disso pra começar"*. NÃO instale MCP.
- Estrutura mínima de projeto (só quando abrir um): `CLAUDE.md` na raiz (contexto auto-lido) +
  `.claude/` pros settings. Não crie subpasta à toa.
- Fonte: code.claude.com/docs/en/settings ; /permissions ; /mcp ; /memory

## Snapshot `.claude/setup-state.md` (Step 8) — persiste pra re-run
```markdown
# Estado do setup — varredura de [DATA]
- SO: Windows 11 (build 26100)
- Perfil escolhido: vídeo + dados
- Instalado: Claude Code 2.x · git 2.53 · winget 1.28 · Node v24.x · ffmpeg 8.x
- Falta: (nada pendente do perfil) | Python (só se for mexer com dados)
- Pendências conhecidas: PATH do Gyan.FFmpeg corrigido manualmente
```
Em re-run (Step 3): comparar scan novo × snapshot, falar só "o que mudou desde [DATA]", mexer só
no delta. (Opcional: referenciar via `@.claude/setup-state.md` no CLAUDE.md do projeto — mas
cuidado pra não inflar contexto no PRO; preferir ler sob demanda.)

## Recurrence (por que roda de novo)
Roda de novo em: PC novo, projeto novo, ou quando começar um tipo de trabalho que pede outra
ferramenta (ex.: começou só com sites, agora vai mexer com vídeo → precisa do ffmpeg). O snapshot
faz a re-varredura ser rápida (só deltas), não um retrabalho do zero.

## Handoff (Step 9)
*"Ambiente pronto. Se mais pra frente alguma ferramenta sua der erro na máquina, isso é trabalho
da `/destrava-ferramenta`. Se você ainda não sabe O QUE construir, roda a `/varredura-de-mercado`."*
