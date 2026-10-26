"""Figuras vetoriais e PNG para o artigo."""
from __future__ import annotations

from pathlib import Path


def gerar_evolucao(dados: dict, destino: Path) -> list[Path]:
    import matplotlib.pyplot as plt

    destino.mkdir(parents=True, exist_ok=True)
    nomes = list(dados)
    cenarios = [dados[n]["cenarios"] for n in nomes]
    testes = [dados[n]["funcoes_teste"] for n in nomes]
    invariantes = [len(dados[n]["invariantes"]) for n in nomes]
    locs = {
        "Documentação": [dados[n]["loc_documentacao"] for n in nomes],
        "Código": [dados[n]["loc_codigo"] for n in nomes],
        "Dados/contratos": [dados[n]["loc_dados_contratos"] for n in nomes],
    }
    saidas = []
    fig, ax = plt.subplots(figsize=(10, 5))
    base = [0] * len(nomes)
    for rotulo, valores in locs.items():
        ax.bar(nomes, valores, bottom=base, label=rotulo)
        base = [a + b for a, b in zip(base, valores)]
    ax.set_ylabel("Linhas mantidas")
    ax.set_title("Evolução dos artefatos Reg10k")
    ax.tick_params(axis="x", rotation=35)
    ax.legend()
    fig.tight_layout()
    for ext in ("svg", "png"):
        p = destino / f"evolucao-loc.{ext}"; fig.savefig(p, dpi=180); saidas.append(p)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(nomes, cenarios, "o-", label="Cenários")
    ax.plot(nomes, testes, "s-", label="Funções de teste")
    ax.plot(nomes, invariantes, "^-", label="Invariantes")
    ax.set_title("Crescimento da massa de verificação")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(); fig.tight_layout()
    for ext in ("svg", "png"):
        p = destino / f"evolucao-verificacao.{ext}"; fig.savefig(p, dpi=180); saidas.append(p)
    plt.close(fig)
    return saidas
