from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from reg10k_estudo.tabelas import tabela_evolucao
from reg10k_estudo.graficos import gerar_evolucao

fonte = RAIZ / "dados/processados/metricas-evolucao.json"
if not fonte.exists():
    raise SystemExit("Execute scripts/coletar.py primeiro.")
dados = json.loads(fonte.read_text(encoding="utf-8"))
destino = RAIZ / "resultados/tabelas/evolucao.md"
destino.parent.mkdir(parents=True, exist_ok=True)
destino.write_text(tabela_evolucao(dados), encoding="utf-8")
print(destino)
for grafico in gerar_evolucao(dados, RAIZ / "resultados/graficos"):
    print(grafico)
