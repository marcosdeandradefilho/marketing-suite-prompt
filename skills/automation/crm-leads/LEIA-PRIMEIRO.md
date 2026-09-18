# CRM de Leads — como instalar e usar

**O que essa skill faz:** ela pega os leads que você levantou e monta um **painel visual no seu
computador** — um quadro estilo Trello onde cada lead é um card que você arrasta de **Novos** para
**Contatado**, **Respondeu**, **Proposta**, **Fechado** ou **Descartado**.

Clicando no card, abre o dossiê inteiro: por que entrar em contato com aquele negócio agora, o
gancho pronto pra usar, WhatsApp/telefone/e-mail/site clicáveis, quem decide, a nota de calor com a
conta e de onde veio cada informação. Ali mesmo você marca (lead quente, sem resposta, voltar
depois, não perturbe), escreve o que rolou na conversa e anota a próxima ação.

E o principal: **os leads da próxima prospecção caem no MESMO painel**. Achou 5 hoje e mais 5
amanhã? Os 5 novos entram na coluna Novos, sem duplicar ninguém e **sem mexer no que você já
arrastou ou anotou**.

Não é um CRM de nuvem: **não tem login, não tem mensalidade, não tem conta**. Roda na sua máquina e
os dados ficam dentro da pasta do seu projeto.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `crm-leads` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. **Sem chave de API, sem cadastro, sem instalar programa.**

> **Um detalhe honesto:** o painel usa o **Node** pra guardar o que você mexe direto num arquivo do
> projeto. O Node já vem junto com o Claude Code na maioria das instalações — se não tiver, o painel
> ainda abre com dois cliques, mas aí o que você mexer fica guardado só naquele navegador (e o
> Firefox não guarda). Se aparecer esse aviso na tela, instale o Node em nodejs.org (versão LTS).

---

## Usar

Abre o Claude Code e faz **uma** das coisas:

- Digita o comando: **`/crm-leads`**
- Ou fala, em português normal:
  - *"abre o painel dos meus leads"*
  - *"joga esses leads no painel"*
  - *"como tá meu funil?"*
  - *"importa essa planilha de leads que eu já tinha"*

Depois de montado, dá pra abrir o painel **sem o Claude Code**: dois cliques em
`abrir-painel.bat` (Windows) ou `abrir-painel.command` (Mac/Linux), dentro da pasta
`.claude/leads/crm/` do seu projeto.

---

## Como funciona na prática

1. Você prospecta (a skill **Prospector** faz isso) e manda jogar no painel.
2. O painel abre no navegador com os leads na coluna **Novos**, ordenados do mais quente pro mais frio.
3. Você chama o cliente pelo WhatsApp direto do card e arrasta ele pra **Contatado**.
4. Escreve o que ele respondeu, marca **voltar depois** ou **não perturbe**, define a próxima ação.
5. Amanhã você prospecta de novo: os novos entram na coluna Novos, o resto fica exatamente como você
   deixou.

**Marcou "não perturbe"?** Aquele negócio fica de fora de todas as prospecções futuras. Isso não é
firula: é o respeito básico a quem pediu pra não ser procurado.

---

## Onde ficam seus dados

Tudo dentro do projeto, em `.claude/leads/crm/`:

- `leads.json` — os leads em si (empresa, contatos, sinal, gancho, nota).
- `estado.json` — o SEU trabalho: em que coluna está cada um, marcas, anotações, próxima ação.
  Ganha um backup automático a cada mudança.
- `painel.html` — a tela.

Quer levar pra outra máquina ou guardar? Copia a pasta `.claude/leads/crm/` inteira. Ela abre em
qualquer computador com Node, do mesmo jeito.

Nada sai da sua máquina. O painel só escuta em `127.0.0.1` — ninguém na sua rede alcança ele.

---

## Dupla com a Prospector

- **`/prospector`** acha os clientes e explica por que cada um precisa de você agora.
- **`/crm-leads`** (esta) organiza, guarda e acompanha do primeiro contato até o fechamento.
- Escolheu um lead quente? **`/gerar-proposta`** monta a proposta a partir do dossiê dele.
