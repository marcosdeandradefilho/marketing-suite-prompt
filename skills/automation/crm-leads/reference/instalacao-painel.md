# instalacao-painel.md — montar, abrir e destravar o painel

Tudo roda na máquina do usuário. Sem conta, sem nuvem, sem chave de API.

---

## §1 — A pasta do painel

Sempre a mesma, dentro do projeto aberto:

```
.claude/leads/crm/
├── painel.html         copiado do assets/ da skill (a tela)
├── servidor.mjs        copiado (servidor local, sem dependência)
├── importar.mjs        copiado (junta leads novos sem duplicar)
├── abrir-painel.bat    copiado (Windows: dois cliques)
├── abrir-painel.command copiado (Mac/Linux: dois cliques)
├── leads.json          os leads (fatos) — escrito pelo importar.mjs
├── estado.json         o funil (o que a pessoa mexeu) — SÓ o painel escreve
└── dados.js            cópia embutida pro modo sem servidor — escrito pelo importar.mjs
```

**Copiar, nunca redigitar.** Os 5 arquivos de `assets/` são copiados como estão. Se algum não for
achado, diga qual faltou e pare — não tente reescrever o painel na mão.

Onde a skill está instalada, em ordem de tentativa:
1. `~/.claude/skills/crm-leads/assets/` (instalação normal, vale em qualquer projeto)
2. `.claude/skills/crm-leads/assets/` (instalada só neste projeto)

`leads.json` nasce como `{"versao":1,"leads":[]}`. **`estado.json` não se cria na mão** — o painel cria
sozinho na primeira mexida, e criar antes só arrisca sobrescrever trabalho.

---

## §2 — Abrir o painel

Rode em SEGUNDO PLANO (o servidor fica no ar enquanto a pessoa usa):

```
cd .claude/leads/crm && node servidor.mjs
```

Ele imprime o endereço (`http://127.0.0.1:7788/`) e já abre o navegador. Se a porta estiver ocupada,
ele anda pra próxima sozinho — **leia o endereço que ele imprimiu** e é esse que você passa.

O que dizer pro usuário, em 3 linhas no máximo:
- o endereço que abriu;
- que a janela do terminal precisa ficar aberta enquanto ele usa (fechar = painel sai do ar);
- que tudo que ele mexer é gravado no projeto, então na próxima vez está lá.

Pra ele abrir sozinho depois, sem Claude Code: dois cliques em `abrir-painel.bat` (Windows) ou
`abrir-painel.command` (Mac/Linux).

**Nunca** exponha o painel na rede. O servidor só escuta em `127.0.0.1` de propósito: são dados de
contato de empresas reais.

---

## §3 — Trazer leads pra dentro

Sempre pelo script, nunca editando `leads.json` na mão:

```
cd .claude/leads/crm
node importar.mjs entrada-<lote>.json     junta leads novos (JSON no formato do modelo-dados)
node importar.mjs minha-lista.csv         junta uma planilha que a pessoa já tinha
node importar.mjs --skip                  lista quem JÁ está na base (pra prospecção não repetir)
node importar.mjs --refazer-dados         regenera só o dados.js (modo sem servidor)
```

O script imprime números reais: quantos entraram, quantos já existiam, quantos campos vazios foram
completados. **Repasse esses números como saíram.** Se entraram menos do que a prospecção achou, o
motivo é dedup — diga isso, não esconda.

O CSV pode vir com `;` ou `,`, com ou sem acento, e aceita apelidos de coluna comuns (nome, celular,
zap, fone, sinal, motivo, gancho). Linha sem nome de empresa é ignorada de propósito.

---

## §4 — Quando dá ruim (o que é cada caso)

**"node não é reconhecido" / command not found**
Não tem Node na máquina. Diga em uma linha e ofereça os dois caminhos: instalar o Node (nodejs.org,
versão LTS) ou usar o painel sem servidor. Não trate como erro do painel.

**O painel abre vazio**
Ou `leads.json` está vazio de verdade (aí o caminho é `/prospector`), ou o servidor foi aberto de
outra pasta. Confira que o `servidor.mjs` que está rodando é o de dentro de `.claude/leads/crm/`.

**"Não consegui gravar o estado no arquivo" na faixa amarela**
O servidor caiu (janela do terminal fechada). Suba de novo e mande a pessoa recarregar a página.
O que ela mexeu antes da queda já estava gravado; o que mexeu depois, não. Diga isso com essas palavras.

**Aviso "aberto sem o servidor"**
Ela abriu o `painel.html` com dois cliques. Funciona, mas o que ela mexer fica só naquele navegador
(e o Firefox nem guarda). O jeito certo é o atalho `abrir-painel`.

**Porta ocupada**
O servidor tenta 12 portas seguidas antes de desistir. Se desistiu, tem coisa demais escutando —
passe uma porta na mão: `node servidor.mjs 8100`.

**Acento saindo torto no painel**
Não é o painel. É arquivo de entrada salvo em ANSI. Regrave o JSON/CSV de entrada em UTF-8 e importe
de novo — o `importar.mjs` completa o que estava vazio, então não duplica nada.

**Perdi tudo depois de limpar o navegador**
Só acontece no modo sem servidor. Os LEADS não se perdem (estão em `leads.json`); o que se perde é
coluna/marca/anotação. Fale exatamente isso, sem enfeitar, e mude a pessoa pro modo com servidor.

---

## §5 — Backup (uma linha, sem cerimônia)

`estado.json` ganha um `.bak` a cada gravação, feito pelo próprio servidor. Pra guardar o funil
inteiro fora do projeto, é só copiar a pasta `.claude/leads/crm/` — ela é autossuficiente e abre em
qualquer máquina com Node.
