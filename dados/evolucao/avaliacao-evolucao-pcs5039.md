# Evolução experimental da plataforma Reg10k — base PCS5039

**Gerado em:** 2026-10-29T19:40:34.093935+00:00  
**Escopo observado:** tags v0dtb, v1dtc e v2dta, todas sobre nucleo-v1.2.  
**Escopo planejado:** v1dt.1/nucleo-v1.3, ainda sem resultados empíricos.

## Síntese quantitativa

| Versão | Cômodos | Cenários | Execuções | LOC rastreadas | Eventos médios | Eventos/cômodo | Fidelidade média do espelho (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V0 | 1 | 38 | 2280 | 7955 | 1073.13 | 1073.13 | 59.94 |
| V1 | 2 | 26 | 1560 | 5743 | 1044.33 | 522.17 | 62.27 |
| V2 | 4 | 29 | 1740 | 6426 | 2021.11 | 505.28 | 55.92 |

## Leitura de engenharia

1. A progressão V0→V1→V2 aumenta a topologia de 1 para 2 e 4 cômodos, mas mantém núcleo, sementes e controladores; isso forma um quase-experimento de escalabilidade espacial.
2. Totais brutos crescem com a planta. As conclusões do artigo devem privilegiar medidas por cômodo, por minuto ocupado e comparações pareadas por cenário/semente.
3. As famílias F1–F7 cobrem uso normal, falsos negativos, falsos positivos, falhas, rede, comandos remotos e espelho. Resultados agregados sem estratificação podem ocultar o mecanismo responsável.
4. A v1dt.1 amplia o eixo comportamental com F8–F10. Ela deve entrar na base como marco planejado até existir CSV e manifesto reproduzíveis.
5. O Digital Twin deve ser avaliado por fidelidade e pela decomposição do erro: percepção local versus sincronização, além de atualidade, divergência e reconciliação.

## Regras de interpretação

- São resultados de simulação determinística, não medições de residências reais.
- Correlação não demonstra causalidade; famílias e parâmetros devem ser controlados.
- O número de moradores do CSV representa entidades simuladas atuais; a v1dt.1 muda essa população e exige nova rodada de 30 sementes.
- O SQLite preserva cada execução bruta em JSON e as sínteses em tabelas normalizadas, com hashes SHA-256 das fontes.

## Próxima rodada mínima

Implementar v1dt.1, congelar tag e commit do núcleo, executar os dois controladores nas mesmas 30 sementes, publicar CSV+manifesto e recalcular E01–E10. Para F10, acrescentar matriz de confusão e latências de suspeita, confirmação e conciliação.
