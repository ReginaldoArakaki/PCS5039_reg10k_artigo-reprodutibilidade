"""Gera as figuras vetoriais e tabelas finais do artigo CIACA 2027."""
from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


AZUL = "#17365D"
AZUL2 = "#2F75B5"
LARANJA = "#C55A11"
CINZA = "#D9E2F3"
FUNDO = "#F7F9FC"
TEXTO = "#1F1F1F"


def caixa(ax, xy, wh, titulo, corpo, face, hatch=None, fontsize=8.6):
    x, y = xy
    w, h = wh
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.018,rounding_size=0.015",
                       linewidth=1.1, edgecolor=AZUL, facecolor=face, hatch=hatch)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h * 0.70, titulo, ha="center", va="center",
            fontsize=fontsize + 0.4, fontweight="bold", color=AZUL)
    ax.text(x + w / 2, y + h * 0.35, corpo, ha="center", va="center",
            fontsize=fontsize, color=TEXTO, linespacing=1.2)
    return p


def seta(ax, origem, destino, texto=None, curva=0):
    a = FancyArrowPatch(origem, destino, arrowstyle="-|>", mutation_scale=12,
                        linewidth=1.15, color="#555555",
                        connectionstyle=f"arc3,rad={curva}")
    ax.add_patch(a)
    if texto:
        ax.text((origem[0] + destino[0]) / 2, (origem[1] + destino[1]) / 2 + 0.035,
                texto, ha="center", va="bottom", fontsize=7.6, color="#444444")


def salvar(fig, base: Path):
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight", metadata={"Creator": "Reg10k reproducibility package"})
    fig.savefig(base.with_suffix(".png"), dpi=240, bbox_inches="tight")
    plt.close(fig)


def figura_evolucao(destino: Path):
    fig, ax = plt.subplots(figsize=(11.4, 4.3))
    fig.patch.set_facecolor("white")
    ax.set_facecolor(FUNDO)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 0.94, "Evolução de capacidades do laboratório Reg10k", ha="center", va="center",
            fontsize=14, fontweight="bold", color=AZUL)
    estagios = [
        ("Kit isolado", "controle local\ne log", "uma sala"),
        ("V0", "Digital Twin\ne espelho", "estado"),
        ("V1", "dois cômodos\ne passagem", "correlação"),
        ("V2", "quatro cômodos\ne geração", "escala"),
        ("V3", "sete cômodos,\nsono e família", "comportamento"),
        ("v3dt.1", "perfil, predição\ne aceite", "aprendizado"),
    ]
    xs = [0.025, 0.19, 0.355, 0.52, 0.685, 0.85]
    faces = ["#F2F2F2", "#EAF2F8", "#DCE6F1", "#D9EAD3", "#FCE4D6", "#FFF2CC"]
    hatches = ["..", None, "//", "\\", "xx", "--"]
    for i, ((tit, corpo, desafio), x) in enumerate(zip(estagios, xs)):
        caixa(ax, (x, 0.46), (0.125, 0.30), tit, corpo, faces[i], hatches[i])
        ax.text(x + 0.0625, 0.37, desafio.upper(), ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=LARANJA)
        if i < len(xs) - 1:
            seta(ax, (x + 0.127, 0.61), (xs[i + 1] - 0.006, 0.61))
    ax.text(0.5, 0.18,
            "Cada incremento preserva o núcleo anterior e introduz nova capacidade, nova falha observável e nova métrica.",
            ha="center", va="center", fontsize=9.4, color=TEXTO)
    ax.plot([0.04, 0.96], [0.10, 0.10], color="#888888", lw=0.8)
    ax.text(0.04, 0.055, "Evidência observada: V0–V3 e comportamento", ha="left", fontsize=8.2, color=AZUL)
    ax.text(0.96, 0.055, "Planejamento: v3dt.1 e aprendizado", ha="right", fontsize=8.2, color=LARANJA)
    salvar(fig, destino / "figura-1-evolucao-capacidades")


def figura_ciclo(destino: Path):
    fig, ax = plt.subplots(figsize=(11.4, 5.2))
    fig.patch.set_facecolor("white"); ax.set_facecolor(FUNDO)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 0.95, "Ciclo experimental e rastreabilidade das evidências", ha="center",
            fontsize=14, fontweight="bold", color=AZUL)
    caixa(ax, (0.04, 0.58), (0.15, 0.23), "Entradas", "planta, cenário,\nsemente e controlador", "#F2F2F2", "..")
    caixa(ax, (0.235, 0.58), (0.15, 0.23), "Simulador", "mundo, sensores,\natuadores e falhas", "#EAF2F8")
    caixa(ax, (0.43, 0.58), (0.15, 0.23), "Hub / CEP", "correlação, estado\ne decisão local", "#DCE6F1", "//")
    caixa(ax, (0.625, 0.58), (0.15, 0.23), "Digital Twin", "percepção,\nsincronização e ação", "#D9EAD3", "\\")
    caixa(ax, (0.82, 0.58), (0.14, 0.23), "Avaliação", "oráculo, requisitos,\ninvariantes e métricas", "#FCE4D6", "xx")
    for x1, x2 in [(0.19, 0.235), (0.385, 0.43), (0.58, 0.625), (0.775, 0.82)]:
        seta(ax, (x1, 0.695), (x2 - 0.006, 0.695))
    caixa(ax, (0.19, 0.19), (0.20, 0.20), "Execuções", "versão × cenário ×\ncontrolador × semente", "#FFF2CC", "--")
    caixa(ax, (0.44, 0.19), (0.20, 0.20), "Base longitudinal", "SQLite, CSV, hashes,\ntags e commits", "#E2F0D9", "//")
    caixa(ax, (0.69, 0.19), (0.20, 0.20), "Artigo reproduzível", "estatística, tabelas,\nfiguras e limites", "#E4DFEC", "xx")
    seta(ax, (0.89, 0.575), (0.79, 0.395), "registros")
    seta(ax, (0.39, 0.29), (0.435, 0.29))
    seta(ax, (0.64, 0.29), (0.685, 0.29))
    ax.plot([0.89, 0.89, 0.115], [0.815, 0.865, 0.865], color="#555555", lw=1.15)
    seta(ax, (0.115, 0.865), (0.115, 0.815))
    ax.text(0.50, 0.882, "novos cenários e versões", ha="center", va="bottom", fontsize=7.8, color="#444444")
    ax.text(0.5, 0.07, "Proveniência: repositório + tag + commit + manifesto + hash das entradas",
            ha="center", fontsize=9.2, color=AZUL, fontweight="bold")
    salvar(fig, destino / "figura-2-ciclo-experimental")


def ler_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def gerar_tabelas(base: Path, destino: Path):
    destino.mkdir(parents=True, exist_ok=True)
    taxas = {(r["versao"], r["controlador"]): r for r in ler_csv(base / "taxas-atendimento.csv")}
    tabela1 = [
        ("Pontes", "estrutura", "vibração + deformação crescente", "horas/dias", "inspeção ou restrição"),
        ("Apoio a idosos", "pessoa e rotina", "ausência de movimento/resposta", "segundos/minutos", "verificação e alerta graduado"),
        ("CI/CD", "pipeline e arquitetura", "falha recorrente após alteração", "minutos/horas", "bloqueio ou rollback"),
        ("Veículo autônomo", "veículo e entorno", "obstáculo dentro da distância de frenagem", "milissegundos", "frenagem ou evasão"),
    ]
    versoes = [
        ("V0", "v0dtc", "76a711e", 1, 40, 2400),
        ("V1", "v1dt.1", "9e0f8a8", 2, 38, 2280),
        ("V2", "v2dtb", "75225e9", 4, 37, 2220),
        ("V3", "v3dt", "13b6200", 7, 60, 3600),
    ]
    tabela2 = [(v, tag, commit, com, cen, exe,
                f"{float(taxas[(v, 'referencia')]['requisitos_pct']):.2f}",
                f"{float(taxas[(v, 'grupo_exemplo')]['requisitos_pct']):.2f}")
               for v, tag, commit, com, cen, exe in versoes]
    tabela3 = [
        ("10.500 execuções; 5.250 pares", "protocolo executável e pareado", "simulação, não campo"),
        ("100% de invariantes", "integridade estrutural preservada", "invariantes disponíveis"),
        ("V3: desperdício −7,98 s; IC95 [−15,93; −2,00]", "grupo usa menos luz", "condicional aos cenários"),
        ("V3: escuro +1,82 s; IC95 [1,47; 2,16]", "troca energia por conforto", "não é superioridade geral"),
        ("Erro de percepção >> sincronização", "limite sensorial domina no modelo", "rede simulada"),
        ("4 domínios de projetos", "transferência estrutural do padrão", "sem efeito pedagógico causal"),
    ]

    md = ["# Tabelas compactas — CIACA 2027", "", "## Tabela 1 — Transferência do padrão CEP–Digital Twin", "",
          "| Domínio | Entidade do gêmeo | Evento complexo | Janela | Ação |", "|---|---|---|---|---|"]
    md += ["| " + " | ".join(map(str, r)) + " |" for r in tabela1]
    md += ["", "## Tabela 2 — Versões e massa experimental", "",
           "| Versão | Tag | Commit | Cômodos | Cenários | Execuções | Req. ref. (%) | Req. grupo (%) |",
           "|---|---|---|---:|---:|---:|---:|---:|"]
    md += ["| " + " | ".join(map(str, r)) + " |" for r in tabela2]
    md += ["", "## Tabela 3 — Evidência, interpretação e limite", "",
           "| Evidência | Interpretação permitida | Limite |", "|---|---|---|"]
    md += ["| " + " | ".join(map(str, r)) + " |" for r in tabela3]
    (destino / "tabelas-ciaca2027.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    def esc(s):
        return str(s).replace("%", r"\%").replace("_", r"\_").replace("−", r"$-$")
    tex = [
        r"% Tabelas compactas para inclusão no manuscrito CIACA 2027",
        r"\begin{table}[ht]", r"\centering", r"\caption{Transferência do padrão CEP--Digital Twin.}",
        r"\small\begin{tabular}{p{1.8cm}p{2.2cm}p{4.0cm}p{1.8cm}p{3.0cm}}", r"\toprule",
        r"Domínio & Entidade & Evento complexo & Janela & Ação \\ \midrule",
    ]
    tex += [" & ".join(map(esc, r)) + r" \\" for r in tabela1]
    tex += [r"\bottomrule\end{tabular}", r"\end{table}", "", r"\begin{table}[ht]", r"\centering",
            r"\caption{Versões e massa experimental.}", r"\small\begin{tabular}{lllrrrrr}", r"\toprule",
            r"Versão & Tag & Commit & Côm. & Cen. & Exec. & Req. ref./grupo (\%) \\ \midrule"]
    tex += [f"{esc(r[0])} & {esc(r[1])} & {esc(r[2])} & {r[3]} & {r[4]} & {r[5]} & {r[6]}/{r[7]} \\\\" for r in tabela2]
    tex += [r"\bottomrule\end{tabular}", r"\end{table}", "", r"\begin{table}[ht]", r"\centering",
            r"\caption{Evidências, interpretações e limites.}", r"\small\begin{tabular}{p{4.1cm}p{4.2cm}p{4.0cm}}", r"\toprule",
            r"Evidência & Interpretação permitida & Limite \\ \midrule"]
    tex += [" & ".join(map(esc, r)) + r" \\" for r in tabela3]
    tex += [r"\bottomrule\end{tabular}", r"\end{table}"]
    (destino / "tabelas-ciaca2027.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analise", type=Path, required=True)
    ap.add_argument("--saida", type=Path, required=True)
    args = ap.parse_args()
    figura_evolucao(args.saida / "figuras")
    figura_ciclo(args.saida / "figuras")
    gerar_tabelas(args.analise, args.saida)
    print(args.saida)


if __name__ == "__main__":
    main()
