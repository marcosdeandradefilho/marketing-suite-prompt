# FICHA DE OBRA — modelo

> Copiar este bloco para dentro de `MEMORY.md`, entre os marcadores
> `<!-- INICIO-FICHAS -->` e `<!-- FIM-FICHAS -->`. Uma ficha por obra.
> Nunca apagar ficha: obra abandonada vira `arquivada`.

---

## <TÍTULO> — `<estado>`

```yaml
titulo:
titulo_provisorio:
forma:                  # fragmento | conto | novela curta | novela | romance
estado:                 # entrevista | arquitetura | rascunho | burilamento | lapidação | finalizada | arquivada | suspensa
criada_em:
atualizada_em:

# --- ORIGEM ---
imagem_semente:
ferida:
risco_assumido:
recusas: []             # o que esta obra se proíbe de ser

# --- ARGUMENTO ---
argumento: |
  <4 a 6 linhas; sem nomes; sem explicação de motivos>
epilogo_em_vista: |
  <o fim, mesmo provisório>

# --- REGIME ---
regime:
  genero_dominante:     # trágico | dramático | cômico
  irrupcoes: []         # [{bloco:, genero:, razao:}]
  tom:
  andamento_base:       # lento | oscilante | sincopado | levíssimo
  foco_narrativo:       # eu ficcional | eu confessional | alter ego | terceira | alter ego em terceira | segunda
  ponto_de_vista_dominante:
  regime_de_voz:        # Hemingway | Rulfo | Kerouac | Dostoiévski | Autran | Graciliano | híbrido
  angulo:               # fechado | aberto
  extensao_alvo:

# --- PERSONAGENS ---
personagens:
  - nome:
    metafora_do_nome:
    inominado:          # sim | não
    plano_ou_redondo:
    hierarquia:         # central | secundário | ilustrativo
    gramatica:
      pontuacao:
      tempo_verbal:
      lexico:
      tiques:
    gesto_recorrente:
    o_que_esconde:
    passado_nao_narrado:
hierarquia_de_apresentacao: []   # ordem de entrada e razão

# --- FORMA ---
dispositivo_formal:
precedente_identificado:
desvio_em_relacao_ao_precedente:
fratura_sintatica:      # onde e qual (única por obra)

eco_de_costura:
  elemento:
  plantado_em:
  retorna_em:
  como_muda:

elipses:
  - tipo:               # fato | motivo | qualidade | tempo | nome | sentido
    onde:
    permanece_aberta:   # sim | não

# --- BLOCOS ---
blocos:
  - n:
    funcao_no_todo:
    cena_ou_cenario:
    quem_ve:
    andamento:
    furos_abertos: []
    furos_fechados: []
    estado:             # planejado | rascunhado | burilado | lapidado

# --- PROCESSO ---
decisoes_tecnicas:
  - decisao:
    razao:
    quem_decidiu:       # autor | Claude (proposta aceita)
    data:
traicoes_da_planta:
  - o_que:
    por_que:
tentado_e_descartado:
  - caminho:
    razao_do_descarte:

# --- ESTADO DO TEXTO ---
texto_atual:
  palavras:
  ultimo_bloco:
  onde_parou:
  passadas_de_burilamento_concluidas:   # 0 a 6

notas:
  voz:
  pulsacao:
  invencao:
  retencao:
  inevitabilidade:

furos_abertos: []
proximo_passo:
```
