# Passe Livre (leia primeiro)

O que essa skill faz, em uma linha: configura o Claude Code pra ele PARAR de te pedir "Sim / Permitir"
a cada comando e a cada edição de arquivo. Libera sozinho o que é seguro e só te pergunta no que é de
verdade arriscado.

Sem chave de API. Não instala nada. Não configura API nenhuma. Só mexe num arquivo de configuração seu
(o settings.json do Claude Code), fazendo backup antes.

## Antes e depois (o que muda de verdade)

Sem a skill: você fica clicando "permitir" o dia todo, a cada `npm test`, a cada arquivo que o Claude
edita, a cada commit. Pra fugir disso, a maioria acaba caindo no `--dangerously-skip-permissions`, que
libera TUDO (inclusive apagar coisa e ler suas senhas). Ou desiste e continua clicando.

Com a skill: em um comando, o Claude passa a fazer sozinho o trabalho comum (rodar teste e build,
editar e criar arquivo, commitar, instalar dependência do projeto, ler documentação). Continua te
perguntando antes do que é arriscado (apagar arquivo, git push, publicar, fazer deploy, baixar pacote
de terceiro). E fica BLOQUEADO no perigoso (rodar como administrador, apagar o computador inteiro, ler
seu arquivo de senhas .env). É o meio-termo seguro que a documentação oficial recomenda.

## Quando usar

Quando você JÁ tem a máquina pronta (Node, Python, git já instalados) e só quer parar de clicar
permitir toda hora. Frases que disparam: "cansei de clicar permitir", "parar de pedir permissão",
"libera o Claude", "deixa ele trabalhar sozinho", "configura as permissões", ou é só chamar
/passe-livre.

Se você ACABOU de instalar o Claude Code e ainda não configurou nada (não sabe se tem Node/Python),
use antes a /preparar-maquina, que deixa o PC pronto e já liga as permissões básicas. A Passe Livre é
pra depois, quando a máquina já está de pé e você quer o ajuste fino das permissões.

## Como instalar a skill

Copie a pasta `passe-livre` inteira pra dentro da pasta de skills do seu Claude Code:

- Windows: `C:\Users\SEU-NOME\.claude\skills\`
- Mac/Linux: `~/.claude/skills/`

Ou seja, o caminho final fica `.../.claude/skills/passe-livre/`. Reabra o Claude Code e a skill aparece.

## Como usar

- `/passe-livre`: libera pra todos os seus projetos (grava no seu settings.json global). É o padrão.
- `/passe-livre projeto`: libera só no projeto que você está agora.
- `/passe-livre ver`: só mostra o que ela MUDARIA, sem mexer em nada.
- `/passe-livre reverter`: desfaz, voltando pro backup.

Ela sempre te mostra o que vai mudar e pede um "ok" antes de gravar. Faz backup do seu settings.json
antes de qualquer coisa (fica um arquivo `settings.json.bak-...` do lado). Depois de aplicar, reabra o
Claude Code pra valer (as permissões são lidas quando ele abre).

## Importante

- Ela nunca usa o modo "libera tudo" (bypassPermissions / --dangerously-skip-permissions). O sentido
  da skill é justamente NÃO fazer isso.
- Ela não apaga o que você já tinha no settings.json. Se você já tinha regras suas (ou os hooks da
  skill Handoff, por exemplo), tudo continua lá. Se você já bloqueava alguma coisa, o seu bloqueio
  continua valendo (a regra mais restritiva ganha).
- Ler arquivo de senha (.env, chaves) fica bloqueado de propósito. Se um dia você precisar que o Claude
  leia um .env específico seu, é só pedir, que ela te explica como liberar aquele caso.

## Quando rodar de novo

Sempre que aparecer um comando que você usa muito e ele ainda te pergunta (aí você pede pra liberar), ou
quando quiser apertar de volta alguma coisa. É só chamar /passe-livre. Pra liberar um comando pontual na
hora, o próprio Claude Code tem o /permissions nativo.
