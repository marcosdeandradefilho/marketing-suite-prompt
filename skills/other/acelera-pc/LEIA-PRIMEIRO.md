# Acelera PC - leia primeiro

Essa skill devolve pro seu Windows aquela sensação de PC recém-formatado (abre rápido, clica e já responde)
SEM formatar, SEM reinstalar o Windows e SEM perder nenhum arquivo. Ela mede o que dá pra melhorar, cria
uma rede de segurança, limpa o lixo, enxuga o que abre junto com o Windows e desliga o peso invisível. Tudo
reversível.

Só de Windows. Ela mexe em configuração do Windows que no Mac/Linux não existe (se você instalar lá, ela avisa
e para). Funciona no Windows 10 e no Windows 11.

## O que ela faz na prática

1. Olha sua máquina (Windows 10 ou 11, SSD ou HD, notebook ou desktop, se você é administrador).
2. MEDE antes de mexer: quantos programas abrem no boot, quanto lixo tem, quanto de disco livre. Se o PC já
   estiver enxuto, ela fala na lata que tem pouco a ganhar, não inventa serviço.
3. Deixa VOCÊ escolher a intensidade: Conservadora, Equilibrada ou Agressiva. E os módulos opcionais.
4. MONTA no seu Desktop DOIS arquivos, feitos pra sua máquina e suas escolhas:
   - acelera-pc.ps1 - a otimização COMPLETA (o "modo Setup"), pra rodar uma vez (ou de vez em quando).
   - acelera-pc-semanal.bat - a limpeza leve, pra você CLICAR toda semana (ele pede admin sozinho).
   Por que um script? Porque a otimização de verdade (ponto de restauração, mexer em serviço, registro,
   cache do sistema) precisa rodar num PowerShell como administrador, fora do Claude Code. Aí funciona 100%.
5. Você roda o acelera-pc.ps1 num PowerShell como administrador (a skill te passa o passo a passo). Ele cria
   o ponto de restauração ANTES de tudo, pergunta antes de esvaziar a Lixeira, e deixa você escolher quais
   programas do boot, serviços de terceiro e itens de menu desligar.
6. O que ele faz (completo, não só limpeza): limpa dezenas de caches, enxuga boot e serviços (inclusive
   updaters de terceiros), desliga telemetria e peso invisível, deixa a interface imediata, faxina o menu de
   contexto, ajusta energia, privacidade e debloat. E RECUSA os "super tweaks" que são placebo ou quebram o
   PC (registry cleaner, RAM booster, desligar Superfetch/pagefile, timer resolution), te explicando por quê.
7. No fim salva um recibo honesto no Desktop: antes e depois em números, o que fez, o que NÃO fez e por quê,
   e exatamente como desfazer tudo (ponto de restauração + backups do registro).
   Depois, é só clicar no acelera-pc-semanal.bat uma vez por semana pra manter limpo.

## Com a skill vs sem a skill

- SEM a skill, você pede "otimiza meu PC" e o Claude te joga uma lista genérica de dicas, ou pior, roda um
  monte de comando de registro que ele leu em algum lugar, sem medir nada, sem rede de segurança, e às
  vezes repetindo mito que deixa o PC pior.
- COM a skill, ele mede sua máquina de verdade, cria o ponto de restauração, aplica só o que rende e não
  quebra, preserva teus arquivos e teus mods, e te entrega o antes/depois com o passo pra desfazer. É a
  diferença entre "chutar tweak da internet" e "otimizar com engenharia e rede de segurança".

## Como instalar (não instala nada no sistema, não pede chave de API, não configura nada)

É só copiar a pasta `acelera-pc` pra dentro da pasta de skills do Claude Code:

- Windows: `C:\Users\SEU-NOME\.claude\skills\`
- Mac/Linux: `~/.claude/skills/` (lembra: a skill só ATUA no Windows)

Ficando assim: `.../.claude/skills/acelera-pc/SKILL.md`

Importante: a otimização de verdade roda num PowerShell como administrador (a skill monta o script e te
passa o passo a passo pra rodar). Ela NÃO precisa que o Claude Code em si seja admin — o script é que roda
elevado. Sem admin o script ainda faz a parte segura e te avisa o que ficou de fora.

## Como usar

Digite `/acelera-pc` ou fale naturalmente:
- "meu PC tá muito lento, dá um jeito"
- "queria meu computador voando de novo, aquela sensação de formatado"
- "faz uma limpeza geral no Windows sem formatar"
- "meu PC de jogo tá travando mas eu uso mod, não quero perder nada"

Pra desfazer depois: `/acelera-pc reverter` mostra o ponto de restauração e os backups pra você
voltar.

## Quando rodar de novo

Não é toda semana. Roda de novo daqui a umas semanas ou meses: o lixo temporário volta, programa novo se
mete no boot, e um feature update grande do Windows reseta alguns ajustes. Quando sentir arrastando de novo,
roda de novo, e ela mede e te mostra o que mudou desde a última vez.

## Uma verdade que a skill não esconde

A sensação de "rápido" vem de três coisas: menos programa abrindo no boot, disco com espaço livre e menos
coisa rodando escondida. Não existe tweak mágico que dá "300% de FPS". O que promete isso é conversa. Essa
skill faz o que rende de verdade e não quebra nada, e te fala a verdade sobre o tamanho do ganho.
