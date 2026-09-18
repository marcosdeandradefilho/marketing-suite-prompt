# Oficina MAFI

Pacote de skills de criação literária para Claude, construído sobre o método integral de
**Raimundo Carrero** (*Os segredos da ficção*, Agir, 2005) e configurado como um único
cérebro autoral: o de **Marcos de Andrade Filho**.

---

## O que o pacote faz

- Entrevista o autor e extrai a matéria viva de uma obra nova
- Arquiteta a narrativa com planta baixa completa (esboço → argumento → blocos)
- Escreve rascunhos sob comando e os burila em seis passadas
- Lapida o texto até o padrão de consagração e emite laudo técnico
- Continua textos interrompidos preservando voz, pulso e decisões anteriores
- Diagnostica e eleva textos já escritos sem trair a voz do autor
- Mantém memória permanente de todas as obras, nomes, decisões e furos abertos

---

## Estrutura

```
oficina-mafi/
├── SKILL.md                          orquestradora (autocontida)
├── CLAUDE.md                         identidade e preferências do autor
├── MEMORY.md                         memória viva das obras
├── README.md
├── skills/
│   ├── 01-entrevista-autoral/        levantamento em 7 perguntas
│   ├── 02-voz-narrativa/             investigação da frase; indireto livre
│   ├── 03-foco-narrativo/            eu ficcional, alter ego, 2ª e 3ª pessoa
│   ├── 04-personagem/                nome como metáfora; Teoria da Iluminação
│   ├── 05-cena-e-cenario/            distinção, ângulo, espaço e tempo
│   ├── 06-dialogos-e-vozes/          as cinco formas; monólogo e fluxo
│   ├── 07-elipse-e-bordado/          Henry James, Calvino, o "branco" de Proust
│   ├── 08-pulsacao-narrativa/        tom, andamento, efeito, função, ritmo
│   ├── 09-genero-tom-andamento/      trágico, dramático, cômico
│   ├── 10-arquitetura-da-narrativa/  imaginar, inventar, selecionar; argumento
│   ├── 11-rascunho/                  impulso materializado; /continuar
│   ├── 12-burilamento/               seis passadas; laudo técnico
│   ├── 13-lapidacao-nobel/           irredutibilidade, inevitabilidade, permanência
│   ├── 14-invencao-contemporanea/    dispositivo formal; aprisionamento do leitor
│   └── 15-memoria-e-coerencia/       protocolo de MEMORY.md
├── referencias/
│   ├── carrero-mapa-tecnico.md       doutrina completa com exemplos canônicos
│   ├── glossario-operacional.md      definições sem ambiguidade
│   ├── checklist-nobel.md            40 verificações finais
│   └── protocolo-antisimulacro.md    o que nunca escrever
├── templates/
│   ├── FICHA-OBRA.md
│   ├── DOSSIE-PERSONAGEM.md
│   ├── PLANTA-BAIXA.md
│   └── ENTRADA-MEMORY.md
└── scripts/
    └── validar_pacote.py             validação de integridade
```

---

## Instalação

O pacote foi desenhado como **monorepo de skill**: a orquestradora referencia as demais
por caminho relativo, e nada quebra desde que a pasta permaneça inteira.

### Opção A — Claude Projects (recomendada)

1. Crie um Projeto novo, dedicado (arquitetura "um tema = um projeto").
2. Descompacte o zip e envie **todos os arquivos `.md`** ao *Project knowledge*.
3. Cole o conteúdo de `SKILL.md` nas **instruções do Projeto**.
4. Abra um chat novo e escreva `/entrevista` ou apenas descreva uma ideia.

> `MEMORY.md` precisa ser reenviado ao Projeto sempre que for atualizado — é assim que a
> memória persiste entre conversas.

### Opção B — Claude Code / sistema de arquivos

```bash
unzip oficina-mafi.zip -d ~/.claude/skills/
python3 ~/.claude/skills/oficina-mafi/scripts/validar_pacote.py ~/.claude/skills/oficina-mafi
```

Neste modo `MEMORY.md` é atualizado no disco e a persistência é automática.

### Opção C — skills instaladas separadamente

Se preferir instalar cada subskill de forma independente, os `name` já vêm prefixados
com `mafi-` para evitar colisão. Neste caso, ajuste os caminhos relativos citados na
orquestradora para os nomes de skill correspondentes.

---

## Uso

| Comando | O que faz |
|---|---|
| `/entrevista` | Abre obra nova; 7 perguntas; devolve bloco de matéria viva |
| `/arquitetar` | Esboço → argumento → planta baixa completa |
| `/rascunhar` | Escreve o texto bruto, bloco a bloco |
| `/burilar` | Seis passadas de investigação, com diário de operações |
| `/lapidar` | Camada final; checklist de 40 itens; dossiê de lapidação |
| `/continuar` | Retoma texto interrompido após extração de DNA |
| `/diagnosticar` | Laudo técnico de qualquer texto colado |
| `/memoria` | Estado da oficina: obras, decisões, furos, alertas |

Comandos são opcionais: a orquestradora infere a fase pelo que você trouxer.

---

## Validação

```bash
python3 scripts/validar_pacote.py .
```

Verifica arquivos obrigatórios, frontmatter YAML, formato e unicidade dos campos `name`,
resolução de todas as referências cruzadas, marcadores de `MEMORY.md` e arquivos órfãos.
Sem dependências externas. Código de saída 0 = íntegro.

---

## Notas de método

- Nenhum texto sai da oficina antes de três passadas completas.
- Nenhum recurso permanece no texto sem **função** e **efeito** declarados.
- Nenhuma sessão produtiva encerra sem registro em `MEMORY.md`.
- Elogio vazio é o único crime imperdoável da oficina.

---

## Fonte

CARRERO, Raimundo. *Os segredos da ficção: um guia da arte de escrever narrativas*.
Rio de Janeiro: Agir, 2005. 336 p.

O pacote sistematiza e operacionaliza o método do livro. Todos os exemplos citados nas
skills são referenciados à obra e a seus autores originais. Nenhum trecho extenso é
reproduzido: as passagens servem de demonstração técnica pontual, com atribuição.

Textos produzidos com este pacote são de autoria de **Marcos de Andrade Filho**.
