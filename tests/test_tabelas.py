from reg10k_estudo.tabelas import tabela_evolucao


def test_tabela_mantem_identidade_do_commit_logico():
    dados = {"v0": {"versao": "v0", "artefatos": 1, "loc_documentacao": 2,
             "loc_codigo": 3, "loc_dados_contratos": 4, "loc_total": 9,
             "cenarios": 20, "schemas": 6, "funcoes_teste": 14}}
    tabela = tabela_evolucao(dados)
    assert "| v0 | 1 | 2 | 3 | 4 | 9 | 20 | 6 | 14 |" in tabela
