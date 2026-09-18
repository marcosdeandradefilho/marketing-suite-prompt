# instalacao.md — comandos de instalação por SO + pegadinhas

⚠️ **Antes de QUALQUER comando daqui:** a skill já perguntou "posso? (s/n)" e o usuário disse
sim (regra 2 do SKILL.md). Os flags `--accept-*` e `--silent` só evitam os prompts DO winget
DEPOIS do sim — nunca pulam a pergunta. Pipe-to-shell, mudança de PATH/ExecutionPolicy e
`--allowerasing` = consentimento REFORÇADO (regras 4-6).

---

## WINDOWS (plataforma prioritária) — winget

IDs canônicos confirmados (usar com `-e --id`):
| ferramenta | ID winget |
|---|---|
| Node.js LTS | `OpenJS.NodeJS.LTS` |
| Python | `Python.Python.3.13` (ou `.3.12`; **não** existe meta-pacote confiável `Python.Python.3`) |
| git | `Git.Git` |
| ffmpeg | `Gyan.FFmpeg` |
| VS Code | `Microsoft.VisualStudioCode` |
| uv | `astral-sh.uv` |
| Build Tools (sob demanda) | `Microsoft.VisualStudio.2022.BuildTools` |

Comando padrão (sem admin — escopo de usuário, evita UAC):
```
winget install -e --id OpenJS.NodeJS.LTS --scope user --accept-package-agreements --accept-source-agreements
```
- `--accept-source-agreements` + `--accept-package-agreements`: **obrigatórios** — sem eles o
  winget TRAVA esperando "Y" na 1ª vez. `--source winget` força a fonte oficial (evita prompt da
  msstore). Fonte: learn.microsoft.com/windows/package-manager/winget/install ; winget-cli #3742
- `--scope user` não precisa de admin; `--scope machine` exige terminal elevado. Prefira user.
  (confidence média: validar empiricamente que Node/Git instalam em user sem UAC.)
- IDs: winstall.app / winget.run

### Pegadinhas Windows (cada uma vira uma fala da skill)
1. **PATH não recarrega:** depois de instalar, `node`/`git`/`ffmpeg` seguem "não reconhecido" na
   MESMA janela. **Reabra o terminal** antes de re-checar. É por design (winget é processo filho).
   Fonte: github.com/microsoft/winget-cli/issues/531
2. **Gyan.FFmpeg adiciona o PATH ERRADO:** aponta pra pasta-pai sem o sufixo
   `\ffmpeg-<versão>-full_build\bin`. Se `where.exe ffmpeg` falhar mesmo após reabrir o terminal,
   ache o .exe real em `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*-full_build\bin`
   e avise o usuário pra adicionar ESSE caminho ao PATH (escopo User, com consentimento — regra 5).
   Fonte: github.com/microsoft/winget-pkgs/issues/95349
3. **winget pode não existir** (Windows Server, conta recém-criada, Windows antigo). Detecte com
   `winget --version`. Escada de fallback, em ordem:
   1. reabrir o terminal / relogar (registro assíncrono);
   2. `Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe`;
   3. instalar "App Installer" pela Microsoft Store;
   4. baixar o `.msixbundle` em github.com/microsoft/winget-cli/releases.
   (Chocolatey é alternativa, mas exige instalação extra + admin — só último recurso.)
   Fonte: learn.microsoft.com/windows/package-manager/winget/
4. **ExecutionPolicy:** só importa pros `.ps1` que o ALUNO for rodar depois (não pro winget/node,
   que são .exe). Se um script .ps1 dele for bloqueado: `Set-ExecutionPolicy RemoteSigned -Scope
   CurrentUser` (sem admin, com consentimento). Se houver GPO corporativo, o CurrentUser não cola
   — rode pontual: `powershell -ExecutionPolicy Bypass -File script.ps1`.
   Fonte: learn.microsoft.com/powershell/.../about_execution_policies
5. **node-gyp / módulo nativo falha** (`gyp ERR! find VS`): precisa de Visual C++ Build Tools +
   Python. `winget install -e --id Microsoft.VisualStudio.2022.BuildTools` (pesado). Só recomende
   SE o aluno for usar lib nativa — muita ferramenta moderna usa binário pré-compilado e dispensa.
   Fonte: npmjs.com/package/node-gyp
6. **Hash mismatch / SmartScreen:** se o winget abortar com "Installer hash does not match", NÃO
   ensine flag de risco — peça pra tentar mais tarde (o manifesto costuma ser corrigido) ou use o
   instalador oficial do site. `--ignore-security-hash` é arriscado e não funciona elevado — evite.
   Fonte: blog.intunepckgr.com (winget hash) ; winget-cli #3640

---

## macOS — Homebrew

Pré-requisito antes do brew: Command Line Tools.
```
xcode-select -p          # detecta (sai 0 e imprime caminho se já tem)
xcode-select --install   # instala (popup do sistema — normal num Mac novo)
```
Instalar o Homebrew (pipe-to-shell → consentimento reforçado: é script oficial da internet):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**Pegadinha Apple Silicon:** depois de instalar, `brew` dá "command not found" porque
`/opt/homebrew/bin` não está no PATH. Corrija (com consentimento — edita o `.zprofile`):
```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"   # ativa já na sessão atual
```
(Em Mac Intel o prefixo é `/usr/local`. Derive pelo `uname -m`: arm64 → /opt/homebrew, x86_64 →
/usr/local. Melhor ainda: rode `brew --prefix` depois.) Fonte: docs.brew.sh/Installation

Instalar (sem sudo, depois do brew configurado): `brew install node` · `brew install python` ·
`brew install git` · `brew install ffmpeg`. (git já vem com o Xcode CLT — detecte antes.)

---

## LINUX — apt (Debian/Ubuntu) e dnf (Fedora)

Descobrir o gerenciador: `command -v apt` vs `command -v dnf` (ou ler `/etc/os-release`).
Dentro do WSL, trate como Linux (apt/dnf), **não** winget.

### Debian / Ubuntu (apt — pede sudo)
Base: `sudo apt update && sudo apt install -y git python3 python3-pip ffmpeg`
- **ffmpeg "Unable to locate package":** está no componente `universe` →
  `sudo add-apt-repository universe && sudo apt update` primeiro. Fonte: linuxcapable (ffmpeg ubuntu)
- **Node do apt é velho demais** pra ferramentas atuais. Use NodeSource (pipe-to-shell com sudo →
  consentimento reforçado, mostre a URL):
  ```
  curl -fsSL https://deb.nodesource.com/setup_lts.x -o nodesource_setup.sh
  sudo -E bash nodesource_setup.sh
  sudo apt install -y nodejs
  ```
  `setup_lts.x` acompanha a LTS atual sozinho. Fonte: github.com/nodesource/distributions DEV_README

### Fedora (dnf — pede sudo)
Base: `sudo dnf install -y nodejs npm python3 python3-pip git`
- **ffmpeg na Fedora:** o repo padrão traz `ffmpeg-free`, SEM codecs patenteados (H.264/H.265/AAC).
  Pra ffmpeg completo precisa do RPM Fusion:
  ```
  sudo dnf install -y https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
  sudo dnf swap ffmpeg-free ffmpeg --allowerasing
  ```
  ⚠️ **`--allowerasing` REMOVE o `ffmpeg-free` (destrutivo)** → consentimento reforçado: avise em
  PT-BR que vai trocar o ffmpeg atual; ofereça **manter o ffmpeg-free** se o trabalho não exige
  H.264/AAC. Fonte: linuxcapable (ffmpeg fedora) ; docs RPM Fusion

### Alternativa sem sudo (Mac/Linux): nvm
Pra quem não pode/não quer sudo ou quer várias versões de Node (pipe-to-shell → consentimento):
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh | bash
# reabra o terminal OU: source ~/.bashrc  (ou ~/.zshrc)
nvm install --lts
```
**Pegadinha:** o nvm NÃO fica ativo na MESMA sessão que rodou o installer — reabra/`source`.
Fonte: github.com/nvm-sh/nvm (releases/latest)

---

## Validação por smoke-test (não só `--version`)
Depois de instalar, prove que FUNCIONA:
- **Node:** `node -e "console.log(1+1)"` → imprime `2`.
- **Python:** `py -c "print(1+1)"` (Win) / `python3 -c "print(1+1)"` (Mac/Linux) → `2`.
- **ffmpeg:** gera 1s de áudio → `ffmpeg -f lavfi -i sine=d=1 -y out_teste.wav` (e apague depois).
- **git:** `git --version` + checar `git config user.name` (se vazio, oferecer configurar).
- **Fechar:** `claude doctor` (diagnostica o próprio Claude Code).
