# Blindagem de Segurança — leia primeiro

Passa um pente-fino de segurança no teu projeto **antes de você publicar**. Acha chave de API
exposta, senha no código, `.env` que ia vazar pro GitHub, segredo aparecendo no navegador, banco de
dados aberto e dependência furada — explica cada coisa em português de gente, **conserta junto com
você** e te diz, no fim, se dá pra publicar ou não.

> Por que importa: chave de API jogada num projeto público é varrida por robô em **minutos**. Tem
> gente que publicou com a chave da OpenAI à mostra e acordou com a conta zerada. Essa skill é o
> "passa a blindagem antes de subir".

## O que ela NÃO faz (pra ficar honesto)
Ela lê os **arquivos** do teu projeto — não testa o app rodando nem o teu servidor na nuvem. Não é
certificado de segurança nem de LGPD. No fim ela sempre te mostra o que **não** deu pra checar. Sem
"tá 100% seguro", porque isso não existe.

## Instalar (não instala nada, não pede chave de API)

É só copiar a pasta `blindagem-de-seguranca/` inteira pra dentro da tua pasta de skills do Claude Code:

- **Windows:** `C:\Users\SEU-NOME\.claude\skills\`
- **Mac/Linux:** `~/.claude/skills/`

Ficando assim: `.claude/skills/blindagem-de-seguranca/SKILL.md`. Fecha e abre o Claude Code. Pronto.
Sem configurar nada, sem API, sem instalar programa.

## Como usar

Abre o Claude Code **dentro da pasta do teu projeto** e fala naturalmente:

- *"revisa a segurança antes de eu publicar"*
- *"tá seguro pra subir pro GitHub?"*
- *"tem alguma chave minha exposta?"*
- *"vou lançar essa ferramenta, dá uma blindada"*

Ela vai te perguntar se o projeto já foi publicado (isso muda tudo), varrer, te mostrar os problemas
no semáforo 🔴🟡🟢 e **te pedir permissão antes de mexer em qualquer coisa**. Nada destrutivo roda
sozinho.

## Antes e depois (o que muda ter a skill)

- **Sem a skill:** você pede "vê se tá seguro" e o Claude dá uns conselhos genéricos sobre o pouco
  que você colou no chat. Ele não varre o projeto, não acha a chave escondida no `docker-compose`,
  não sabe que o teu segredo tá indo pro navegador, e te dá um "parece ok" sem base.
- **Com a skill:** ela varre TODO o projeto (código, configs, histórico do git), reconhece o formato
  real das chaves de cada provedor (OpenAI, Anthropic, AWS, Stripe, Supabase, Mercado Pago…), separa
  o que é grave do que é frescura, **conserta junto** — inclusive te guiando pra **girar a chave que
  já vazou** (o passo que ninguém ensina) — e te dá um veredito honesto com o que ela não conseguiu ver.

## Roda de novo quando

Antes de **cada** publicação, e depois de **toda** mudança grande. Cada feature nova pode reabrir um
buraco. É hábito, não evento único.
