# DA AUTOMAÇÃO IOT ISOLADA À PLATAFORMA ORIENTADA A EVENTOS: UM LABORATÓRIO REPRODUZÍVEL DE DIGITAL TWINS NA PÓS-GRADUAÇÃO

> Esqueleto argumentativo para artigo longo, em português, planejado para oito páginas no padrão CIACA. As regras oficiais de 2027 ainda precisam ser confirmadas; até lá, adota-se o limite e a estrutura editorial de 2026. A versão para avaliação deve permanecer anônima.

## RESUMO PROVISÓRIO

A formação em Engenharia de Software Orientada a IoT enfrenta uma dificuldade estrutural: kits didáticos tornam sensores, atuadores e protocolos observáveis, mas raramente permitem acompanhar a evolução completa de um dispositivo isolado para uma plataforma distribuída, orientada a eventos e integrada a Digital Twins. Este artigo investiga como essa evolução pode ser materializada em um laboratório reproduzível de pós-graduação. O objeto de estudo é o ambiente Reg10k, desenvolvido como exemplo condutor da disciplina PCS5039, no qual uma automação residencial de iluminação evolui de uma sala controlada localmente para residências com múltiplos cômodos, conectividade, histórico de eventos, espelho digital e cenários comportamentais. A pesquisa combina Design Science, estudo de caso educacional e experimento computacional. Três versões publicadas, executadas sobre o mesmo núcleo, totalizam 5.580 execuções com 30 sementes e dois controladores, abrangendo uso normal, falsos positivos, falsos negativos, falhas de dispositivos, desconexões, comandos remotos e fidelidade do gêmeo. Os resultados demonstram a viabilidade de comparar incrementalmente decisões arquiteturais, desde que métricas brutas sejam normalizadas por cômodo, tempo ocupado e família de cenário. O laboratório também permitiu que grupos aplicassem o padrão evento, processamento, Digital Twin e ação a pontes, apoio a idosos, pipelines de hardware e software e veículos autônomos. A contribuição é um método experimental e reproduzível para ensinar a transformação de kits IoT em plataformas digitais, acompanhado por uma base de versões, métricas e protocolos. Os resultados sustentam a viabilidade técnica e a transferência arquitetural; a efetividade pedagógica quantitativa permanece como trabalho futuro.

**PALAVRAS-CHAVE:** Digital Twin; Internet das Coisas; arquitetura de software; processamento de eventos; ensino de pós-graduação; reprodutibilidade.

## TESE DO ARTIGO

Um kit IoT torna-se pedagogicamente mais relevante quando deixa de ser apresentado como uma solução pronta e passa a funcionar como uma sequência controlada de problemas arquiteturais. A introdução gradual de conectividade, eventos, estado digital, falhas, comportamento e serviços permite que o aluno observe não apenas o funcionamento de sensores e atuadores, mas as consequências das decisões que transformam um sistema local em plataforma.

O argumento é construído em cinco passos:

1. Um kit isolado resolve uma função local, mas não oferece estado compartilhado, correlação entre fontes, aprendizado de comportamento ou serviços de plataforma.
2. A simples conexão com a nuvem não resolve essas limitações; é necessário definir contratos de eventos, janelas de decisão, estado do Digital Twin e fluxo de atuação.
3. Essas capacidades podem ser introduzidas em versões pequenas e comparáveis, preservando um núcleo comum e um protocolo experimental.
4. As versões produzem evidências técnicas reproduzíveis e expõem compromissos entre conforto, energia, disponibilidade, fidelidade e conectividade.
5. O padrão resultante pode ser transferido para outros domínios, embora a entidade do gêmeo, a janela de decisão e a ação sejam diferentes.

## PERGUNTAS DE PESQUISA

**RQ1.** Como a evolução incremental de um kit IoT isolado para uma plataforma orientada a eventos e Digital Twins pode ser organizada como laboratório de arquitetura de software na pós-graduação?

**RQ2.** Quais métricas permitem comparar versões com diferentes quantidades de cômodos, cenários, eventos e estados digitais?

**RQ3.** Que capacidades arquiteturais deixam de existir no kit isolado e passam a ser observáveis com eventos, Hub, histórico e Digital Twin?

**RQ4.** Em que medida o padrão evento → processamento → Digital Twin → ação pode ser transferido para os projetos desenvolvidos pelos alunos em outros domínios?

## PROPOSIÇÕES DE TRABALHO

As proposições orientam a análise, mas não devem ser apresentadas como hipóteses estatísticas confirmadas sem os testes correspondentes.

**P1 — Progressão observável.** A decomposição do laboratório em versões permite associar novas métricas e novos modos de falha às capacidades arquiteturais introduzidas em cada incremento.

**P2 — Comparabilidade condicionada.** Métricas totais não são suficientes para comparar versões de diferentes dimensões; a interpretação exige normalização por cômodo, duração, ocupação e família experimental.

**P3 — Digital Twin como instrumento de engenharia.** O valor didático do Digital Twin está na separação entre estado real, estado percebido, estado sincronizado e ação, e não apenas na visualização da residência.

**P4 — Transferência estrutural.** O padrão arquitetural permanece reconhecível entre domínios, ainda que eventos, janelas temporais, modelos de estado e mecanismos de atuação mudem.

## CONTRIBUIÇÕES PRETENDIDAS

**C1. Um laboratório incremental e reproduzível.** O artigo descreve como o Reg10k organiza a evolução de uma automação local para uma plataforma orientada a eventos, com versões, tags, cenários, oráculos, sementes e manifestos.

**C2. Um modelo de avaliação da evolução.** O trabalho reúne métricas estáticas e dinâmicas e propõe regras de normalização que evitam atribuir ao crescimento arquitetural efeitos causados apenas por massas de teste diferentes.

**C3. Uma interpretação do Digital Twin para o ensino de arquitetura.** O gêmeo é tratado como elemento que mantém estado, recebe eventos, explicita divergências, suporta decisões e fecha o ciclo de atuação.

**C4. Evidência inicial de transferência.** Os projetos da disciplina mostram como o mesmo padrão pode estruturar problemas de engenharia civil, saúde, pipelines de desenvolvimento e veículos autônomos.

## 1. INTRODUÇÃO — MENSAGEM E ENCADEAMENTO

### Mensagem central

Ensinar IoT como integração de dispositivos é necessário, mas insuficiente para formar arquitetos capazes de projetar plataformas distribuídas. O problema relevante surge quando o kit precisa manter continuidade de serviço, correlacionar eventos, aprender comportamento, justificar decisões e oferecer serviços além da automação original.

### Encadeamento proposto

- Iniciar com o contraste entre acender uma lâmpada e operar uma plataforma de residências conectadas.
- Mostrar que a diferença não é apenas escala: muda a natureza da informação, da decisão e da responsabilidade.
- Introduzir o problema educacional: como tornar essa passagem observável e experimentalmente verificável?
- Apresentar o Reg10k e a PCS5039 como estudo de caso.
- Declarar RQ1–RQ4.
- Antecipar os principais números: três versões observadas, 5.580 execuções, 30 sementes, dois controladores e sete famílias implementadas.
- Encerrar com as quatro contribuições.

### Frase de abertura candidata

Acender automaticamente uma lâmpada é um problema de controle local; transformar eventos de milhares de residências em decisões, aprendizado e serviços é um problema de plataforma.

### Frase de fechamento candidata

O artigo examina essa passagem como objeto de ensino e de experimentação, e não como simples substituição de sensores ou adoção de uma tecnologia de nuvem.

## 2. FUNDAMENTAÇÃO E TRABALHOS RELACIONADOS

### Mensagem central

O laboratório ocupa a interseção de quatro campos normalmente estudados em separado: IoT, processamento de eventos, Digital Twins e ensino experimental de arquitetura de software.

### Blocos argumentativos

1. **IoT e arquiteturas distribuídas:** dispositivo, edge, Hub, plataforma e serviços.
2. **Eventos e CEP:** eventos simples, ausência, sequência, correlação, atraso, perda e duplicidade.
3. **Digital Twin:** distinção entre modelo digital, sombra digital e gêmeo com fluxo bidirecional.
4. **Ensino de arquitetura:** cenários de qualidade, decisões, ATAM, protótipos e reprodutibilidade.
5. **Lacuna:** ausência de ambientes didáticos incrementais que mantenham rastreabilidade entre versão, capacidade, cenário, métrica e resultado.

### Posição em relação ao artigo ACDSA

O trabalho do ACDSA sustenta que eventos processados em tempo operacional constituem infraestrutura de controle e que o Digital Twin converte o fluxo em estado e ação. O presente artigo muda a unidade de análise: investiga como essa arquitetura pode ser ensinada e experimentalmente observada por meio de versões reproduzíveis. Não deve repetir a simulação de 10.000 casas nem a comparação de latência de intrusão como contribuição principal.

## 3. MÉTODO DE PESQUISA

### Mensagem central

O estudo combina construção de artefato, estudo de caso educacional e experimento computacional; cada tipo de evidência sustenta uma conclusão diferente.

### Desenho da pesquisa

- **Design Science:** construção do kit, núcleo, versões, cenários, catálogo e base de evolução.
- **Estudo de caso:** utilização do exemplo na disciplina PCS5039 e transferência para projetos de grupos.
- **Experimento computacional:** execução de cenários por versão, controlador e semente.
- **Análise documental:** requisitos, decisões arquiteturais, versões e entregas.

### Unidades experimentais

A unidade elementar é `versão × família × cenário × controlador × semente`. A base atual contém 5.580 unidades executadas. A análise agregada deve preservar versão, controlador e família antes de calcular totais.

### Variáveis

- independentes: versão, controlador, cenário, família, modo de rede e semente;
- estruturais: número de cômodos, moradores modelados, sensores, atuadores e passagens;
- dependentes: latência, desperdício, tempo no escuro, acionamentos, perdas, atualidade, fidelidade e componentes do erro do gêmeo.

### Estratégia de comparação

- resultados brutos para caracterizar a carga;
- métricas por cômodo e por tempo ocupado para comparação espacial;
- análise por família para localizar mecanismos;
- comparação pareada por cenário e semente quando houver cenários equivalentes;
- média, mediana, dispersão e intervalo de confiança;
- separação explícita entre resultados observados e capacidades planejadas.

### Limite metodológico

Os dados demonstram comportamento do simulador e viabilidade do laboratório. Não representam consumo de residências reais nem, isoladamente, comprovam aprendizagem dos estudantes.

## 4. EVOLUÇÃO DO KIT E ARQUITETURA

### Mensagem central

A evolução não consiste em acrescentar componentes a uma planta, mas em introduzir capacidades que tornam novos problemas observáveis.

### Linha narrativa

| Marco | Capacidade | Problema tornado observável |
|---|---|---|
| Kit isolado | controle local e log | decisões rígidas e ausência de estado compartilhado |
| V0 | um cômodo, gêmeo e espelho | percepção versus estado real |
| V1 | sala, cozinha e vão | correlação entre cômodos e passagem |
| V2 | quatro cômodos | escala espacial, parâmetros e geração de cenários |
| v1dt.1 | múltiplos ocupantes, sono e visitante | comportamento não diretamente observável |
| Plataforma | agregação entre residências | serviços, aprendizado e atuação coordenada |

### Argumento sobre o Digital Twin

O gêmeo deve ser descrito por quatro estados relacionados:

1. estado do mundo simulado;
2. estado percebido pelos sensores e pelo Hub;
3. estado sincronizado com a plataforma;
4. estado utilizado para decisão e atuação.

Essa decomposição permite distinguir erro de percepção de erro de sincronização. Também permite discutir quando o gêmeo é apenas sombra, quando fecha o ciclo de controle e quando começa a sustentar aprendizado de comportamento.

### Figura 1 planejada

**Evolução de capacidades do Reg10k:** kit isolado → Hub orientado a eventos → Digital Twin → plataforma → histórico comportamental → serviços.

## 5. O LABORATÓRIO PCS5039

### Mensagem central

O exemplo resolvido fornece um vocabulário comum, enquanto os projetos dos grupos testam a transferência do raciocínio arquitetural para outros domínios.

### Sequência didática

1. problema, atores e hipótese de valor;
2. requisitos e cenários de qualidade;
3. catálogo e contratos de eventos;
4. componentes, interfaces e regras de correlação;
5. modelo e ciclo de vida do Digital Twin;
6. táticas e decisões arquiteturais;
7. protocolo experimental congelado;
8. implementação, medição e defesa.

### Projetos como evidência de transferência

| Domínio | Entidade do gêmeo | Evento complexo | Ação possível |
|---|---|---|---|
| Pontes | estrutura | vibração anômala com deformação crescente | inspeção ou restrição de uso |
| Apoio a idosos | pessoa e rotina | ausência de movimento ou resposta fora do hábito | verificação e alerta graduado |
| CI/CD | pipeline, arquitetura e bancada | falha recorrente após alteração correlacionada | bloqueio, rollback ou notificação |
| Veículo autônomo | veículo e entorno | obstáculo dentro da distância de frenagem | frenagem ou evasão |

### Cuidado interpretativo

A diversidade dos projetos evidencia reutilização do padrão. Para afirmar ganho de aprendizagem, será necessário aplicar rubrica, instrumento pré/pós, avaliação das entregas ou triangulação com entrevistas.

## 6. IMPLEMENTAÇÃO E BASE EXPERIMENTAL

### Mensagem central

A reprodutibilidade não é um apêndice administrativo; ela faz parte da arquitetura do experimento.

### Elementos que devem aparecer no corpo

- núcleo compartilhado `nucleo-v1.2`;
- tags `v0dtb`, `v1dtc` e `v2dta`;
- repositórios de versão;
- cenários e resultados esperados;
- dois controladores;
- sementes 1–30;
- CSV e manifesto por rodada;
- hashes das entradas;
- base SQLite longitudinal;
- scripts de coleta e análise.

### Tabela 2 planejada

| Versão | Cômodos | Cenários | Execuções | Núcleo | Estado |
|---|---:|---:|---:|---|---|
| V0 | 1 | 38 | 2.280 | v1.2 | observado |
| V1 | 2 | 26 | 1.560 | v1.2 | observado |
| V2 | 4 | 29 | 1.740 | v1.2 | observado |
| v1dt.1 | 2 | P01–P08 e F8–F10 | a executar | v1.3 | planejado |

## 7. RESULTADOS E DISCUSSÃO

### 7.1 Progressão técnica

**Mensagem:** o laboratório produz uma evolução mensurável, mas a dimensão da massa experimental não cresce linearmente com o número de cômodos.

- V0 possui 38 cenários e 2.280 execuções.
- V1 possui 26 cenários e 1.560 execuções.
- V2 possui 29 cenários e 1.740 execuções.
- Os eventos médios por cômodo, no controlador de referência, passam de aproximadamente 1.073 na V0 para 522 na V1 e 505 na V2.

Essa redução não deve ser interpretada imediatamente como melhoria de eficiência. Ela reflete diferenças de cenário, duração e composição. O resultado sustenta P2: a comparação exige estratificação e normalização.

### 7.2 Digital Twin e qualidade da decisão

**Mensagem:** a instrumentação permite observar onde o gêmeo deixa de representar corretamente o ambiente.

Discutir:

- fidelidade do espelho;
- atualidade do gêmeo;
- tempo de estado não atual;
- erro de percepção;
- erro de sincronização;
- divergência além do prazo;
- reconciliação após desconexão.

O ponto didático é que uma decisão incorreta pode decorrer do sensor, do modelo, do transporte ou da política. O Digital Twin torna essas causas separáveis e discutíveis.

### 7.3 Comportamento e v1dt.1

**Mensagem:** ocupação múltipla, sono e visitante introduzem situações em que o estado relevante não é diretamente observável pelo sensor.

As famílias propostas são:

- F8: um ocupante sai e outro permanece;
- F9: permanência acordada versus sono;
- F10: presença incompatível, confirmação e conciliação.

As métricas deverão incluir luz com todos dormindo, escuro com ocupante acordado, precisão e revocação de presença incompatível, tempo de confirmação e conciliações. Enquanto a rodada não for executada, esses elementos permanecem como desenho experimental.

### 7.4 Transferência e serviços

**Mensagem:** a conectividade permite novos serviços, mas o artigo não deve confundir possibilidade arquitetural com benefício comprovado.

Relacionar os eventos e estados do gêmeo com energia, saúde, segurança, transporte e educação. Serviços públicos e privados devem aparecer como extensões possíveis, condicionadas por consentimento, qualidade de dados, responsabilidades e avaliação econômica.

### Tabela 3 planejada

| Evidência | Resultado | Interpretação permitida | Limite |
|---|---|---|---|
| 5.580 execuções | protocolo executável e repetível | viabilidade experimental | não representa residências reais |
| versões V0–V2 | capacidades incrementais observáveis | evolução técnica | massas de cenários diferentes |
| métricas do gêmeo | erro de percepção e sincronização separáveis | valor para diagnóstico arquitetural | modelo simulado |
| projetos dos grupos | padrão reutilizado em quatro domínios | transferência estrutural | sem medida pré/pós de aprendizagem |

## 8. CONCLUSÃO — RESPOSTA PRETENDIDA

O estudo deverá responder que a evolução incremental transforma um kit de automação em laboratório de arquitetura porque cada versão acrescenta uma capacidade, um conjunto de falhas e métricas correspondentes. A preservação do núcleo, dos manifestos e das sementes torna os experimentos auditáveis. O Digital Twin amplia o exercício ao separar mundo, percepção, sincronização e decisão, e permite discutir comportamento e serviços além da iluminação.

A evidência disponível sustenta viabilidade técnica, reprodutibilidade e transferência do padrão. Não sustenta ainda uma conclusão causal sobre aprendizagem. O próximo ciclo deverá executar a v1dt.1 e avaliar as entregas dos estudantes com uma rubrica comum e, se possível, instrumento pré/pós.

### Frase final candidata

O principal resultado do laboratório não é uma residência que acende suas luzes, mas um ambiente no qual decisões arquiteturais podem ser construídas, perturbadas, medidas e explicadas.

## FIGURAS E TABELAS DO CORPO

1. **Figura 1 — Evolução de capacidades:** kit → Hub → Digital Twin → plataforma → comportamento → serviços.
2. **Figura 2 — Ciclo experimental:** cenário → eventos → controlador → gêmeo → métricas → base longitudinal.
3. **Tabela 1 — Transferência entre domínios:** entidade, eventos, padrão, janela e ação.
4. **Tabela 2 — Versões e massa experimental:** V0, V1, V2 e v1dt.1.
5. **Tabela 3 — Evidência, interpretação e limite.**

## APÊNDICE TÉCNICO PLANEJADO — TRÊS PÁGINAS

### Apêndice A — Implementação e arquitetura

- diagrama de componentes;
- responsabilidades do núcleo, simulador, Hub, plataforma e catálogo;
- tags e commits;
- contrato reduzido de evento;
- comando mínimo de reprodução.

### Apêndice B — Navegação

- painel de cenários;
- planta e estado do ambiente;
- Digital Twin/espelho;
- linha do tempo e métricas.

Cada captura deve identificar versão, cenário, controlador e mensagem técnica demonstrada.

### Apêndice C — Dados e reprodutibilidade

- esquema da base SQLite;
- exemplo de execução;
- métricas principais;
- manifestos e hashes;
- repositório, release e instruções de reprodução.

## PORTÕES ANTES DA REDAÇÃO INTEGRAL

- [ ] Confirmar as regras e o template oficial do CIACA 2027.
- [ ] Definir se o apêndice será suplementar ou incorporado apenas à versão final.
- [ ] Congelar autores, preservando anonimização na submissão.
- [ ] Executar ou retirar da seção de resultados qualquer afirmação quantitativa sobre v1dt.1.
- [ ] Definir instrumento para avaliação pedagógica ou limitar a conclusão à viabilidade e transferência.
- [ ] Calcular intervalos de confiança e comparações pareadas aplicáveis.
- [ ] Produzir as duas figuras em formato vetorial e legíveis em escala de cinza.
- [ ] Fixar uma release do pacote de reprodutibilidade citada no artigo.
