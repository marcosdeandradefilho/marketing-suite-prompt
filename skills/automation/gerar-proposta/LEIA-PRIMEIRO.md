# Geradora de Proposta — como instalar e usar

**O que essa skill faz:** você fala pra quem é a proposta, qual serviço e quanto você cobra
("monta uma proposta de site pra Padaria do Zé, R$ 1.500"), e ela monta um **deck de proposta
comercial nível agência, em PDF** — capa cinematográfica com a sua marca, diagnóstico do problema
do cliente, solução, escopo, cronograma, preço em destaque, garantia e próximo passo. No fim, ela
ainda te entrega o **texto pronto pra mandar no WhatsApp** junto. Se você quiser, dá pra incluir um
**QR Pix de verdade** pra ele pagar a entrada na hora (opcional — por padrão não vem).

Não é "escrever o texto da proposta no chat". É o documento bonito, fechado, pronto pra enviar —
do jeito que as ferramentas pagas (Proposify, PandaDoc) fazem, só que de graça e na sua máquina.

---

## Instalar (1 minuto, sem programar)

1. Pegue a pasta inteira `gerar-proposta` (a que tem o `SKILL.md` dentro).
2. Jogue ela dentro da pasta de skills do seu usuário:
   - **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
   - **Mac/Linux:** `~/.claude/skills/`
   - Se a pasta `skills` não existir, crie ela.
3. Pronto. **Sem chave de API, não instala nada, não configura nada.**

> A skill é **offline** — os dados do cliente e a sua chave Pix ficam só na sua máquina, não vão
> pra lugar nenhum. Pra virar o PDF automático ela usa o **navegador que você já tem** (Edge no
> Windows, Chrome no Mac/Linux). Se ela não achar um, te entrega o arquivo pronto pra você salvar
> como PDF com **Ctrl+P** (fica idêntico).

---

## Usar

Abre o Claude Code e faz **uma** das duas coisas:

- Digita o comando: **`/gerar-proposta`**
- Ou fala, em português normal:
  - *"monta uma proposta de site institucional pra Padaria do Zé, R$ 1.500"*
  - *"gera uma proposta de gestão de tráfego, R$ 1.800/mês, pro cliente X"*
  - *"preciso mandar uma proposta de social media pra essa loja, cobra R$ 1.200"*
  - *"faz a proposta pro lead quente da lista do Prospector"* (puxa os dados sozinha)

Ela pergunta **no máximo uma coisa** se faltar o essencial (serviço + valor), e o resto ela decide:
escolhe uma paleta de cor profissional pela área do cliente, escreve o texto que converte, monta o
layout, gera o Pix e arquiva tudo. Os arquivos ficam salvos em `.claude/propostas/` dentro do seu
projeto (o `.pdf`, o `.html` e o `.txt` do WhatsApp).

**Sua marca, salva uma vez:** na primeira proposta ela oferece guardar seu nome, logo, cor e chave
Pix num arquivo (`.claude/brand-kit-freelancer.md`). Aí **toda proposta nova já sai com a sua cara**,
sem você repetir nada.

---

## Sem a skill vs com a skill

- **Sem a skill:** o Claude te escreve o *texto* de uma proposta no chat. Você ainda tem que jogar
  no Word/Canva, formatar, achar uma cor, montar a tabela de preço, gerar o Pix em outro site, salvar
  o PDF e escrever o WhatsApp na mão — 1 a 2 horas por proposta, e quase sempre sai sem padrão.
- **Com a skill:** sai o **deck profissional pronto** (capa cinematográfica branded, diagnóstico do
  cliente, escopo, preço em destaque, garantia, CTA — e, se você pedir, **QR Pix que funciona de
  verdade**) + o **texto do WhatsApp** — tudo arquivado, no mesmo padrão toda vez. Você só revisa e manda.

---

## Detalhes que importam

- **Não inventa.** Depoimento, case, logo ou resultado do cliente — se você não der, ela **não
  inventa** (proposta com case falso te queima). Garantia é sempre sobre o seu trabalho, nunca uma
  promessa de "vou triplicar seu faturamento".
- **Pix é opcional.** Por padrão a proposta vem só com as condições de pagamento (a maioria das
  propostas não embute Pix). Se você pedir, ela inclui um QR Pix + código copia-e-cola gerados com o
  cálculo oficial (CRC válido), não um QR de enfeite.
- **Roda de novo a cada cliente.** Com o brand kit salvo, a próxima proposta sai na hora. Se você
  mandar proposta de novo pro mesmo cliente, ela detecta e marca como "2ª versão" com o que mudou.
- **Funciona no PRO** (US$ 20/mês). É offline e leve.

---

## Depois da proposta

Cliente aprovou um serviço de site? Dentro do pack, o próximo passo é a skill **Site Institucional**
(`/site-institucional`): ela entrega o site que você acabou de vender.
