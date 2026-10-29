# Tabelas compactas — CIACA 2027

## Tabela 1 — Transferência do padrão CEP–Digital Twin

| Domínio | Entidade do gêmeo | Evento complexo | Janela | Ação |
|---|---|---|---|---|
| Pontes | estrutura | vibração + deformação crescente | horas/dias | inspeção ou restrição |
| Apoio a idosos | pessoa e rotina | ausência de movimento/resposta | segundos/minutos | verificação e alerta graduado |
| CI/CD | pipeline e arquitetura | falha recorrente após alteração | minutos/horas | bloqueio ou rollback |
| Veículo autônomo | veículo e entorno | obstáculo dentro da distância de frenagem | milissegundos | frenagem ou evasão |

## Tabela 2 — Versões e massa experimental

| Versão | Tag | Commit | Cômodos | Cenários | Execuções | Req. ref. (%) | Req. grupo (%) |
|---|---|---|---:|---:|---:|---:|---:|
| V0 | v0dtb | 4041399 | 1 | 38 | 2280 | 100.00 | 100.00 |
| V1 | v1dtc | 9b58a1c | 2 | 26 | 1560 | 99.87 | 89.87 |
| V2 | v2dta | 17578dd | 4 | 29 | 1740 | 100.00 | 68.05 |

## Tabela 3 — Evidência, interpretação e limite

| Evidência | Interpretação permitida | Limite |
|---|---|---|
| 5.580 execuções; 2.790 pares | protocolo executável e pareado | simulação, não campo |
| 100% de invariantes | integridade estrutural preservada | invariantes disponíveis |
| V2: desperdício −12,37 s; IC95 [−26,75; −2,07] | grupo usa menos luz | condicional aos cenários |
| V2: escuro +1,41 s; IC95 [1,02; 1,85] | troca energia por conforto | não é superioridade geral |
| Erro de percepção >> sincronização | limite sensorial domina no modelo | rede simulada |
| 4 domínios de projetos | transferência estrutural do padrão | sem efeito pedagógico causal |
