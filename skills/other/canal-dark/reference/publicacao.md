# publicacao.md — o pacote pronto pra subir no YouTube

O vídeo renderizado é metade do trabalho. A outra metade é o PACKAGING de publicação: título,
descrição, capítulos, tags e hashtags nas boas práticas do YouTube, prontos pra copiar e colar.
Quem faz a parte determinística (capítulos com os tempos REAIS, validação de limite) é o
`scripts/publicar.py`. Quem escreve a parte criativa é você (o Claude), num `publicar-input.json`.

## O fluxo (Stage 13)

1. Você escreve `<projeto>/06-saida/publicar-input.json` (contrato abaixo), seguindo as regras.
2. Rode `python scripts/publicar.py <projeto>`.
3. Ele lê o input + o `01-voz/manifest.json` (tempos) + o `03-clipes/creditos.json` e escreve
   `<projeto>/06-saida/PUBLICAR.txt` — texto puro, um bloco por campo do Studio, capítulos já
   calculados, tudo conferido. Ele imprime avisos `[CONFERIR]` no fim se algo furou um limite.
4. Se aparecer `[CONFERIR]`, conserte o `publicar-input.json` e rode de novo.

## O contrato — publicar-input.json

```json
{
  "titulo": "A LICAO DE EPICTETO QUE APAGA A ANSIEDADE | Estoicismo",
  "titulos_alternativos": ["...", "...", "..."],
  "descricao_gancho": "1 a 2 frases fortes. E o que aparece antes do 'mostrar mais'.",
  "descricao_corpo": "2 a 4 paragrafos. Use \\n\\n entre eles.",
  "capitulos": ["Rotulo do bloco 1", "Rotulo do bloco 2", "..."],
  "hashtags": ["estoicismo", "filosofia", "epicteto"],
  "tags": ["estoicismo", "epicteto", "filosofia estoica", "ansiedade"]
}
```

- `capitulos`: UM rótulo por bloco do roteiro, na ordem. O publicar.py casa cada rótulo com o
  tempo REAL de início daquele bloco (do manifest) e força o primeiro a 0:00. Rótulo de
  espectador ("As duas caixas"), não a função interna do bloco ("gancho").

## As regras (fontes oficiais — dossiê publicacao-youtube.md)

### Título
- Limite duro: **100 caracteres**. O começo (~50) é o que aparece no celular e na busca —
  o gancho e a palavra-chave têm que estar nas **primeiras 4–5 palavras**.
- Alavancas de CTR: 1 número específico, curiosidade (não entregue a resposta), 1–2 palavras
  fortes. CAIXA ALTA em 1–2 palavras e o separador "|" são padrão do nicho, sem exagero.
- Ofereça **até 3 alternativos** (o "Testar e comparar" nativo do YouTube roda até 3 títulos e
  decide por TEMPO DE EXIBIÇÃO, não CTR).

### Descrição
- Limite: **5000 caracteres**. As primeiras ~157 (desktop) / ~100 (celular) são o que aparece
  antes do "mostrar mais" [OFICIAL: "as primeiras linhas são o que o espectador vê primeiro"].
  Ponha a palavra-chave principal + o gancho aí.
- A descrição AINDA ajuda a busca/algoritmo [OFICIAL], MAS keyword stuffing prejudica. Uma
  descrição única por vídeo. ~800–1300 caracteres bastam. Link/redes/CTA vão ABAIXO da dobra.

### Capítulos (todos OFICIAIS — se um falhar, o YouTube não gera nenhum). O publicar.py garante:
- Primeira linha exatamente **0:00**.
- **Mínimo 3** capítulos, em ordem crescente.
- Cada capítulo **≥ 10 segundos** do anterior (bloco curto demais é absorvido no anterior).
- Formato `M:SS Rótulo` (ou `H:MM:SS Rótulo`), um por linha.

### Tags
- Papel MÍNIMO na descoberta hoje [OFICIAL]. 5–10 tags relevantes bastam; inclua 1–2 grafias
  alternativas se a palavra-chave for muito escrita errada. Não gaste esforço aqui.

### Hashtags
- Limite duro oficial: **60** (acima disso o YouTube IGNORA TODAS). O "15" que circula é boato
  velho. Mas o ideal é **3 a 5** fortes, na descrição. As 3 primeiras aparecem acima do título.

### Conteúdo alterado ou sintético (IA) — importante neste pipeline
- No upload, em Atributos → "Conteúdo alterado ou sintético", **marque SIM**. A narração é voz
  de IA (não é a voz do criador) e, se houver música de IA, isso é gatilho explícito [OFICIAL].
- No caso (áudio de IA + b-roll de acervo, sem pessoa/evento real falsificado), o selo aparece
  na DESCRIÇÃO EXPANDIDA, não no player. Marcar SIM não tira monetização por si só.
- Isento (não precisa marcar): roteiro feito com IA e clonar a PRÓPRIA voz. Como aqui a voz é
  sintética genérica, o padrão seguro é marcar SIM. O publicar.py já escreve esse lembrete no
  PUBLICAR.txt.
