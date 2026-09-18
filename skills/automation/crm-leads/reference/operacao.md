# operacao.md — o dia a dia: relatório do funil, mexer por chat, exportar, limpar

Tudo que a pessoa vê aqui é **texto puro** (ela lê o `.md` cru no editor): sem emoji, sem
`**negrito**`, sem tabela com `|`. Severidade e etapa viram palavra.

---

## §1 — Relatório do funil (a pergunta "como tá minha prospecção?")

Leia `leads.json` + `estado.json` e responda com números REAIS, nesta ordem:

```
FUNIL - 28/07/2026

Na base: 34 leads (3 lotes)
  Novos ........... 18   (11 quentes ainda sem toque)
  Contatado ....... 9
  Respondeu ....... 4
  Proposta ........ 2
  Fechado ......... 1
  Descartado ...... 0
  Nao perturbe .... 0

COMECE POR ESTES (quente, novo, com WhatsApp)
  1. Barbearia Dom Costa - Anapolis/GO - 82 - site nao abre no celular
  2. Pizzaria Forno de Pedra - Anapolis/GO - 74 - cardapio so em PDF

COM PROXIMA ACAO MARCADA
  - Studio Express: ligar terca
  - Need Estetica: mandar proposta

PARADOS HA MAIS DE 7 DIAS EM CONTATADO
  - Odontologia Sorriso Claro (contatado em 18/07, sem anotacao nova)
```

Regras do relatório:
- **Quente sem toque é o topo.** É a resposta prática da pergunta "por quem eu começo".
- **"Parado" usa data real** (`atualizado_em` do estado). Sem data, não invente: escreva
  "sem data de movimento".
- Se a base está vazia, diga isso em uma linha e aponte a `/prospector`. Nada de relatório de zero.

---

## §2 — Mexer num lead por chat (mover, marcar, anotar)

O painel é o dono do `estado.json`. Quando a pessoa pede pelo chat ("marca a barbearia como
contatado"), faça assim e nada além disso:

1. Confirme de qual lead se trata pelo nome (se houver dois parecidos, pergunte qual).
2. Leia `estado.json` inteiro.
3. Reescreva o arquivo com a mudança pontual: só o `coluna` / `tags` / `notas` / `proxima_acao`
   daquele `id`, mantendo TODO o resto byte a byte.
4. Diga em uma linha que você mexeu no arquivo do funil e que, se o painel estiver aberto, ele
   precisa recarregar a página pra ver.

**Se o painel estiver aberto naquele momento, avise ANTES:** a página em cima é a versão antiga e
salva por cima quando a pessoa mexer em qualquer coisa. O caminho seguro é ela fechar o painel,
você editar, ela abrir de novo. Diga isso — é o erro mais fácil de cometer aqui.

---

## §3 — Exportar planilha

Dois caminhos, e o do painel é o melhor:
- **No painel:** botão Exportar baixa o que está FILTRADO na tela, já com `;` e acento certo pro
  Excel em português, e já com etapa/marcas/próxima ação/última anotação junto.
- **Pelo chat:** se a pessoa quer o arquivo dentro do projeto, gere `.claude/leads/<nome>.csv`
  seguindo as mesmas regras: separador `;`, BOM UTF-8 no começo, `nota_calor` numérica, campo vazio
  fica vazio.

Nunca gere planilha com vírgula como separador: no Excel em português tudo cai numa coluna só.

---

## §4 — Fechar o ciclo com a prospecção

Antes de uma rodada nova de `/prospector`:

```
cd .claude/leads/crm && node importar.mjs --skip
```

Sai a lista de quem já está na base, com etapa e marcas. Passe isso pra prospecção com uma regra
clara: **não trazer de novo quem está na lista**, e principalmente ignorar quem está marcado
`nao-perturbe` (é opt-out, não é preferência). Depois que a rodada nova chega, importe e reporte os
números do script.

---

## §5 — Limpar sem quebrar

- **Tirar um lead:** removê-lo de `leads.json` deixa o registro dele órfão em `estado.json`. Tire dos
  dois, ou (melhor) mova pra Descartado no painel e deixe a base intacta — o histórico vale.
- **Recomeçar do zero:** apagar `leads.json` E `estado.json`. Diga em voz alta que isso apaga o
  funil inteiro e não tem volta, e confirme antes.
- **Base grande:** o painel aguenta bem alguns milhares de cards; acima disso a rolagem fica pesada.
  Se chegar lá, o caminho é dividir por lote em pastas diferentes, não "otimizar" o painel.
