"""Constrói a base longitudinal Reg10k a partir dos repositórios publicados.

Saídas: SQLite normalizado, CSVs de síntese e relatório Markdown. O script não
altera os repositórios de origem e registra commits, tags e hashes das entradas.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
import statistics
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


VERSOES = {
    "V0": {"repo": "PCS5039_ambiente_reg10k_V0", "tag": "v0dtc", "dados": "experimentos-V0-20261029-v13", "estagio": "observado"},
    "V1": {"repo": "PCS5039_ambiente_reg10k_V1", "tag": "v1dt.1", "dados": "experimentos-V1-20261029-v1dt1", "estagio": "observado"},
    "V2": {"repo": "PCS5039_ambiente_reg10k_V2", "tag": "v2dtb", "dados": "experimentos-V2-20261029-v13", "estagio": "observado"},
    "V3": {"repo": "PCS5039_ambiente_reg10k_V3", "tag": "v3dt", "dados": "experimentos-V3-20261029", "estagio": "observado"},
}

METRICAS_DINAMICAS = [
    "n_eventos", "desperdicio_s", "escuro_com_ocupante_s",
    "apagamentos_indevidos", "acionamentos", "latencia_reacao_ms_p95",
    "latencia_reacao_ms_max", "atraso_percebido_ms_max",
    "desperdicio_por_saida_s_max", "ocupacao_desconhecida_s",
    "tempo_ocupada_s", "tempo_luz_acesa_s", "atualidade_gemeo_ms_p95",
    "gemeo_nao_atual_s", "comando_remoto_ms_p95", "comandos_remotos",
    "comandos_vencidos_executados", "efeitos_duplicados_remotos",
    "reconciliacao_ms_max", "divergencia_alem_prazo_s",
    "eventos_nao_entregues", "fila_max", "espelho_fiel_pct",
    "espelho_fiel_s", "erro_de_percepcao_s", "erro_de_sincronizacao_s",
    "espelho_nao_afirma_s",
    "luz_com_todos_dormindo_s", "suspeitas_abertas",
    "suspeitas_confirmadas", "suspeitas_conciliadas",
]

EXPERIMENTOS_PROPOSTOS = [
    ("E01", "Escalabilidade espacial", "V0→V1→V2→V3", "Normalizar eventos, desperdício e erro por cômodo e por minuto ocupado", "Mantém comparabilidade ao aumentar a planta", "alta"),
    ("E02", "Robustez por família", "F1–F10", "Taxas de requisitos/invariantes e distribuição das métricas por família", "Localiza em qual mecanismo surge a degradação", "alta"),
    ("E03", "Comparação pareada de controlador", "referência × grupo_exemplo", "Diferença por cenário e semente, com IC por bootstrap", "Reduz efeito da massa de teste desigual", "alta"),
    ("E04", "Ocupação múltipla", "v1dt.1 / F8", "FN de ocupação após saída parcial; desperdício por ocupante-minuto", "Testa 'um sai e outro fica'", "alta"),
    ("E05", "Sono versus permanência", "v1dt.1 / F9", "escuro acordado × luz com todos dormindo", "Expõe compromisso não observável pelo sensor", "alta"),
    ("E06", "Presença incompatível", "v1dt.1 / F10", "precisão, revocação, tempo de confirmação e conciliações", "Avalia inteligência no Hub sem rotular invasão", "alta"),
    ("E07", "Sensibilidade temporal", "timeouts e atrasos", "Curvas de resposta variando timeout PIR, atraso de SA e janela de reconciliação", "Mostra robustez das decisões de projeto", "média"),
    ("E08", "Resiliência de rede", "IDEAL/DEGRADADA/OFFLINE", "AUC de divergência, fila máxima, perda e tempo de reconciliação", "Evidencia valor do Digital Twin sob desconexão", "alta"),
    ("E09", "Fidelidade do gêmeo", "percepção/sincronização", "Decompor erro total em percepção e sincronização por família", "Separa limitação sensorial de conectividade", "alta"),
    ("E10", "Repetibilidade", "30 sementes", "CV, IC95 e estabilidade de ranking", "Demonstra suficiência ou necessidade de mais sementes", "alta"),
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def numero(valor):
    if valor in (None, ""):
        return None
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def bool_int(valor):
    return 1 if str(valor).lower() in {"true", "1", "sim"} else 0


def medir_estatica(repo: Path, ref: str) -> dict:
    arquivos = git(repo, "ls-tree", "-r", "--name-only", ref).splitlines()
    ext = Counter()
    loc = Counter()
    testes = 0
    for nome in arquivos:
        sufixo = Path(nome).suffix.lower() or "[sem_extensão]"
        ext[sufixo] += 1
        if sufixo not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".mmd"}:
            continue
        try:
            texto = git(repo, "show", f"{ref}:{nome}")
        except subprocess.CalledProcessError:
            continue
        loc[sufixo] += len(texto.splitlines())
        if nome.startswith("tests/") and sufixo == ".py":
            testes += len(re.findall(r"^def test_", texto, re.MULTILINE))
    roteiros = sum(1 for n in arquivos if n.startswith("cenarios/roteiros/") and n.endswith(".json"))
    gabaritos = sum(1 for n in arquivos if n.startswith("cenarios/esperado/") and n.endswith(".json"))
    return {
        "arquivos": len(arquivos), "arquivos_py": ext[".py"], "arquivos_json": ext[".json"],
        "arquivos_md": ext[".md"], "loc_total": sum(loc.values()), "loc_py": loc[".py"],
        "loc_json": loc[".json"], "loc_md": loc[".md"], "cenarios": roteiros,
        "gabaritos": gabaritos, "testes_declarados": testes,
    }


def criar_esquema(db: sqlite3.Connection):
    db.executescript("""
    PRAGMA foreign_keys=ON;
    CREATE TABLE fonte (id INTEGER PRIMARY KEY, tipo TEXT, caminho_ou_url TEXT, sha256 TEXT, coletado_em TEXT, observacao TEXT);
    CREATE TABLE versao (id TEXT PRIMARY KEY, titulo TEXT, descricao TEXT, estagio TEXT, repositorio TEXT, tag TEXT, commit_tag TEXT, commit_main TEXT, nucleo_tag TEXT, nucleo_commit TEXT, n_comodos INTEGER, n_moradores INTEGER, n_cenarios INTEGER, n_familias INTEGER, n_sementes INTEGER, n_controladores INTEGER, n_execucoes INTEGER);
    CREATE TABLE metrica_estatica (versao_id TEXT, metrica TEXT, valor REAL, unidade TEXT, metodo TEXT, PRIMARY KEY (versao_id, metrica), FOREIGN KEY (versao_id) REFERENCES versao(id));
    CREATE TABLE execucao (id INTEGER PRIMARY KEY, versao_id TEXT, familia TEXT, cenario TEXT, tipo TEXT, controlador TEXT, semente INTEGER, modo TEXT, modo_rede TEXT, requisitos_ok INTEGER, invariantes_ok INTEGER, n_comodos INTEGER, n_moradores INTEGER, metricas_json TEXT, UNIQUE (versao_id, familia, cenario, controlador, semente), FOREIGN KEY (versao_id) REFERENCES versao(id));
    CREATE TABLE metrica_dinamica_resumo (versao_id TEXT, controlador TEXT, familia TEXT, metrica TEXT, n INTEGER, media REAL, mediana REAL, desvio_padrao REAL, minimo REAL, maximo REAL, media_por_comodo REAL, PRIMARY KEY (versao_id, controlador, familia, metrica));
    CREATE TABLE experimento_proposto (id TEXT PRIMARY KEY, nome TEXT, escopo TEXT, metricas TEXT, finalidade TEXT, prioridade TEXT, estado TEXT);
    CREATE TABLE marco_planejado (id TEXT PRIMARY KEY, base TEXT, estado TEXT, objetivo TEXT, ocupantes TEXT, familias_novas TEXT, metricas_novas TEXT, fonte_id INTEGER, FOREIGN KEY (fonte_id) REFERENCES fonte(id));
    """)


def escrever_csv(path: Path, colunas, linhas):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(colunas)
        w.writerows(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", type=Path, required=True)
    ap.add_argument("--plano", type=Path, required=True)
    ap.add_argument("--sincronismo", type=Path, required=True)
    ap.add_argument("--saida", type=Path, required=True)
    args = ap.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    db_path = args.saida / "reg10k-evolucao.sqlite"
    if db_path.exists():
        db_path.unlink()
    db = sqlite3.connect(db_path)
    criar_esquema(db)
    agora = datetime.now(timezone.utc).isoformat()
    fontes = [
        ("especificacao", str(args.plano), sha256(args.plano), agora, "Plano v3dt.1; aprendizado do gêmeo tratado como marco planejado"),
        ("planilha", str(args.sincronismo), sha256(args.sincronismo), agora, "Sincronismo informado; commits reconferidos nos clones"),
    ]
    db.executemany("INSERT INTO fonte(tipo,caminho_ou_url,sha256,coletado_em,observacao) VALUES (?,?,?,?,?)", fontes)

    execucoes = []
    estaticas_csv = []
    versoes_csv = []
    for vid, cfg in VERSOES.items():
        repo = args.repos / cfg["repo"]
        manifesto_path = repo / "dados" / f"{cfg['dados']}.manifesto.json"
        csv_path = repo / "dados" / f"{cfg['dados']}.csv"
        manifesto = json.loads(manifesto_path.read_text(encoding="utf-8"))
        versao = json.loads((repo / "versao.json").read_text(encoding="utf-8"))
        commit_tag = git(repo, "rev-list", "-n", "1", cfg["tag"])
        commit_main = git(repo, "rev-parse", "main")
        estat = medir_estatica(repo, cfg["tag"])
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        n_comodos = max(int(r["n_comodos"]) for r in rows)
        n_moradores = max(int(r["n_moradores"]) for r in rows)
        db.execute("""INSERT INTO versao VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            vid, versao["titulo"], versao["descricao"], cfg["estagio"],
            f"https://github.com/ReginaldoArakaki/{cfg['repo']}", cfg["tag"], commit_tag,
            commit_main, versao["nucleo_tag"], manifesto["nucleo"]["commit"], n_comodos,
            n_moradores, len({r["cenario"] for r in rows}), len({r["familia"] for r in rows}),
            len(manifesto["sementes"]), len(manifesto["controladores"]), len(rows)))
        versoes_csv.append((vid, cfg["tag"], commit_tag, commit_main, versao["nucleo_tag"], n_comodos, n_moradores, len({r["cenario"] for r in rows}), len(rows), "observado"))
        for metrica, valor in estat.items():
            unidade = "linhas" if metrica.startswith("loc_") else "quantidade"
            db.execute("INSERT INTO metrica_estatica VALUES (?,?,?,?,?)", (vid, metrica, valor, unidade, f"git ls-tree/show na tag {cfg['tag']}"))
            estaticas_csv.append((vid, metrica, valor, unidade, cfg["tag"]))
        db.execute("INSERT INTO fonte(tipo,caminho_ou_url,sha256,coletado_em,observacao) VALUES (?,?,?,?,?)", ("dados_brutos", str(csv_path), sha256(csv_path), agora, f"{len(rows)} execuções; {cfg['tag']}"))
        for r in rows:
            metricas = {m: numero(r.get(m)) for m in METRICAS_DINAMICAS}
            cur = db.execute("""INSERT INTO execucao(versao_id,familia,cenario,tipo,controlador,semente,modo,modo_rede,requisitos_ok,invariantes_ok,n_comodos,n_moradores,metricas_json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                vid, r["familia"], r["cenario"], r["tipo"], r["controlador"], int(r["semente"]),
                r["modo"], r["modo_rede"], bool_int(r["requisitos_ok"]), bool_int(r["invariantes_ok"]),
                int(r["n_comodos"]), int(r["n_moradores"]), json.dumps(metricas, ensure_ascii=False)))
            execucoes.append((vid, r, metricas))

    grupos = defaultdict(list)
    for vid, r, metricas in execucoes:
        for familia in (r["familia"], "TODAS"):
            for metrica, valor in metricas.items():
                if valor is not None:
                    grupos[(vid, r["controlador"], familia, metrica)].append((valor, int(r["n_comodos"])))
    dinamicas_csv = []
    for (vid, ctrl, fam, met), vals in sorted(grupos.items()):
        xs = [v for v, _ in vals]
        norm = [v / c for v, c in vals if c]
        linha = (vid, ctrl, fam, met, len(xs), statistics.fmean(xs), statistics.median(xs), statistics.stdev(xs) if len(xs) > 1 else 0.0, min(xs), max(xs), statistics.fmean(norm))
        db.execute("INSERT INTO metrica_dinamica_resumo VALUES (?,?,?,?,?,?,?,?,?,?,?)", linha)
        dinamicas_csv.append(linha)

    db.executemany("INSERT INTO experimento_proposto VALUES (?,?,?,?,?,?,?)", [(*e, "proposto") for e in EXPERIMENTOS_PROPOSTOS])
    fonte_plano = db.execute("SELECT id FROM fonte WHERE tipo='especificacao'").fetchone()[0]
    db.execute("INSERT INTO marco_planejado VALUES (?,?,?,?,?,?,?,?)", (
        "v3dt.1", "nucleo-v1.4", "planejado", "Aprender perfis comportamentais e produzir sugestões explicáveis com aceite",
        "ocupantes e rotinas observados nas versões comportamentais", "aprendizado longitudinal e sugestões com aceite",
        "calibração; precisão/recall; ganho energético; conforto; aceite; deriva; reversões", fonte_plano))
    db.commit()

    escrever_csv(args.saida / "versoes.csv", ["versao","tag","commit_tag","commit_main","nucleo","comodos","moradores_modelados","cenarios","execucoes","estado"], versoes_csv)
    escrever_csv(args.saida / "metricas-estaticas.csv", ["versao","metrica","valor","unidade","tag"], estaticas_csv)
    escrever_csv(args.saida / "metricas-dinamicas-resumo.csv", ["versao","controlador","familia","metrica","n","media","mediana","desvio_padrao","minimo","maximo","media_por_comodo"], dinamicas_csv)
    escrever_csv(args.saida / "experimentos-propostos.csv", ["id","nome","escopo","metricas","finalidade","prioridade"], EXPERIMENTOS_PROPOSTOS)

    selecionadas = ("n_eventos", "desperdicio_s", "escuro_com_ocupante_s", "apagamentos_indevidos", "latencia_reacao_ms_p95", "atualidade_gemeo_ms_p95", "gemeo_nao_atual_s", "eventos_nao_entregues", "espelho_fiel_pct", "erro_de_percepcao_s", "erro_de_sincronizacao_s")
    workbook_data = {
        "versoes": [list(r) for r in versoes_csv],
        "estaticas": [list(r) for r in estaticas_csv],
        "dinamicas": [list(r) for r in dinamicas_csv if r[2] == "TODAS" and r[3] in selecionadas],
        "experimentos": [list(r) for r in EXPERIMENTOS_PROPOSTOS],
        "fontes": [["Plano v3dt.1", str(args.plano), sha256(args.plano), "marco planejado"], ["Sincronismo", str(args.sincronismo), sha256(args.sincronismo), "inventário inicial; reconferido via Git"]] + [[f"Dados {v}", str(args.repos / VERSOES[v]['repo'] / 'dados' / f"{VERSOES[v]['dados']}.csv"), sha256(args.repos / VERSOES[v]['repo'] / 'dados' / f"{VERSOES[v]['dados']}.csv"), VERSOES[v]["tag"]] for v in VERSOES],
    }
    (args.saida / "workbook-data.json").write_text(json.dumps(workbook_data, ensure_ascii=False, indent=2), encoding="utf-8")

    resumo = []
    for row in db.execute("""SELECT v.id,v.n_comodos,v.n_cenarios,v.n_execucoes,
        (SELECT valor FROM metrica_estatica e WHERE e.versao_id=v.id AND e.metrica='loc_total'),
        (SELECT media FROM metrica_dinamica_resumo d WHERE d.versao_id=v.id AND d.controlador='referencia' AND d.familia='TODAS' AND d.metrica='n_eventos'),
        (SELECT media_por_comodo FROM metrica_dinamica_resumo d WHERE d.versao_id=v.id AND d.controlador='referencia' AND d.familia='TODAS' AND d.metrica='n_eventos'),
        (SELECT media FROM metrica_dinamica_resumo d WHERE d.versao_id=v.id AND d.controlador='referencia' AND d.familia='TODAS' AND d.metrica='espelho_fiel_pct')
        FROM versao v ORDER BY v.id"""):
        resumo.append(row)
    rel = [
        "# Evolução experimental da plataforma Reg10k — base PCS5039", "",
        f"**Gerado em:** {agora}",
        "**Escopo observado:** tags v0dtc, v1dt.1, v2dtb e v3dt, todas sobre nucleo-v1.3.",
        "**Escopo planejado:** v3dt.1/nucleo-v1.4, com aprendizado comportamental ainda sem resultados empíricos.", "",
        "## Síntese quantitativa", "",
        "| Versão | Cômodos | Cenários | Execuções | LOC rastreadas | Eventos médios | Eventos/cômodo | Fidelidade média do espelho (%) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for v,c,s,e,l,ev,evc,fid in resumo:
        rel.append(f"| {v} | {c} | {s} | {e} | {int(l)} | {ev:.2f} | {evc:.2f} | {fid:.2f} |")
    rel += [
        "", "## Leitura de engenharia", "",
        "1. A progressão V0→V1→V2→V3 aumenta a topologia de 1 para 2, 4 e 7 cômodos, mantendo núcleo, sementes e controladores; isso forma um quase-experimento de escalabilidade espacial.",
        "2. Totais brutos crescem com a planta. As conclusões do artigo devem privilegiar medidas por cômodo, por minuto ocupado e comparações pareadas por cenário/semente.",
        "3. As famílias F1–F10 cobrem uso normal, falsos negativos, falsos positivos, falhas, rede, comandos remotos, espelho, ocupação múltipla, sono e presença incompatível. Resultados agregados sem estratificação podem ocultar o mecanismo responsável.",
        "4. A v1dt.1 e as versões sobre nucleo-v1.3 fornecem evidência observada do eixo comportamental; aprendizado do gêmeo permanece como marco planejado da v3dt.1.",
        "5. O Digital Twin deve ser avaliado por fidelidade e pela decomposição do erro: percepção local versus sincronização, além de atualidade, divergência e reconciliação.",
        "", "## Regras de interpretação", "",
        "- São resultados de simulação determinística, não medições de residências reais.",
        "- Correlação não demonstra causalidade; famílias e parâmetros devem ser controlados.",
        "- O número de moradores varia por cenário na V1; comparações comportamentais devem controlar essa população simulada.",
        "- O SQLite preserva cada execução bruta em JSON e as sínteses em tabelas normalizadas, com hashes SHA-256 das fontes.",
        "", "## Próxima rodada mínima", "",
        "Implementar v3dt.1 sobre nucleo-v1.4, congelar tags limpas, executar os dois controladores nas mesmas 30 sementes e avaliar previsão, sugestão, aceite, energia, conforto, calibração e deriva.",
    ]
    (args.saida / "avaliacao-evolucao-pcs5039.md").write_text("\n".join(rel) + "\n", encoding="utf-8")
    db.close()
    print(json.dumps({"sqlite": str(db_path), "execucoes": len(execucoes), "resumos_dinamicos": len(dinamicas_csv), "versoes": len(versoes_csv)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
