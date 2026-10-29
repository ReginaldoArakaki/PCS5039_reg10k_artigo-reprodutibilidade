# Reg10k — pacote de reprodutibilidade do artigo

Repositório-companheiro do estudo sobre a evolução arquitetural da plataforma
Reg10k: automação local, conectividade, Digital Twin, fidelidade causal,
residência multiambiente e inteligência comportamental no Hub.

## Resultado reproduzido

- 8 marcos Git analisados;
- evolução de 20 para 46 cenários e de 6 para 14 invariantes;
- 92 execuções no catálogo atual;
- 210 testes aprovados na v1dtb Codex;
- correlação exploratória entre taxa de erro de percepção e tempo no escuro;
- tabelas derivadas de dados e commits identificáveis.

## Base longitudinal PCS5039

A base `dados/evolucao/reg10k-evolucao.sqlite` consolida as versões publicadas
V0/v0dtb, V1/v1dtc e V2/v2dta: 5.580 execuções, métricas estáticas por tag,
sínteses dinâmicas por versão/controlador/família e proveniência com SHA-256.
A especificação v1dt.1 aparece separadamente como marco planejado, sem ser
confundida com evidência observada. A planilha em `outputs/evolucao-reg10k-20261029/`
é a visão de leitura da mesma base.

## Reprodução rápida

```powershell
python -m pip install -r requirements.txt
python scripts/coletar.py --repo ..\reg10k-v0dtb
python scripts/analisar.py --catalogo ..\reg10k-v0dtb\saida\catalogo.json
python scripts/gerar_resultados.py
python scripts/construir_base_evolucao.py --repos <diretorio-dos-clones> --plano <ambiente-simulacao-v1dt.1.md> --sincronismo <sincronismo.xlsx> --saida dados/evolucao
python scripts/analisar_evidencias_ciaca.py --base dados/evolucao/reg10k-evolucao.sqlite --saida dados/evolucao/analise-ciaca --bootstrap 5000 --semente 5039
python -m pytest -q
```

Os comandos geram arquivos auditáveis em `dados/processados/` e artefatos de
publicação em `resultados/`. O diretório da implementação também pode ser
informado pela variável `REG10K_REPO`.

## Escopo e limites

Este é um experimento didático determinístico, não uma medição de dez mil
residências reais. Correlações entre cenários ajudam a localizar mecanismos,
mas não constituem causalidade ou inferência populacional. Consulte
`artigo/ameacas-validade.md`.

## Citação

Use os metadados de `CITATION.cff`. Para uma publicação, cite também a release
imutável deste pacote e os commits da implementação listados em
`configuracao/versoes.yaml`.

## Idiomas

- documentação científica principal: português;
- resumo internacional: [`README.en.md`](README.en.md).

## Licença

Código sob licença MIT. Textos, tabelas e dados derivados sob CC BY 4.0, salvo
indicação diferente nos arquivos de origem.
