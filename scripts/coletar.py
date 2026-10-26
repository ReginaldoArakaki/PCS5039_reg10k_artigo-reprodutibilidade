from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from reg10k_estudo.coleta_git import coletar

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, default=Path(os.environ.get("REG10K_REPO", RAIZ.parent / "reg10k-v0dtb")))
p.add_argument("--config", type=Path, default=RAIZ / "configuracao/versoes.yaml")
args = p.parse_args()
dados = coletar(args.repo.resolve(), args.config)
destino = RAIZ / "dados/processados/metricas-evolucao.json"
destino.parent.mkdir(parents=True, exist_ok=True)
destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
print(destino)
