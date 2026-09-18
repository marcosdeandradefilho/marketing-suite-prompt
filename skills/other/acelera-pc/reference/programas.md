# programas.md — módulo opt-in: desinstalar programa de fábrica (Win32/OEM)

Este é o módulo que mais devolve a sensação de "recém-formatado" num notebook de loja: o bloatware Win32
(trial de McAfee/Norton, utilitários do fabricante, WildTangent, updaters) que a limpeza de app da Store
(catalogo.md §5) NÃO alcança. Só roda se o usuário aceitou no Stage 2.

HONESTO: desinstalar programa parado não "acelera" muito por si — o ganho vem de tirar o que fica RODANDO
(trial de antivírus que escaneia em background, updater que sobe no boot). Ainda assim é a faxina que mais
faz o PC "parecer de fábrica". Fonte da abordagem (recon por chaves Uninstall + winget): crítico de
completude da pesquisa Stage-3.

---

## 1. Recon — listar o que está instalado (só lê)

Enumerar as chaves Uninstall (pega Win32 real, não só Store) + winget:
```powershell
$keys = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
Get-ItemProperty $keys -EA SilentlyContinue |
  Where-Object { $_.DisplayName -and -not $_.SystemComponent } |
  Select-Object DisplayName, DisplayVersion, Publisher, UninstallString, QuietUninstallString |
  Sort-Object DisplayName
# se winget existir, complementa (mais fácil de desinstalar limpo):
if (Get-Command winget -EA SilentlyContinue) { winget list }
```
Mostrar a lista ao usuário em PT-BR simples, destacando os SUSPEITOS DE BLOAT (trial de antivírus,
"...Assistant", "...Update", jogos WildTangent, toolbars). NÃO desinstalar nada ainda.

---

## 2. Desinstalar — UM por vez, só o que o usuário confirmar

Para cada item que o usuário marcou (AskUserQuestion mostrando a lista), usar o comando de desinstalação
que o próprio programa registrou (ou winget):
```powershell
# preferir winget (silencioso e limpo) quando o id existir:
winget uninstall --id "<Id>" --silent
# senão, usar a string que o programa registrou:
#   QuietUninstallString roda sem UI; UninstallString abre o desinstalador do programa
Start-Process cmd -ArgumentList '/c', $quietUninstallString -Wait
```
Sem `QuietUninstallString`, abrir o `UninstallString` e deixar o usuário clicar no wizard do próprio
programa (mais seguro que forçar). Registrar cada remoção pro recibo.

---

## 3. DENYLIST — NUNCA oferecer/desinstalar

Não sugerir remoção destes (mesmo que apareçam na lista) — remover quebra o PC ou tira função essencial:
- **Drivers e painéis de GPU/chipset:** NVIDIA Graphics Driver / GeForce Experience / NVIDIA App, AMD
  Software Adrenalin, Intel Graphics/Chipset, Realtek Audio. (Driver de GPU faz PARTE da sensação de
  recém-formatado pra quem joga — se estiver velho, a dica é ATUALIZAR, não remover.)
- **Runtimes/frameworks:** Microsoft Visual C++ Redistributable (qualquer ano), .NET / .NET Framework /
  .NET Runtime, DirectX. Outros programas dependem; remover quebra sem aviso.
- **Antivírus ATIVO** (o que o usuário usa de verdade — diferente de trial expirado): não remover sem ele
  saber que fica desprotegido. Trial expirado de McAfee/Norton PODE remover, com confirmação.
- **Microsoft Office / 365** se em uso, navegadores em uso, e qualquer coisa que o usuário disser que usa.
- Qualquer app do fabricante que controle HARDWARE (tecla Fn, bateria, câmera, teclado RGB) — pode tirar
  função física. Na dúvida, perguntar, não remover.

Regra de ouro: na dúvida se é bloat ou essencial, PERGUNTAR ao usuário em linguagem simples ("esse aqui é
da placa de vídeo, melhor deixar" / "esse parece um teste de antivírus vencido, pode tirar?"), nunca decidir
sozinho por um item que controla hardware ou é runtime.

---

## 4. Undo
Desinstalar não tem "restore point que recupera programa" — reinstalar é baixando de novo do fabricante/
Store. Por isso a confirmação item-a-item é obrigatória. Avisar: *"Desinstalar é pra valer; pra ter de
volta você baixa de novo. Por isso só tiro o que você marcar."*
