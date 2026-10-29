# Análise estatística para o artigo CIACA 2027

**Base:** `reg10k-evolucao.sqlite`  
**Bootstrap:** 5000 reamostragens de cenários; semente 5039.  
**Regra:** execuções são pareadas por versão, cenário e semente; o IC95 é calculado sobre médias por cenário.

## Atendimento de requisitos e invariantes

| Versão | Controlador | n | Requisitos (%) | Invariantes (%) |
|---|---|---:|---:|---:|
| V0 | referencia | 1140 | 100,00 | 100,00 |
| V0 | grupo_exemplo | 1140 | 100,00 | 100,00 |
| V1 | referencia | 780 | 99,87 | 100,00 |
| V1 | grupo_exemplo | 780 | 89,87 | 100,00 |
| V2 | referencia | 870 | 100,00 | 100,00 |
| V2 | grupo_exemplo | 870 | 68,05 | 100,00 |

## Discordâncias pareadas de requisitos

| Versão | Pares | Ambos OK | Só referência OK | Só grupo OK | Nenhum OK | Saldo referência |
|---|---:|---:|---:|---:|---:|---:|
| V0 | 1140 | 1140 | 0 | 0 | 0 | 0 |
| V1 | 780 | 701 | 78 | 0 | 1 | 78 |
| V2 | 870 | 592 | 278 | 0 | 0 | 278 |

O saldo não é um teste de superioridade geral: as versões possuem conjuntos de cenários diferentes. Ele localiza discordâncias dentro da mesma execução pareada.

## Comparações pareadas selecionadas

Diferença = grupo_exemplo − referência. Intervalos que atravessam zero não oferecem evidência direcional neste resumo exploratório.

| Versão | Métrica | Pares | Cenários | Dif. média | IC95 por cenário |
|---|---|---:|---:|---:|---:|
| V0 | desperdicio_s | 1140 | 38 | -3,16 | [-7,89; 0,00] |
| V0 | escuro_com_ocupante_s | 1140 | 38 | 0,47 | [0,28; 0,75] |
| V0 | gemeo_nao_atual_s | 1140 | 38 | 0,00 | [0,00; 0,00] |
| V0 | espelho_fiel_pct | 1140 | 38 | -0,09 | [-0,12; -0,06] |
| V0 | erro_de_percepcao_s | 1140 | 38 | -3,07 | [-7,91; 0,21] |
| V1 | desperdicio_s | 780 | 26 | -4,62 | [-11,54; 0,00] |
| V1 | escuro_com_ocupante_s | 780 | 26 | 1,30 | [0,95; 1,64] |
| V1 | gemeo_nao_atual_s | 780 | 26 | 0,00 | [0,00; 0,00] |
| V1 | espelho_fiel_pct | 780 | 26 | -0,21 | [-0,27; -0,15] |
| V1 | erro_de_percepcao_s | 780 | 26 | -4,47 | [-11,45; 0,23] |
| V2 | desperdicio_s | 870 | 29 | -12,37 | [-26,75; -2,07] |
| V2 | escuro_com_ocupante_s | 870 | 29 | 1,41 | [1,02; 1,85] |
| V2 | gemeo_nao_atual_s | 870 | 29 | 0,00 | [0,00; 0,00] |
| V2 | espelho_fiel_pct | 870 | 29 | -0,08 | [-0,11; -0,06] |
| V2 | erro_de_percepcao_s | 870 | 29 | -12,25 | [-28,59; -1,91] |

## Nulos e zeros

Um valor nulo significa que a métrica não se aplica ou não foi produzida. Zero é um valor registrado, mas sua interpretação depende do fenômeno: pode indicar ausência de ocorrência, não necessariamente desempenho perfeito. A tabela `semantica-nulos-zeros.csv` preserva essa distinção.

## Regras para o manuscrito

1. Reportar n de execuções e n de cenários.
2. Usar IC por cenário para evitar pseudorreplicação das sementes.
3. Não comparar versões por agregado bruto sem controlar a composição das famílias.
4. Não interpretar latência zero como resposta instantânea sem verificar aplicabilidade.
5. Tratar os resultados como evidência do simulador e do protocolo, não de residências reais ou aprendizagem causal.
