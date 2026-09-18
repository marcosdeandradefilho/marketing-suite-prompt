# ENTRADA DE MEMÓRIA — modelo de fim de sessão

> Preencher e aplicar a `MEMORY.md` antes de encerrar qualquer sessão produtiva.
> Ordem obrigatória: índice → léxico → ficha → furos transversais → diário.

---

## 1. Índice de obras (atualizar linha)

```markdown
| <#> | <Título> | <forma> | <estado> | <palavras> | <AAAA-MM-DD> |
```

## 2. Léxico ocupado (acrescentar; nunca remover)

```yaml
nomes_de_personagem: ["<nome> — <metáfora> (<obra>)"]
toponimos: ["<lugar> (<obra>)"]
imagens_matriciais: ["<imagem> (<obra>)"]
estruturas_formais_ja_usadas: ["<dispositivo> (<obra>)"]
primeiras_frases_ja_usadas: ["<frase> (<obra>)"]
finais_ja_usados: ["<gesto final> (<obra>)"]
```

## 3. Ficha da obra

Inserir ou atualizar entre `<!-- INICIO-FICHAS -->` e `<!-- FIM-FICHAS -->`,
usando `templates/FICHA-OBRA.md`.

Campos que mudam com mais frequência:

```yaml
estado:
atualizada_em:
texto_atual: {palavras:, ultimo_bloco:, onde_parou:, passadas_concluidas:}
decisoes_tecnicas: [{decisao:, razao:, quem_decidiu:, data:}]
traicoes_da_planta: [{o_que:, por_que:}]
tentado_e_descartado: [{caminho:, razao_do_descarte:}]
furos_abertos: []
proximo_passo:
```

## 4. Furos abertos transversais

```yaml
- pergunta:
  origem:
  potencial:
```

## 5. Decisões de poética (só se a decisão valer além desta obra)

```markdown
| <AAAA-MM-DD> | <decisão> | <obra de origem> | vigente |
```

## 6. Diário de sessões

```markdown
| <AAAA-MM-DD> | <obra> | <fase> | <o que foi feito> | <próximo passo> |
```

---

## Verificação antes de encerrar

- [ ] índice atualizado
- [ ] léxico acrescido (nada removido)
- [ ] ficha atualizada entre os marcadores
- [ ] decisões distinguem o que o autor decidiu do que Claude propôs
- [ ] toda decisão está datada
- [ ] traições da planta registradas com razão
- [ ] o que foi tentado e descartado está registrado
- [ ] próximo passo declarado no diário
