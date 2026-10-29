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
    assert "5.580 execuções; 2.790 pares" in md
    assert "desperdício −12,37 s" in md
    assert "escuro +1,41 s" in md
    assert "| V2 | v2dta | 17578dd | 4 | 29 | 1740 | 100.00 | 68.05 |" in md


def test_tabelas_latex_estao_prontas_para_booktabs():
    tex = (OUT / "tabelas-ciaca2027.tex").read_text(encoding="utf-8")
    assert tex.count("\\begin{table}") == 3
    assert tex.count("\\toprule") == 3
    assert tex.count("\\bottomrule") == 3
    assert "$-$12,37" in tex
