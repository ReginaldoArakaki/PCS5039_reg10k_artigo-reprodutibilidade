"""Extrai resultados comparáveis do catálogo Reg10k."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from .estatistica import media, pearson


def analisar_catalogo(caminho: Path) -> dict:
    cat = json.loads(caminho.read_text(encoding="utf-8"))
    cenarios = {c["id"]: c for c in cat["cenarios"]}
    execucoes = [e for e in cat["execucoes"] if e["controlador"] == "referencia"]
    grupos = defaultdict(list)
    for e in execucoes:
        grupos[(e["versao_cenario"], cenarios[e["cenario"]]["tipo"])].append(e)
    resumo = {}
    for chave, itens in sorted(grupos.items()):
        resumo["/".join(chave)] = {
            "n": len(itens),
            "desperdicio_s_media": media(e["metricas"].get("desperdicio_s") for e in itens),
            "escuro_s_media": media(e["metricas"].get("escuro_com_ocupante_s") for e in itens),
            "fidelidade_pct_media": media(e["metricas"].get("espelho_fiel_pct") for e in itens),
        }
    capacidades = [cenarios[e["cenario"]]["duracao_ms"] / 1000 * max(1, len(e.get("comodos") or {}))
                   for e in execucoes]
    percepcao = [100 * e["metricas"].get("erro_de_percepcao_s", 0) / cap
                 for e, cap in zip(execucoes, capacidades)]
    escuro = [100 * e["metricas"].get("escuro_com_ocupante_s", 0) / cap
              for e, cap in zip(execucoes, capacidades)]
    fidelidade = [e["metricas"].get("espelho_fiel_pct") for e in execucoes]
    return {
        "execucoes_total": len(cat["execucoes"]), "execucoes_referencia": len(execucoes),
        "problemas": cat.get("problemas", []), "grupos": resumo,
        "correlacoes_pearson": {
            "taxa_percepcao_x_taxa_escuro": pearson(percepcao, escuro),
            "taxa_percepcao_x_fidelidade_pct": pearson(percepcao, fidelidade),
        },
    }
