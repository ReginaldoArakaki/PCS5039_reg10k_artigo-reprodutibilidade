# NÚCLEO DO ARTIGO CIACA 2027 — MÉTODO, EVOLUÇÃO E RESULTADOS

> Rascunho para incorporação ao manuscrito de oito páginas. A numeração pressupõe as seções 1, Introdução, e 2, Fundamentação e trabalhos relacionados, ainda não redigidas. Resultados da v1dt.1 são identificados como planejamento experimental, não como evidência observada.

## 2. FUNDAMENTOS DE ARQUITETURA, EVENTOS E DIGITAL TWIN

Arquitetura de sistemas é usada neste trabalho como a descrição das estruturas, relações e decisões necessárias para que um sistema cumpra seus propósitos e atributos de qualidade ao longo da evolução. Em sistemas distribuídos, uma única representação não é suficiente para expressar simultaneamente objetivos, informação, decomposição funcional, mecanismos de distribuição e tecnologias. O Reference Model of Open Distributed Processing, RM-ODP, organiza a especificação em cinco viewpoints relacionados — enterprise, information, computational, engineering e technology — e fornece uma base sistemática para descrever sistemas abertos, heterogêneos e distribuídos (ISO/IEC 10746-1, 1998). No Reg10k, esses viewpoints conectam a finalidade educacional e os serviços esperados, o estado do ambiente e do gêmeo, os componentes que processam eventos, os canais entre residência e plataforma e as tecnologias usadas na implementação.

As decisões arquiteturais são avaliadas por seus efeitos observáveis. A ISO/IEC 25010 fornece um modelo de qualidade para especificar e avaliar características de produtos de software e sistemas intensivos em software (ISO/IEC 25010, 2023). Desempenho, confiabilidade, compatibilidade, segurança e manutenibilidade deixam, assim, de ser qualificações genéricas e são ligados a cenários e medidas: latência de reação, perda e duplicidade de eventos, autonomia durante desconexão, tempo de reconciliação, rastreabilidade e preservação de invariantes. O laboratório não procura uma arquitetura abstratamente “melhor”; procura explicitar compromissos e evidências associados a cada decisão.

Complex Event Processing, CEP, é o mecanismo que transforma ocorrências isoladas em situações arquiteturalmente relevantes por sequência, conjunção, ausência, contagem e janelas temporais. Em trabalho anterior, Saad e Arakaki (2014) empregaram uma arquitetura de processamento de eventos para atualizar continuamente barreiras de risco operacional, substituindo uma análise estática por supervisão orientada a eventos. O mesmo princípio aparece no Reg10k: passagem, presença, ausência, falha e atraso tornam-se evidências correlacionadas antes que o estado do Digital Twin seja atualizado e uma ação seja tomada.

O Digital Twin é tratado como elemento arquitetural que mantém estado digital associado a uma entidade, recebe fluxos do mundo físico e participa do retorno de decisões. Essa interpretação ultrapassa a visualização. Fujii et al. (2022) validaram uma arquitetura de Digital Twin com MLOps sobre 31 medidores e tomadas inteligentes e 19 meses de dados residenciais, produzindo previsões e recomendações personalizadas de resposta à demanda. Brandão, Arakaki e Silva (2026) aplicaram RM-ODP à modelagem de Digital Twins educacionais para supervisão em ciclo fechado. Esses trabalhos fundamentam os dois usos explorados aqui: o gêmeo do ambiente físico e o gêmeo como instrumento de supervisão, aprendizagem e governança do próprio processo de engenharia.

## 3. MÉTODO DE PESQUISA

O estudo combina três estratégias. A primeira é Design Science, paradigma no qual conhecimento sobre um problema é produzido pela construção e avaliação de artefatos que ampliam capacidades humanas ou organizacionais (Hevner et al., 2004). O processo adotado segue a sequência problema e objetivos, projeto e desenvolvimento, demonstração, avaliação e comunicação proposta por Peffers et al. (2007). O artefato inclui o ambiente Reg10k, os sucessivos kits, o protocolo experimental e o pacote de reprodutibilidade. A segunda estratégia é um estudo de caso educacional: o ambiente foi usado como exemplo condutor da disciplina PCS5039 — Engenharia de Software Orientada a IoT, na qual grupos de pós-graduação especificam, implementam e avaliam arquiteturas orientadas a eventos e integradas a Digital Twins. A terceira é um experimento computacional que compara versões do ambiente sob um mesmo núcleo de execução. Essa separação é necessária porque as evidências respondem a perguntas diferentes: o artefato demonstra viabilidade, as execuções caracterizam comportamento técnico e os projetos dos grupos indicam transferência do padrão arquitetural. Nenhuma delas, isoladamente, demonstra ganho de aprendizagem.

### 3.1 Objeto e versões analisadas

O objeto de estudo é uma automação residencial de iluminação que evolui por incrementos. A V0 contém uma sala, uma porta, sensores, atuador, morador e cachorro. A V1 acrescenta uma cozinha ligada à sala por um vão e passa a exigir inferência entre cômodos. A V2 amplia a planta para quatro cômodos. As três versões possuem Digital Twin local e remoto e um espelho usado para avaliar a fidelidade da representação. A v1dt.1, planejada como incremento seguinte, mantém a planta da V1 e altera a população: inclui mais moradores, criança, idoso, visitante e ocupante dormindo. Assim, a variável principal deixa de ser apenas a topologia e passa a incluir comportamento não diretamente observável.

As versões observadas foram congeladas nas tags `v0dtb`, `v1dtc` e `v2dta`. Todas usam o núcleo `nucleo-v1.2`, no commit `c7e8b05`, o que reduz a possibilidade de atribuir ao ambiente uma diferença introduzida pelo motor. Código, cenários e dados dessas versões são publicados em repositórios Git independentes e identificados por tags imutáveis (Arakaki, 2026a). A v1dt.1 depende do núcleo `nucleo-v1.3` e permanece fora dos resultados até que sua implementação, tag, manifesto e massa de execução estejam publicados.

### 3.2 Unidade experimental e protocolo

Uma unidade experimental é definida pela tupla:

> versão × família × cenário × controlador × semente.

Foram executadas 30 sementes, numeradas de 1 a 30, para dois controladores: o controlador de referência e um controlador de grupo usado como exemplo de implementação discente. A V0 contém 38 cenários e gera 2.280 execuções; a V1 contém 26 cenários e gera 1.560; a V2 contém 29 cenários e gera 1.740. A base longitudinal reúne, portanto, 5.580 execuções.

Os cenários são organizados em sete famílias. F1 cobre uso normal; F2, permanência sem movimento e falsos negativos; F3, passagem sem entrada e falsos positivos; F4, falhas de dispositivos; F5, quedas de rede, plataforma ou Hub; F6, comandos remotos e preferências; e F7, espelho e consulta pelo aplicativo. Cada cenário possui roteiro e resultado esperado. O manifesto da rodada registra versão, núcleo, commit, versão do Python, sementes, controladores, arquivos de entrada e seus hashes SHA-256.

O procedimento possui quatro passos: carregar ambiente, roteiro e controlador; executar a simulação determinística para a semente; verificar requisitos e invariantes; e registrar métricas, proveniência e resultado. Os CSVs das versões são consolidados em uma base SQLite. A base preserva cada execução e contém tabelas distintas para versões, métricas estáticas, resumos dinâmicos, fontes e marcos planejados. Dessa forma, a especificação da v1dt.1 pode participar do planejamento sem ser contada como resultado.

O ciclo de Design Science aparece também entre versões. Resultados e falhas observados em um incremento realimentam requisitos e cenários do incremento seguinte. A V0 demonstra estado e fidelidade; a V1 introduz correlação espacial; a V2 avalia escala por planta; e a v1dt.1 converte limitações de percepção em problemas comportamentais explícitos. O artefato não é avaliado apenas ao final: construção e avaliação alternam-se e deixam evidências versionadas.

### 3.3 Variáveis e métricas

As variáveis independentes são versão, controlador, família, cenário, semente, modo da simulação e modo da rede. Número de cômodos e moradores modelados são variáveis estruturais. As variáveis dependentes incluem eventos processados, latência de reação, desperdício de iluminação, tempo no escuro com ocupante, apagamentos indevidos, ocupação desconhecida, atualidade do gêmeo, tempo de estado não atual, comandos remotos, divergência, reconciliação, eventos não entregues e fidelidade do espelho.

A fidelidade é decomposta em erro de percepção e erro de sincronização. O primeiro mede o intervalo em que o Hub representa incorretamente o mundo mesmo antes do envio à plataforma; o segundo mede o intervalo adicional causado pelo fluxo entre Hub e plataforma. Essa distinção impede que uma decisão errada seja atribuída genericamente ao Digital Twin quando sua origem é sensorial, temporal ou de comunicação.

Métricas totais caracterizam carga, mas não são usadas isoladamente para comparar versões. O número de eventos, o desperdício e os tempos acumulados tendem a crescer com o número de cômodos, a duração do cenário e a quantidade de situações exercitadas. As comparações empregam, conforme o caso, normalização por cômodo, tempo ocupado e família, além de pareamento por cenário e semente. Média e mediana são reportadas em conjunto porque várias distribuições possuem muitos zeros e caudas longas.

### 3.4 Critérios de validade e reprodução

Uma rodada é aceita quando tags e commits podem ser resolvidos, os hashes das entradas coincidem, os dados respeitam os esquemas, percentuais permanecem entre 0 e 100 e os testes terminam sem erro. O pacote de reprodução contém scripts, CSVs derivados, banco SQLite, planilha de leitura e documentação do protocolo.

Há quatro ameaças principais. Primeiro, são simulações, não medições em residências reais. Segundo, os conjuntos de cenários diferem entre versões; por isso, agregados globais não constituem comparação causal. Terceiro, o controlador de grupo representa apenas uma solução alternativa e não a população de alunos. Quarto, a utilização do kit e a diversidade dos projetos mostram aplicabilidade, mas ainda não medem aprendizagem. A conclusão pedagógica é deliberadamente limitada à viabilidade do laboratório e à transferência observada do padrão.

## 4. EVOLUÇÃO DO KIT E DA ARQUITETURA

O ponto de partida é um kit de automação isolado. Sensores detectam passagem e presença, um controlador decide e um atuador comanda a lâmpada. A arquitetura resolve o ciclo local, mas seu estado termina na residência. Não existe fluxo comum para correlacionar casas, comparar o presente com históricos ou oferecer serviços que dependem de uma visão de plataforma. O log local registra o ocorrido, mas o dado armazenado depois da decisão não substitui o evento processado dentro da janela em que a ação ainda é útil.

O Reg10k transforma essa limitação numa sequência de problemas. Em vez de apresentar imediatamente uma plataforma completa, cada versão introduz uma capacidade e conserva as anteriores. O aluno pode observar qual novo estado precisa ser mantido, que eventos passam a existir, quais falhas são produzidas e que métrica torna a decisão verificável.

### 4.1 V0: do controle ao estado digital

A V0 mantém uma única sala, mas introduz Digital Twin e espelho. O mundo simulado possui a posição e as ações dos ocupantes; o Hub mantém o estado percebido; a plataforma recebe atualizações; e o espelho compara representação e realidade ao longo do tempo. Com isso, “a luz acendeu” deixa de ser a única saída relevante. Torna-se possível perguntar se o sistema sabia que o cômodo estava ocupado, se o gêmeo estava atual e por quanto tempo a plataforma afirmou um estado incorreto.

Essa versão introduz uma distinção que permanece nas demais: mundo, percepção, sincronização e decisão não são o mesmo estado. Um sensor pode deixar de perceber alguém parado; a rede pode atrasar um estado correto; o controlador pode decidir com informação incompleta. O Digital Twin funciona como instrumento de engenharia porque torna essas separações mensuráveis.

### 4.2 V1: correlação espacial

A V1 acrescenta uma cozinha ligada à sala por um vão. A passagem entre ambientes produz dois efeitos: o cômodo de origem pode tornar-se vazio e o de destino, ocupado. Sensores de passagem, entretanto, não identificam direção ou identidade. A decisão depende da correlação temporal entre passagem, presença e estado anterior.

O incremento expõe problemas que não existem numa sala isolada: uma pessoa pode sair de um cômodo sem deixar a residência; uma passagem pode gerar acionamento indevido nos dois lados; e estados independentes podem divergir durante uma transição. O Digital Twin deixa de representar apenas um dispositivo e passa a manter uma pequena topologia residencial.

### 4.3 V2: escala espacial e geração sistemática

A V2 amplia a residência para sala, cozinha, quarto e banheiro. O crescimento não é apenas quantitativo. Parâmetros podem variar por cômodo, passagens possuem características diferentes e a cobertura manual de combinações torna-se frágil. O ambiente passa a depender mais fortemente da geração de cenários por planta e da normalização dos resultados.

A principal provocação é que escala não pode ser confundida com quantidade bruta de eventos. Quatro cômodos naturalmente produzem mais telemetria e mais tempo acumulado de divergência que um cômodo. Uma arquitetura comparável precisa associar cada observação à topologia que a produziu e oferecer medidas por cômodo ou por unidade de ocupação.

### 4.4 v1dt.1: do espaço ao comportamento

A v1dt.1 mantém a planta da V1 para alterar uma variável: os ocupantes. Morador, moradora, criança, idoso, cachorro e visitante geram movimentos diferentes, mas os sensores não fornecem identidade, idade ou intenção. A ação `DORMIR` cria o contraste com alguém que permanece parado lendo. Para quem lê, apagar é indevido; para quem dorme, manter a luz acesa é desperdício e desconforto. O sensor observa ausência de movimento nos dois casos.

Três famílias complementam o protocolo. F8 examina ocupação múltipla — um sai e outro fica. F9 examina sono. F10 examina presença incompatível: movimento detectado sem passagem recente que o explique. A situação é registrada como suspeita, verificada após uma janela e conciliada se um evento atrasado chegar; não é rotulada automaticamente como invasão.

Esse incremento desloca o Digital Twin de uma representação topológica para uma base de inferência comportamental. A dificuldade não é armazenar mais dados, mas reconhecer o limite do que os sensores permitem afirmar. O gêmeo deve representar também incerteza, origem da evidência e possibilidade de revisão.

### 4.5 Da residência à plataforma

Quando residências são conectadas, eventos derivados podem sustentar serviços inexistentes no kit isolado: recomendação energética, previsão de carga, identificação de falhas regionais, apoio a idosos e alertas graduados. A plataforma também pode integrar educação, saúde, segurança e transporte, além de serviços privados que reduzam custos para assinantes. Essas possibilidades não são resultados deste experimento; são consequências arquiteturais que dependem de consentimento, qualidade dos eventos, responsabilidade e modelos de negócio.

O padrão comum é evento → processamento → Digital Twin → ação. Nos projetos da PCS5039, a entidade do gêmeo muda: ponte, pessoa, pipeline ou veículo. Muda também a janela de decisão, de milissegundos na frenagem a dias na degradação estrutural. Permanece a necessidade de correlacionar eventos, comparar o presente com um estado ou comportamento esperado e agir antes que o fato perca valor.

## 6. IMPLEMENTAÇÃO E BASE EXPERIMENTAL

A implementação separa núcleo e repositórios de versão. O núcleo contém simulador, Hub, canal com a plataforma, modelos do Digital Twin, avaliação, gerador de cenários, comparador e catálogo. Cada versão contém planta, roteiros, resultados esperados, controladores, documentação e dados da rodada. O vínculo com o núcleo é registrado como submódulo, o que permite usar o mesmo motor e conservar a identidade do experimento.

Os artefatos de entrada são JSON validados por esquemas. Cada execução produz requisitos e invariantes, métricas operacionais e medidas do gêmeo. O manifesto relaciona o CSV às entradas e ao código que o produziu. A base longitudinal foi construída a partir das tags publicadas, e não de diretórios de trabalho. Ela contém 5.580 execuções, 1.212 resumos dinâmicos por versão, controlador, família e métrica, além das métricas estáticas obtidas da árvore Git.

Os repositórios constituem parte da evidência. O núcleo está publicado em `PCS5039_ambiente_reg10k_vCl0`, tag `nucleo-v1.2`, commit `c7e8b05`. As massas observadas estão em `PCS5039_ambiente_reg10k_V0`, tag `v0dtb`, commit `4041399`; `PCS5039_ambiente_reg10k_V1`, tag `v1dtc`, commit `9b58a1c`; e `PCS5039_ambiente_reg10k_V2`, tag `v2dta`, commit `17578dd` (Arakaki, 2026a). A identificação simultânea de repositório, tag e commit permite reconstruir a configuração mesmo que o ramo principal continue evoluindo.

Um segundo repositório reúne o pacote de reprodutibilidade do artigo: scripts de coleta e análise, banco SQLite, CSVs derivados, planilha, protocolo, testes e os documentos do manuscrito (Arakaki, 2026b). A referência é distinta da implementação porque possui finalidade e ciclo de vida próprios. O primeiro conjunto executa os experimentos; o segundo preserva a seleção, transformação e interpretação das evidências usadas no artigo.

| Versão | Tag | Cômodos | Cenários | Execuções | Estado |
|---|---|---:|---:|---:|---|
| V0 | `v0dtb` | 1 | 38 | 2.280 | observado |
| V1 | `v1dtc` | 2 | 26 | 1.560 | observado |
| V2 | `v2dta` | 4 | 29 | 1.740 | observado |
| v1dt.1 | a publicar | 2 | P01–P08 e F8–F10 | a executar | planejado |

A navegação apresenta painel de cenários, planta, estados físicos, espelho, linha do tempo e métricas. Ela serve ao exercício porque permite relacionar uma decisão visível à sequência de eventos e ao estado interno que a produziu. Capturas e detalhes de reprodução são reservados ao apêndice técnico, para que o corpo permaneça centrado no argumento e nos resultados.

## 7. RESULTADOS E DISCUSSÃO

### 7.1 Cobertura e verificabilidade

As três versões executaram integralmente as 30 sementes e os dois controladores. Todos os 5.580 registros satisfizeram os invariantes avaliados. O controlador de referência satisfez os requisitos em 100% das execuções da V0, 99,87% da V1 e 100% da V2. O controlador de grupo obteve 100%, 89,87% e 68,05%, respectivamente.

O resultado não permite afirmar que a arquitetura de referência é universalmente melhor, pois os cenários não formam a mesma amostra entre versões. Ele mostra, contudo, uma propriedade didática importante: o aumento da topologia e da diversidade de situações expõe limitações de uma implementação alternativa que não aparecem no ambiente mais simples. Os invariantes permanecerem satisfeitos enquanto requisitos de cenário falham também separa duas dimensões: integridade estrutural do ambiente e adequação funcional do controlador.

### 7.2 Escala e normalização

No controlador de referência, o número médio de eventos por execução é 1.073,13 na V0, 1.044,33 na V1 e 2.021,11 na V2. O total da V2 quase duplica em relação à V1, coerente com a ampliação da planta. Quando normalizado por cômodo, entretanto, o valor passa de 1.073,13 na V0 para 522,17 na V1 e 505,28 na V2.

Essa queda não deve ser lida como ganho direto de eficiência. A V0 possui 38 cenários e participação maior de famílias de falha e rede; V1 e V2 possuem outras composições e durações. O resultado demonstra por que totais globais são insuficientes. Uma comparação explicativa deve controlar família, cenário equivalente e tempo de ocupação. A base torna essa análise possível, mas o artigo preserva a distinção entre caracterização longitudinal e inferência causal.

O desperdício médio do controlador de referência cresce de 56,61 s na V0 para 93,58 s na V1 e 155,23 s na V2. Por cômodo, os valores são 56,61 s, 46,79 s e 38,81 s. O tempo médio no escuro com ocupante apresenta comportamento semelhante: 105,84 s, 39,11 s e 45,30 s em valor bruto; 105,84 s, 19,56 s e 11,32 s por cômodo. As medianas, entretanto, são muito inferiores às médias em várias versões, indicando muitos cenários sem ocorrência e poucos casos com duração elevada. A família e a distribuição são mais informativas que uma única média.

### 7.3 Estado e fidelidade do Digital Twin

A fidelidade média do espelho, no controlador de referência, é 59,94% na V0, 62,27% na V1 e 55,92% na V2. Esses percentuais agregam cenários com objetivos distintos, inclusive desconexão e falhas, e não constituem uma nota global da arquitetura. Sua utilidade está em permitir decomposição.

O erro médio de percepção é 127,68 s na V0, 99,42 s na V1 e 175,08 s na V2. O erro médio de sincronização é 0,016 s, 0,004 s e zero, respectivamente. Nos parâmetros usados, portanto, a maior parcela da divergência agregada está associada ao que o Hub consegue inferir a partir dos sensores e dos cenários, e não ao transporte adicional para a plataforma. O resultado reforça uma provocação do laboratório: conectar uma percepção incorreta apenas distribui o erro com maior velocidade.

O tempo médio de gêmeo não atual passa de 47,42 s na V0 para 92,68 s na V1 e 124,84 s na V2. Normalizado por cômodo, corresponde a 47,42 s, 46,34 s e 31,21 s. Novamente, o total cresce com a topologia, enquanto a medida normalizada muda a interpretação. A atualidade p95 média do controlador de referência é 124,34 ms na V0 e 100 ms nas versões V1 e V2; nestas, o valor por cômodo é 50 e 25 ms, respectivamente. Esses números caracterizam o modelo simulado e não devem ser extrapolados para uma rede real.

### 7.4 Controladores e interpretação dos resultados

Os dois controladores produzem cargas próximas. Na V2, por exemplo, o controlador de referência processa em média 2.021,11 eventos e o de grupo, 2.019,18. As diferenças de requisitos, portanto, não decorrem de uma ausência geral de execução. Elas devem ser localizadas nas famílias e decisões específicas.

Algumas métricas não podem ser comparadas por média simples. A latência de reação p95 média do controlador de referência permanece próxima de 50 ms nos cenários que exercitam reação, enquanto o controlador de grupo possui muitas observações iguais a zero. Zero pode significar ausência do fenômeno medido, e não reação instantânea. A análise final deverá separar valores não aplicáveis de valores efetivamente nulos antes de comparar desempenho.

Esse cuidado é parte da contribuição metodológica. Um laboratório de arquitetura não deve apenas gerar números; deve tornar explícitas a semântica da métrica, a população considerada e as condições em que uma agregação é válida.

### 7.5 Evidência educacional e transferência

O kit foi usado como exemplo para projetos de pontes, apoio a idosos, CI/CD de hardware e software e carros autônomos. Nos quatro casos, os grupos puderam identificar eventos simples, situação complexa, entidade mantida pelo gêmeo e ação. A janela de decisão variou de milissegundos a dias, mas o encadeamento permaneceu reconhecível.

Essa evidência sustenta reutilização do padrão e adequação do kit como ponto de partida. Não mede, porém, quanto cada aluno aprendeu nem compara a abordagem com outro método de ensino. Uma avaliação pedagógica posterior deverá empregar rubrica comum para arquitetura, eventos, gêmeo, protocolo e reprodutibilidade; comparar entregas iniciais e finais; e triangular resultados com percepção dos participantes.

### 7.6 Síntese das respostas

Os resultados respondem parcialmente às perguntas de pesquisa. Para RQ1, a progressão por versões associa capacidades a problemas observáveis e mantém um protocolo comum. Para RQ2, as medidas úteis são estratificadas por família e normalizadas pela estrutura e pelo tempo; médias globais não bastam. Para RQ3, o Digital Twin introduz estados e erros que o kit isolado não consegue representar. Para RQ4, os projetos mostram transferência estrutural, mas não efetividade pedagógica quantitativa.

O próximo experimento é a v1dt.1. Sua contribuição será testar a fronteira entre estado físico e interpretação comportamental: um sai e outro fica, alguém permanece lendo, alguém dorme e uma presença aparece sem passagem explicativa. Para essa rodada, as métricas deverão incluir luz com todos dormindo, escuro com ocupante acordado, precisão e revocação da presença incompatível, tempo de confirmação e quantidade de conciliações.
