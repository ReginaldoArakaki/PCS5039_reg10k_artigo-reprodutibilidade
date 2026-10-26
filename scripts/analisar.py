from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from reg10k_estudo.coleta_catalogo import analisar_catalogo

p = argparse.ArgumentParser()
p.add_argument("--catalogo", type=Path, default=Path(os.environ.get("REG10K_CATALOGO", RAIZ.parent / "reg10k-v0dtb/saida/catalogo.json")))
args = p.parse_args()
dados = analisar_catalogo(args.catalogo.resolve())
destino = RAIZ / "dados/processados/metricas-resultados.json"
destino.parent.mkdir(parents=True, exist_ok=True)
destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
print(destino)
