# deteccao.md — como varrer o PC (read-only) + pegadinhas

A detecção NUNCA instala nada. Só lê versões. Os blocos de detecção no fim deste arquivo são
**comandos** determinísticos (não arquivos `.ps1`), então rodam direto sem esbarrar na
ExecutionPolicy do Windows e sem depender de diretório de trabalho. Rode o bloco do SO certo
e leia a saída `chave|status|versão|nota`.

## O que o scan checa (ambos os SOs)
OS + arquitetura · Claude Code (`claude --version`, `claude doctor`) · gerenciador de pacote
(winget / brew / apt / dnf) · **Node.js** + npm · **Python** + pip · **git** · **ffmpeg** ·
VS Code (`code`) · uv (opcional). No Mac também: Xcode Command Line Tools.

Saída padrão, uma linha por item: `chave|status|versão|nota`
(`status` = `OK` ou `MISSING`). Ex.: `node|OK|v24.14.1` · `python|MISSING|stub da Store no PATH`.

## Regra de ouro da detecção (por SO)
- **Windows:** caminho real de um comando com `where.exe <cmd>` ou `Get-Command <cmd> -All`
  (lista TODAS as ocorrências no PATH — revela colisões). Existência sem erro vermelho:
  `if (Get-Command node -ErrorAction SilentlyContinue) { node --version }`.
- **macOS / Linux:** `command -v <cmd>` (POSIX, melhor que `which`). Sai 0 e imprime o caminho
  se existe, !=0 se não. No Linux dá pra cruzar com `dpkg -s <pkg>` (Debian/Ubuntu) ou
  `rpm -q <pkg>` (Fedora).
- Sempre tratar `command not found` / exit code != 0 como **não instalado**.
- Fonte: code.claude.com/docs/en/setup ; docs.python.org/3/using/windows.html

## ⚠️ Pegadinhas de detecção (as que derrubam um leigo)

### 1. Windows: `python` pode ser o STUB falso da Microsoft Store
Num Windows 11 limpo existem stubs de 0 byte (app execution aliases) em
`%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe` e `python3.exe`. Digitar `python` abre a
Loja ou imprime *"Python was not found"* — NÃO é Python.
- **Detecte Python REAL com `py --version`** (o Python Launcher, que não é stub). Liste todas
  as versões reais com `py -0p` (o `*` marca a default).
- Se `where.exe python` cair dentro de `\WindowsApps\`, é stub → Python **não está** instalado.
- Correção (avisar o usuário, não fazer escondido): Configurações > Apps > Configurações
  avançadas de apps > Aliases de execução de aplicativo > desligar `python.exe`/`python3.exe`.
- Fonte: learn.microsoft.com/windows/dev-environment/python ; learn.microsoft.com/answers (stub Store)

### 2. `where.exe` retorna VÁRIOS caminhos — desambiguar
`where.exe python` pode listar 2 linhas (stub da Store + Python real). `where.exe git` idem
(mingw64 + cmd). Use o primeiro caminho que **não** esteja em `\WindowsApps\` como o real.
Fonte: docs.python.org/3/using/windows.html

### 3. macOS Apple Silicon: brew instalado mas fora do PATH
Em Mac M1+ o Homebrew fica em `/opt/homebrew` (Intel: `/usr/local`), e `/opt/homebrew/bin` não
está no PATH por padrão — `brew --version` pode dar *"command not found"* mesmo instalado.
- Descubra o chip: `uname -m` → `arm64` (Apple Silicon → `/opt/homebrew`) ou `x86_64`
  (Intel → `/usr/local`). Teste o caminho absoluto, não só `brew`.
- Fonte: docs.brew.sh/Installation

### 4. VS Code pode existir sem o comando `code`
O comando `code` no PATH é opcional na instalação — o app pode estar lá e `code --version`
falhar. Não conclua "VS Code ausente" só por isso; é opcional de qualquer jeito.
Fonte: code.visualstudio.com/docs/configure/command-line

### 5. PATH não recarrega depois de instalar (pós-detecção, vale pro Step 6)
Logo após um `winget install`, `node`/`git`/`ffmpeg` continuam "não reconhecido" na MESMA
janela — o winget é processo filho e não muda o PATH do shell pai. Reabra o terminal antes de
re-checar. Fonte: github.com/microsoft/winget-cli/issues/531

## Comandos de verificação canônicos (por ferramenta)
| ferramenta | Windows | macOS / Linux |
|---|---|---|
| Node.js | `node --version` / `npm --version` | `node -v` / `npm -v` |
| Python | `py --version` (e `py -0p`) | `python3 --version` / `pip3 --version` |
| git | `git --version` | `git --version` |
| ffmpeg | `ffmpeg -version` (UM traço) | `ffmpeg -version` |
| VS Code | `code --version` | `code --version` |
| winget | `winget --version` | — |
| Homebrew | — | `brew --version` (mac) |
| Claude Code | `claude --version` / `claude doctor` | idem |
| uv (opcional) | `uv --version` | `uv --version` |

> `ffmpeg -version` é com **um** traço (flag oficial do ffmpeg). Fonte: ffmpeg.org/download.html

## Blocos de detecção (rode o do SO certo)

### Windows (PowerShell — são COMANDOS, não .ps1; não esbarram na ExecutionPolicy)
```powershell
$os = (Get-CimInstance Win32_OperatingSystem).Caption; "OS|$os build $([Environment]::OSVersion.Version.Build)"
foreach ($c in 'claude','winget','node','npm','git','ffmpeg','code','uv') {
  $p = (Get-Command $c -ErrorAction SilentlyContinue).Source
  if ($p) { "$c|OK|$p" } else { "$c|MISSING|" }
}
# Python: py launcher primeiro (evita o stub da Store)
if (Get-Command py -ErrorAction SilentlyContinue) { "python|OK|" + (py --version) }
elseif (((Get-Command python -All -ErrorAction SilentlyContinue).Source -join ';') -match 'WindowsApps') { "python|MISSING|stub da Store no PATH" }
else { "python|MISSING|" }
```

### macOS / Linux (bash)
```bash
echo "OS|$(uname -s) $(uname -m)"
for c in claude brew node npm python3 pip3 git ffmpeg code uv; do
  if command -v "$c" >/dev/null 2>&1; then echo "$c|OK|$(command -v $c)"; else echo "$c|MISSING|"; fi
done
[ "$(uname -s)" = "Darwin" ] && { xcode-select -p >/dev/null 2>&1 && echo "xcode-clt|OK" || echo "xcode-clt|MISSING|necessário antes do Homebrew"; }
```
