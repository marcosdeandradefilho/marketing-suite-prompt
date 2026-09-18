# 🎯 Marketing Suite — Repositório de Skills

**26 skills profissionais** de marketing, vendas, copywriting e automação — prontos para uso.

## 📦 O que você tem aqui

- **27 skills instaladas** organizadas em **6 categorias**
- Conteúdo **integral** de cada skill (configuração + documentação + exemplos)
- Estrutura **pronta para production** (sem dependências externas)
- Documentação em **pt-BR** para cada skill

## 📂 Estrutura de Diretórios

```
skills/
├── marketing-core/          # 4 skills de copywriting
├── sales-funnels/          # 2 skills de vendas
├── content-creation/       # 3 skills de criação
├── automation/             # 4 skills de automação
├── support/                # 2 skills de apoio
├── other/                  # 12 skills utilitários
└── README.md              # Este arquivo
```

## 🚀 Categorias e Skills

### 📝 Marketing Core (4 skills)

**Fundamentais para qualquer campanha de marketing.**

- **`copywriting-psychology`** — Gatilhos psicológicos de Cialdini + framework HSO
- **`headline-generator`** — Fórmula "4U" para headlines que convertem
- **`cta-optimization`** — Botões, copy, timing — tudo testado
- **`battle-tested`** — Framework provado em campanhas de alto orçamento

**Uso combinado:** Sempre use copywriting-psychology + headline-generator + cta-optimization.

### 💰 Sales Funnels (2 skills)

**Estruture funis de venda do zero.**

- **`sales-funnel-script`** — Perfect Webinar Script + 3-Act Launch + stack de valor
- **`pagina-de-vendas`** — Landing pages high-converting com psicologia de precificação

### 🎬 Content Creation (3 skills)

**Crie criativos de alta qualidade.**

- **`briefing-de-imagem`** — Design briefs prontos para usar
- **`carrossel`** — Estrutura de carrosséis que vendem
- **`reels`** — Copywriting + ideação para reels curtos e virais

### ⚙️ Automation (4 skills)

**Automatize tarefas repetitivas.**

- **`crm-leads`** — Pipeline de leads automático
- **`prospector`** — Identificação de prospects qualificados
- **`gerar-proposta`** — Propostas customizadas em minutos
- **`handoff`** — Transição automática entre equipes/etapas

### 🤝 Support (2 skills)

**Polish e humanização.**

- **`authorial-recomposition`** — Remove tom robótico, adiciona voz pessoal
- **`app-viral-framework`** — Framework de viralidade comprovado

### 📚 Other (12 skills)

Ferramentas adicionais para produtividade, segurança e documentação.

- `acelera-pc`, `preparar-maquina`, `destrava-ferramenta`
- `blindagem-de-seguranca`, `busca-documentacao`, `canal-dark`
- `oficina-mafi`, `passe-livre`, `site-institucional`, `varredura-de-mercado`

## 📖 Como Usar

### 1️⃣ Abrir uma Skill

Cada skill tem estrutura padronizada:

```
skill-name/
├── LEIA-PRIMEIRO.md    # Início rápido
├── SKILL.md            # Documentação completa
└── assets/             # Referências e templates
```

### 2️⃣ Pipeline Recomendado por Use Case

#### Para **LIVE/Webinar**
```
1. /skill sales-funnel-script (estrutura)
2. /skill headline-generator (promise)
3. /skill copywriting-psychology (body)
4. /skill cta-optimization (botão + email)
5. /skill authorial-recomposition (polimento)
```

#### Para **LANDING PAGE**
```
1. /skill sales-funnel-script (4U offer)
2. /skill headline-generator (5 opções de hero)
3. /skill copywriting-psychology (HSO framework)
4. /skill cta-optimization (botões)
```

#### Para **EMAIL SEQUENCE**
```
1. /skill headline-generator (subject lines)
2. /skill copywriting-psychology (corpo de cada email)
3. /skill cta-optimization (timing + urgência)
```

#### Para **CRIATIVOS (Posts + Ads)**
```
1. /skill headline-generator (título)
2. /skill copywriting-psychology (3-liner copy)
3. /skill briefing-de-imagem (ou carrossel/reels)
4. /skill cta-optimization (botão)
```

### 3️⃣ Instalar Localmente

```bash
# Copiar skills para ~/.claude/skills/
cp -r skills/* ~/.claude/skills/

# Validar
ls ~/.claude/skills/ | wc -l
```

## 📋 Checklist: Antes de Qualquer Campanha

- [ ] Defini meu headline com `/headline-generator`?
- [ ] Apliquei "Hook → Story → Offer" com `/copywriting-psychology`?
- [ ] Meu CTA tem verbo + benefício com `/cta-optimization`?
- [ ] Incluí urgência/escassez **real** (não fake)?
- [ ] Humanizei o texto com `/authorial-recomposition`?
- [ ] Testei com A/B (headline A vs B)?

Se sim em TODOS → Campanha pronta para rodar.

## 💡 Dicas de Ouro

### 1. Sempre use em PIPELINE
```
❌ Usar só /headline-generator = fraco
✅ /headline-generator → /copywriting-psychology → /cta-optimization = poderoso
```

### 2. Teste 3-5 variações
Gere múltiplas opções, teste as 3 melhores, continua com a vencedora.

### 3. Urgência REAL é 10x melhor
```
❌ Fake: "Oferta termina amanhã" (todos dizem)
✅ Real: "Preço sobe quando atingir 100 vendas" (52 vendidas agora)
```

### 4. Social proof ESPECÍFICO
```
❌ Genérico: "5k clientes satisfeitos"
✅ Específico: "João (taxista, SP) ganhou R$15k em 30 dias • 4.9★"
```

### 5. Story é 70% da conversão
Sempre: **Eu era assim → Fiz isso → Virei assim**

## 📞 Suporte Rápido

| Use Case | Skills |
|----------|--------|
| **LIVE** | sales-funnel-script + headline-generator + copywriting-psychology |
| **LANDING** | copywriting-psychology + cta-optimization |
| **EMAIL** | headline-generator + copywriting-psychology |
| **CRIATIVOS** | briefing-de-imagem + carrossel/reels + copywriting-psychology |

## 🔗 Referências

- **Catálogo Completo:** Veja `MARKETING-SUITE-CATALOG.md` na raiz deste repo
- **Instalar no Claude:** Veja `INSTALL.md`
- **INDEX:** Veja `INDEX.md` para lista detalhada de cada skill

## ✅ Verificação

```bash
# Contar skills
find skills -name "SKILL.md" -o -name "skill.yaml" | wc -l

# Listar todas
ls -1 skills/*/
```

---

**Status:** ✅ 27 skills prontas para uso  
**Última atualização:** 2026-09-18  
**Formato:** skill.yaml + SKILL.md (dupla redundância)  
**Garantia:** Testadas em campanha ao vivo

