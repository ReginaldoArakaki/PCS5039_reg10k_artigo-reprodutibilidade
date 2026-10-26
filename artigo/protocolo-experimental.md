# Protocolo experimental

## Unidade experimental

Uma execução é identificada por versão, commit, cenário, controlador, semente e
configuração. A execução canônica usa semente 42. Cenários realistas são
complementados por distribuições de 30 sementes.

## Coleta

- métricas estáticas são extraídas de objetos Git, sem checkout destrutivo;
- artefatos derivados são excluídos de LOC para evitar dupla contagem;
- métricas dinâmicas são lidas do catálogo validado;
- no multiambiente, fidelidade usa cômodo-segundo;
- toda correlação deve informar tamanho amostral e regra de normalização.

## Critérios de aceitação

- hashes e commits resolvem no repositório indicado;
- schemas e resultados são válidos;
- conservação temporal do espelho é respeitada;
- percentuais permanecem entre 0 e 100;
- scripts e testes terminam sem erro.
