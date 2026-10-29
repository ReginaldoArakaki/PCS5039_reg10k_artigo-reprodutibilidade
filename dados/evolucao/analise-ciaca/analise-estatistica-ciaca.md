# Análise estatística para o artigo CIACA 2027

**Base:** `reg10k-evolucao.sqlite`  
**Bootstrap:** 5000 reamostragens de cenários; semente 5039.  
**Regra:** execuções são pareadas por versão, cenário e semente; o IC95 é calculado sobre médias por cenário.

## Atendimento de requisitos e invariantes

| Versão | Controlador | n | Requisitos (%) | Invariantes (%) |
|---|---|---:|---:|---:|
| V0 | referencia | 1200 | 100,00 | 100,00 |
| V0 | grupo_exemplo | 1200 | 100,00 | 100,00 |
| V1 | referencia | 1140 | 99,91 | 100,00 |
| V1 | grupo_exemplo | 1140 | 87,81 | 100,00 |
| V2 | referencia | 1110 | 100,00 | 100,00 |
| V2 | grupo_exemplo | 1110 | 66,85 | 100,00 |
| V3 | referencia | 1800 | 100,00 | 100,00 |
| V3 | grupo_exemplo | 1800 | 66,72 | 100,00 |

## Discordâncias pareadas de requisitos

| Versão | Pares | Ambos OK | Só referência OK | Só grupo OK | Nenhum OK | Saldo referência |
|---|---:|---:|---:|---:|---:|---:|
| V0 | 1200 | 1200 | 0 | 0 | 0 | 0 |
| V1 | 1140 | 1001 | 138 | 0 | 1 | 138 |
| V2 | 1110 | 742 | 368 | 0 | 0 | 368 |
| V3 | 1800 | 1201 | 599 | 0 | 0 | 599 |

O saldo não é um teste de superioridade geral: as versões possuem conjuntos de cenários diferentes. Ele localiza discordâncias dentro da mesma execução pareada.

## Comparações pareadas selecionadas

Diferença = grupo_exemplo − referência. Intervalos que atravessam zero não oferecem evidência direcional neste resumo exploratório.

| Versão | Métrica | Pares | Cenários | Dif. média | IC95 por cenário |
|---|---|---:|---:|---:|---:|
| V0 | desperdicio_s | 1200 | 40 | -3,00 | [-7,50; 0,00] |
| V0 | escuro_com_ocupante_s | 1200 | 40 | 0,46 | [0,29; 0,74] |
| V0 | gemeo_nao_atual_s | 1200 | 40 | 0,00 | [0,00; 0,00] |
| V0 | espelho_fiel_pct | 1200 | 40 | -0,09 | [-0,12; -0,06] |
| V0 | erro_de_percepcao_s | 1200 | 40 | -2,91 | [-7,51; 0,20] |
| V1 | desperdicio_s | 1140 | 38 | -3,16 | [-7,89; 0,00] |
| V1 | escuro_com_ocupante_s | 1140 | 38 | 1,22 | [0,95; 1,49] |
| V1 | gemeo_nao_atual_s | 1140 | 38 | 0,00 | [0,00; 0,00] |
| V1 | espelho_fiel_pct | 1140 | 38 | -0,18 | [-0,23; -0,13] |
| V1 | erro_de_percepcao_s | 1140 | 38 | -3,02 | [-7,80; 0,20] |
| V2 | desperdicio_s | 1110 | 37 | -9,69 | [-21,01; -1,62] |
| V2 | escuro_com_ocupante_s | 1110 | 37 | 1,50 | [1,14; 1,88] |
| V2 | gemeo_nao_atual_s | 1110 | 37 | 0,00 | [0,00; 0,00] |
| V2 | espelho_fiel_pct | 1110 | 37 | -0,09 | [-0,11; -0,06] |
| V2 | erro_de_percepcao_s | 1110 | 37 | -9,52 | [-20,88; -1,39] |
| V3 | desperdicio_s | 1800 | 60 | -7,98 | [-15,93; -2,00] |
| V3 | escuro_com_ocupante_s | 1800 | 60 | 1,82 | [1,47; 2,16] |
| V3 | gemeo_nao_atual_s | 1800 | 60 | 0,00 | [0,00; 0,00] |
| V3 | espelho_fiel_pct | 1800 | 60 | -0,06 | [-0,07; -0,04] |
| V3 | erro_de_percepcao_s | 1800 | 60 | -7,68 | [-15,61; -1,74] |

## Nulos e zeros

Um valor nulo significa que a métrica não se aplica ou não foi produzida. Zero é um valor registrado, mas sua interpretação depende do fenômeno: pode indicar ausência de ocorrência, não necessariamente desempenho perfeito. A tabela `semantica-nulos-zeros.csv` preserva essa distinção.

## Regras para o manuscrito

1. Reportar n de execuções e n de cenários.
2. Usar IC por cenário para evitar pseudorreplicação das sementes.
3. Não comparar versões por agregado bruto sem controlar a composição das famílias.
4. Não interpretar latência zero como resposta instantânea sem verificar aplicabilidade.
5. Tratar os resultados como evidência do simulador e do protocolo, não de residências reais ou aprendizagem causal.
