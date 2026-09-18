# fluxo.md — análise profunda, posturas, recibo

O SKILL.md chama este arquivo pra: analisar a máquina a fundo (só leitura), mapear postura→camada, e
descrever o recibo. Textos ao usuário em PT-BR anti-guru.

---

## §Análise — recon + auditoria (Stage 0, só leitura, você roda)
Primeiro entenda a máquina toda antes de propor qualquer coisa. Rode (nada aqui altera nada):
```powershell
$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$build = [int](Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').CurrentBuild   # >=22000 = Win11
$pd = Get-Partition -DriveLetter C | Get-Disk | Get-PhysicalDisk; $media = $pd.MediaType   # SSD | HDD | Unspecified
$laptop = [bool](Get-CimInstance Win32_Battery)
$startup = (Get-CimInstance Win32_StartupCommand).Count
$freeGB = [math]::Round((Get-PSDrive C).Free/1GB,1); $freePct = [math]::Round((Get-PSDrive C).Free/((Get-PSDrive C).Used+(Get-PSDrive C).Free)*100)
function DirMB($p){ if(Test-Path $p){ [int]((Get-ChildItem $p -Recurse -Force -EA SilentlyContinue|Measure-Object Length -Sum).Sum/1MB) } else { 0 } }
$lixoMB = (DirMB $env:TEMP)+(DirMB 'C:\Windows\Temp')+(DirMB 'C:\Windows\SoftwareDistribution\Download')
$prog = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' -EA SilentlyContinue|Where-Object DisplayName).Count
$svc3 = @(Get-CimInstance Win32_Service|Where-Object{ $_.StartMode -eq 'Auto' -and $_.State -eq 'Running' -and $_.PathName -notmatch [regex]::Escape($env:WINDIR) }).Count
$boot = (Get-WinEvent -LogName 'Microsoft-Windows-Diagnostics-Performance/Operational' -EA SilentlyContinue|Where-Object Id -eq 100|Select-Object -First 1)
```
Se não for Windows → *"Essa skill é de Windows, aqui ela não roda."* e PARE. Se for, apresente um retrato
curto e honesto: *"Vi aqui: Windows 11, SSD, desktop, admin. Achei {startup} programas no boot, {svc3}
serviços de terceiro rodando junto, ~{lixoMB} MB de lixo, disco com {freePct}% livre, {prog} programas
instalados."* **Portão de honestidade:** se já tá enxuto (startup≤6, lixo<500MB, livre>25%), diga que há
pouco a ganhar. Esses números são o "antes" do recibo.

## §Posturas — mapa (Stage 1) com rótulos HONESTOS
AskUserQuestion (header "Postura"):
- **Conservadora** — *"Só o 100% seguro e reversível: faxina de lixo e interface mais imediata. Roda até sem admin."*
- **Equilibrada (recomendada)** — *"A conservadora + os ganhos reais que precisam de cuidado: serviços (inclusive updaters de terceiros), telemetria, tarefas de fundo, energia, privacidade, component store. Ponto de restauração antes."*
- **Agressiva** — *"A equilibrada + o resto (menu clássico, handlers mortos, HAGS, hibernação). Vou ser direto: agressivo entrega quase o mesmo que equilibrado. Os 'super tweaks' de milagre (registry cleaner, RAM booster, pagefile off, Superfetch off, timer resolution) são placebo ou risco, e eu não faço."*
Segunda pergunta (Uso: Trabalho / Jogos / Os dois → liga o módulo de jogos). Terceira (módulos extras,
multiSelect): desinstalar programa de fábrica · passar antivírus · resetar rede · reparar sistema.
Mapa postura→camada detalhado em `catalogo.md §Mapa por postura`.

## §Geração — o que setar no motor (Stage 2)
Copie `assets/acelera-pc.ps1` pro Desktop, setando os toggles: `$Postura`; `$OtimizarJogos` (se Jogos/Os
dois); `$DesinstalarBloatware`/`$PassarAntivirus`/`$ResetarRede`/`$RepararSistema` (só os escolhidos). Carimbe
o cabeçalho com o que detectou. Copie o `assets/acelera-pc-semanal.bat` pro lado (ele precisa do .ps1 junto).

## §Recibo — o motor salva em TEXTO PURO (Desktop\acelera-pc-recibo.txt)
Antes/depois (boot Run/Startup, MB liberados, disco livre), o que fez, sanidade com TAG, como desfazer
(rstrui + .reg + Enable-ScheduledTask + reinstalar app), a verdade sobre o ganho, e o lembrete do .bat
semanal. Sem negrito, sem emoji, sem tabela `|`.
