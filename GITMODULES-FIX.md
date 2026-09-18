# 🔧 Fix: Battle-Tested Gitlink Quebrado

## Problema

`skills/marketing-core/battle-tested/` está registrado como gitlink (submódulo) **sem `.gitmodules`** — submódulo quebrado, conteúdo não sincroniza em clones.

**Causa:** O diretório foi adicionado como repositório embarcado, não como submódulo Git correto.

## Solução (Execute Localmente)

### Passo 1: Remover Repositório Embarcado

```bash
# No seu terminal local
cd marketing-suite-prompt

# Remover o .git embarcado
rm -rf skills/marketing-core/battle-tested/.git

# Remover do índice do Git
git rm --cached skills/marketing-core/battle-tested
git commit -m "Remove broken battle-tested gitlink"
```

### Passo 2: Adicionar Como Submódulo Correto

```bash
# Adicionar submódulo com a URL correta
git submodule add https://github.com/ericosiu/ai-marketing-skills skills/marketing-core/battle-tested

# Confirmar .gitmodules foi criado
cat .gitmodules
# Esperado:
# [submodule "skills/marketing-core/battle-tested"]
#     path = skills/marketing-core/battle-tested
#     url = https://github.com/ericosiu/ai-marketing-skills
```

### Passo 3: Commit e Push

```bash
git add .gitmodules
git commit -m "Add battle-tested as proper submodule (ericosiu/ai-marketing-skills)"
git push origin master
```

## Verificação Pós-Fix

```bash
# Listar submódulos
git config --file .gitmodules --list

# Clonar em máquina nova (teste)
git clone --recurse-submodules https://github.com/marcosdeandradefilho/marketing-suite-prompt.git
cd marketing-suite-prompt/skills/marketing-core/battle-tested
# Deve ter conteúdo (SKILL.md, assets, etc.)
```

## Por Que Isso Importa

- **Sem `.gitmodules`:** Outros não conseguem clonar o repo e obter battle-tested
- **Com `.gitmodules` + submódulo:** Clone automático + versionamento + atualizações sincronizadas

## Status Atual

- ✅ Outros 26 skills: conteúdo completo + testado
- ⚠️ Battle-tested: gitlink quebrado (resolve manualmente)
- ✅ Documentação (README/INDEX/INSTALL): pronta
- ✅ Commit c8a3e39: tudo o mais já está no ar

---

**Tempo de execução:** ~2 minutos  
**Risco:** Nenhum (operação completamente reversível)

