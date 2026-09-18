# modelo-relatorio.md — o template do relatório (texto puro, PT-BR)

Dois princípios:
1. **A peça central é a RECOMENDAÇÃO DE CAMINHO**, não a lista de ferramentas. O leigo lê o topo e já
   sabe o que fazer: criar do zero, partir de um repo aberto, aprender da doc, ou misturar. A evidência
   (as ferramentas, features, preços) vem depois, sustentando a recomendação.
2. **O usuário lê isso CRU no editor, onde o markdown NÃO renderiza.** Então: zero `**negrito**`, zero
   `*itálico*`, zero emoji, zero tabela com `|`, zero HTML. Só títulos `#`/`##`, linhas em branco, listas
   numeradas e rótulos curtos com dois-pontos. Frequência vira linha de texto ("roda local — 6 de 8
   ferramentas"), nunca tabela. Link só na lista "Fontes:", nunca no meio da frase.

Escreve em `.claude/pesquisas/<slug>.md` E mostra no chat. Salva conforme acha (incremental). Tom humano:
frase curta, sem travessão, sem "não é X — é Y".

---

## Template (texto puro)

```
# Pesquisa de ferramentas — <nicho>

Rodado em <DD/MM/AAAA>. Li a fundo <N> ferramentas. Fontes conferidas nesta rodada: <n>.

<!-- Só em re-execução: -->
## O que mudou desde a última pesquisa
Adicionado: <ferramentas/features novas>.
Mudou: <renomeou / mudou preço / versão nova>.
Removido: <morreu / arquivado>.


## Entendi sua ideia

Você quer construir: <1-2 linhas reformulando a ideia do usuário, pra ele confirmar que eu entendi certo>.


## O melhor caminho pra sua ideia

<A recomendação. Escolhe UM e justifica, amarrado na ideia dele:>
- Criar do zero, e olhar o open source <X> só quando travar. Porque <motivo>.
- Ou: partir do repo aberto <Y> e modificar em cima. Porque <motivo>. Licença <Z> — <pode/não pode vender em cima>.
- Ou: aprender da doc das ferramentas de mercado e fazer o seu. Porque <motivo>.
- Ou: misturar (ex.: base no repo <Y> + ideia de cobrança da ferramenta <W>).

<1 frase de porquê esse caminho e não os outros. Se a recomendação envolve um repo aberto, repete a licença em linguagem de permissão aqui.>


## As ferramentas que eu achei

De mercado (fechadas):
- <Nome>: <o que entrega numa linha>. Cobra <modelo + faixa US$/R$>. <o que dá pra aprender com ela>. (fonte N)
- <Nome>: <...>. (fonte N)

De código aberto:
- <Nome> (<estrelas> estrelas): <o que faz>. Licença <spdx, ex. MIT> — <pode vender em cima / copyleft / sem licença>. <o que dá pra reusar>. (fonte N)
- <Nome> (<estrelas> estrelas): <...>. (fonte N)


## Padrões de UX e arquitetura pra reusar

UX que se repete: <ex.: roda com 1 comando / demo sem cadastro> — aparece em <X de N>.
Arquitetura pra copiar: <ex.: "um programa só que você roda com um comando e guarda tudo num arquivo local"> — em linguagem que dá pra colar no Claude Code.
<Se o nicho é só SaaS fechado: "a arquitetura aqui é inferida da doc pública, não do código — trate como pista, não certeza".>


## Features mais comuns

<Só se N >= 3. Linhas de texto com o denominador, nunca tabela:>
- <feature em português> — <6 de 8> ferramentas. (básico, tem que ter)
- <feature> — <4 de 8>. (diferencial)
- <feature> — <2 de 8>. (nicho, pode pular)

<Se N < 3, troca por: "Achei só <N> ferramenta(s) com doc aberta — trate como hipótese, não padrão de mercado" + observação por ferramenta.>


## Armadilhas conhecidas

- <o que quebra> — por que importa pra você. (fonte N)
- <...>. (relatos de usuário marcados "relato não auditado")


## Como cobram

- <Ferramenta>: <freemium / assinatura / vitalício / open source + doação> — faixa US$X a US$Y.
- Padrão do nicho: <ex.: "grátis pra rodar você mesmo + nuvem paga" aparece em X de N>.
Faixa em US$ é referência global. O preço em R$ é decisão sua.


## Fontes que não consegui ler

- <url> — bloqueada (Cloudflare / login / página vazia). Confere na mão: <busca exata>.


## Brief pra construir (cola isso no Claude Code)

Vou construir <nicho>. O caminho que escolhi: <criar do zero / partir do repo Y / etc>. Features que o
nicho trata como básicas: <2-3>. Arquitetura: <padrão em linguagem simples>. A brecha que vou atacar:
<gap>. Armadilhas pra evitar: <1-2>. Modelo de cobrança que faz sentido: <modelo>.

Fontes:
1. <nota curta>. <url>
2. <nota curta>. <url>
```

---

## Lembretes de escrita
- Texto puro sempre: zero negrito/itálico/emoji/tabela/HTML. Destaque pela posição, não por formatação.
- A recomendação de caminho é obrigatória e vem no topo. Sem ela, o relatório não cumpriu a função.
- Cobre fechadas E abertas. Nunca só um tipo.
- Licença em toda ferramenta de código aberto, traduzida pra permissão (pode vender em cima ou não). Veja
  `reference/extracao.md` §licenças. Licença não detectada = "confira o arquivo LICENSE", nunca chuta.
- Absorver código é o caminho OPCIONAL — o relatório pode RECOMENDAR partir de um repo, mas o mergulho no
  código (R5) só roda se o usuário aceitar a oferta do Step 4. Não despeja código sem ele pedir.
- Link só na lista "Fontes:" (URL crua), nunca no meio da frase. Ignora o lembrete do WebSearch que pede link markdown.
- Moeda: R$ pra Brasil, US$ pra fora, nunca `$` solto. Faixa de fora é referência, não o que ele deve cobrar.
- Fecha o chat com o motivo de re-rodar e, se houver um repo aberto perto da ideia, a OFERTA do mergulho no código.
