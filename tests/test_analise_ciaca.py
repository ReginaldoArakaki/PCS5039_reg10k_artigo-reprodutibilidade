import csv
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
DATA = ROOT / "dados" / "evolucao" / "analise-ciaca"


def ler(nome):
    with (DATA / nome).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def test_manifesto_e_pareamento_completos():
    manifesto = json.loads((DATA / "manifesto-analise.json").read_text(encoding="utf-8"))
    assert manifesto["n_execucoes"] == 10500
    assert manifesto["n_pares"] == 5250
    assert manifesto["bootstrap"] == 5000
    assert manifesto["semente"] == 5039


def test_discordancias_de_requisitos_reproduzidas():
    rows = {r["versao"]: r for r in ler("discordancias-pareadas.csv")}
    assert int(rows["V0"]["somente_referencia_ok"]) == 0
    assert int(rows["V1"]["somente_referencia_ok"]) == 138
    assert int(rows["V2"]["somente_referencia_ok"]) == 368
    assert int(rows["V3"]["somente_referencia_ok"]) == 599
    assert all(int(r["somente_grupo_ok"]) == 0 for r in rows.values())


def test_intervalo_v3_documenta_compromisso():
    rows = ler("comparacao-pareada-controladores.csv")
    index = {(r["versao"], r["metrica"]): r for r in rows}
    desperdicio = index[("V3", "desperdicio_s")]
    escuro = index[("V3", "escuro_com_ocupante_s")]
    assert float(desperdicio["ic95_cluster_superior"]) < 0
    assert float(escuro["ic95_cluster_inferior"]) > 0
