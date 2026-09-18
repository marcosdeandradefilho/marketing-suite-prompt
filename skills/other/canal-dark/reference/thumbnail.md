# thumbnail.md — a miniatura (Stage 11)

A thumb decide o clique. As regras aqui não saíram de blog de CTR: saíram de medição própria de
12 pares **outlier × mediana dentro do MESMO canal** (mesma audiência, mesmo template — o que
sobra de diferença é o que fez estourar).

A skill entrega **duas** thumbs: a que ela renderiza aqui (determinística, sem chave) e um
**prompt pronto pra colar no ChatGPT**. Quem escolhe é o usuário.

---

## 1. Primeiro decida o ARQUÉTIPO. Só depois o layout.

Não existe regra única de "máximo 4 palavras". O campeão da amostra (408x a mediana do canal
dele) tem 7 palavras. O que manda é o tipo de vídeo.

**ARQUÉTIPO A — a IMAGEM manda.**
Mistério, caso real, documentário, "isso existe?", crime, achado impossível.
0 a 4 palavras, às vezes ZERO texto. O quadro mostra uma ANOMALIA e o texto atrapalha.
Layouts: `anomalia`, `evidencia`, `cena`, `simbolo`.

**ARQUÉTIPO B — o TEXTO manda.**
Estoicismo, motivação, dinheiro, conselho, hábitos, listas.
5 a 9 palavras em 3 a 5 LINHAS, caixa alta, ocupando 50–70% do quadro, alternando branco e a
cor de acento, com um retrato/busto ocupando um terço.
Layouts: `retrato`, `citacao`, `manchete`.

Na dúvida entre os dois: se o valor do vídeo é *ver* uma coisa, é A. Se o valor é *saber* uma
coisa, é B.

---

## 2. As leis medidas (as que se repetiram nos 12 pares)

1. **A copy é a variável, não a arte.** Dois pares tiveram arte IDÊNTICA no outlier e no
   mediano (Caminhos da Alma 19x, Escola da Filosofia 22x). Só mudou a frase. Trate o texto da
   thumb como copy, com fórmula — nunca como rótulo do assunto.
2. **O acento de cor cai na PUNCHLINE, não no tema.** "envergonhe quem não `TE RESPEITA`"
   ganhou de "`O DESAPEGO` muda tudo". Mesmo canal, mesma arte.
3. **Marca de anotação é a arma mais barata.** Seta, círculo, barbante de mural. Em 4 dos 12
   vencedores; em NENHUM dos medianos. Ela obriga o olho a caçar e cria a pergunta. Máximo uma
   por thumb.
4. **Revelação parcial ganha de revelação total.** Criatura cortada na borda bateu a criatura
   inteira e centralizada em 4,8x. Mostrar tudo mata o motivo de clicar.
5. **Escala humana faz o impossível virar crível.** Um homem em pé do lado do muro fez 15x num
   canal de 14,9 mil inscritos. Sem ele, é só uma parede.
6. **Canal faceless não é thumb sem rosto.** 10 dos 12 vencedores têm rosto como ponto focal —
   do personagem, da vítima, da autoridade, da estátua, da criatura. Não é o rosto do dono do
   canal. Se der pra colocar um rosto humano com emoção legível, coloque.
7. **A imagem tem que PAGAR a promessa do texto.** "Atraente" com um casal fez 408x; "atraente"
   com um guerreiro bravo afundou. Mesma palavra, canais parecidos.
8. **Bagunça mata.** Todo mediano da amostra tinha mais objeto no quadro que o outlier do mesmo
   canal. Sem exceção. Um assunto só, reconhecível em menos de 1 segundo.
9. **Amarelo em preto é a paleta que domina o dark BR.** Use `#f2c230` como primeira opção e
   `#e8804f` (brasa) como alternativa. UMA cor de acento pro canal inteiro, fixa entre vídeos.
   Vermelho entra só como MARCA (seta, círculo, caixa da punchline), nunca como fundo.
10. **Consistência de marca.** Mesma fonte, mesma cor de acento, logo/ícone sempre no mesmo
    canto. Todo canal que cresce na amostra tem isso.
11. **Instrução com QUANDO ganha de frase de autoajuda.** "Ouça isso todas as manhãs" fez 28x
    contra "desperte sua melhor versão".

---

## 3. Fórmulas de copy que estouraram (use uma, não invente)

| — | Fórmula | Exemplo medido | Ganho |
|---|---|---|---|
| F1 | Instrução + quando | OUÇA ISSO TODAS AS MANHÃS | 28x |
| F2 | Inimigo social | ENVERGONHE QUEM NÃO TE RESPEITA | 19x |
| F3 | Dor nomeada (COMO NÃO) | COMO NÃO FICAR COM RAIVA E NEM SE INCOMODAR | 22x |
| F4 | Citação de autoridade (entre aspas) | "EU FICARIA RICO EM 6 MESES COM UM SALÁRIO MÍNIMO" | 80x |
| F5 | Promessa + imagem que prova | SEJA ATRAENTE SEM DIZER UMA PALAVRA (+ casal na foto) | 408x |
| F6 | Confronto direto | ENTÃO POR QUE VOCÊ NÃO FAZ? | 29x |
| F7 | Anomalia sem texto | foto única do impossível + seta | 15x |

Âncora brasileira quando couber: salário mínimo, R$, classe social, nome de caso ou cidade/UF
("URUPEMA - SC"). É o que gringo não copia.

A frase da thumb **não é o título do vídeo**. Título e thumb dizem coisas diferentes que se
somam; repetir o título em texto foi o que os medianos fizeram.

---

## 4. O fluxo determinístico (sem gerador de imagem, sem chave)

1. Decida o arquétipo (§1), a fórmula de copy (§3) e o layout.
2. Escolha UMA foto de fundo forte do Pexels pro gancho (escura, cinematográfica, 1 assunto —
   ex.: "marcus aurelius bust statue dark", "stormy ocean night", "ancient ruins fog"), ou um
   frame marcante de um clipe já baixado. Confira se a foto PAGA a promessa da frase (lei 7).
3. **REDUZA a foto pra ~1280px de largura antes de renderizar** (passo obrigatório):
   `ffmpeg -y -i <foto> -vf "scale=1280:-1" -q:v 3 <foto-sm.jpg>`.
   Foto do Pexels vem com 4000px+; jogar isso num render 2560x1440 trava o screenshot do
   Chrome sob pressão de RAM (bug real, medido). Reduzida, renderiza liso e fica igual.
4. Preencha `assets/thumb/template.html` (1 ou 2 variantes) e renderize todas de uma vez num
   navegador só: `node scripts/thumb.js --multi <a.html> <a.png> <b.html> <b.png>`
   (o `--multi` faz UM cold-start em vez de N — no Windows, abrir vários headless em sequência
   estoura o watchdog).
5. LEIA os PNGs (é o portão visual). Escolha a melhor ou ajuste e re-renderize. Se o
   Node/Chrome faltar, avise e peça pra fazer na mão — nunca finja que gerou.

**Se o `thumb.js` der `ERR timeout`:** não é o HTML, é a FOTO. Certas fotos travam o Chrome
mesmo já em 1280px (medido: o mesmo HTML renderiza liso trocando só o arquivo da foto).
Na ordem: (a) reduza mais, pra 960px
(`ffmpeg -y -i <foto> -vf "scale=960:-1" -q:v 4 <foto-960.jpg>`) — resolveu no caso medido;
(b) se ainda travar, troque a foto de fundo; (c) só então avise que não deu.
Nunca diga que gerou um PNG que não existe.
6. Gere o pacote do ChatGPT (§6).

---

## 5. O template — placeholders

`{{FONTE}}` (caminho do Anton) · `{{IMG}}` (a foto JÁ reduzida) · `{{LAYOUT}}` ·
`{{ACENTO}}` (`#f2c230` ou `#e8804f`) · `{{TAMANHO}}` (font-size em px) · `{{TITULO}}` (as
linhas) · `{{MARCA}}` (seta/círculo ou vazio) · `{{SELO}}` (opcional).

O título vai em LINHAS, com a punchline marcada:

```html
<span class="l">ENVERGONHE</span>
<span class="l">QUEM NÃO</span>
<span class="l a">TE RESPEITA</span>
```

`.l` = linha branca · `.l.a` = linha no acento (a punchline) · `.l.cx` = linha em caixa cheia
(punchline de citação) · `<b>` = uma palavra solta no acento dentro de uma linha branca.

Tamanho por número de linhas: 2 → 168px · 3 → 132px · 4 → 104px · 5 → 86px (no layout
`manchete`, 3 linhas → 176px).

Os 7 layouts, os snippets prontos de seta e círculo e as regras que não afrouxam estão no
comentário do topo do `template.html`. Leia antes de preencher.

---

## 6. O pacote do ChatGPT (entrega junto, sempre)

Copie `assets/thumb/prompt-chatgpt.md` pra `<projeto>/06-saida/prompt-chatgpt.md` e preencha os
placeholders. O prompt vai em INGLÊS (o gerador obedece melhor); o texto da thumb vai em
PORTUGUÊS entre aspas; tudo que o usuário lê vai em PT-BR.

O que faz o prompt funcionar, na ordem de importância:

- **Texto exato entre aspas e em CAIXA ALTA**, linha por linha, num bloco `Typography:`
  separado. Aspas e caixa alta funcionam como restrição dura. Nunca deixe o modelo escolher a
  frase, e nunca deixe ele "melhorar" o português.
- **Uma linha curta por vez.** A precisão cai com linha longa.
- **Fonte descrita por função**, não por nome ("bold condensed sans-serif, very heavy weight,
  tight tracking"). Nome de fonte é só pista de estilo; ele não carrega o arquivo.
- **Restrinja o que importa.** O que não é restringido sai no default feio.
- **Negativas explícitas**: nenhum outro texto, sem marca d'água, sem logo, nada encostando na
  borda.
- **Layout em posição**, não em vibe ("subject on the right third facing left, text block on
  the left half, bottom-right corner empty").
- **Corrija em conversa, uma variável por vez**, em vez de reescrever o prompt inteiro.

Estado da ferramenta: o modelo atual é o ChatGPT Images 2.0 (`gpt-image-2`, anunciado pela
OpenAI em 21/04/2026). Aceita pedido de proporção, então dá pra pedir 16:9 direto — mas confira
e corte se voltar 3:2. A nota antiga de que "gpt-image só faz 1:1/3:2/2:3" é da geração
anterior e não vale mais.

**O risco real é ACENTO.** Modelo treinado majoritariamente em inglês erra diacrítico: til que
vira traço, cedilha que some, letra trocada no meio da palavra. Melhorou muito, continua
acontecendo. Por isso o arquivo entregue já leva o checklist de conferência letra por letra e o
**plano B**: pedir a mesma imagem SEM texto e assar a manchete por cima no template daqui, que
controla o texto no pixel. Cena do ChatGPT + texto certo.

Segundo risco: pessoa real. A política afrouxou, mas ainda recusa em vários casos. Não dependa
disso — descreva a pessoa em vez de nomear, ou use foto de imprensa como fundo.

Nunca prometa que o ChatGPT vai acertar de primeira. A skill entrega as duas opções e o
usuário compara.

---

## 7. Técnico (YouTube Help oficial)

1280x720 é baseline válido (acima do mínimo de 640px). O `thumb.js` renderiza a 2x → 2560x1440
pra o texto não borrar. PNG/JPG, abaixo de 2MB, 16:9.

Teste final dos dois caminhos: encolha pra ~160px (o tamanho real no celular). Não leu? Menos
palavra, fonte maior, mais contraste.
