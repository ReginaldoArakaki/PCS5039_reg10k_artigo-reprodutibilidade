from pathlib import Path


ROOT = Path(__file__).parents[1]
OUT = ROOT / "resultados" / "ciaca2027"


def test_figuras_publicadas_em_vetor_e_raster():
    for nome in ("figura-1-evolucao-capacidades", "figura-2-ciclo-experimental"):
        svg = OUT / "figuras" / f"{nome}.svg"
        png = OUT / "figuras" / f"{nome}.png"
        assert svg.stat().st_size > 10_000
        assert png.stat().st_size > 10_000
        assert "<svg" in svg.read_text(encoding="utf-8")[:1000]


def test_tabelas_conservam_resultados_auditados():
    md = (OUT / "tabelas-ciaca2027.md").read_text(encoding="utf-8")
    assert "10.500 execuções; 5.250 pares" in md
    assert "desperdício −7,98 s" in md
    assert "escuro +1,82 s" in md
    assert "| V3 | v3dt | 13b6200 | 7 | 60 | 3600 | 100.00 | 66.72 |" in md


def test_tabelas_latex_estao_prontas_para_booktabs():
    tex = (OUT / "tabelas-ciaca2027.tex").read_text(encoding="utf-8")
    assert tex.count("\\begin{table}") == 3
    assert tex.count("\\toprule") == 3
    assert tex.count("\\bottomrule") == 3
    assert "$-$7,98" in tex
