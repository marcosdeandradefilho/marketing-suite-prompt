---
name: analise_authormaton_technical_content_synthesis
description: Análise de Authormaton/marketing; conceito de verifiable synthesis + multi-agent workflows aplicável a SuperAgent e ENADE
metadata:
  type: project
  date: 2026-09-17
  status: avaliado; skill futura pendente
  source: https://github.com/Authormaton/marketing
---

# Authormaton: Technical Content Synthesis Pattern

## O que é Authormaton

Plataforma para geração de conteúdo técnico com IA, focada em:

1. **Human-Quality Writing** — escrita com profundidade de especialista, não genérica
2. **Verifiable Synthesis** — cada afirmação linkada a fontes verificáveis com rastreabilidade completa
3. **Multi-Agent Workflows** — agentes coordenados em pipeline: research → analysis → writing → review
4. **Human-AI Collaboration** — IA executa, humano estrategiza (não o inverso)

## Relevância para Marcos

### Aplicável imediatamente a:
- [[superagent_corte_de_exibicao_vs_geracao]] — SuperAgent v3.2 já implementa verifiable synthesis (bijeção URL↔referência, zero DOI fabricado)
- [[projeto_enade_app_gamificado]] — ENADE precisa de síntese verificável para respostas (edital 2024/2025 exige precisão)
- [[projeto_atlas_virtual_literatura_univisa]] — Atlas IELit beneficiaria de multi-agent para síntese de crítica literária

### Padrão de Ouro
Authormaton demonstra que **multi-agent + verifiable synthesis** é o padrão competitivo (não 1 agente monolítico):
- Research agent (busca/síntese de fontes)
- Analysis agent (interpretação/crítica)
- Writing agent (composição de estilo)
- Review agent (validação de precisão + factualidade)

## Arquivo do repositório
- **Status:** É apenas site Next.js de marketing, **não contém skill/prompts/agentes executáveis**
- **Valor:** Conceito replicável, não código reusável

## Skill futura sugerida

`/technical-content-synthesis` — coordena multi-agent para escrita técnica com verificação de fontes:
- Entrada: tema + formato (artigo/doc/post)
- Pipeline: research (Perplexity/SerpAPI) → analysis (Claude) → writing (Claude) → review (fact-check)
- Saída: conteúdo + referências verificadas + dashboard de confiança por seção

**Bloqueador:** Exige decisão de Marcos sobre model stack (Perplexity API custo vs. gratuito sonar-deep-research).

## Referências cruzadas

- [[superagent_corte_de_exibicao_vs_geracao]] — padrão de síntese verificável já em produção
- [[projeto_enade_app_gamificado]] — próximo projeto que se beneficiaria
- [[TEMPORAL-LOBE]] § `regra-pickaxe-zero-claude-models` — constraint de custo aplicável também aqui
