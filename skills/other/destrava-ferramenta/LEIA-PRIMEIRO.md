# Destrava Ferramenta — como instalar e usar

**O que essa skill faz:** quando seu projeto no Claude Code **empacou** — um erro que não vai
embora, o código virou uma bagunça que você não entende mais, a janela de contexto estourou, ou o
Claude começou a rodar em círculos e você perdeu o fio — você chama a skill e ela: **olha o estado
real do seu projeto** (o que mudou no git, os arquivos mexidos por último, o erro), **pergunta onde
e como você travou** (inclusive como você tá se sentindo — porque cansado e confuso pedem respostas
diferentes), e te devolve um **diagnóstico em 3 camadas** + **2 ou 3 caminhos pra sair**, cada um
com um "tá resolvido quando..." que você mesmo consegue conferir. Ela aponta o primeiro passo mais
seguro e te deixa escolher.

---

## Sem a skill x Com a skill

- **Sem a skill:** você cola o erro no chat e o Claude chuta uma solução de memória — às vezes
  conserta, às vezes piora, e você não sabe POR QUE travou nem o que tentar se não der.
- **Com a skill:** ela **lê o seu projeto de verdade** (git diff, arquivos recentes, o erro
  literal), separa o que é erro pontual / decisão errada lá atrás / escopo grande demais, e te dá
  caminhos com critério claro de sucesso — começando pela ação **mais barata e mais fácil de
  desfazer**, pra você tentar sem medo de quebrar mais. E guarda um histórico das suas travas, pra
  reconhecer quando a mesma coisa volta.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `destrava-ferramenta` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. **Não tem chave de API, não instala nada, não configura nada.**

> Skill instalada no usuário funciona em **qualquer projeto** que você abrir no Claude Code.
>
> **O comando é o nome da pasta:** `/destrava-ferramenta`. Se você preferir um comando mais curto,
> é só renomear a pasta pra `destrava` — aí o comando vira `/destrava`. (O nome de dentro do
> arquivo não muda o comando; quem manda é o nome da pasta.)

---

## Usar

Abre o Claude Code, dentro do projeto que travou, e faz **uma** das duas coisas:

- Digita o comando: **`/destrava-ferramenta`**
- Ou simplesmente fala, em português normal — ela entende e aparece sozinha:
  - *"tô travado, esse erro não vai embora"*
  - *"o código virou uma bagunça e eu me perdi"*
  - *"o Claude tá rodando em círculos, me ajuda a destravar"*
  - *"meu projeto quebrou e não sei mais o que fazer"*
  - *"tentei de tudo e nada, tô quase desistindo"*

Você não precisa saber explicar tecnicamente o problema — ela olha o projeto e te pergunta o que
precisa. Se quiser, cola o erro inteiro que apareceu na tela; ajuda. No fim, o diagnóstico aparece
na conversa **e** (se você deixar) fica salvo em `.claude/travas/` dentro do seu projeto, pra você
reabrir depois.

---

## Detalhes que importam

- **Funciona no PRO** (US$ 20/mês) e no MAX. Não depende de internet pra te ajudar — ela diagnostica
  lendo o seu projeto local; a web é só um extra pra confirmar quando o Claude inventou uma função
  que não existe.
- **Não roda nada destrutivo sozinha.** Ela LÊ o seu projeto (git só de leitura, arquivos) e
  **sugere** os comandos de recuperação pra VOCÊ rodar — nunca apaga nem desfaz nada por conta
  própria. Quando o jeito de recuperar é arriscado, ela avisa em uma linha.
- **Sem git? Projeto vazio? Sem problema.** Ela detecta e se adapta — usa a data dos arquivos, o
  erro que você colou, e o que você descreve. Só sugere `git init` se você quiser uma rede de
  segurança pro futuro (não é obrigatório).
- **Roda de novo toda vez que travar.** E se for a MESMA trava de antes, ela reconhece o padrão
  ("isso já aconteceu, o que funcionou foi...") — porque travas que voltam costumam ter uma causa
  mais funda do que o erro da vez.

---

## Depois de destravar

Você sai com um caminho claro e um primeiro passo. Se a trava era de **escopo grande demais**, vale
voltar pra fatiar o projeto menor antes de seguir. Se você travou porque não sabia como os parecidos
resolvem o problema, a skill **`/busca-documentacao`** (do mesmo pack) pesquisa a documentação real
de ferramentas semelhantes. E se você ainda nem começou e travou no "por onde começo", a skill te
ajuda a montar um **esqueleto que anda** — uma versão mínima que roda ponta a ponta — pra destravar
a partir dali.
