# Preparador de Máquina — como instalar e usar

É a **primeira** skill pra rodar depois de instalar o Claude Code. Ela prepara teu PC e o próprio
Claude Code ANTES de você construir, fazendo as **duas coisas que o Claude Code não resolve sozinho
no meio de um projeto**:

1. **Deixa a máquina capaz de RODAR o que ele constrói.** Ela vê o que você já tem e instala a
   fundação que faltar — Node, Python, git, ffmpeg — com a tua permissão, um de cada vez, e
   *testando* que funcionou. Sem isso, na primeira ferramenta você esbarra num erro vermelho
   (`npm não é reconhecido`) e trava. Esse é o ponto onde muita gente desiste.
2. **Faz o Claude parar de pedir permissão toda hora.** No padrão, ele pede confirmação em quase
   tudo, e você não sabe o que clicar. Ela configura o Claude Code (com a tua permissão) pra ele
   editar arquivo direto — mas ainda confirmar comando de terminal — e pra proteger teu `.env`.

**O que ela NÃO faz (de propósito):** ela não pré-instala a biblioteca do teu projeto (tipo o
`pandas` pra uma planilha, ou um pacote específico de um site). **Isso o Claude Code instala
sozinho na hora que constrói.** O setup entrega o motor; o build entrega o resto. Por isso ela não
sobrepõe o que o Claude já faz — ela cobre o buraco ANTES, que é onde o iniciante apanha.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `preparar-maquina` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. Não tem chave de API, não instala nada sozinha, não configura nada sem te perguntar.

> Skill instalada no usuário funciona em **qualquer projeto** que você abrir no Claude Code.

---

## Usar

Abre o Claude Code e faz **uma** das duas coisas:

- Digita o comando: **`/preparar-maquina`**
- Ou simplesmente fala, em português normal:
  - *"acabei de instalar o Claude Code, por onde eu começo?"*
  - *"o que eu preciso instalar pra usar isso direito?"*
  - *"deixa meu PC pronto"*
  - *"preciso instalar Node? Python? como?"*
  - *"tô perdido, instalei e agora?"*

Ela dá uma olhada no teu PC (só leitura, não mexe em nada), faz **1 pergunta** rápida pra saber o
que você quer construir, e te mostra a lista. Aí, **pra cada coisa que falta, ela pergunta antes de
instalar** e mostra o comando exato. Você decide.

---

## Antes e depois (o que muda)

- **Sem a skill:** o Claude te manda *"instale o Node.js"* e você fica perdido — qual versão? de
  onde? por que deu "npm não é reconhecido"? por que `python` abre a Loja da Microsoft? Muita gente
  trava aqui e desiste.
- **Com a skill:** ela vê o que já tem, te diz em português o que falta e **por que** importa,
  instala com você aprovando cada passo, e confirma que funcionou de verdade (não só "instalei" —
  ela testa). E ainda configura o Claude Code pra ele parar de te pedir permissão toda hora. No fim
  a máquina tá pronta e o Claude flui — sem aquele erro vermelho logo na primeira ferramenta.

---

## Detalhes que importam

- **Funciona no PRO** (US$20/mês). Ela não precisa de plano caro.
- **Não instala nada escondido.** Toda instalação passa por uma pergunta "posso? (s/n)". Coisas mais
  sensíveis (baixar script da internet, mexer no PATH) ela avisa com mais cuidado ainda.
- **Roda de novo quando quiser.** Trocou de PC, abriu um projeto novo, ou vai começar um tipo de
  trabalho que pede outra ferramenta (ex.: começou com sites, agora vai mexer com vídeo)? Roda de
  novo — ela compara com a última vez e mexe só no que mudou.
- **Funciona no Windows, Mac e Linux.** No Windows (a maioria de vocês) ela usa o winget; no Mac, o
  Homebrew; no Linux, apt/dnf.

---

## Depois do setup

Ambiente pronto. Daí pra frente:
- Se ainda não sabe **o que** construir → roda a **`/varredura-de-mercado`**.
- Se mais pra frente alguma ferramenta sua **der erro na máquina** → isso é trabalho da
  **`/destrava-ferramenta`**.
