import sqlite3
from pathlib import Path


BASE = Path(__file__).parents[1] / "dados" / "evolucao" / "reg10k-evolucao.sqlite"


def test_base_integra_evidencias_sem_misturar_plano():
    db = sqlite3.connect(BASE)
    assert db.execute("SELECT COUNT(*) FROM execucao").fetchone()[0] == 10500
    assert db.execute("SELECT GROUP_CONCAT(id, ',') FROM versao ORDER BY id").fetchone()[0] == "V0,V1,V2,V3"
    assert db.execute("SELECT estado FROM marco_planejado WHERE id='v3dt.1'").fetchone()[0] == "planejado"
    assert db.execute("SELECT COUNT(*) FROM execucao WHERE familia IN ('F8','F9','F10')").fetchone()[0] == 2040
    assert db.execute("SELECT COUNT(*) FROM (SELECT versao_id,familia,cenario,controlador,semente,COUNT(*) n FROM execucao GROUP BY 1,2,3,4,5 HAVING n>1)").fetchone()[0] == 0
    assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    db.close()


def test_todas_as_execucoes_tem_proveniencia_de_versao():
    db = sqlite3.connect(BASE)
    orfas = db.execute("SELECT COUNT(*) FROM execucao e LEFT JOIN versao v ON v.id=e.versao_id WHERE v.id IS NULL").fetchone()[0]
    assert orfas == 0
    db.close()
