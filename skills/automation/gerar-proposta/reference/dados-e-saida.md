# dados-e-saida.md — de onde vêm os dados e onde a proposta vai parar

> Step 1 + Step 6 detail. The skill is proactive: it pulls from a Prospector lead when there is
> one, asks at most one combined question when the input is empty, and archives every proposal as
> its own file so the freelancer builds a history.

## Entrada — campos
**Obrigatório pra montar a proposta:**
- `cliente_nome` — nome do cliente/empresa (vai na capa e no corpo, escrito por extenso e certo).
- `servico` — o que está sendo oferecido, 1-3 linhas (ex: "gestão de tráfego no Meta + criativos").
- `valor` — preço em R$ (mensal, à vista, ou faixa). Aceita "R$ 1.500/mês", "1500", "entre 1,2k e 2k".

**Opcional (inferir ou puxar; nunca travar por falta):**
- `dor`/`contexto` — o problema do cliente (vem do "sinal de oportunidade" do Prospector, ou inferido do serviço).
- `prazo` — prazo/cronograma (senão use fases relativas: "Semana 1...", "Etapa 2...").
- `escopo` — itens inclusos/não-inclusos (inferir do serviço; sempre liste o "não incluso").
- `garantia` — senão proponha uma garantia honesta sobre o trabalho (ver `reference/estrutura-copy.md`).
- `prova_social` — só se o usuário fornecer (NUNCA inventar).
- brand kit (logo, cores, contato, chave Pix) — ver `reference/brand-kit.md`.

## Detecção da fonte (em silêncio) + read-back
Dê UMA linha de read-back suave do que entendeu, pra o usuário corrigir cedo. Ex:
> *"Entendi: proposta de [serviço] pra [cliente], R$ [valor]. Vou puxar o resto do que você já me
> deu e assumir [X, Y] — se algo tiver errado, me corrige numa frase."*

### Caso A — veio do Prospector
Gatilhos: "o lead X", "aquele da lista", "o primeiro/quente da prospecção", ou o usuário acabou de
rodar `/prospector`.
1. `Glob .claude/leads/*.csv` e `.claude/leads/*.md`.
2. Read o roll-up `.md` e ache o dossiê do lead escolhido. Campos do dossiê do Prospector:
   **Negócio** (segmento/cidade/porte), **Sinal de oportunidade** (→ vira o diagnóstico/contexto da
   proposta), **Gancho de abordagem** (→ semente do hook do WhatsApp), **contatos** (WhatsApp/Instagram).
3. Puxe esses dados — **não faça o usuário redigitar**. O serviço + valor o usuário diz ("proposta de
   site R$ 1.500 pra esse"). Use o "Sinal" como a DOR do §3 da proposta (com a evidência, sem inventar).

### Caso B — manual
Parse cliente/serviço/valor/prazo/escopo da mensagem. O que faltar de opcional, infira e declare no read-back.

### Caso C — vazio ou vago demais
Não dispare um formulário. Faça UMA pergunta combinada via AskUserQuestion (opções fixas):
- Header "Proposta", pergunta *"Pra quem é a proposta e do que é o serviço? E quanto você vai cobrar?"*
- Como o AskUserQuestion só aceita opções fixas, use-o pro **tipo de serviço** (4 opções: Site/Landing ·
  Gestão de tráfego · Social media/Conteúdo · Outro/Consultoria) e, no texto ao redor, peça em uma
  frase: *"me diz numa linha: nome do cliente + o valor (ex: 'Padaria do Zé, R$ 1.500')"*.
- **Se o usuário não responder o cliente/valor:** não trave. Monte uma proposta-modelo clara pro
  serviço escolhido com valores marcados como *"[ajuste o valor]"* — NÃO, espera: nunca deixe
  placeholder visível no PDF final. Em vez disso, gere a proposta com um valor exemplo CLARAMENTE
  rotulado no chat ("usei R$ X de exemplo — me diz o real que eu regenero") e mantenha o cliente como
  "Cliente" genérico só se ele realmente recusar dar o nome, avisando que ficou genérico. Prefira
  sempre obter nome + valor reais antes de finalizar.

## Saída — arquivamento
Pasta `.claude/propostas/` (crie se não existir; sugira pôr no .gitignore se o projeto for versionado).
Slug do cliente = nome em minúsculas, sem acento, espaços→hífen (ex: "Padaria do Zé" → `padaria-do-ze`).
Use a data de hoje (AAAA-MM-DD). Grave 3 arquivos:
- `.claude/propostas/<slug>-<AAAA-MM-DD>-proposta.html` — o HTML auto-contido.
- `.claude/propostas/<slug>-<AAAA-MM-DD>-proposta.pdf` — o PDF (se o navegador renderizou).
- `.claude/propostas/<slug>-<AAAA-MM-DD>-whatsapp.txt` — o texto do WhatsApp.
**Nunca sobrescreva.** Se já existir proposta pra esse slug, é nova versão (ver dedup abaixo).

## Texto do WhatsApp (gere sempre)
Mande junto com o PDF. Estrutura:
1. **Saudação + nome do cliente.**
2. **Gancho personalizado de 1-2 linhas** ancorado num fato REAL (do "Sinal/Gancho" do Prospector,
   ou do que o usuário disse) — nunca inventado. Ex: *"Vi que a [Clínica X] ainda não tem site e tá
   recebendo agendamento só no Direct — montei uma proposta rápida de como resolver isso."*
3. **Frase do que é** ("segue a proposta de [serviço]").
4. **CTA único** — agendar uma call OU aprovar + pagar a entrada no Pix (alinhe com o CTA da proposta).
Tom de WhatsApp: curto, humano, sem parecer copiado de template. PT-BR direto. Sem emoji em excesso
(no máximo 1). Mostre o texto num bloco copia-e-cola no chat E salve no `.txt`.

## Recorrência / dedup
No Step 6, `Glob .claude/propostas/<slug>-*-proposta.*`. Se houver proposta anterior pro mesmo
cliente:
- Read a anterior, e gere a nova como versão nova (arquivo com a data de hoje).
- Diga: *"Você já tinha mandado uma proposta pra [cliente] em [data]. Essa é a 2ª versão — mudou
  [valor/escopo/o que for]."* Liste o delta, não reimprima tudo igual.
Isso evita reenviar byte-idêntico e dá histórico pro freelancer. Re-run nudge no fim: brand kit fica
salvo, então cada cliente novo sai na hora.
