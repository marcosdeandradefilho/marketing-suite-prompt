# Handoff — leia primeiro

Salva onde teu trabalho parou num arquivo enxuto e faz a **próxima sessão do Claude Code abrir já
sabendo o que tu tava fazendo**. É o jeito de **nunca mais rodar `/compact`** (que reprocessa a
conversa inteira e ainda perde detalhe) nem recomeçar do zero no dia seguinte.

## O que ela faz, em uma frase
Tu digita `/handoff` antes de parar → ela escreve um resumo curto em `.claude/context.md` (objetivo,
onde tá, decisões, becos sem saída, próximo passo) → tu dá `/clear` (que custa ~0) → quando abrir esse
projeto de novo, o Claude já vem com esse resumo carregado.

## Antes / depois
- **Sem a skill:** tu fecha o Claude, no dia seguinte ele não lembra de nada; ou tu roda `/compact`, que
  relê tua conversa toda pra resumir (tu paga por essa releitura) e ainda perde caminho de arquivo e
  decisão. Aí tu gasta tempo re-explicando tudo.
- **Com a skill:** um arquivinho enxuto guarda o essencial (caminhos e decisões EXATOS, que um resumo
  perderia). `/clear` é de graça. A sessão seguinte recarrega sozinha. Tu continua de onde parou.

> Honestidade: isso **não reseta teu limite** do plano PRO nem é “economia mágica de 90%”. O ganho real
> é simples: tu **para de reprocessar contexto velho** toda hora e para de pagar `/compact`. Sem número
> inventado.

## Como instalar a skill (só copiar a pasta — sem chave de API, sem instalar nada)
Copia a pasta `handoff` inteira (com a subpasta `assets/` junto) pra dentro da tua pasta de skills:

- **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
  (fica `C:\Users\SEU-NOME\.claude\skills\handoff\`)
- **Mac/Linux:** `~/.claude/skills/`
  (fica `~/.claude/skills/handoff/`)

Depois fecha e abre o Claude Code. Pronto, o comando `/handoff` já existe.

## Como usar
- Vai parar / fechar / pausar: digita **`/handoff`**. Ele salva e te diz pra dar `/clear`.
- Quer o auto-carregamento (a próxima sessão abrir já sabendo): **`/handoff instalar`** — ele liga dois
  “gatilhos” nativos do Claude Code (um que recarrega o resumo quando tu abre o projeto, outro que faz
  backup se a janela encher de repente). **Ele mexe num arquivo de config teu (settings.json), mas faz
  backup antes e te mostra o que vai pôr — só com teu “pode”.**
- Cansou e quer desligar o auto-carregamento: **`/handoff off`**.
- Frases que também chamam a skill sozinha: “vou parar agora”, “salva onde parei”, “continuo amanhã”,
  “antes de dar clear”, “tô perdendo contexto”, “o compact apagou tudo”.

> Depois de `/handoff instalar`, **reabre o Claude Code** pra os gatilhos valerem (eles carregam quando
> o programa abre).

## Quando rodar de novo
Toda vez que for parar, antes de dar `/clear`, ou quando a janela de contexto começar a encher. Cada vez ele ATUALIZA o
resumo (não reescreve do zero) — mantém o que ainda vale e troca o que mudou.