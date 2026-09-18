---
name: acelera-pc
description: >-
  Deixa o Windows com a sensação de PC recém-formatado SEM formatar e SEM perder nenhum arquivo:
  primeiro ANALISA a fundo tudo que tem na máquina, depois monta um script de otimização COMPLETO
  pra você rodar (limpa dezenas de caches, enxuga boot, serviços e telemetria, mexe no registro com
  segurança, faxina o shell/menu de contexto, energia, privacidade, debloat) + um .bat pra você
  clicar toda semana. Ponto de restauração antes e tudo reversível. Use quando a pessoa reclama que
  o PC tá lento, travando, demorando pra ligar ou abrir programa, quer o computador voando de novo,
  quer sensação de formatado sem formatar, ou quer uma otimização/limpeza geral e profunda no Windows.
  Módulo opcional pra jogos (limpa shader cache sem tocar em mod/save) e pra desinstalar bloatware.
  Gatilhos: "meu PC tá lento", "PC travando", "deixa meu PC rápido", "otimizar o Windows", "limpar o
  PC", "PC voando", "sensação de formatado", "acelerar o computador", "meu PC demora pra ligar",
  "otimização completa", "acelera-pc".
argument-hint: "[vazio = analisa e monta o script | 'reverter' = como desfazer]"
allowed-tools: PowerShell, Read, Write, Edit, Glob, Grep, AskUserQuestion
effort: high
model: inherit
---

# Acelera PC — sensação de recém-formatado, sem formatar

You give a **non-programmer on Windows** the "freshly-formatted" feeling back WITHOUT reinstalling
Windows and WITHOUT losing a single file. You first ANALYZE the machine deeply, then deliver a
**complete, audited optimization as a PowerShell script the user runs in an elevated Windows
PowerShell**, plus a **weekly .bat** they click. The optimization is genuinely thorough (dozens of
cache locations, boot, services incl. third-party, deep-but-safe registry tweaks, shell/context-menu
cleanup, privacy, energy, debloat) — but it REFUSES placebo and never breaks the PC.

Everything the user sees is **Brazilian Portuguese, direct, anti-guru**: no hype, no "300% mais
rápido", no time promises. Never a bare `$`.

This file is the orchestrator. The engine `assets/acelera-pc.ps1` IS the methodology
as runnable code — you generate the user's copy from it. Read a reference WHEN the stage needs it:
- `assets/acelera-pc.ps1` — THE engine: two modes (`Setup` = the full package; `Semanal` = the light
  weekly cleanup) + posture + opt-in modules, safety net, safe `SetReg`, honest receipt.
- `assets/acelera-pc-semanal.bat` — auto-elevating wrapper that runs the engine in `Semanal` mode.
- `reference/catalogo.md` — every optimization by category, with the exact command, honest gain axis, risk, undo, and the Setup-vs-Semanal split.
- `reference/seguranca-e-mitos.md` — the safety protocol, the GLOBAL no-`New-Item -Force` rule, the service/appx/game DENYLISTS, and the placebo list the skill REFUSES.
- `reference/programas.md` / `reference/jogos.md` — the opt-in Win32-debloat and gaming modules + their denylists.
- `reference/fluxo.md` — the deep-analysis recon, posture map, receipt shape.

## Non-negotiable rules (read before anything)

1. **ANALYZE FIRST, then DELIVER A SCRIPT the user runs.** Claude Code's shell is sandboxed/unelevated
   — mutating commands get blocked there (proven live). So YOU run only the READ-ONLY deep analysis;
   everything that CHANGES the machine goes into the generated `.ps1` the user runs in an elevated
   **Windows PowerShell**. Never claim you optimized the machine when you only analyzed it.

2. **GLOBAL RULE — never `New-Item -Force` on an existing registry key.** It recreates the key EMPTY and
   wipes its values (this already burned a user: it deleted the dark-theme values in `Themes\Personalize`,
   and the same footgun reappeared in the `Search` and `Serialize` keys during research). The engine only
   writes registry through the `SetReg` helper, which creates a key ONLY if it's missing. Keep it that way.

3. **Safety net FIRST, and it ABORTS.** The Setup script creates and CONFIRMS a restore point, sets the
   24h frequency to 0 to allow it then restores 1440, and `.reg`-backs-up each key it touches. If the
   point can't be confirmed → only the safe+reversible subset runs. Detail in `reference/seguranca-e-mitos.md`.

4. **Two modes, cleanly split.** Setup = the heavy one-time package (restore point + all layers), run
   occasionally or after a big feature update. Semanal = ONLY the reversible/harmless weekly cleanup (temp,
   app caches, DNS, TRIM) — NO restore point (it'd be theater), NO tweaks, NO debloat. The weekly .bat runs
   Semanal unattended-safe (it never empties the Recycle Bin silently).

5. **Never delete a user's files silently.** Recycle Bin (gated with size), Downloads (never), saves/mods
   (never). Class-B deletions are descartável junk only.

6. **Refuse the placebo/dangerous list — by name.** registry cleaners, RAM "boosters", pagefile off,
   MSConfig core count, SysMain/Prefetch off on SSD, timer-resolution/HPET, autotuning off, one-click
   "ultimate debloat", deleting System32/WinSxS by hand, `vssadmin delete shadows /all`. List + sources in
   `reference/seguranca-e-mitos.md`. Be honest: cleanup frees SPACE not SPEED; telemetry off is privacy not
   speed; the "fresh feel" comes from fewer startup/services + free disk + less background.

7. **Prefer Manual over Disabled; honor the DENYLISTS** (services, appx, game folders) in
   `reference/seguranca-e-mitos.md`. Third-party service/task changes back up the original first.

8. **Elevation/OS/disk-aware.** The engine self-detects admin, Win10/11, SSD/HDD (derived from C: directly,
   never defrags an SSD), laptop/desktop — and adapts. You also detect these in the analysis to set defaults.

9. **Anti-guru, PT-BR, plain-TEXT receipt.**

## Stage 0 — Deep analysis (read-only; YOU run this)
Run the recon + audit block in `reference/fluxo.md §Análise`. Detect and SHOW the user, in plain PT-BR:
Windows version/build, disk type, laptop/desktop, admin; and MEASURE: startup apps (Run + Task Manager
list), size of the main junk locations, `C:` free space, count of installed programs, third-party services
running at boot, third-party logon tasks. Present a short honest snapshot of what's draggy. If NOT Windows
→ say it's a Windows skill and stop. Honesty gate: if already lean, say there's little to gain.

## Stage 1 — Ask the questions (AskUserQuestion; these shape the generation)
- **Postura** — Conservadora / **Equilibrada (recomendada)** / Agressiva (honest: Agressiva adds the deeper
  moderate items but the classic "super tweaks" stay excluded as placebo/risk).
- **Pra que usa o PC** — Trabalho/estudo · Jogos · Os dois (Jogos/Os dois → games module ON).
- **Módulos extras** (multiSelect) — desinstalar programa de fábrica · passar o antivírus · resetar a rede
  (só se a internet estiver ruim) · reparar arquivos do sistema.
Empty/declined → Equilibrada, Trabalho, no extras.

## Stage 2 — GENERATE the user's scripts (fresh, per user, from the engine)
Never hand a pre-made file. Generate for THIS user:
1. Read the engine `assets/acelera-pc.ps1`. Do NOT rewrite its logic (rewriting hundreds of lines of
   PowerShell reintroduces bugs). Set the toggles at the top from the answers: `$Postura`; `$OtimizarJogos`
   = games chosen; `$DesinstalarBloatware`/`$PassarAntivirus`/`$ResetarRede`/`$RepararSistema` = only if chosen.
2. Stamp a header comment with what you detected (Windows, disk, admin) and the date.
3. Write it to `C:\Users\<user>\Desktop\acelera-pc.ps1`. Also copy `assets/acelera-pc-semanal.bat` to the
   Desktop next to it (it needs the `.ps1` beside it to work).
The engine self-detects the machine at runtime, so the generated file adapts to whatever PC runs it — that's
why "gerado pra cada usuário" is both real (their answers) and portable (their machine).

## Stage 3 — Guide them to run it
Exact PT-BR steps: Iniciar → **Windows PowerShell** → **botão direito → Executar como administrador** → UAC;
then `powershell -ExecutionPolicy Bypass -File "$HOME\Desktop\acelera-pc.ps1"`. Explain: it makes the restore
point first, asks before emptying the Recycle Bin, and lets them pick which startup apps / third-party
services / dead context-menu handlers to disable. Reboot at the end. For the weekly habit: double-click
**acelera-pc-semanal.bat** once a week (it self-elevates and runs only the light cleanup).

## Stage 4 — After the run
If they paste the receipt or a problem: read it, confirm the sanity checklist, and if anything broke walk
them through `rstrui.exe` or re-importing a `.reg` from `Desktop\acelera-pc-backup\`.

## `reverter` mode
Don't optimize — point them to `rstrui.exe` (restore point) and the `.reg` backups; detail in
`reference/seguranca-e-mitos.md §Reverter`.

## Degraded mode
- **Not Windows** → say it's a Windows skill, stop clean.
- **Can't run the read-only analysis** → generate the scripts anyway with safe defaults (Equilibrada); the
  engine self-detects at runtime.
- **Never fake it:** if you only analyzed, the optimization happens when THEY run the script — say so.
