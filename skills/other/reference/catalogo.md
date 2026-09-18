# catalogo.md — todas as otimizações, por categoria

Este é o mapa do que o motor `assets/acelera-pc.ps1` faz. Toda técnica traça pra uma fonte real.
Legenda de ganho HONESTO:
`sensacao` (fluidez percebida) · `velocidade` (mensurável) · `espaco` (só disco) · `privacidade` ·
`manutencao` · `placebo` (marcado e RECUSADO). **Setup** = pacote uma-vez. **Semanal** = o .bat leve.

Regra de ouro (vale o motor inteiro): **nunca `New-Item -Force` numa chave de registro existente** —
recria vazia e apaga os valores. Todo registro passa pela função `SetReg` (cria a chave só se faltar).

---

## 1. Faxina de disco profunda (Setup: tudo; Semanal: temp + cache de app + DNS)
Honesto: liberar espaço dá ESPAÇO, não velocidade — só ajuda a velocidade quando o disco tá quase cheio.
- Temp do usuário (`%TEMP%`) e do sistema (`C:\Windows\Temp`). Fonte: windowsforum.
- Cache do Windows Update (`SoftwareDistribution\Download`, parando wuauserv/bits), Delivery Optimization
  (`Delete-DeliveryOptimizationCache`). WER (ReportQueue/Archive), crash dumps (Minidump), INetCache,
  cache de miniaturas, D3DSCache, arquivos recentes/jump lists.
- SCANNER GENÉRICO de cache de apps Chromium/Electron: varre `%LOCALAPPDATA%`+`%APPDATA%` (profundidade 4)
  por subpastas `Cache`/`Code Cache`/`GPUCache`/`blob_storage`, PULANDO `User Data\...\Login Data|Cookies|Web
  Data` e `LocalState` (senha/login preservados). Pega navegadores, Discord, Teams, Spotify, etc. de uma vez.
- Caches de dev (npm/pip/NuGet) só se a ferramenta existir. Cache da Store (LocalCache, sem popup).
- Component store WinSxS: `DISM /StartComponentCleanup` (Equilibrada+; NUNCA `/ResetBase` no automático).
- Lixeira: SÓ com confirmação mostrando itens (contém arquivo do usuário). Windows.old: caminho GUI opt-in.
- TRIM (SSD) via `Optimize-Volume -ReTrim` / defrag (HDD) — com detecção de disco derivada do C: direto
  (`Get-Partition C | Get-Disk | Get-PhysicalDisk`), NUNCA defrag em SSD. Fonte: learn.microsoft.

## 2. Boot e segundo plano (Setup) — a MAIOR alavanca real
- Apps em segundo plano off (`BackgroundAccessApplications\GlobalUserDisabled=1`).
- Startup interativo: lista `Win32_StartupCommand`, usuário escolhe o que desligar (backup das chaves Run).
- Tarefas de telemetria/CEIP desligadas (`Disable-ScheduledTask`: Compatibility Appraiser, ProgramDataUpdater,
  Consolidator, UsbCeip, DiskDiagnostic, Autochk\Proxy). Fonte: Win11Debloat.
- **Tarefas de logon de TERCEIROS** (updaters Google/Adobe/Edge/OEM) — lista interativa, desliga (não deleta).
- `StartupDelayInMSec` fica FORA do default (é sensação, pode travar mais o desktop no login) — só via edição
  manual do toggle na Agressiva, com aviso.

## 3. Serviços (Setup, admin) — Manual, nunca em massa
- MS raramente usados → Manual/Disabled com backup do Start: RetailDemo, MapsBroker, Fax, WMPNetworkSvc,
  lfsvc, WpcMonSvc, PhoneSvc, RemoteRegistry, dmwappushservice. DiagTrack (telemetria) → Disabled.
- **Serviços de TERCEIROS em Automatic+Running** (updaters/helpers) — lista interativa → Manual, com backup.
  Denylist de terceiros no aviso: antivírus ativo, serviço da GPU, áudio do fabricante, VPN, chipset.
- Prefere `Manual` a `Disabled` (sobe sob demanda). DENYLIST de serviços core em `seguranca-e-mitos.md`.
  Fonte: learn.microsoft (IoT optimize/services).

## 4. Responsividade (registro seguro, HKCU) — sensação
`VisualFXSetting=3` (custom), `MinAnimate=0`, `TaskbarAnimations=0`, `ListviewAlphaSelect/Shadow=0`,
`DragFullWindows=0`, `EnableAeroPeek=0`, `MenuShowDelay=150`, `EnableTransparency=0` (SÓ o valor único —
nunca `New-Item -Force` na chave Themes\Personalize), `TaskbarDa=0` (widgets, Win11), `ShowCopilotButton=0`.
`WaitToKillServiceTimeout=2000` (Agressiva; só acelera o DESLIGAMENTO). Backups .reg das chaves-pai. Fonte:
winutil Chris Titus, theregister, elevenforum.

## 5. Shell / Explorer / menu de contexto (Setup) — sensação de fluidez
- Abrir em "Este PC" (`LaunchTo=1`), sem recentes/frequentes, Automatic Folder Type Discovery off
  (`Bags\AllFolders\Shell\FolderType=NotSpecified` — Explorer para de "farejar" cada pasta).
- Ícones fantasma da bandeja limpos (com backup). Menu de contexto clássico do Win10 (Agressiva opt-in).
- **Handlers de menu-de-contexto MORTOS** (de apps desinstalados que travam o botão-direito): lista
  interativa (Agressiva), só marca morto se a DLL for caminho ABSOLUTO e sumiu (expande env vars), remove
  com backup .reg. Fonte: elevenforum, winutil.

## 6. Privacidade e anúncios (Equilibrada+) — privacidade, NÃO velocidade
`AdvertisingInfo\Enabled=0`, Tailored experiences, Feedback=Never, bloco ContentDeliveryManager (anúncios do
Iniciar/tela de bloqueio/Config), `Start_IrisRecommendations=0`, `BingSearchEnabled=0`. Policies (admin):
`AllowTelemetry=0` (honesto: em Home/Pro o piso é Basic), `DisableWindowsConsumerFeatures`, WER off, Edge
StartupBoost/BackgroundMode off. Fonte: pdq, winaero, elevenforum, learn.microsoft (Edge policies).

## 7. Energia (Equilibrada+) — sensação (desktop) / cuidado (laptop)
Plano Alto Desempenho só em DESKTOP (laptop mantém Balanceado — na bateria só queima autonomia). Pagefile
garantido "gerenciado pelo sistema" (NUNCA desligar). Hiberfil: reduzido na Equilibrada (mantém Fast Startup,
libera disco); Agressiva pergunta se desliga de vez (`powercfg /h off`, com aviso do tradeoff). Fonte: ninjaone.

## 8. Módulos opt-in
- **Jogos** (`jogos.md`): shader cache de todos (NVIDIA/AMD/Intel/DirectX/Steam) com Test-Path; Game DVR off;
  Game Mode confirmado ligado; HAGS (Agressiva). DENYLIST de save/mod/config rígida.
- **Debloat** (`programas.md`): appx de consumo (lista segura, checa existência, interativo) + provisionados;
  Win32/OEM. DENYLIST forte.
- **Reparar sistema**: `DISM /ScanHealth` + `/RestoreHealth` + `sfc /scannow` (idempotente, não depende de
  texto localizado). **Rede** (conserto): salva `ipconfig /all` antes, reset winsock/ip/ipv6, exige reboot.
  **Antivírus**: `Update-MpSignature` + `Start-MpScan QuickScan`.

## Mapa por postura
- **Conservadora**: faxina + responsividade (HKCU) + shell básico. Roda sem admin.
- **Equilibrada**: + component store, serviços (MS+terceiros), telemetria, tarefas, energia, privacidade, hiberfil reduzido.
- **Agressiva**: + WaitToKill, menu clássico, handlers mortos, HAGS, hibernação-off (com aviso). Honesto no
  recibo: "agressivo entrega quase o mesmo que equilibrado; os super-tweaks de milagre ficaram DE FORA".

Tudo o que é `placebo` foi RECUSADO — ver `seguranca-e-mitos.md`.
