# =====================================================================
#  ACELERA PC - otimizacao COMPLETA do Windows (sensacao de recem-formatado)
#  Gerado pela skill /acelera-pc. Faz de tudo o que uma otimizacao de verdade
#  faz: limpa dezenas de locais de cache, enxuga boot e servicos, mexe no
#  registro (com seguranca), faxina o shell/menu de contexto, privacidade,
#  debloat, energia. SEM formatar e SEM apagar seus arquivos.
#
#  >>> COMO RODAR <<<
#    1. Menu Iniciar > "Windows PowerShell" > botao direito > "Executar como administrador"
#    2. powershell -ExecutionPolicy Bypass -File "$HOME\Desktop\acelera-pc.ps1"
#    (Windows PowerShell azul, nao o PowerShell 7, pra rede de restauracao funcionar.)
#
#  DOIS MODOS:
#    $Modo = 'Setup'   -> o pacote INTEIRO (uma vez, ou quando quiser refazer).
#    $Modo = 'Semanal' -> so a limpeza leve e reversivel (o acelera-pc.bat usa este).
#
#  REGRA DE OURO DE SEGURANCA (embutida): NUNCA se usa New-Item -Force numa chave
#  de registro que ja existe (isso apaga os valores dela - foi o que quebrou o tema
#  escuro na v1). Todo registro passa pela funcao SetReg, que so cria a chave se ela
#  faltar. Nada de save/mod/arquivo do usuario e apagado no automatico.
# =====================================================================

param([string]$ModoArg = '')   # o acelera-pc.bat passa 'Semanal' aqui pra forcar a limpeza leve

# ============ ESCOLHA AQUI ============
$Modo                 = 'Setup'         # 'Setup' | 'Semanal'  (o .bat sobrescreve pra Semanal)
$Postura              = 'Equilibrada'   # 'Conservadora' | 'Equilibrada' | 'Agressiva'
$OtimizarJogos        = $false          # limpa shader cache (regeneravel) + Game DVR off. NUNCA toca mod/save.
$DesinstalarBloatware = $false          # lista appx/programas e VOCE escolhe (interativo)
$PassarAntivirus      = $false          # varredura rapida do Defender
$ResetarRede          = $false          # CONSERTO: reset da pilha de rede (so se a internet estiver ruim; exige reboot)
$RepararSistema       = $false          # DISM /RestoreHealth + sfc /scannow se achar corrupcao (demora)
# ======================================
if($ModoArg){ $Modo = $ModoArg }   # argumento (do .bat) vence o toggle

$ErrorActionPreference = 'SilentlyContinue'
$rank = @{ 'Conservadora'=1; 'Equilibrada'=2; 'Agressiva'=3 }[$Postura]
if(-not $rank){ Write-Host "Postura invalida." -ForegroundColor Red; return }
$backup = "$env:USERPROFILE\Desktop\acelera-pc-backup"
New-Item $backup -ItemType Directory -Force | Out-Null
$log = New-Object System.Collections.ArrayList
function Nota($t){ [void]$log.Add($t); Write-Host "  . $t" -ForegroundColor DarkGray }
function MB($b){ [int]($b/1MB) }
function DirMB($p){ if(Test-Path $p){ MB((Get-ChildItem $p -Recurse -Force -EA SilentlyContinue | Measure-Object Length -Sum).Sum) } else { 0 } }
# SetReg: escrita SEGURA - so cria a chave se ela NAO existir (nunca -Force numa existente)
function SetReg($path,$name,$value,$type){
  if(-not (Test-Path $path)){ New-Item -Path $path -Force | Out-Null }
  New-ItemProperty -Path $path -Name $name -Value $value -PropertyType $type -Force | Out-Null
}
function BackupKey($nome,$caminho){ reg export $caminho "$backup\$nome.reg" /y *>$null }
function LimparPastaConteudo($p){ if($p -and $p -notmatch '^[A-Za-z]:\\?$' -and (Test-Path $p)){ Remove-Item "$p\*" -Recurse -Force -EA SilentlyContinue } }

# ---------------- RECON ----------------
$admin  = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$build  = [int](Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').CurrentBuild
$win11  = $build -ge 22000
$pd = Get-Partition -DriveLetter C -EA SilentlyContinue | Get-Disk -EA SilentlyContinue | Get-PhysicalDisk -EA SilentlyContinue
$media = $pd.MediaType
if($media -eq 'Unspecified' -or -not $media){ if($pd.SpindleSpeed -eq 0 -or $pd.BusType -eq 'NVMe'){ $media = 'SSD' } else { $media = 'Desconhecido' } }
$laptop = [bool](Get-CimInstance Win32_Battery)
$c0 = Get-PSDrive C
$freeAntesGB = [math]::Round($c0.Free/1GB,1); $freeInicio = $c0.Free
$startupAntes = (Get-CimInstance Win32_StartupCommand).Count

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "  ACELERA PC  |  modo: $Modo  |  postura: $Postura" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ("Windows {0} (build {1}) | disco {2} | {3} | admin: {4}" -f $(if($win11){'11'}else{'10'}),$build,$media,$(if($laptop){'notebook'}else{'desktop'}),$admin)
Write-Host ("Antes: {0} programas no boot | disco C {1} GB livre" -f $startupAntes,$freeAntesGB)
if(-not $admin){ Write-Host "SEM administrador: varias camadas ficam de fora. Rode como admin pro pacote completo." -ForegroundColor Yellow }

# ============================================================
#  MODO SEMANAL  (o .bat usa este) - so limpeza leve e reversivel
# ============================================================
if($Modo -eq 'Semanal'){
  Write-Host "`n[semanal] Limpeza leve (temp, cache de apps, DNS, TRIM)..." -ForegroundColor Green
  LimparPastaConteudo $env:TEMP; Nota "Temporarios do usuario limpos"
  if($admin){ LimparPastaConteudo "$env:WINDIR\Temp"; Nota "Temporarios do sistema limpos" }
  # cache de navegadores + apps Electron (fecha o app -> senao pula os travados)
  $caches = @(
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\Cache",
    "$env:APPDATA\discord\Cache","$env:APPDATA\discord\Code Cache","$env:APPDATA\discord\GPUCache",
    "$env:LOCALAPPDATA\Spotify\Data","$env:LOCALAPPDATA\Microsoft\Windows\INetCache",
    "$env:LOCALAPPDATA\Microsoft\Windows\Explorer" )
  $lib = 0
  foreach($p in $caches){ if(Test-Path $p){ $lib += DirMB $p; if($p -like '*Explorer'){ Remove-Item "$p\thumbcache_*.db" -Force -EA SilentlyContinue } else { LimparPastaConteudo $p } } }
  Nota "Cache de navegadores/apps limpo (~$lib MB estavam la)"
  ipconfig /flushdns | Out-Null; Nota "Cache de DNS limpo"
  if($admin -and $media -eq 'SSD'){ Optimize-Volume -DriveLetter C -ReTrim -EA SilentlyContinue; Nota "TRIM reenviado no SSD" }
  Stop-Process -Name StartMenuExperienceHost,SearchHost -Force -EA SilentlyContinue; Nota "Menu Iniciar e Busca reiniciados"
  $c1 = Get-PSDrive C; $lib2 = MB($c1.Free - $freeInicio)
  Write-Host "`n[semanal] Pronto. Liberou ~$lib2 MB. (A Lixeira NAO foi mexida - use o modo Setup se quiser esvaziar.)" -ForegroundColor Green
  ("Acelera PC - limpeza semanal de $(Get-Date -Format 'dd/MM/yyyy HH:mm') - liberou ~$lib2 MB") | Add-Content "$env:USERPROFILE\Desktop\acelera-pc-semanal.log"
  return
}

# ============================================================
#  MODO SETUP  -  o pacote completo
# ============================================================

# ---------- [1] REDE DE SEGURANCA ----------
$temRestore = $false
if($admin){
  Write-Host "`n[1] Rede de seguranca: ponto de restauracao..." -ForegroundColor Green
  try{
    if(Get-Command Enable-ComputerRestore -EA SilentlyContinue){ Enable-ComputerRestore -Drive "C:\" }
    reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore" /v SystemRestorePointCreationFrequency /t REG_DWORD /d 0 /f | Out-Null
    $seqB = (Get-CimInstance -Namespace root/default -ClassName SystemRestore | Measure-Object SequenceNumber -Maximum).Maximum
    if(Get-Command Checkpoint-Computer -EA SilentlyContinue){ Checkpoint-Computer -Description "Antes de Acelera-PC" -RestorePointType MODIFY_SETTINGS }
    else { ([wmiclass]"\\.\root\default:SystemRestore").CreateRestorePoint("Antes de Acelera-PC",0,100) | Out-Null }
    $seqA = (Get-CimInstance -Namespace root/default -ClassName SystemRestore | Measure-Object SequenceNumber -Maximum).Maximum
    $temRestore = ($seqA -gt $seqB) -or ($seqA -ge 1 -and (-not $seqB))
    # devolve a trava de 24h pro padrao (nao churnar o VSS)
    reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore" /v SystemRestorePointCreationFrequency /t REG_DWORD /d 1440 /f | Out-Null
  } catch { $temRestore = $false }
  if($temRestore){ Nota "Ponto de restauracao criado e confirmado (undo global: rstrui.exe)" }
  else { Write-Host "  NAO confirmei o ponto. Rodando SO o seguro+reversivel (regra de abort)." -ForegroundColor Red; Nota "Ponto de restauracao FALHOU - abortei as camadas fundas" }
} else { Nota "Sem admin: subconjunto seguro/HKCU" }
$fundo = $admin -and $temRestore   # camadas moderadas so com admin + restore confirmado

# ---------- [2] LIMPEZA PROFUNDA DE DISCO ----------
Write-Host "`n[2] Faxina de disco (dezenas de locais de cache/lixo)..." -ForegroundColor Green
LimparPastaConteudo $env:TEMP; Nota "Temporarios do usuario"
if($admin){
  LimparPastaConteudo "$env:WINDIR\Temp"; Nota "Temporarios do sistema"
  net stop wuauserv *>$null; net stop bits *>$null; LimparPastaConteudo "$env:WINDIR\SoftwareDistribution\Download"; net start wuauserv *>$null; net start bits *>$null; Nota "Cache do Windows Update"
  LimparPastaConteudo "$env:ProgramData\Microsoft\Windows\WER\ReportQueue"; LimparPastaConteudo "$env:ProgramData\Microsoft\Windows\WER\ReportArchive"; Nota "Relatorios de erro (WER)"
  Remove-Item "$env:WINDIR\Minidump\*" -Force -EA SilentlyContinue; Nota "Crash dumps antigos"
}
if(Get-Command Delete-DeliveryOptimizationCache -EA SilentlyContinue){ Delete-DeliveryOptimizationCache -Force; Nota "Cache do Delivery Optimization" }
LimparPastaConteudo "$env:LOCALAPPDATA\Microsoft\Windows\INetCache"; Nota "INetCache (Temporary Internet Files)"
Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\thumbcache_*.db" -Force -EA SilentlyContinue; Nota "Cache de miniaturas"
LimparPastaConteudo "$env:LOCALAPPDATA\D3DSCache"; Nota "DirectX Shader Cache"
LimparPastaConteudo "$env:APPDATA\Microsoft\Windows\Recent"; Nota "Arquivos recentes / jump lists"
# scanner GENERICO de cache de apps Chromium/Electron (so subpastas de cache; nunca User Data/LocalState/login)
Write-Host "  (Dica: feche navegadores e apps como Discord/Teams antes; caches abertos sao pulados)" -ForegroundColor DarkGray
foreach($raiz in $env:LOCALAPPDATA,$env:APPDATA){
  Get-ChildItem $raiz -Recurse -Directory -Depth 4 -EA SilentlyContinue |
    Where-Object { $_.Name -in @('Cache','Code Cache','GPUCache','blob_storage') -and $_.FullName -notmatch '\\(User Data\\Default\\(Login Data|Cookies|Web Data)|LocalState)\\' } |
    ForEach-Object { LimparPastaConteudo $_.FullName }
}
Nota "Cache de apps (navegadores, Discord, Teams, Spotify, Electron...) varrido dinamicamente"
# caches de dev, so se existir a ferramenta
if(Get-Command npm -EA SilentlyContinue){ npm cache clean --force *>$null; Nota "Cache do npm" }
if(Get-Command pip -EA SilentlyContinue){ pip cache purge *>$null; Nota "Cache do pip" }
if(Get-Command dotnet -EA SilentlyContinue){ dotnet nuget locals all --clear *>$null; Nota "Cache do NuGet/.NET" }
LimparPastaConteudo "$env:LOCALAPPDATA\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe\LocalCache"; Nota "Cache da Microsoft Store"
# component store (Equilibrada+, admin)
if($rank -ge 2 -and $admin){ Dism /Online /Cleanup-Image /StartComponentCleanup *>$null; Nota "Component store (WinSxS) enxugado (sem ResetBase; mantem rollback)" }
# manutencao de disco
if($fundo){ if($media -eq 'SSD'){ Optimize-Volume -DriveLetter C -ReTrim -EA SilentlyContinue; Nota "TRIM no SSD" } elseif($media -eq 'HDD'){ Optimize-Volume -DriveLetter C -Defrag -EA SilentlyContinue; Nota "HDD desfragmentado" } }
# Lixeira - so com confirmacao
try { $rb = @((New-Object -ComObject Shell.Application).NameSpace(0xA).Items()); $rbN=$rb.Count } catch { $rbN=0 }
if($rbN -gt 0){ $r = Read-Host "  A Lixeira tem $rbN itens (contem SEUS arquivos apagados). Esvaziar? Nao da pra desfazer [s/N]"; if($r -match '^[sS]'){ Clear-RecycleBin -Force; Nota "Lixeira esvaziada ($rbN itens) - com sua confirmacao" } }

# ---------- [3] BOOT E SEGUNDO PLANO ----------
Write-Host "`n[3] Enxugando boot, servicos e tarefas..." -ForegroundColor Green
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications' 'GlobalUserDisabled' 1 'DWord'; Nota "Apps em segundo plano desligados"
# startup interativo
$apps = @(Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location)
if($apps.Count -gt 0){
  Write-Host "  --- Programas que abrem no boot ---" -ForegroundColor Cyan
  for($i=0;$i -lt $apps.Count;$i++){ Write-Host ("   [{0}] {1}" -f ($i+1),$apps[$i].Name) }
  $sel = Read-Host "  Numeros pra DESLIGAR do boot (virgula), ou Enter pra pular"
  if($sel.Trim()){
    BackupKey 'Run_HKCU' 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'
    if($admin){ BackupKey 'Run_HKLM' 'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' }
    foreach($n in ($sel -split ',')){ $idx=([int]($n.Trim()))-1; if($idx -ge 0 -and $idx -lt $apps.Count){
      $nome=$apps[$idx].Name
      Remove-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name $nome -EA SilentlyContinue
      if($admin){ Remove-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' -Name $nome -EA SilentlyContinue }
      Nota "Startup desligado: $nome" } }
  }
}
if($fundo){
  # tarefas de telemetria (seguras, reversiveis)
  foreach($t in @(
    @{p='\Microsoft\Windows\Application Experience\';n='Microsoft Compatibility Appraiser'},
    @{p='\Microsoft\Windows\Application Experience\';n='ProgramDataUpdater'},
    @{p='\Microsoft\Windows\Application Experience\';n='StartupAppTask'},
    @{p='\Microsoft\Windows\Customer Experience Improvement Program\';n='Consolidator'},
    @{p='\Microsoft\Windows\Customer Experience Improvement Program\';n='UsbCeip'},
    @{p='\Microsoft\Windows\Autochk\';n='Proxy'})){ Disable-ScheduledTask -TaskPath $t.p -TaskName $t.n -EA SilentlyContinue | Out-Null }
  Nota "Tarefas de telemetria (Compatibility Appraiser, CEIP) desligadas"
  # tarefas de logon de TERCEIROS (updaters) - interativo
  $tk = @(Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\Microsoft\*' -and $_.State -eq 'Ready' -and ($_.Triggers.CimClass.CimClassName -contains 'MSFT_TaskLogonTrigger') })
  if($tk.Count -gt 0){
    Write-Host "  --- Tarefas de terceiros que abrem no logon (updaters) ---" -ForegroundColor Cyan
    for($i=0;$i -lt $tk.Count;$i++){ Write-Host ("   [{0}] {1}" -f ($i+1),$tk[$i].TaskName) }
    $sel = Read-Host "  Numeros pra DESLIGAR (virgula), ou Enter pra pular"
    foreach($n in ($sel -split ',')){ $idx=([int]($n.Trim()))-1; if($idx -ge 0 -and $idx -lt $tk.Count){ Disable-ScheduledTask -TaskName $tk[$idx].TaskName -TaskPath $tk[$idx].TaskPath -EA SilentlyContinue | Out-Null; Nota "Tarefa de logon desligada: $($tk[$idx].TaskName)" } }
  }
}

# ---------- [4] SERVICOS ----------
if($fundo){
  Write-Host "`n[4] Servicos..." -ForegroundColor Green
  $denyServ = 'RpcSs|RpcEptMapper|DcomLaunch|Dhcp|Dnscache|nsi|NlaSvc|BFE|mpssvc|WinDefend|WdNisSvc|SecurityHealthService|wscsvc|Sense|CryptSvc|KeyIso|VaultSvc|SamSs|EventLog|Winmgmt|gpsvc|ProfSvc|UserManager|LSM|Power|PlugPlay|DeviceInstall|Schedule|TrustedInstaller|msiserver|UsoSvc|WaaSMedicSvc|BrokerInfrastructure|CoreMessagingRegistrar|SystemEventsBroker|FontCache|Audiosrv|AudioEndpointBuilder|W32Time|SysMain|DoSvc|DPS|WdiSystemHost|WSearch'
  # MS seguros -> Manual/Disabled (backup do Start antes)
  $svcSafe = @('RetailDemo','MapsBroker','Fax','WMPNetworkSvc','lfsvc','WpcMonSvc','PhoneSvc','RemoteRegistry','dmwappushservice')
  foreach($s in $svcSafe){ $svc = Get-Service $s -EA SilentlyContinue; if($svc -and $s -notmatch $denyServ){ BackupKey "svc_$s" "HKLM\SYSTEM\CurrentControlSet\Services\$s"; Set-Service $s -StartupType Manual -EA SilentlyContinue } }
  Nota "Servicos MS raramente usados postos em Manual (backup salvo)"
  # DiagTrack (telemetria) -> Disabled
  if(Get-Service DiagTrack -EA SilentlyContinue){ BackupKey 'svc_DiagTrack' 'HKLM\SYSTEM\CurrentControlSet\Services\DiagTrack'; Stop-Service DiagTrack -Force -EA SilentlyContinue; Set-Service DiagTrack -StartupType Disabled -EA SilentlyContinue; Nota "Telemetria DiagTrack desligada" }
  # servicos de TERCEIROS em Automatic+Running - interativo
  $svc3 = @(Get-CimInstance Win32_Service | Where-Object { $_.StartMode -eq 'Auto' -and $_.State -eq 'Running' -and $_.PathName -and ($_.PathName -notmatch [regex]::Escape($env:WINDIR)) -and $_.Name -notmatch $denyServ } | Sort-Object DisplayName)
  if($svc3.Count -gt 0){
    Write-Host "  --- Servicos de TERCEIROS rodando no boot (updaters/helpers) ---" -ForegroundColor Cyan
    Write-Host "  (NAO desligue antivirus ativo, servico da placa de video, audio ou VPN que voce usa)" -ForegroundColor DarkGray
    for($i=0;$i -lt $svc3.Count;$i++){ Write-Host ("   [{0}] {1}" -f ($i+1),$svc3[$i].DisplayName) }
    $sel = Read-Host "  Numeros pra por em Manual (virgula), ou Enter pra pular"
    foreach($n in ($sel -split ',')){ $idx=([int]($n.Trim()))-1; if($idx -ge 0 -and $idx -lt $svc3.Count){ $nm=$svc3[$idx].Name; BackupKey "svc_$nm" "HKLM\SYSTEM\CurrentControlSet\Services\$nm"; Set-Service $nm -StartupType Manual -EA SilentlyContinue; Nota "Servico de terceiro em Manual: $($svc3[$idx].DisplayName)" } }
  }
}

# ---------- [5] RESPONSIVIDADE (registro seguro) ----------
Write-Host "`n[5] Deixando a interface imediata..." -ForegroundColor Green
BackupKey 'Explorer_Advanced' 'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
BackupKey 'ControlPanel_Desktop' 'HKCU\Control Panel\Desktop'
BackupKey 'Explorer_VisualEffects' 'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects'
BackupKey 'DWM' 'HKCU\Software\Microsoft\Windows\DWM'
BackupKey 'Personalize' 'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects' 'VisualFXSetting' 3 'DWord'
SetReg 'HKCU:\Control Panel\Desktop\WindowMetrics' 'MinAnimate' '0' 'String'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'TaskbarAnimations' 0 'DWord'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'ListviewAlphaSelect' 0 'DWord'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'ListviewShadow' 0 'DWord'
SetReg 'HKCU:\Control Panel\Desktop' 'DragFullWindows' '0' 'String'
SetReg 'HKCU:\Software\Microsoft\Windows\DWM' 'EnableAeroPeek' 0 'DWord'
SetReg 'HKCU:\Control Panel\Desktop' 'MenuShowDelay' '150' 'String'
# transparencia: SO o valor unico (a chave Themes\Personalize guarda o modo escuro - NUNCA New-Item -Force nela)
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' 'EnableTransparency' 0 'DWord'
if($win11){ SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'TaskbarDa' 0 'DWord'; SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'ShowCopilotButton' 0 'DWord' }
Nota "Efeitos visuais/animacoes off, menu rapido, transparencia off, widgets/Copilot fora da barra"
if($rank -ge 3 -and $fundo){ SetReg 'HKLM:\SYSTEM\CurrentControlSet\Control' 'WaitToKillServiceTimeout' '2000' 'String'; Nota "Desligamento mais rapido (WaitToKillServiceTimeout=2000)" }

# ---------- [6] SHELL / EXPLORER ----------
Write-Host "`n[6] Faxina do Explorer e menu de contexto..." -ForegroundColor Green
BackupKey 'Explorer_Root' 'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'LaunchTo' 1 'DWord'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer' 'ShowRecent' 0 'DWord'
SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer' 'ShowFrequent' 0 'DWord'
# Automatic Folder Type Discovery off (Explorer para de 'farejar' cada pasta)
SetReg 'HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags\AllFolders\Shell' 'FolderType' 'NotSpecified' 'String'
Nota "Explorer abre em 'Este PC', sem recentes/frequentes, sem farejar tipo de pasta"
# icones fantasma da bandeja (reversivel; explorer reconstroi)
if($win11){ BackupKey 'NotifyIconSettings' 'HKCU\Control Panel\NotifyIconSettings'; reg delete "HKCU\Control Panel\NotifyIconSettings" /f *>$null } else { reg delete "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\TrayNotify" /v IconStreams /f *>$null; reg delete "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\TrayNotify" /v PastIconsStream /f *>$null }
Nota "Icones fantasma da bandeja limpos"
# menu de contexto classico (Agressiva, opt-in por postura) - so no Win11
if($rank -ge 3 -and $win11){ reg add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve *>$null; Nota "Menu de contexto classico (Win10) restaurado" }
# auditar shell handlers MORTOS (DLL some) - Agressiva, interativo
if($rank -ge 3){
  $mortos = @()
  foreach($h in '*','AllFilesystemObjects','Directory','Directory\Background','Folder','Drive'){
    Get-ChildItem "Registry::HKEY_CLASSES_ROOT\$h\shellex\ContextMenuHandlers" -EA SilentlyContinue | ForEach-Object {
      $clsid = (Get-ItemProperty $_.PSPath -EA SilentlyContinue).'(default)'
      if($clsid -match '^{.*}$'){ $dll = (Get-ItemProperty "Registry::HKEY_CLASSES_ROOT\CLSID\$clsid\InprocServer32" -EA SilentlyContinue).'(default)'
        if($dll){ $dllp = [Environment]::ExpandEnvironmentVariables(($dll -replace '"','')); if(($dllp -match '^([A-Za-z]:\\|\\\\)') -and ($dllp -notmatch 'windows\\system32') -and -not (Test-Path $dllp)){ $mortos += [pscustomobject]@{ Hive=$h; Handler=$_.PSChildName; Dll=$dll } } } } }
  }
  if($mortos.Count -gt 0){
    Write-Host "  --- Itens de menu-de-contexto de apps que NAO existem mais (deixam o botao-direito lento) ---" -ForegroundColor Cyan
    for($i=0;$i -lt $mortos.Count;$i++){ Write-Host ("   [{0}] {1}  ({2})" -f ($i+1),$mortos[$i].Handler,$mortos[$i].Hive) }
    $sel = Read-Host "  Numeros pra REMOVER (com backup), ou Enter pra pular"
    foreach($n in ($sel -split ',')){ $idx=([int]($n.Trim()))-1; if($idx -ge 0 -and $idx -lt $mortos.Count){ $m=$mortos[$idx]; reg export "HKCR\$($m.Hive)\shellex\ContextMenuHandlers\$($m.Handler)" "$backup\handler_$($m.Handler).reg" /y *>$null; reg delete "HKCR\$($m.Hive)\shellex\ContextMenuHandlers\$($m.Handler)" /f *>$null; Nota "Handler morto removido: $($m.Handler)" } }
  }
}

# ---------- [7] PRIVACIDADE E ANUNCIOS ----------
if($rank -ge 2){
  Write-Host "`n[7] Privacidade e anuncios do sistema..." -ForegroundColor Green
  BackupKey 'ContentDeliveryManager' 'HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager'
  SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo' 'Enabled' 0 'DWord'
  SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Privacy' 'TailoredExperiencesWithDiagnosticDataEnabled' 0 'DWord'
  SetReg 'HKCU:\Software\Microsoft\Siuf\Rules' 'NumberOfSIUFInPeriod' 0 'DWord'
  SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Search' 'BingSearchEnabled' 0 'DWord'
  foreach($v in 'ContentDeliveryAllowed','SilentInstalledAppsEnabled','SystemPaneSuggestionsEnabled','SoftLandingEnabled','RotatingLockScreenOverlayEnabled','SubscribedContent-338388Enabled','SubscribedContent-338389Enabled','SubscribedContent-338393Enabled','SubscribedContent-353694Enabled','SubscribedContent-353696Enabled'){ SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' $v 0 'DWord' }
  if($win11){ SetReg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'Start_IrisRecommendations' 0 'DWord' }
  Nota "Anuncios do Iniciar/tela de bloqueio/Config desligados; busca web off; ID de anuncio off"
  if($fundo){
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f | Out-Null
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent" /v DisableWindowsConsumerFeatures /t REG_DWORD /d 1 /f | Out-Null
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f | Out-Null
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v StartupBoostEnabled /t REG_DWORD /d 0 /f | Out-Null
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v BackgroundModeEnabled /t REG_DWORD /d 0 /f | Out-Null
    Nota "Telemetria no minimo (em Home/Pro o piso e Basic), consumer features off, Edge sem pre-carga"
  }
}

# ---------- [8] ENERGIA ----------
if($rank -ge 2){
  Write-Host "`n[8] Energia..." -ForegroundColor Green
  if($laptop){ Nota "Notebook: mantido o plano Balanceado (Alto Desempenho na bateria so queima autonomia)" }
  else { powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c *>$null; Nota "Plano Alto Desempenho (desktop)" }
  if($fundo){ $cs = Get-CimInstance Win32_ComputerSystem; if(-not $cs.AutomaticManagedPagefile){ $cs | Set-CimInstance -Property @{AutomaticManagedPagefile=$true} -EA SilentlyContinue; Nota "Pagefile voltou pra 'gerenciado pelo sistema' (o correto)" } }
  # hibernacao reduzida (Equilibrada) libera disco mantendo Fast Startup; Agressiva pergunta se desliga de vez
  if($fundo){
    if($rank -eq 2){ powercfg /h /type reduced *>$null; Nota "Hiberfil.sys reduzido (mantem Inicializacao Rapida, libera disco)" }
    elseif($rank -ge 3){ $r = Read-Host "  Desligar a hibernacao libera varios GB, MAS voce perde a Inicializacao Rapida (boot a frio fica uns segundos mais lento). Desligar? [s/N]"; if($r -match '^[sS]'){ powercfg /h off *>$null; Nota "Hibernacao desligada (hiberfil.sys apagado; reverter: powercfg /h on)" } else { powercfg /h /type reduced *>$null; Nota "Hiberfil.sys reduzido" } }
  }
}

# ---------- [9] MODULOS OPT-IN ----------
if($OtimizarJogos){
  Write-Host "`n[jogos] Limpando shader cache (regeneravel; NUNCA toca mod/save)..." -ForegroundColor Green
  $sh = @("$env:LOCALAPPDATA\NVIDIA\DXCache","$env:LOCALAPPDATA\NVIDIA\GLCache","$env:LOCALAPPDATA\NVIDIA\NV_Cache","$env:ProgramData\NVIDIA Corporation\NV_Cache",
          "$env:LOCALAPPDATA\AMD\DxCache","$env:LOCALAPPDATA\AMD\DxcCache","$env:LOCALAPPDATA\AMD\VkCache","$env:ProgramData\Intel\ShaderCache",
          "$env:LOCALAPPDATA\D3DSCache","$env:LOCALAPPDATA\Microsoft\D3DSCache")
  $steam=(Get-ItemProperty 'HKCU:\Software\Valve\Steam' -EA SilentlyContinue).SteamPath; if($steam){ $sh += (Join-Path $steam 'steamapps\shadercache') }
  $n=0; foreach($p in $sh){ if(Test-Path $p){ LimparPastaConteudo $p; $n++ } }
  Nota "Shader cache limpo em $n local(is) (regenera sozinho no proximo jogo)"
  SetReg 'HKCU:\System\GameConfigStore' 'GameDVR_Enabled' 0 'DWord'
  SetReg 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR' 'AppCaptureEnabled' 0 'DWord'
  if($fundo){ reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f | Out-Null }
  SetReg 'HKCU:\Software\Microsoft\GameBar' 'AutoGameModeEnabled' 1 'DWord'
  Nota "Gravacao em segundo plano (Game DVR) desligada; Game Mode confirmado ligado"
  if($rank -ge 3 -and $fundo){ SetReg 'HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers' 'HwSchMode' 2 'DWord'; Nota "HAGS ligado (teste on/off; obrigatorio pra DLSS Frame Gen; reboot)" }
}
if($DesinstalarBloatware -and $admin){
  Write-Host "`n[debloat] Apps que vieram de fabrica..." -ForegroundColor Green
  Get-AppxPackage -AllUsers | Select-Object Name,PackageFullName | Out-File "$backup\appx-antes.txt"
  $denyAppx = 'Store|VCLibs|NET\.Native|UI\.Xaml|AppRuntime|ShellExperience|StartMenuExperience|SecHealth|DesktopAppInstaller|Edge|CBS|AAD|AccountsControl|LockApp|CredDialog'
  $cand = @('Microsoft.BingNews','Microsoft.BingWeather','Microsoft.GetHelp','Microsoft.Getstarted','Microsoft.MicrosoftSolitaireCollection','Microsoft.MicrosoftOfficeHub','Microsoft.Office.OneNote','Microsoft.People','Microsoft.WindowsMaps','Microsoft.WindowsAlarms','Microsoft.WindowsFeedbackHub','Microsoft.SkypeApp','Microsoft.ZuneMusic','Microsoft.ZuneVideo','Microsoft.Todos','Microsoft.MicrosoftStickyNotes','MicrosoftCorporationII.QuickAssist','Clipchamp.Clipchamp','Microsoft.PowerAutomateDesktop','5A894077.McAfeeSecurity')
  $inst = @(); foreach($c in $cand){ if((Get-AppxPackage -AllUsers $c) -and $c -notmatch $denyAppx){ $inst += $c } }
  if($inst.Count -gt 0){
    for($i=0;$i -lt $inst.Count;$i++){ Write-Host ("   [{0}] {1}" -f ($i+1),$inst[$i]) }
    $sel = Read-Host "  Numeros pra REMOVER (virgula), Enter pra pular"
    foreach($n in ($sel -split ',')){ $idx=([int]($n.Trim()))-1; if($idx -ge 0 -and $idx -lt $inst.Count){ $nm=$inst[$idx]; Get-AppxPackage -AllUsers $nm | Remove-AppxPackage -AllUsers -EA SilentlyContinue; Get-AppxProvisionedPackage -Online | Where-Object DisplayName -eq $nm | Remove-AppxProvisionedPackage -Online -EA SilentlyContinue; Nota "App removido: $nm (reinstala pela Store)" } }
  } else { Nota "Nenhum app de consumo removivel encontrado" }
}
if($RepararSistema -and $admin){
  Write-Host "`n[reparo] Checando integridade do sistema..." -ForegroundColor Green
  Write-Host "  Verificando e reparando (demora, precisa de internet)..." -ForegroundColor Yellow
  DISM /Online /Cleanup-Image /ScanHealth | Out-Null
  DISM /Online /Cleanup-Image /RestoreHealth
  sfc /scannow | Out-Null
  Nota "Integridade do sistema verificada e reparada se preciso (DISM RestoreHealth + sfc)"
}
if($ResetarRede -and $admin){
  Write-Host "`n[rede] Reset da pilha de rede (CONSERTO)..." -ForegroundColor Green
  ipconfig /all > "$backup\rede-antes.txt"
  Nota "Config de rede salva em rede-antes.txt (se usava IP/DNS fixo, reconfigure depois)"
  netsh winsock reset *>$null; netsh int ip reset "$backup\resetlog.txt" *>$null; netsh int ipv6 reset *>$null
  Nota "Pilha de rede resetada pro padrao - PRECISA REINICIAR pra valer"
}
if($PassarAntivirus -and (Get-Command Start-MpScan -EA SilentlyContinue)){
  Write-Host "`n[antivirus] Varredura rapida do Defender..." -ForegroundColor Green
  Update-MpSignature -EA SilentlyContinue; Start-MpScan -ScanType QuickScan; Nota "Varredura rapida do Defender concluida"
}

# reinicia o explorer pra aplicar visual/shell
Stop-Process -Name explorer -Force -EA SilentlyContinue; Start-Sleep 1; if(-not (Get-Process explorer -EA SilentlyContinue)){ Start-Process explorer }

# ---------- [10] SANIDADE + RECIBO ----------
Write-Host "`n[10] Conferindo que o PC continua saudavel..." -ForegroundColor Green
$san = @()
$san += "Defender: " + $(if((Get-MpComputerStatus -EA SilentlyContinue).RealTimeProtectionEnabled){'[VERDE] ligado'}else{'[CONFERIR]'})
$wu = Get-Service wuauserv -EA SilentlyContinue; $san += "Windows Update: " + $(if(-not $wu){'[CONFERIR] ausente'}elseif($wu.StartType -ne 'Disabled'){'[VERDE] ok'}else{'[VERMELHO] desativado'})
$ws = Get-Service WSearch -EA SilentlyContinue; $san += "Busca (WSearch): " + $(if(-not $ws){'[CONFERIR] ausente'}elseif($ws.Status -eq 'Running' -or $ws.StartType -ne 'Disabled'){'[VERDE] ok'}else{'[AMARELO] parada'})
$san += "Internet: " + $(if(Test-Connection 1.1.1.1 -Count 2 -Quiet){'[VERDE] ok'}else{'[AMARELO] sem resposta'})

$c1 = Get-PSDrive C
$startupDepois = (Get-CimInstance Win32_StartupCommand).Count
$liberado = MB($c1.Free - $freeInicio)
$r = New-Object System.Collections.ArrayList
[void]$r.Add("# Acelera PC - recibo de $(Get-Date -Format 'dd/MM/yyyy HH:mm')")
[void]$r.Add("")
[void]$r.Add("Modo: $Modo | Postura: $Postura | admin: $admin | ponto de restauracao: $temRestore")
[void]$r.Add("")
[void]$r.Add("## Antes e depois")
[void]$r.Add("Programas no boot (Run/Startup): $startupAntes -> $startupDepois  (tarefas e servicos desligados nao entram nesta conta)")
[void]$r.Add("Disco C livre: $freeAntesGB GB -> $([math]::Round($c1.Free/1GB,1)) GB   (liberou ~$liberado MB)")
[void]$r.Add("")
[void]$r.Add("## O que fiz")
foreach($l in $log){ [void]$r.Add("- $l") }
[void]$r.Add("")
[void]$r.Add("## Sanidade (pos-otimizacao)")
foreach($l in $san){ [void]$r.Add("- $l") }
[void]$r.Add("")
[void]$r.Add("## Como desfazer")
if($temRestore){ [void]$r.Add("- Voltar TUDO: rodar rstrui.exe e escolher 'Antes de Acelera-PC'") }
[void]$r.Add("- Desfazer um ajuste: dar 2 cliques num .reg em $backup")
[void]$r.Add("- Servico: reg import do svc_<nome>.reg em $backup (volta o tipo original)")
[void]$r.Add("- Tarefa agendada desligada: Enable-ScheduledTask -TaskName <nome> -TaskPath <caminho> (ou pelo Agendador de Tarefas)")
[void]$r.Add("- App removido: reinstalar pela Microsoft Store")
[void]$r.Add("- Lixo/cache apagado nao volta, mas era descartavel/regeneravel")
[void]$r.Add("")
[void]$r.Add("## A verdade sobre o ganho")
[void]$r.Add("A sensacao de recem-formatado vem de: menos programa e servico no boot, disco com")
[void]$r.Add("espaco, menos coisa rodando escondida e a interface mais imediata. Isso foi mexido de")
[void]$r.Add("verdade. Os 'super tweaks' de milagre (registry cleaner, RAM booster, pagefile off,")
[void]$r.Add("Superfetch off, timer resolution) sao placebo/risco e ficaram DE FORA de proposito.")
[void]$r.Add("")
[void]$r.Add("## Rodar de novo")
[void]$r.Add("Semana que vem, use o acelera-pc.bat (limpeza leve). O Setup completo so vale refazer")
[void]$r.Add("de vez em quando (ou depois de um feature update grande, que reseta alguns ajustes).")
$reciboPath = "$env:USERPROFILE\Desktop\acelera-pc-recibo.txt"
$r | Set-Content -Path $reciboPath -Encoding UTF8

Write-Host "`n===============================================" -ForegroundColor Green
Write-Host "  PRONTO" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ("Boot: {0} -> {1} | liberou ~{2} MB | disco livre: {3} GB" -f $startupAntes,$startupDepois,$liberado,[math]::Round($c1.Free/1GB,1))
foreach($l in $san){ Write-Host "  $l" }
Write-Host "Recibo: $reciboPath  |  Backups (desfazer): $backup"
if($ResetarRede){ Write-Host "REINICIE agora - o reset de rede so vale apos reboot." -ForegroundColor Yellow }
Write-Host "Reinicie o PC pra alguns ajustes valerem." -ForegroundColor Cyan
