from reg10k_estudo.estatistica import media, pearson


def test_media_ignora_nulos():
    assert media([1, None, 3]) == 2.0


def test_pearson_identifica_relacoes_perfeitas():
    assert pearson([1, 2, 3], [2, 4, 6]) == 1.0
    assert pearson([1, 2, 3], [6, 4, 2]) == -1.0


def test_pearson_abstem_com_amostra_insuficiente():
    assert pearson([1, 2], [1, 2]) is None
