# jogos.md — módulo opt-in: otimizar jogos SEM tocar em mod/save/patch

Só roda se o usuário aceitou no Stage 2. Regra suprema deste módulo: **shader cache é regenerável e pode
apagar; save/mod/config/patch NUNCA se toca.** As duas coisas convivem no mesmo `%LOCALAPPDATA%`/`%APPDATA%`,
então só apagar pasta cujo NOME LITERAL é de cache. Fonte-base: NVIDIA/Steam/Microsoft (URLs por item).

Escopo declarado (dizer ao usuário): este módulo cobre **cache de shader (Windows/NVIDIA/AMD/Steam) +
Game DVR + dica de driver GPU**. Epic/GOG/EA/Ubisoft têm cache próprio mas NÃO estão cobertos a fundo aqui.

---

## DENYLIST — pastas que a skill JAMAIS apaga (são save/mod/config)

Nunca apagar, nunca oferecer apagar:
- `Documentos\My Games\*` e `%USERPROFILE%\Saved Games\*` (saves)
- `%USERPROFILE%\AppData\LocalLow\*` (saves de Unity/muitos jogos)
- qualquer `%APPDATA%\<Jogo>` ou `%LOCALAPPDATA%\<Jogo>` que NÃO seja literalmente uma pasta `*Cache`
- a pasta de instalação do jogo: `steamapps\common\*`
- pastas `mods`/`Mods`/`saves`/`save`/`profiles`/`config` dentro do jogo
- `steamapps\...\userdata` (guarda saves na nuvem da Steam)
Fonte: pesquisa Stage-3 (gaming lane).

---

## 1. Limpar shader cache (regenerável) — Ganho: espaço/troubleshooting · NÃO dá FPS extra

Fechar TODOS os jogos e launchers antes. Apagar o CONTEÚDO, não a pasta. Detecção DINÂMICA (os caminhos
variam por driver) — só apagar o que `Test-Path` confirmar:
```powershell
$alvos = @(
  "$env:LOCALAPPDATA\NVIDIA\DXCache",
  "$env:LOCALAPPDATA\NVIDIA\GLCache",
  "$env:LOCALAPPDATA\NVIDIA Corporation\NV_Cache",
  "$env:ProgramData\NVIDIA Corporation\NV_Cache",   # NV_Cache aparece em 2 lugares — testar os dois
  "$env:LOCALAPPDATA\D3DSCache"                       # DirectX Shader Cache do Windows
)
# AMD: nomes divergem por driver (DxCache/DxcCache/VkCache/AMDCache) — enumerar dinamicamente:
$alvos += (Get-ChildItem "$env:LOCALAPPDATA\AMD" -Directory -EA SilentlyContinue | Where-Object Name -match 'Cache').FullName
foreach ($a in $alvos) { if (Test-Path $a) { Remove-Item "$a\*" -Recurse -Force -EA SilentlyContinue } }
```
Steam (fechar a Steam antes): apagar as subpastas de `...\Steam\steamapps\shadercache\{appid}` (padrão
`C:\Program Files (x86)\Steam\steamapps\shadercache`). NÃO confundir com "Delete local game content" (isso
apaga o JOGO). Efeito: o PRIMEIRO launch recompila (fica mais lento uma vez); jogo/saves intactos.
Fontes: https://nvidia.custhelp.com/app/answers/detail/a_id/5735/ · https://steamcommunity.com/discussions/forum/1/6679490060452861540/ · https://learn.microsoft.com/en-us/answers/questions/4120670/can-i-delete-dxcache

Alternativa segura pro DirectX cache: `cleanmgr` marcando "DirectX Shader Cache" (a própria MS marca só o
descartável).

---

## 2. Desligar Game DVR / gravação em segundo plano — Ganho: velocidade (médio) · Risco: seguro · reboot

Este é o ganho REAL do "modo jogo" popular (não o Game Mode em si): a Xbox Game Bar grava/encoda em
background mesmo sem você mandar, gastando CPU/GPU/RAM.
```powershell
Set-ItemProperty 'HKCU:\System\GameConfigStore' -Name GameDVR_Enabled -Value 0 -Type DWord
# política global (admin): New-Item 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR' -Force | Out-Null
#                          Set-ItemProperty 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR' -Name AllowGameDVR -Value 0 -Type DWord
```
Undo: `GameDVR_Enabled = 1` (e apagar/`=1` o `AllowGameDVR`). Reboot pra aplicar. Backup .reg antes.
Fonte: https://www.tenforums.com/tutorials/51180-enable-disable-windows-game-recording-broadcasting-windows-10-a.html

---

## 3. Game Mode e HAGS — o que dizer (sem prometer FPS)

- **Game Mode do Windows:** deixar LIGADO (padrão). Efeito é pequeno/nulo em máquina boa; raramente
  atrapalha. NÃO vender como "boost de FPS". Se der stutter (relatos com AMD), desligar resolve. Fonte: https://www.indiekings.com/2025/07/is-windows-11-game-mode-good-for-pc.html
- **HAGS:** ganho médio ~0% e gasta VRAM; só é "obrigatório" pra DLSS Frame Generation (RTX 40/50). Em GPU
  fraca pode PIORAR. Oferecer como teste A/B (catalogo.md §3.6), nunca como acelerador garantido. Fonte: https://devblogs.microsoft.com/directx/hardware-accelerated-gpu-scheduling/

---

## 4. Steam — cache de download e verificar integridade (COM aviso)

Ambos exigem confirmação explícita e aviso — mexem em estado do usuário:
- **Limpar cache de download** (`Steam > Configurações > Downloads > Limpar cache de download`): resolve
  download travado, mas DESLOGA a conta e cancela downloads/mods pendentes. NÃO apaga jogo/save. Fonte: https://help.steampowered.com/en/faqs/view/6AD7-820D-8BE5-E51F
- **Verificar integridade** (`botão direito no jogo > Propriedades > Arquivos instalados > Verificar`):
  repara arquivo corrompido sem reinstalar. AVISO: se um mod substitui um arquivo base do jogo, a
  verificação baixa o original de volta e "apaga" esse mod (reinstalar o mod resolve). Saves NÃO são
  tocados. Só oferecer pra quem tem crash/arquivo corrompido, avisando quem usa mod pesado. Fonte: https://help.steampowered.com/en/faqs/view/0C48-FCBD-DA71-93EB

---

## 5. Driver de GPU (dica, não ação automática)
Driver velho tira da sensação de "recém-formatado" pra quem joga. Sugerir checar/atualizar pelo app oficial
(GeForce App / AMD Adrenalin) — a skill NÃO baixa driver sozinha (evita instalar coisa errada). É uma dica
no recibo, opt-in manual.
