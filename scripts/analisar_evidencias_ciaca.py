"""Fecha as estatísticas usadas no artigo CIACA sobre a base longitudinal.

As comparações são pareadas por versão, cenário e semente. Intervalos de
confiança usam bootstrap de médias por cenário para evitar pseudorreplicação
das 30 sementes do mesmo roteiro.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path


METRICAS = {
    "n_eventos": "eventos",
    "desperdicio_s": "s",
    "escuro_com_ocupante_s": "s",
    "apagamentos_indevidos": "ocorrências",
    "latencia_reacao_ms_p95": "ms",
    "atualidade_gemeo_ms_p95": "ms",
    "gemeo_nao_atual_s": "s",
    "espelho_fiel_pct": "%",
    "erro_de_percepcao_s": "s",
    "erro_de_sincronizacao_s": "s",
    "eventos_nao_entregues": "eventos",
}


def quantil(xs: list[float], p: float) -> float:
    if not xs:
        return math.nan
    ys = sorted(xs)
    pos = (len(ys) - 1) * p
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return ys[lo]
    return ys[lo] * (hi - pos) + ys[hi] * (pos - lo)


def bootstrap_cenarios(valores: dict[str, list[float]], rng: random.Random, n_boot: int) -> tuple[float, float]:
    medias = {cenario: statistics.fmean(xs) for cenario, xs in valores.items() if xs}
    cenarios = sorted(medias)
    if not cenarios:
        return math.nan, math.nan
    if len(cenarios) == 1:
        v = medias[cenarios[0]]
        return v, v
    boots = []
    for _ in range(n_boot):
        amostra = [medias[rng.choice(cenarios)] for _ in cenarios]
        boots.append(statistics.fmean(amostra))
    return quantil(boots, 0.025), quantil(boots, 0.975)


def escrever_csv(path: Path, headers: list[str], rows: list[tuple]):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def fmt(v: float | None, casas: int = 2) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:.{casas}f}".replace(".", ",")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--saida", type=Path, required=True)
    ap.add_argument("--bootstrap", type=int, default=5000)
    ap.add_argument("--semente", type=int, default=5039)
    args = ap.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(args.base)
    db.row_factory = sqlite3.Row
    registros = []
    for r in db.execute("SELECT * FROM execucao ORDER BY versao_id,cenario,semente,controlador"):
        d = dict(r)
        d["metricas"] = json.loads(d.pop("metricas_json"))
        registros.append(d)

    # Taxas de atendimento e discordâncias pareadas.
    por_chave = defaultdict(dict)
    for r in registros:
        por_chave[(r["versao_id"], r["cenario"], r["semente"])][r["controlador"]] = r
    pass_rows = []
    for versao in sorted({r["versao_id"] for r in registros}):
        for ctrl in ("referencia", "grupo_exemplo"):
            xs = [r for r in registros if r["versao_id"] == versao and r["controlador"] == ctrl]
            pass_rows.append((versao, ctrl, len(xs), sum(r["requisitos_ok"] for r in xs), 100 * statistics.fmean(r["requisitos_ok"] for r in xs), sum(r["invariantes_ok"] for r in xs), 100 * statistics.fmean(r["invariantes_ok"] for r in xs)))
    discord_rows = []
    for versao in sorted({r["versao_id"] for r in registros}):
        pares = [v for (ve, _, _), v in por_chave.items() if ve == versao and {"referencia", "grupo_exemplo"} <= v.keys()]
        ambos = sum(p["referencia"]["requisitos_ok"] and p["grupo_exemplo"]["requisitos_ok"] for p in pares)
        so_ref = sum(p["referencia"]["requisitos_ok"] and not p["grupo_exemplo"]["requisitos_ok"] for p in pares)
        so_grp = sum(not p["referencia"]["requisitos_ok"] and p["grupo_exemplo"]["requisitos_ok"] for p in pares)
        nenhum = len(pares) - ambos - so_ref - so_grp
        discord_rows.append((versao, len(pares), ambos, so_ref, so_grp, nenhum, so_ref - so_grp))

    # Diferenças contínuas: grupo_exemplo - referência, IC por cenário.
    rng = random.Random(args.semente)
    paired_rows = []
    for versao in sorted({r["versao_id"] for r in registros}):
        pares = [(chave, v) for chave, v in por_chave.items() if chave[0] == versao and {"referencia", "grupo_exemplo"} <= v.keys()]
        for metrica, unidade in METRICAS.items():
            diffs, por_cenario = [], defaultdict(list)
            n_nulo = 0
            for (_, cenario, _), p in pares:
                a = p["referencia"]["metricas"].get(metrica)
                b = p["grupo_exemplo"]["metricas"].get(metrica)
                if a is None or b is None:
                    n_nulo += 1
                    continue
                dif = float(b) - float(a)
                diffs.append(dif)
                por_cenario[cenario].append(dif)
            lo, hi = bootstrap_cenarios(por_cenario, rng, args.bootstrap)
            paired_rows.append((versao, metrica, unidade, len(diffs), len(por_cenario), n_nulo, statistics.fmean(diffs) if diffs else None, statistics.median(diffs) if diffs else None, lo, hi))

    # Semântica observada: nulo, zero e positivo/negativo por versão e controlador.
    semantics_rows = []
    for versao in sorted({r["versao_id"] for r in registros}):
        for ctrl in ("referencia", "grupo_exemplo"):
            xs = [r for r in registros if r["versao_id"] == versao and r["controlador"] == ctrl]
            for metrica, unidade in METRICAS.items():
                vals = [r["metricas"].get(metrica) for r in xs]
                nulos = sum(v is None for v in vals)
                zeros = sum(v is not None and float(v) == 0 for v in vals)
                positivos = sum(v is not None and float(v) > 0 for v in vals)
                negativos = sum(v is not None and float(v) < 0 for v in vals)
                semantics_rows.append((versao, ctrl, metrica, unidade, len(vals), nulos, zeros, positivos, negativos, 100 * nulos / len(vals), 100 * zeros / len(vals)))

    # Resumo por família com métricas de leitura direta.
    family_rows = []
    for (versao, ctrl, familia), xs in sorted(defaultdict(list, {
        k: [r for r in registros if (r["versao_id"], r["controlador"], r["familia"]) == k]
        for k in {(r["versao_id"], r["controlador"], r["familia"]) for r in registros}
    }).items()):
        for metrica in ("desperdicio_s", "escuro_com_ocupante_s", "espelho_fiel_pct", "erro_de_percepcao_s", "gemeo_nao_atual_s"):
            vals = [float(r["metricas"][metrica]) for r in xs if r["metricas"].get(metrica) is not None]
            family_rows.append((versao, ctrl, familia, metrica, len(vals), len({r["cenario"] for r in xs}), statistics.fmean(vals) if vals else None, statistics.median(vals) if vals else None, statistics.stdev(vals) if len(vals) > 1 else 0.0, min(vals) if vals else None, max(vals) if vals else None))

    escrever_csv(args.saida / "taxas-atendimento.csv", ["versao","controlador","n","requisitos_ok","requisitos_pct","invariantes_ok","invariantes_pct"], pass_rows)
    escrever_csv(args.saida / "discordancias-pareadas.csv", ["versao","n_pares","ambos_ok","somente_referencia_ok","somente_grupo_ok","nenhum_ok","saldo_referencia"], discord_rows)
    escrever_csv(args.saida / "comparacao-pareada-controladores.csv", ["versao","metrica","unidade","n_pares_validos","n_cenarios","n_pares_nulos","diferenca_media_grupo_menos_referencia","diferenca_mediana","ic95_cluster_inferior","ic95_cluster_superior"], paired_rows)
    escrever_csv(args.saida / "semantica-nulos-zeros.csv", ["versao","controlador","metrica","unidade","n","nulos","zeros","positivos","negativos","nulos_pct","zeros_pct"], semantics_rows)
    escrever_csv(args.saida / "resumo-por-familia.csv", ["versao","controlador","familia","metrica","n","n_cenarios","media","mediana","desvio_padrao","minimo","maximo"], family_rows)

    # Texto pronto para auditoria e posterior síntese no artigo.
    lines = [
        "# Análise estatística para o artigo CIACA 2027", "",
        f"**Base:** `{args.base.name}`  ", f"**Bootstrap:** {args.bootstrap} reamostragens de cenários; semente {args.semente}.  ",
        "**Regra:** execuções são pareadas por versão, cenário e semente; o IC95 é calculado sobre médias por cenário.", "",
        "## Atendimento de requisitos e invariantes", "",
        "| Versão | Controlador | n | Requisitos (%) | Invariantes (%) |", "|---|---|---:|---:|---:|",
    ]
    for v, c, n, _, rp, _, ip in pass_rows:
        lines.append(f"| {v} | {c} | {n} | {fmt(rp)} | {fmt(ip)} |")
    lines += ["", "## Discordâncias pareadas de requisitos", "", "| Versão | Pares | Ambos OK | Só referência OK | Só grupo OK | Nenhum OK | Saldo referência |", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in discord_rows:
        lines.append("| " + " | ".join(map(str, r)) + " |")
    lines += [
        "", "O saldo não é um teste de superioridade geral: as versões possuem conjuntos de cenários diferentes. Ele localiza discordâncias dentro da mesma execução pareada.", "",
        "## Comparações pareadas selecionadas", "",
        "Diferença = grupo_exemplo − referência. Intervalos que atravessam zero não oferecem evidência direcional neste resumo exploratório.", "",
        "| Versão | Métrica | Pares | Cenários | Dif. média | IC95 por cenário |", "|---|---|---:|---:|---:|---:|",
    ]
    foco = {"desperdicio_s", "escuro_com_ocupante_s", "espelho_fiel_pct", "erro_de_percepcao_s", "gemeo_nao_atual_s"}
    for v, m, _, n, nc, _, media, _, lo, hi in paired_rows:
        if m in foco:
            lines.append(f"| {v} | {m} | {n} | {nc} | {fmt(media)} | [{fmt(lo)}; {fmt(hi)}] |")
    lines += [
        "", "## Nulos e zeros", "",
        "Um valor nulo significa que a métrica não se aplica ou não foi produzida. Zero é um valor registrado, mas sua interpretação depende do fenômeno: pode indicar ausência de ocorrência, não necessariamente desempenho perfeito. A tabela `semantica-nulos-zeros.csv` preserva essa distinção.", "",
        "## Regras para o manuscrito", "",
        "1. Reportar n de execuções e n de cenários.",
        "2. Usar IC por cenário para evitar pseudorreplicação das sementes.",
        "3. Não comparar versões por agregado bruto sem controlar a composição das famílias.",
        "4. Não interpretar latência zero como resposta instantânea sem verificar aplicabilidade.",
        "5. Tratar os resultados como evidência do simulador e do protocolo, não de residências reais ou aprendizagem causal.",
    ]
    (args.saida / "analise-estatistica-ciaca.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifesto = {
        "base": str(args.base), "bootstrap": args.bootstrap, "semente": args.semente,
        "n_execucoes": len(registros), "n_pares": len(por_chave),
        "arquivos": ["taxas-atendimento.csv", "discordancias-pareadas.csv", "comparacao-pareada-controladores.csv", "semantica-nulos-zeros.csv", "resumo-por-familia.csv", "analise-estatistica-ciaca.md"],
    }
    (args.saida / "manifesto-analise.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    db.close()
    print(json.dumps(manifesto, ensure_ascii=False))


if __name__ == "__main__":
    main()
