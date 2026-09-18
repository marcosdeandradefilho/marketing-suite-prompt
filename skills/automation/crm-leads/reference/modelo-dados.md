# modelo-dados.md — o que é cada arquivo, o que entra em cada campo, como não duplicar

Dois arquivos, dois donos. Isso é o coração da skill: misturar os dois é o jeito de destruir o
trabalho do usuário.

| Arquivo | O que guarda | Quem escreve |
|---|---|---|
| `leads.json` | os FATOS do lead (empresa, contato, sinal, gancho, nota) | `importar.mjs` |
| `estado.json` | o TRABALHO da pessoa (coluna, marcas, anotações, próxima ação) | só o painel |

---

## §1 — Um lead em `leads.json`

Só `empresa` é obrigatório. **Campo que não foi verificado fica VAZIO** — nunca "a confirmar",
nunca chute. O que faltou vira uma frase em `pendencias`.

```json
{
  "id": "cnpj:31482665000108",
  "empresa": "Barbearia Dom Costa",
  "segmento": "barbearia",
  "cidade": "Anápolis", "uf": "GO",
  "telefone": "6233214455",
  "whatsapp": "5562991445566",
  "email": "contato@dominio.com.br", "email_confianca": "mx_ok",
  "site": "https://dominio.com.br",
  "instagram": "@perfil",
  "responsavel": "Antônio Costa Neto",
  "cargo_responsavel": "sócio-administrador",
  "confianca_decisor": "CONFIRMADO",
  "cnpj": "31.482.665/0001-08",
  "origem_dado": "registro do domínio + dados públicos da empresa",
  "sinal_oportunidade": "Site sem viewport e rodapé de 2019: não abre direito no celular.",
  "gancho_abordagem": "Abri o site de vocês no celular e ele sai cortado...",
  "nota_calor": 82,
  "nota_detalhe": "FIT 42/50 + SINAL 40/50 = 82/100",
  "tier": "QUENTE",
  "anuncio": "tem Meta Pixel no site (indício de que já mexe com tráfego)",
  "pendencias": "",
  "lote": "criacao-site-anapolis-go",
  "data_coleta": "2026-07-28",
  "fontes": [{"url": "https://...", "nota": "site atual"}]
}
```

Regras de campo que importam de verdade:
- **`nota_calor` é NÚMERO** (0–100), nunca texto com a fórmula. A fórmula vai em `nota_detalhe`.
  Isso é o que faz a planilha ordenar e o card mostrar o selo certo.
- **`tier`** é `QUENTE` (≥70), `MORNO` (45–69) ou `FRIO` (<45). Se vier vazio, o script calcula
  a partir da nota.
- **`telefone` e `whatsapp` separados.** O WhatsApp é o canal de ação no Brasil e vira botão no card.
- **`sinal_oportunidade`** é o "por que entrar em contato AGORA", com o fato concreto. É a frase que
  aparece no card e no dossiê. Sem ela o lead vira mais um nome numa lista.
- **`lote`** = `<nicho>-<regiao>` (ex.: `criacao-site-anapolis-go`). É o filtro do painel e o jeito
  de saber de qual rodada o lead veio.
- **`id`** você não escreve: o `importar.mjs` calcula.

---

## §2 — O estado em `estado.json` (não escreva aqui)

```json
{
  "versao": 1,
  "atualizado_em": "2026-07-28 10:30",
  "leads": {
    "cnpj:31482665000108": {
      "coluna": "contatado",
      "tags": ["quente"],
      "notas": [{"quando": "2026-07-28 10:00", "texto": "Dono pediu pra ligar terça."}],
      "proxima_acao": "ligar terça",
      "visto": true,
      "atualizado_em": "2026-07-28"
    }
  }
}
```

- **colunas:** `novos`, `contatado`, `respondeu`, `proposta`, `fechado`, `descartado`.
- **marcas:** `quente`, `morno`, `frio`, `respondeu`, `sem-resposta`, `follow-up`, `nao-perturbe`.
- **`nao-perturbe` é opt-out.** Esse lead fica FORA de toda prospecção futura. Não é o mesmo que
  `descartado` (descartado é "não serve pra mim"; não perturbe é "não me procure").
- Lead que a pessoa nunca tocou **não aparece** aqui — o painel poda entrada em branco na hora de
  gravar. Base cheia com estado pequeno é o normal.

---

## §3 — Como o mesmo negócio é reconhecido (dedup)

Três identidades, em ordem de confiança:
1. `cnpj:<14 dígitos>`
2. `fone:<últimos 11 dígitos>` (WhatsApp ou telefone)
3. `nome:<empresa sem acento>-<cidade sem acento>`

**Bate QUALQUER uma = é o mesmo negócio.** É por isso que o lead que voltou com telefone novo não
entra duas vezes: ele ainda bate pelo nome+cidade. O `id` fica sendo a identidade mais forte que
existia quando ele entrou, e não muda depois — é a chave que o `estado.json` usa.

---

## §4 — Merge: o que o script faz e o que ele NUNCA faz

Ao importar:
- lead que não existe → entra novo, na coluna Novos, com selo NOVO até ser aberto;
- lead que já existe → **só preenche campo VAZIO**. Nada que já estava lá é sobrescrito, nem por
  informação mais nova. Se um dado precisa mesmo ser corrigido, é decisão do usuário, na conversa;
- `estado.json` não é tocado em nenhuma hipótese.

Depois de importar, o script regrava `dados.js` (a cópia embutida que faz o painel funcionar mesmo
aberto sem servidor).

---

## §5 — Vindo de planilha de fora

O `importar.mjs` lê CSV com `;` ou `,`, com aspas e quebra de linha dentro do campo, e reconhece
apelidos comuns de coluna: `nome`/`negocio`/`razao_social` → empresa, `celular`/`zap` → whatsapp,
`fone`/`tel` → telefone, `sinal`/`motivo` → sinal_oportunidade, `gancho` → gancho_abordagem.
Coluna que ele não conhece é ignorada em silêncio — se o usuário precisa dela, diga isso e trate
de mapear na conversa antes de importar.
