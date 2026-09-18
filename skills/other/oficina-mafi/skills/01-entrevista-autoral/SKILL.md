---
name: mafi-entrevista-autoral
description: Conduz a entrevista breve e cirurgica que abre toda obra nova na Oficina MAFI, extraindo do autor a materia viva (impulso, imagem-semente, obsessao, risco) antes de qualquer planejamento. Use quando o usuario trouxer uma ideia solta, uma manchete, um sonho, uma cena, um nome, uma frase que nao sai da cabeca, ou disser que quer escrever algo mas nao sabe o que; e sempre que o comando /entrevista for dado. Nao use para textos ja iniciados.
---

# 01 — Entrevista Autoral

A entrevista é curta de propósito. Carrero é explícito: o autor naufraga quando é
julgado no impulso. Aqui não se julga — se colhe.

**Duração:** uma rodada de 7 perguntas. No máximo uma rodada de follow-up.
**Proibido:** pedir "detalhes do enredo". Enredo é desenvolvimento, vem depois.

## Regra de ouro

O autor quase nunca sabe o que quer escrever. Ele sabe o que **não o larga**. A
entrevista serve para localizar o que não o larga.

## As sete perguntas

Faça-as em bloco, numeradas, permitindo resposta parcial. Se o autor responder três,
está bom — trabalhe com três.

```
1. IMAGEM-SEMENTE
   Que imagem, frase ou cena vem voltando sem pedir licença? Descreva em bruto,
   sem organizar. Se for uma manchete, um sonho ou algo que você viu na rua, melhor.

2. FERIDA
   O que nessa imagem incomoda você especificamente — não o leitor, você?

3. CORPO
   Quem está ali? Não precisa de nome. "Uma mulher", "o homem", "ele" basta.
   O que essa pessoa faz com as mãos?

4. TEMPO
   Isso acontece em quanto tempo? Uma hora? Vinte anos? Um instante que se repete?

5. VOZ
   Se essa pessoa falasse com você agora, ela falaria como? Culta, atravessada,
   econômica, torrencial? Escreva uma frase que ela diria.

6. RISCO
   O que você teria medo de escrever nessa história? Diga mesmo assim.

7. RECUSA
   O que essa história NÃO pode ser? Que versão dela seria a versão fácil?
```

## Perguntas de follow-up (usar só se necessário)

Escolha no máximo duas, e só se a resposta anterior abriu um furo produtivo:

- Você já sabe o fim? (Se sim, guarde-o; Poe exige o epílogo em vista.)
- Existe alguém no mundo real por trás dessa figura? (Só para o autor; não vai ao texto.)
- Que cheiro tem esse lugar?
- O que essa pessoa esconde de quem convive com ela?
- Quem conta isso: alguém dentro ou alguém encostado?

## Se o autor não tem nada

Não force. Aplique o **método da manchete** (Carrero):

1. Peça uma manchete de jornal — real, de hoje — sem ler a matéria.
2. Trabalhe apenas com a manchete. A matéria estraga: ela responde antes da hora.
3. Faça as perguntas: quem é essa pessoa? o que fez? qual o rosto ainda na sombra?

Exemplo canônico do método: *"Mulher tenta suicídio no mar e é salva por pescadores."*
Toda a arquitetura de uma narrativa cabe ali, e nada está resolvido.

Alternativas equivalentes quando não há jornal: uma frase ouvida de estranho, uma
fotografia antiga, um objeto herdado, uma pergunta que alguém fez e ficou.

## Saída obrigatória da entrevista

Devolva ao autor um bloco compacto — **nunca mais de 200 palavras** — no formato:

```yaml
titulo_provisorio: <apelido de trabalho, pode ser feio>
imagem_semente: <uma frase>
ferida: <uma frase>
figura_central: <inominada por enquanto>
gesto_recorrente: <o que faz com as mãos/corpo>
regime_temporal: <instante | dia | ano | décadas | tempo circular>
amostra_de_voz: "<a frase que o personagem diria>"
risco_assumido: <o que dá medo>
recusa: <a versão fácil que fica proibida>
lacunas: [<o que o autor não respondeu>]
```

Depois pergunte, exatamente uma coisa: **"Posso arquitetar?"**

Se sim → `skills/10-arquitetura-da-narrativa/SKILL.md`.

## Registro

Crie imediatamente a ficha da obra em `MEMORY.md` com estado `entrevista`, usando
`templates/FICHA-OBRA.md`. Sem isso, a sessão seguinte recomeça do zero.

## Erros que matam esta fase

| Erro | Por quê |
|---|---|
| Perguntar "qual é o conflito?" | Conflito é achado, não declarado. |
| Sugerir enredo antes do autor terminar | Você rouba o impulso dele. |
| Elogiar a ideia | Elogio no impulso trava; Carrero avisa. |
| Pedir mais de sete respostas | Vira formulário, mata a matéria viva. |
| Nomear o personagem agora | O nome vem depois, e é metáfora — ver skill 04. |
| Corrigir a linguagem do autor | A voz dele é o material bruto. Preserve o barulho. |
