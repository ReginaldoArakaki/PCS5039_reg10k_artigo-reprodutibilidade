"""Coleta métricas estáticas de marcos Git sem alterar o checkout analisado."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath

import yaml

DERIVADOS = {"site/index.html", "codigo-codex-v0dtb.md"}
EXTENSOES = {".md", ".mmd", ".py", ".html", ".json", ".yml", ".yaml"}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8")


def categoria(nome: str) -> str:
    ext = PurePosixPath(nome).suffix
    if ext in {".md", ".mmd"}:
        return "documentacao"
    if ext in {".py", ".html", ".yml", ".yaml"}:
        return "codigo"
    return "dados_contratos" if ext == ".json" else "outros"


def medir(repo: Path, nome_versao: str, ref: str) -> dict:
    arquivos = git(repo, "ls-tree", "-r", "--name-only", ref).splitlines()
    contagem, loc = Counter(), Counter()
    testes, invariantes, tipos = 0, set(), Counter()
    roteiros, gabaritos, schemas = 0, 0, 0
    for nome in arquivos:
        if nome in DERIVADOS or nome.startswith("saida/") or PurePosixPath(nome).suffix not in EXTENSOES:
            continue
        texto = git(repo, "show", f"{ref}:{nome}")
        cat = categoria(nome)
        contagem[cat] += 1
        loc[cat] += len(texto.splitlines())
        invariantes.update(re.findall(r"OR-(?:0[1-9]|1[0-9])", texto))
        if nome.startswith("tests/") and nome.endswith(".py"):
            testes += len(re.findall(r"^def test_", texto, re.MULTILINE))
        if nome.startswith("cenarios/roteiros/") and nome.endswith(".json"):
            roteiros += 1
            tipos[json.loads(texto).get("tipo", "SEM_TIPO")] += 1
        gabaritos += int(nome.startswith("cenarios/esperado/") and nome.endswith(".json"))
        schemas += int(nome.startswith("schemas/") and nome.endswith(".json"))
    return {
        "versao": nome_versao, "ref": ref, "commit": git(repo, "rev-parse", ref).strip(),
        "artefatos": sum(contagem.values()), "loc_total": sum(loc.values()),
        "loc_documentacao": loc["documentacao"], "loc_codigo": loc["codigo"],
        "loc_dados_contratos": loc["dados_contratos"], "cenarios": roteiros,
        "cenarios_por_tipo": dict(sorted(tipos.items())), "gabaritos": gabaritos,
        "schemas": schemas, "funcoes_teste": testes, "invariantes": sorted(invariantes),
    }


def coletar(repo: Path, configuracao: Path) -> dict:
    cfg = yaml.safe_load(configuracao.read_text(encoding="utf-8"))
    return {v["nome"]: medir(repo, v["nome"], v["ref"]) for v in cfg["versoes"]}
