# Evolução experimental da plataforma Reg10k — base PCS5039

**Gerado em:** 2026-10-29T23:16:59.599605+00:00
**Escopo observado:** tags v0dtc, v1dt.1, v2dtb e v3dt, todas sobre nucleo-v1.3.
**Escopo planejado:** v3dt.1/nucleo-v1.4, com aprendizado comportamental ainda sem resultados empíricos.

## Síntese quantitativa

| Versão | Cômodos | Cenários | Execuções | LOC rastreadas | Eventos médios | Eventos/cômodo | Fidelidade média do espelho (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V0 | 1 | 40 | 2400 | 8507 | 1075.48 | 1075.48 | 59.94 |
| V1 | 2 | 38 | 2280 | 8550 | 1445.81 | 722.90 | 64.14 |
| V2 | 4 | 37 | 2220 | 7864 | 2389.10 | 597.27 | 58.64 |
| V3 | 7 | 60 | 3600 | 10957 | 3808.74 | 544.11 | 65.85 |

## Leitura de engenharia

1. A progressão V0→V1→V2→V3 aumenta a topologia de 1 para 2, 4 e 7 cômodos, mantendo núcleo, sementes e controladores; isso forma um quase-experimento de escalabilidade espacial.
2. Totais brutos crescem com a planta. As conclusões do artigo devem privilegiar medidas por cômodo, por minuto ocupado e comparações pareadas por cenário/semente.
3. As famílias F1–F10 cobrem uso normal, falsos negativos, falsos positivos, falhas, rede, comandos remotos, espelho, ocupação múltipla, sono e presença incompatível. Resultados agregados sem estratificação podem ocultar o mecanismo responsável.
4. A v1dt.1 e as versões sobre nucleo-v1.3 fornecem evidência observada do eixo comportamental; aprendizado do gêmeo permanece como marco planejado da v3dt.1.
5. O Digital Twin deve ser avaliado por fidelidade e pela decomposição do erro: percepção local versus sincronização, além de atualidade, divergência e reconciliação.

## Regras de interpretação

- São resultados de simulação determinística, não medições de residências reais.
- Correlação não demonstra causalidade; famílias e parâmetros devem ser controlados.
- O número de moradores varia por cenário na V1; comparações comportamentais devem controlar essa população simulada.
- O SQLite preserva cada execução bruta em JSON e as sínteses em tabelas normalizadas, com hashes SHA-256 das fontes.

## Próxima rodada mínima

Implementar v3dt.1 sobre nucleo-v1.4, congelar tags limpas, executar os dois controladores nas mesmas 30 sementes e avaliar previsão, sugestão, aceite, energia, conforto, calibração e deriva.
