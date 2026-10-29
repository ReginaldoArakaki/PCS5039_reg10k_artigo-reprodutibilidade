# Dados

- `brutos/`: reservado a snapshots indispensáveis e legalmente redistribuíveis;
- `processados/`: JSONs reproduzíveis produzidos pelos coletores.
- `evolucao/`: SQLite canônico, CSVs de intercâmbio, relatório analítico e
  metadados usados para gerar a análise longitudinal V0–V3.
- `evolucao/analise-ciaca/`: taxas de atendimento, discordâncias pareadas,
  bootstrap por cenário, semântica de nulos/zeros e resultados por família
  usados no manuscrito CIACA 2027.

Os arquivos processados devem registrar commits e regras de normalização. O
código-fonte completo da plataforma não é duplicado neste repositório.

Na base de evolução, `execucao` preserva cada observação e suas métricas em
JSON; `metrica_dinamica_resumo` oferece estatística descritiva estratificada;
`metrica_estatica` registra contagens na árvore Git; `fonte` guarda hashes e
proveniência; `marco_planejado` mantém o aprendizado v3dt.1/nucleo-v1.4 fora
dos resultados observados. A base `reg10k-evolucao-v0-v2.sqlite` preserva a
fotografia anterior usada antes da incorporação das famílias comportamentais.
