#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_pacote.py — Validador de integridade do pacote Oficina MAFI.

Verifica, sem dependências externas:
  1. Presença de todos os arquivos obrigatórios
  2. Frontmatter YAML válido em todo SKILL.md
  3. Campos `name` e `description` presentes e não vazios
  4. `name` restrito a [a-z0-9_-] (sem acentos, sem espaços, sem maiúsculas)
  5. Unicidade dos valores de `name`
  6. Todas as referências cruzadas a caminhos internos resolvem
  7. Marcadores de MEMORY.md intactos
  8. Ausência de arquivos órfãos (não referenciados pela orquestradora)

Uso:
    python3 scripts/validar_pacote.py [raiz_do_pacote]

Saída: relatório em texto; código 0 se tudo passar, 1 se houver erro.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
# captura caminhos internos citados em crases: `skills/xx/SKILL.md`
PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py))`")

OBRIGATORIOS = [
    "SKILL.md",
    "CLAUDE.md",
    "MEMORY.md",
    "README.md",
    "referencias/carrero-mapa-tecnico.md",
    "referencias/glossario-operacional.md",
    "referencias/checklist-nobel.md",
    "referencias/protocolo-antisimulacro.md",
    "templates/FICHA-OBRA.md",
    "templates/DOSSIE-PERSONAGEM.md",
    "templates/PLANTA-BAIXA.md",
    "templates/ENTRADA-MEMORY.md",
    "scripts/validar_pacote.py",
]

SKILLS_ESPERADAS = [
    "01-entrevista-autoral",
    "02-voz-narrativa",
    "03-foco-narrativo",
    "04-personagem",
    "05-cena-e-cenario",
    "06-dialogos-e-vozes",
    "07-elipse-e-bordado",
    "08-pulsacao-narrativa",
    "09-genero-tom-andamento",
    "10-arquitetura-da-narrativa",
    "11-rascunho",
    "12-burilamento",
    "13-lapidacao-nobel",
    "14-invencao-contemporanea",
    "15-memoria-e-coerencia",
]

MARCADORES_MEMORY = ["<!-- INICIO-FICHAS -->", "<!-- FIM-FICHAS -->"]

erros: list[str] = []
avisos: list[str] = []
ok: list[str] = []


def parse_frontmatter(texto: str) -> dict[str, str] | None:
    """Extrai o frontmatter YAML simples (chave: valor) de um SKILL.md."""
    if not texto.startswith("---"):
        return None
    fim = texto.find("\n---", 3)
    if fim == -1:
        return None
    bloco = texto[3:fim].strip("\n")
    dados: dict[str, str] = {}
    chave_atual = None
    for linha in bloco.split("\n"):
        if not linha.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", linha)
        if m:
            chave_atual = m.group(1)
            dados[chave_atual] = m.group(2).strip()
        elif chave_atual and (linha.startswith(" ") or linha.startswith("\t")):
            dados[chave_atual] += " " + linha.strip()
        else:
            return None  # linha inesperada: YAML não trivial
    return dados


def validar(raiz: Path) -> None:
    # 1. arquivos obrigatórios
    for rel in OBRIGATORIOS:
        if (raiz / rel).is_file():
            ok.append(f"existe: {rel}")
        else:
            erros.append(f"AUSENTE: {rel}")

    # 2. skills esperadas
    skill_files: list[Path] = [raiz / "SKILL.md"]
    for nome in SKILLS_ESPERADAS:
        p = raiz / "skills" / nome / "SKILL.md"
        if p.is_file():
            ok.append(f"existe: skills/{nome}/SKILL.md")
            skill_files.append(p)
        else:
            erros.append(f"AUSENTE: skills/{nome}/SKILL.md")

    # 3-5. frontmatter
    nomes_vistos: dict[str, str] = {}
    for p in skill_files:
        if not p.is_file():
            continue
        rel = p.relative_to(raiz).as_posix()
        texto = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(texto)
        if fm is None:
            erros.append(f"FRONTMATTER inválido ou ausente: {rel}")
            continue
        nome = fm.get("name", "")
        desc = fm.get("description", "")
        if not nome:
            erros.append(f"campo `name` ausente: {rel}")
        elif not NAME_RE.match(nome):
            erros.append(
                f"campo `name` inválido em {rel}: '{nome}' "
                "(use apenas [a-z0-9_-], sem acentos)"
            )
        elif nome in nomes_vistos:
            erros.append(
                f"campo `name` duplicado: '{nome}' em {rel} e {nomes_vistos[nome]}"
            )
        else:
            nomes_vistos[nome] = rel
            ok.append(f"name válido: {nome}")

        if not desc:
            erros.append(f"campo `description` ausente: {rel}")
        elif len(desc) < 80:
            avisos.append(
                f"description curta ({len(desc)} chars) em {rel} — "
                "descrições curtas reduzem a taxa de acionamento"
            )

    # 6. referências cruzadas
    todos_md = list(raiz.rglob("*.md"))
    referenciados: set[str] = set()
    for p in todos_md:
        rel = p.relative_to(raiz).as_posix()
        texto = p.read_text(encoding="utf-8")
        for alvo in PATH_RE.findall(texto):
            if alvo.startswith(("http", "www")):
                continue
            # ignora nomes soltos sem diretório que não são arquivos de raiz
            candidato = raiz / alvo
            if "/" not in alvo and not candidato.is_file():
                continue
            referenciados.add(alvo)
            if not candidato.exists():
                # tolera globs do tipo templates/*.md
                if "*" in alvo:
                    continue
                erros.append(f"REFERÊNCIA QUEBRADA em {rel}: `{alvo}`")

    if not any(e.startswith("REFERÊNCIA QUEBRADA") for e in erros):
        ok.append(f"referências cruzadas resolvem ({len(referenciados)} alvos)")

    # 7. marcadores do MEMORY.md
    mem = raiz / "MEMORY.md"
    if mem.is_file():
        t = mem.read_text(encoding="utf-8")
        for marc in MARCADORES_MEMORY:
            if marc in t:
                ok.append(f"marcador presente: {marc}")
            else:
                erros.append(f"MARCADOR AUSENTE em MEMORY.md: {marc}")

    # 8. órfãos
    orquestradora = (raiz / "SKILL.md")
    if orquestradora.is_file():
        texto_orq = orquestradora.read_text(encoding="utf-8")
        for p in todos_md:
            rel = p.relative_to(raiz).as_posix()
            if rel in ("SKILL.md", "README.md"):
                continue
            base = rel.split("/")[0]
            if rel in texto_orq or f"{base}/*" in texto_orq or base in texto_orq:
                continue
            avisos.append(f"órfão (não citado na orquestradora): {rel}")


def main() -> int:
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not raiz.is_dir():
        print(f"Diretório inexistente: {raiz}")
        return 1

    print(f"Validando pacote em: {raiz}\n")
    validar(raiz)

    print(f"[OK]     {len(ok)} verificações passaram")
    for a in avisos:
        print(f"[AVISO]  {a}")
    for e in erros:
        print(f"[ERRO]   {e}")

    print()
    if erros:
        print(f"FALHOU — {len(erros)} erro(s), {len(avisos)} aviso(s).")
        return 1
    print(f"PACOTE ÍNTEGRO — 0 erros, {len(avisos)} aviso(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
