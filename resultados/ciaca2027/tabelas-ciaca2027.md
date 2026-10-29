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
| V0 | v0dtc | 76a711e | 1 | 40 | 2400 | 100.00 | 100.00 |
| V1 | v1dt.1 | 9e0f8a8 | 2 | 38 | 2280 | 99.91 | 87.81 |
| V2 | v2dtb | 75225e9 | 4 | 37 | 2220 | 100.00 | 66.85 |
| V3 | v3dt | 13b6200 | 7 | 60 | 3600 | 100.00 | 66.72 |

## Tabela 3 — Evidência, interpretação e limite

| Evidência | Interpretação permitida | Limite |
|---|---|---|
| 10.500 execuções; 5.250 pares | protocolo executável e pareado | simulação, não campo |
| 100% de invariantes | integridade estrutural preservada | invariantes disponíveis |
| V3: desperdício −7,98 s; IC95 [−15,93; −2,00] | grupo usa menos luz | condicional aos cenários |
| V3: escuro +1,82 s; IC95 [1,47; 2,16] | troca energia por conforto | não é superioridade geral |
| Erro de percepção >> sincronização | limite sensorial domina no modelo | rede simulada |
| 4 domínios de projetos | transferência estrutural do padrão | sem efeito pedagógico causal |
