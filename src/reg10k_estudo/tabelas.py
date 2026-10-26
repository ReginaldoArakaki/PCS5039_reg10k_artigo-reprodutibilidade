"""Geração de tabelas Markdown a partir dos JSONs processados."""
from __future__ import annotations


def tabela_evolucao(dados: dict) -> str:
    linhas = ["| Versão | Artefatos | LOC doc. | LOC código | LOC dados | LOC total | Cenários | Schemas | Testes |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for v in dados.values():
        linhas.append(f"| {v['versao']} | {v['artefatos']} | {v['loc_documentacao']} | {v['loc_codigo']} | "
                      f"{v['loc_dados_contratos']} | {v['loc_total']} | {v['cenarios']} | {v['schemas']} | {v['funcoes_teste']} |")
    return "\n".join(linhas) + "\n"
