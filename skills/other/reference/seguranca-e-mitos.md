# seguranca-e-mitos.md — a espinha de honestidade e segurança

Três coisas: (1) as regras de segurança, (2) as DENYLISTS, (3) os mitos/placebo que a skill RECUSA.

---

## Regra de ouro (vale o motor inteiro)
**NUNCA `New-Item -Force` numa chave de registro que já existe.** Em qualquer chave existente, o `-Force`
recria a chave VAZIA e apaga os valores/subchaves. Isso já queimou o usuário: apagou `AppsUseLightTheme`/
`SystemUsesLightTheme` na chave `Themes\Personalize` e jogou o Windows/VS Code/Chrome pro tema branco. O
mesmo footgun reapareceu nas chaves `Search` e `Serialize` durante a pesquisa. Padrão obrigatório: a função
`SetReg` faz `if(-not (Test-Path X)){ New-Item X -Force }` e só então `Set-ItemProperty` — ou seja, só cria a
chave quando ela FALTA, nunca recria uma existente. Alternativa segura: `reg add ... /v <valor>` (nunca
recria a chave). A chave `Themes\Personalize` só recebe `EnableTransparency` via `SetReg` (valor único).

## Rede de segurança (Setup — roda ANTES de qualquer coisa moderada)
Ordem: `Enable-ComputerRestore C:\` → zerar `SystemRestorePointCreationFrequency`=0 → `Checkpoint-Computer`
→ CONFIRMAR via `Get-CimInstance -Namespace root/default -ClassName SystemRestore` → devolver a frequência
pra 1440 (não churnar o VSS). Backup `.reg` de cada chave antes de tocar (pasta `Desktop\acelera-pc-backup`).
Serviços/tarefas de terceiros: backup do Start original antes de mudar. **ABORT:** se o ponto não for
confirmado (sem admin, Restore off por OEM), `$fundo=$false` e só o subconjunto seguro+reversível roda.
NUNCA `vssadmin delete shadows /all` no automático (destruiria o próprio ponto). Fonte: learn.microsoft.

O que o restore point cobre: registro, serviços, config, drivers. NÃO cobre: exclusão de arquivo (temp,
cache, Windows.old), remoção de appx, component store. Esses dependem do undo próprio de cada item.

## Modo Semanal ≠ Setup
O `.bat` semanal roda SÓ o reversível/inofensivo (temp, cache de app, DNS, TRIM, reiniciar Start/Search).
NÃO cria ponto de restauração (seria teatro — nada ali é irreversível), NÃO mexe em registro/serviço/debloat,
e NÃO esvazia a Lixeira no automático. Tweak e debloat rodam SÓ no Setup (uma vez); repetir toda semana é
inútil (idempotente) ou quebra update que reinstala app. Fonte: windowsforum.

## Checklist de sanidade (pós-run, no recibo)
Defender ligado, Windows Update não-Disabled, WSearch ok, internet responde — cada um com TAG
[VERDE]/[AMARELO]/[VERMELHO]/[CONFERIR]. Se algo falhar → `rstrui.exe`.

---

## DENYLIST de serviços — NUNCA tocar (quebram o PC)
RpcSs, RpcEptMapper, DcomLaunch, Dhcp, Dnscache, nsi, NlaSvc, BFE, mpssvc, WinDefend, WdNisSvc,
SecurityHealthService, wscsvc, Sense, CryptSvc, KeyIso, VaultSvc, SamSs, EventLog, Winmgmt, gpsvc, ProfSvc,
UserManager, LSM, Power, PlugPlay, DeviceInstall, Schedule, TrustedInstaller, msiserver, UsoSvc,
WaaSMedicSvc, BrokerInfrastructure, CoreMessagingRegistrar, SystemEventsBroker, FontCache, Audiosrv,
AudioEndpointBuilder, W32Time, SysMain, DoSvc, DPS, WdiSystemHost, WSearch. Terceiros a NÃO tocar: antivírus
ativo, serviço da GPU (NVIDIA Display Container / AMD External Events), áudio do fabricante (Realtek/Nahimic),
VPN, chipset. Fonte: learn.microsoft (IoT optimize/services).

## DENYLIST de appx — NUNCA remover
Store, StorePurchaseApp, DesktopAppInstaller (winget), VCLibs.*, NET.Native.*, UI.Xaml.*, WindowsAppRuntime.*,
ShellExperienceHost, StartMenuExperienceHost, SecHealthUI (Defender), AAD.BrokerPlugin, AccountsControl,
LockApp, Win32WebViewHost, CredDialogHost, Client.CBS/Core, Edge/WebView2. Regra: se o nome tem VCLibs,
NET.Native, Xaml, AppRuntime, Store, ShellExperience, StartMenuExperience — pula. Fonte: patchmypc, Win11Debloat.

## DENYLIST de pastas de jogo — NUNCA apagar (save/mod/config)
`Saved Games\*`, `Documents\My Games\*`, `AppData\LocalLow\*`, `steamapps\common\*` (jogos), `steamapps\userdata`
(saves na nuvem), `steamapps\workshop` (mods), qualquer pasta `mods`/`saves`/`profiles`/`config`/`savegames`.
Só limpa pasta cujo nome é literalmente de cache (`shadercache`/`DXCache`/`GLCache`/`D3DSCache`/`NV_Cache`/
`VkCache`/`DxcCache`), e só o CONTEÚDO. Fonte: pcgamingwiki.

---

## Mitos e placebo — a skill RECUSA (com fonte). Se o usuário pedir, explica em 1 linha por que não.
1. **Registry cleaner** (CCleaner registry, Wise, Advanced SystemCare) — Microsoft não suporta, não acelera,
   pode apagar chave viva. Fonte: xda, learn.microsoft.
2. **RAM booster / memory cleaner** — o Windows gerencia RAM melhor; esvaziar cache útil deixa o próximo uso
   mais lento. O dev do CleanMem admitiu que "não faz nada". Fonte: xda.
3. **Desligar o pagefile** — zero ganho, deixa instável sob pressão de memória, quebra crash dump. Fonte: makeuseof.
4. **MSConfig "número de processadores"** — o Windows já usa todos; a caixa só LIMITA. Fonte: makeuseof.
5. **SysMain/Prefetch off em SSD** — o Windows já ajusta; desligar pode deixar apps frequentes mais lentos. Fonte: thewindowsclub.
6. **Timer resolution / desabilitar HPET pra FPS** — placebo/pode piorar latência DPC. Fonte: blurbusters, xda.
7. **Desabilitar TCP Auto-Tuning / "20% de banda reservada" (QoS) / desligar RSS/IPv6** — a MS diz que
   autotuning off "limita a velocidade e não melhora"; os 20% é mito de 20 anos; RSS off piora em multicore. Fonte: learn.microsoft, howtogeek.
8. **Script one-click "ultimate debloat"** — quebra Update/Store/apps, ganho negligível em hardware moderno,
   difícil de reverter. A skill é cirúrgica, item a item, com undo. Fonte: windowsforum, makeuseof.
9. **Apagar System32/WinSxS na mão / esvaziar C:\Windows\Installer** — destrói o Windows. WinSxS usa hardlink;
   só `DISM /StartComponentCleanup`. Fonte: learn.microsoft ("may severely damage your system").
10. **`DISM /ResetBase` como rotina** — irreversível pros updates já instalados; consolidação pontual, não rotina.
11. **Limpar Prefetch / Event Logs "pra acelerar"** — placebo; Prefetch se auto-mantém e existe pra apps
    abrirem MAIS rápido; apagar log destrói diagnóstico. Fonte: edbott, woshub.
12. **Desabilitar Armazenamento Reservado como rotina** — pode fazer feature update FALHAR se não reativar.
    Fora do padrão. Fonte: winutil.
13. **AutoEndTasks / UserPreferencesMask cru / Win32PrioritySeparation / DisablePagingExecutive** — perigoso ou
    placebo (perde trabalho não salvo, corrompe UI, ganho imperceptível). Fonte: howtogeek, winutil.

### A verdade sobre o ganho (dizer no recibo, sempre)
A sensação de recém-formatado vem de: menos programa E serviço no boot, disco com espaço, menos coisa rodando
escondida, e a interface mais imediata. Tweak de registro de "performance" é, na maioria, ruído dentro da
margem. Limpeza dá espaço, não velocidade. Telemetria off é privacidade. A skill promete isso e nada além.
Fonte: xda ("debloat myths"), howtogeek ("10 tweaking myths").

---

## Reverter (modo `reverter`)
1. `Glob .claude/acelera-pc/*-recibo*` ou o `acelera-pc-recibo.txt` no Desktop → mostrar o nome/data do ponto.
2. Voltar tudo: `rstrui.exe` → escolher "Antes de Acelera-PC".
3. Desfazer um ajuste: dar 2 cliques num `.reg` em `Desktop\acelera-pc-backup\` (registro e serviço).
4. Tarefa desligada: `Enable-ScheduledTask -TaskName <nome> -TaskPath <caminho>`.
5. App removido: reinstalar pela Store. Exclusão de arquivo (classe B) não volta — mas era descartável.
