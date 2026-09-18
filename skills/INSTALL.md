# 📦 INSTALL — Como Instalar as Skills

Instruções para instalar as 27 skills do marketing-suite no seu ambiente local.

---

## 🔧 Instalação Rápida (1 minuto)

### Terminal/PowerShell/Bash

```bash
# 1. Clone ou baixe este repositório
git clone https://github.com/marcosdeandradefilho/marketing-suite-prompt.git
cd marketing-suite-prompt

# 2. Copie a pasta 'skills' para o seu vault local
cp -r skills/* ~/.claude/skills/

# 3. Valide
ls ~/.claude/skills/ | grep -E "copywriting|headline|cta-optimization" | wc -l
# Deve mostrar: 3
```

---

## 📂 Estrutura de Instalação

### Caminho de Instalação

```
~/.claude/skills/                    # Vault local de skills
├── copywriting-psychology/
├── headline-generator/
├── cta-optimization/
├── sales-funnel-script/
├── ...
└── (27 skills totais)
```

### Por Sistema Operacional

**macOS / Linux:**
```bash
~/.claude/skills/
```

**Windows (PowerShell):**
```
$env:USERPROFILE\.claude\skills\
```

**Windows (Git Bash):**
```bash
~/.claude/skills/
```

---

## 🔍 Verificação Pós-Instalação

### 1️⃣ Contar Skills Instaladas
```bash
ls ~/.claude/skills/ | wc -l
# Esperado: 27+
```

### 2️⃣ Verificar Skills Específicas
```bash
# Verificar as 4 principais
for skill in copywriting-psychology headline-generator cta-optimization sales-funnel-script; do
  [ -d ~/.claude/skills/$skill ] && echo "✓ $skill" || echo "✗ $skill"
done
```

### 3️⃣ Validar Estrutura
```bash
# Contar arquivos de configuração
find ~/.claude/skills -name "*.yaml" -o -name "SKILL.md" | wc -l
# Esperado: 27+
```

### 4️⃣ Usar no Claude Code
```bash
# Abrir Claude Code
claude

# Digitar na sessão
/skill copywriting-psychology

# Você deve ver a skill carregada ✓
```

---

## 🚨 Troubleshooting

### Problema: Skills não aparecem no `/skill`

**Solução 1:** Reiniciar Claude Code
```bash
# Feche e abra novamente
exit
claude
```

**Solução 2:** Verificar caminho
```bash
# Confirmar que o caminho existe
ls -la ~/.claude/skills/copywriting-psychology/
# Deve mostrar: skill.yaml ou SKILL.md
```

**Solução 3:** Permissões
```bash
# Dar permissão de leitura
chmod -R 755 ~/.claude/skills/
```

### Problema: "Skill not found"

**Causa:** Skills não foram copiadas corretamente

**Solução:**
```bash
# 1. Remover instalação anterior
rm -rf ~/.claude/skills/*

# 2. Copiar novamente
cp -r ./skills/* ~/.claude/skills/

# 3. Validar
ls ~/.claude/skills/ | wc -l
```

### Problema: Alguns arquivos não copiam

**Causa:** Permissões ou espaço em disco

**Solução:**
```bash
# Verificar espaço
df -h ~

# Verificar permissões
ls -la ~/.claude/

# Se necesário, criar diretório manualmente
mkdir -p ~/.claude/skills
```

---

## 🔄 Atualização das Skills

### Atualizar uma Skill Específica

```bash
# Copiar nova versão
cp -r ./skills/copywriting-psychology/* ~/.claude/skills/copywriting-psychology/

# Confirmar
ls ~/.claude/skills/copywriting-psychology/
```

### Atualizar Todas

```bash
# Backup (opcional)
cp -r ~/.claude/skills ~/.claude/skills.backup

# Copiar versão nova
cp -r ./skills/* ~/.claude/skills/

# Validar
ls ~/.claude/skills/ | wc -l
```

---

## 📱 Instalação no Claude.ai (Web)

Skills locais **não** sincronizam automaticamente com Claude.ai.

**Opção 1:** Use Claude Code (CLI)
- Instale localmente (veja acima)
- Use via `/skill` no Claude Code terminal

**Opção 2:** Copie o conteúdo manualmente
1. Abra a skill em `skills/marketing-core/copywriting-psychology/SKILL.md`
2. Copie o conteúdo
3. Crie uma "Custom Instructions" no Claude.ai com o conteúdo
4. Use prefixo `[copwriting-psychology]` em suas prompts

**Opção 3:** Sincronize via Claude Docs (futuro)
- Se usar Claude Projects, você pode importar skills lá

---

## 🎯 Próximos Passos

### 1️⃣ Testar Primeira Skill
```bash
# Abrir Claude Code
claude

# Usar skill
/skill copywriting-psychology

# Pedir um exemplo
Gere um copy persuasivo para um curso de R$297
```

### 2️⃣ Criar Seu Primeiro Pipeline
```bash
/skill headline-generator
# Gere 5 headlines para landing page

/skill copywriting-psychology
# Escreva a copy principal

/skill cta-optimization
# Otimize o botão de compra
```

### 3️⃣ Compartilhar Skills com Time
```bash
# Se você está em um time, compartilhe:
# 1. Clone do repositório
# 2. Link para este INSTALL.md
# 3. Arquivos de cada skill (LEIA-PRIMEIRO.md)
```

---

## 💾 Backup e Sincronização

### Fazer Backup
```bash
# Backup completo
cp -r ~/.claude/skills ~/.claude/skills.backup.$(date +%Y%m%d)

# Listar backups
ls -la ~/.claude/ | grep "skills.backup"
```

### Sincronizar Entre Máquinas
```bash
# Máquina 1 (origem): Enviar via git/arquivo
tar czf skills.tar.gz ~/.claude/skills/

# Máquina 2 (destino): Receber e extrair
tar xzf skills.tar.gz -C ~/
```

---

## 🔐 Segurança

### Verificar Integridade

```bash
# Contar skills esperadas
ls ~/.claude/skills/ | wc -l
# Esperado: 27

# Verificar se não há arquivos estranhos
ls ~/.claude/skills/ | grep -v "^[a-z-]*$"
# Não deve mostrar nada (sem camelCase ou caracteres especiais)
```

### Proteger Contra Mudanças Acidentais

```bash
# Fazer diretório read-only (cuidado!)
chmod 555 ~/.claude/skills/

# Para editar, desfazer:
chmod 755 ~/.claude/skills/
```

---

## 📞 Suporte

**Problema persiste?**

1. Verifique: `ls ~/.claude/skills/copywriting-psychology/SKILL.md`
   - Deve existir e ter +3KB

2. Teste: `/skill copywriting-psychology` no Claude Code
   - Deve carregar sem erro

3. Reporte: Abra issue no GitHub com:
   - Output de `ls ~/.claude/skills/ | wc -l`
   - Output de `/skill copywriting-psychology` (resultado ou erro)
   - Sistema operacional e versão do Claude Code

---

## 📋 Checklist de Instalação

- [ ] Repositório clonado/baixado
- [ ] Pasta `skills/` copiada para `~/.claude/skills/`
- [ ] Validação: 27+ skills presentes
- [ ] Teste: `/skill copywriting-psychology` funciona
- [ ] Backup feito (opcional)
- [ ] Time notificado (se necessário)

---

**Status:** ✅ Pronto para produção  
**Última atualização:** 2026-09-18  
**Versão:** 1.0 (27 skills)

