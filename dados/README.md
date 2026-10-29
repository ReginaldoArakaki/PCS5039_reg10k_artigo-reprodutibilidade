# Dados

- `brutos/`: reservado a snapshots indispensáveis e legalmente redistribuíveis;
- `processados/`: JSONs reproduzíveis produzidos pelos coletores.
- `evolucao/`: SQLite canônico, CSVs de intercâmbio, relatório analítico e
  metadados usados para gerar a planilha longitudinal V0–V2.

Os arquivos processados devem registrar commits e regras de normalização. O
código-fonte completo da plataforma não é duplicado neste repositório.

Na base de evolução, `execucao` preserva cada observação e suas métricas em
JSON; `metrica_dinamica_resumo` oferece estatística descritiva estratificada;
`metrica_estatica` registra contagens na árvore Git; `fonte` guarda hashes e
proveniência; `marco_planejado` mantém v1dt.1 fora dos resultados observados.
