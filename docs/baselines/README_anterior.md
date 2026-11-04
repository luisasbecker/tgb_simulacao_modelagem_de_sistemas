# Trabalho do Grau B — Simulação e Modelagem de Sistemas

Repositório do grupo para organizar os modelos JaamSim, os experimentos e a documentação do Trabalho do Grau B (GB), dando continuidade ao trabalho do Grau A (GA).

## Objetivo

Simular o atendimento de clientes em um sistema com montagem de pedidos no balcão, tostagem e pagamento. O estudo compara cinco cenários para avaliar como a quantidade de atendentes e caixas, a probabilidade de tostagem e o comportamento dos clientes afetam filas, tempos de atendimento, utilização dos recursos e desistências.

A escolha do cenário recomendado deverá se apoiar nas novas simulações e nos indicadores com intervalos de confiança, considerando a capacidade de atendimento e os recursos necessários.

## Integrantes

Os nomes dos integrantes serão incluídos pelo grupo. As referências a **Pessoa 1** e **Pessoa 2** neste README identificam as frentes de implementação descritas abaixo.

## Status atual

**Referência: 30/10/2026.** Na inspeção do repositório, havia somente um README inicial. Os modelos `.cfg`, os scripts de teste, os resultados e o relatório ainda não estavam versionados.

O histórico de preparação do trabalho registra cinco modelos integrados e um pacote de ambiente online. Como esses arquivos ainda não estão neste repositório, os detalhes de implementação abaixo documentam o que foi relatado nessa preparação; sua conferência nos arquivos e a validação no JaamSim continuam pendentes.

| Frente | Situação |
| --- | --- |
| Configurações dos cenários e integração das Pessoas 1 e 2 | Implementação relatada nos arquivos preparados anteriormente; envio e conferência pendentes |
| Validação estática dos cinco modelos | Relatada como aprovada na preparação anterior; deve ser repetida com os arquivos versionados |
| Analisador de resultados | Teste com dados sintéticos relatado; ainda sem resultados reais dos modelos integrados |
| Execução real no JaamSim | Pendente para a versão integrada |
| GitHub Actions e Codespaces | Estrutura preparada em pacote anterior; ainda não instalada nem validada neste repositório |
| Atualização do relatório do GB | Pendente após a validação e o recálculo dos indicadores |

**Ainda não há resultados reais validados da versão integrada nem um cenário vencedor confirmado.**

## Evolução do GA para o GB

O modelo desenvolvido no GA é a referência para a continuidade do estudo. No GB, o trabalho passa a reunir a comparação de configurações de recursos, a diferenciação dos pedidos, a regra de desistência e a análise estatística das replicações.

As mudanças registradas na preparação do GB são:

- Comparação de cinco cenários, incluindo alternativas com dois caixas em paralelo.
- Três tipos de pedido, com probabilidades e tempos de montagem próprios.
- Decisão de desistência antes da entrada na fila do balcão.
- Contagem de clientes gerados, atendidos e desistentes.
- Controle para encerrar as chegadas aos 90 minutos e manter o atendimento até 150 minutos.
- Planejamento de 30 replicações por cenário, com médias e intervalos de confiança de 95%.
- Preparação de execução automatizada e verificações dos resultados.

Essa lista descreve a evolução consolidada relatada para o GB. A comparação detalhada com cada arquivo original do GA deverá ser confirmada quando as versões de referência forem adicionadas ao repositório.

## Cenários 1–5

| Cenário | Atendentes no balcão | Caixas | Com tostagem | Sem tostagem | Comparação proposta |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 2 | 1 | 55% | 45% | Referência entre os cinco cenários |
| 2 | 3 | 1 | 55% | 45% | Efeito de acrescentar um atendente ao balcão |
| 3 | 2 | 1 | 75% | 25% | Efeito de aumentar a proporção de pedidos tostados |
| 4 | 2 | 2 | 55% | 45% | Efeito de acrescentar um caixa |
| 5 | 3 | 2 | 55% | 45% | Efeito de ampliar balcão e pagamento |

Nos cenários 4 e 5, os dois caixas operam em paralelo e compartilham uma fila de pagamento, conforme a configuração relatada. Os tipos de pedido e a regra de desistência da Pessoa 2 se aplicam aos cinco cenários.

Parâmetros comuns previstos:

- **Chegadas:** durante os primeiros 90 minutos, até o limite de 5.400 segundos.
- **Duração de cada replicação:** 2,5 horas, ou 9.000 segundos.
- **Período adicional para concluir atendimentos:** 60 minutos após o encerramento das chegadas.
- **Replicações:** 30 por cenário, totalizando **150 execuções**.

Os 60 minutos adicionais precisam ser suficientes para esvaziar o sistema; isso deve ser verificado em cada replicação.

## Responsabilidades já implementadas na preparação

### Pessoa 1 — cenários e estrutura dos experimentos

Segundo o histórico da integração, foram mantidas as definições dos cenários 1, 2 e 3 e incorporadas as alternativas dos cenários 4 e 5, com dois caixas em paralelo. Também foram preservados:

- Quantidades de atendentes e caixas de cada cenário.
- Probabilidades de tostagem indicadas na tabela de cenários.
- Distribuições de tempo de tostagem e pagamento.
- Duração de 2,5 horas e 30 replicações por cenário.
- Estrutura existente de estatísticas e saída dos clientes atendidos.

Os parâmetros completos das distribuições preservadas deverão ser consultados nos `.cfg` originais quando forem versionados.

### Pessoa 2 — tipos de pedido, montagem e desistências

As alterações relatadas foram aplicadas aos cinco cenários, preservando a configuração de recursos da Pessoa 1.

| Tipo de pedido | Probabilidade | Montagem: mínimo | Montagem: moda | Montagem: máximo |
| --- | ---: | ---: | ---: | ---: |
| Simples | 40% | 45 s | 70 s | 110 s |
| Tradicional | 45% | 75 s | 110 s | 160 s |
| Complexo | 15% | 120 s | 170 s | 240 s |

Os tempos de montagem seguem distribuições triangulares. O tipo de pedido determina a distribuição usada para sortear o atributo `TempoMontagem`, que passa a ser o tempo de serviço dos balcões. A distribuição original `MontagemDist` permaneceu declarada nos arquivos preparados, mas deixou de ser utilizada pelos balcões.

A desistência é avaliada **na chegada, antes de entrar na fila do balcão**:

- Se `FilaBalcao.QueueLength > 5`, o cliente é registrado como desistente e sai do sistema.
- Se a fila contém até cinco clientes aguardando, o cliente segue para classificação do pedido e atendimento.

A regra considera quem está aguardando na fila; os clientes em atendimento não compõem esse limite. Ela não representa abandono depois de esperar algum tempo na fila.

Fluxo de entrada relatado:

```text
ChegadaClientes → DecisaoDesistencia
  ├─ fila > 5 → RegistroDesistencia → SaidaDesistencia
  └─ fila ≤ 5 → ClassificaPedido → SorteiaMontagem → FilaBalcao
               → montagem → decisão de tostagem → pagamento → saída
```

Também foram acrescentados o contador `TotalDesistencias` e os registros de desistentes e clientes gerados. O controle de chegadas foi corrigido na integração para respeitar os 90 minutos, mantendo a duração total definida pela Pessoa 1.

O mecanismo relatado usa `HorarioPico` com a condição `this.SimTime < 5400[s]` e `OperatingThresholdList` no gerador. **A interrupção efetiva das chegadas nesse instante ainda precisa ser comprovada por execução.**

Preservar as configurações da Pessoa 1 não preserva os resultados numéricos: os novos tempos e as desistências alteram o comportamento do sistema. Os resultados anteriores precisam ser recalculados para a versão integrada.

## Estrutura esperada do repositório

A árvore abaixo é uma proposta de organização para os arquivos que ainda serão enviados. Somente o `README.md` estava presente na inspeção; os demais caminhos não indicam arquivos já disponíveis.

```text
tgb_simulacao_modelagem_de_sistemas/
├── README.md
├── models/                         # Cinco arquivos .cfg integrados e dependências
├── scripts/
│   ├── download_jaamsim.sh          # Download da versão definida do simulador
│   ├── validate_cfg.py              # Conferência das configurações dos modelos
│   ├── run_all.sh                   # Execução dos cinco cenários
│   └── analyze_results.py           # Leitura dos resultados e cálculo dos indicadores
├── results/                        # Saídas reais .dat/.rep, logs e consolidações
├── docs/                           # Enunciado, referências do GA e documentação
├── relatorio/                      # Relatório do GB e sua versão final
├── .github/workflows/jaamsim.yml    # Automação prevista no GitHub Actions
└── .devcontainer/devcontainer.json # Configuração prevista para Codespaces
```

Os nomes dos scripts, do workflow e do arquivo de Codespaces correspondem ao pacote de ambiente online descrito na preparação anterior. Os nomes reais dos cinco `.cfg` e os argumentos dos scripts deverão ser conferidos ao importar o pacote.

Ao adicionar os arquivos, preservar os originais e suas dependências, identificar versões GA/GB e separar dados sintéticos de resultados reais. Mudanças nos modelos deverão ser registradas para permitir reproduzir os experimentos.

## Ferramenta e execução local

O [JaamSim](https://jaamsim.com/) é um simulador de eventos discretos baseado em Java. Os modelos são armazenados em arquivos de configuração `.cfg`.

A versão de referência escolhida na preparação foi o **JaamSim 2026-08**, disponível na [release oficial](https://github.com/jaamsim/jaamsim/releases/tag/v2026-08). O grupo deverá usar a mesma versão em todas as execuções e registrá-la no relatório.

### Pré-requisitos

1. Java compatível com a versão escolhida do JaamSim, acessível pelo comando `java -version`.
2. Arquivo `JaamSim2026-08.jar` obtido da release oficial.
3. Os cinco modelos integrados e todos os arquivos que eles referenciam.
4. Para os scripts do ambiente online: Python 3, suas dependências efetivas e Bash em Linux, Codespaces ou ambiente equivalente.

**O repositório ainda precisa receber os modelos antes que seja possível executar os experimentos.**

### Pela interface gráfica

1. Iniciar o JaamSim pelo executável ou pelo comando abaixo.
2. Abrir um dos arquivos `.cfg` integrados.
3. Conferir os recursos, as distribuições, as regras e os parâmetros de replicação.
4. Executar o modelo, verificar mensagens de erro e salvar as saídas.
5. Repetir para os cinco cenários.

```text
java -jar "JaamSim2026-08.jar"
```

### Sem interface gráfica

Após disponibilizar os modelos, usar o padrão abaixo, substituindo `ARQUIVO_DO_CENARIO.cfg` pelo nome real e ajustando os caminhos:

```text
java -jar "JaamSim2026-08.jar" "models/ARQUIVO_DO_CENARIO.cfg" -headless
```

O modo `-headless` inicia a execução em lote sem interface gráfica. A quantidade de replicações depende da configuração do modelo; o comando, sozinho, não estabelece 30 replicações. A sintaxe está documentada no [manual oficial, seção 2.6](https://jaamsim.com/docs/JaamSim%20User%20Manual%202021-04.pdf).

Executar cada cenário separadamente. Fornecer os cinco `.cfg` em um único comando carrega suas configurações em um mesmo modelo, em vez de iniciar cinco experimentos independentes.

As saídas `.dat` dependem de `RunOutputList`, e os relatórios `.rep`, da configuração de `PrintReport`. A pasta de saída depende de `ReportDirectory`; na ausência dessa definição, a documentação indica a pasta do modelo. Conferir essas opções antes de procurar os resultados em `results/`.

## Ambiente online e testes

O ambiente preparado anteriormente prevê GitHub Codespaces para execução interativa e GitHub Actions para automação. Para ativá-lo, ainda é necessário adicionar e revisar os modelos, scripts, dependências e arquivos de configuração.

Depois dessa importação:

1. Repetir a validação estática com `validate_cfg.py`, conforme seus argumentos reais.
2. No Codespaces, seguir o procedimento do pacote para baixar o JaamSim e executar `run_all.sh`.
3. No GitHub Actions, conferir os gatilhos definidos em `jaamsim.yml` e acompanhar a execução na aba **Actions**. Usar **Run workflow** se o arquivo oferecer execução manual.
4. Recuperar logs e resultados pelo mecanismo efetivamente definido no workflow.
5. Analisar somente os arquivos produzidos pelas execuções reais da versão integrada.

O teste anterior com um `.dat` sintético verificou o analisador, conforme relatado no histórico. Esse teste não comprova que os modelos funcionam no JaamSim nem substitui as 150 execuções.

### Critérios de validação

- Confirmar as configurações dos cinco cenários, as 30 replicações e os 9.000 segundos por replicação.
- Conferir as probabilidades 40%/45%/15%, os parâmetros triangulares e o uso de `TempoMontagem` em todos os balcões.
- Verificar a regra nos limites de fila 5 e 6 e o reinício dos contadores em cada replicação.
- Comprovar que nenhuma chegada ocorre a partir do limite de 5.400 segundos.
- Verificar se há exatamente 30 registros de replicações por cenário, sem contar cabeçalhos ou linhas de resumo como replicações.
- Conferir erros, unidades dos indicadores e conservação dos clientes em cada replicação.

Para um sistema inicialmente vazio, o balanço esperado é:

```text
clientes gerados − clientes atendidos − clientes desistentes = clientes remanescentes
```

O remanescente deve corresponder aos clientes ainda no sistema e, para confirmar o esvaziamento ao final, deve ser **zero**. Se isso não ocorrer, registrar a limitação e revisar o encerramento antes de concluir a comparação.

## Indicadores e análise dos resultados

| Indicador | Uso na comparação |
| --- | --- |
| Clientes gerados | Total de chegadas em cada replicação |
| Clientes atendidos | Total de clientes que concluíram o fluxo e o pagamento |
| Clientes desistentes | Total desviado pela regra de fila do balcão |
| Taxa de desistência | Desistentes / gerados × 100%; tratar separadamente replicações sem chegadas |
| Tempo de espera | Espera nas filas do balcão e do pagamento, com unidade explícita |
| Comprimento das filas | Comprimento médio e máximo por fila |
| Tempo total no sistema (lead time) | Tempo da chegada até a saída dos clientes atendidos |
| Utilização dos recursos | Ocupação de cada atendente, equipamento de tostagem e caixa disponível no modelo |
| Clientes remanescentes | Conferência do esvaziamento e do balanço de clientes |

Essa tabela define o conjunto esperado para análise; sua disponibilidade precisa ser conferida nas saídas dos modelos. Informar também se a utilização e os indicadores de fila foram medidos nos 90 minutos de chegadas ou em toda a janela de 150 minutos.

Calcular os indicadores de cada replicação e consolidá-los por cenário. Para médias de 30 replicações independentes, usar o intervalo de confiança de 95% com a distribuição t de Student:

```text
IC95% = média ± t(0,975; 29) × desvio-padrão amostral / √30
```

Registrar as sementes ou subfluxos aleatórios, as unidades e a versão dos modelos. Não tratar clientes de uma mesma replicação como replicações independentes. Para comparar cenários, documentar se foram usadas replicações independentes ou pareadas.

Uma redução de espera pode acompanhar um aumento de desistências; por isso, avaliar conjuntamente tempos, atendimento concluído, perdas e utilização. A recomendação deverá explicitar também a quantidade de recursos necessária.

## Entregáveis do GB

- Cinco modelos JaamSim integrados, identificados por cenário e com suas dependências.
- Documentação das premissas, distribuições, regras e diferenças em relação ao GA.
- Evidências da validação e das 30 replicações de cada cenário.
- Arquivos de saída reais e logs que permitam conferir os resultados.
- Tabelas e gráficos comparativos com médias, unidades e IC95%.
- Relatório atualizado do GB, com metodologia, resultados recalculados, limitações e conclusão.
- Ambiente de execução e análise reproduzível, acompanhado deste README.

Os requisitos formais de entrega deverão ser conferidos com o enunciado da disciplina quando ele estiver disponível no repositório.

## Próximos passos

1. Adicionar os cinco `.cfg` integrados e o pacote de ambiente online, preservando os arquivos de referência.
2. Conferir a correspondência entre este README, o enunciado e os modelos efetivamente enviados.
3. Validar o funcionamento no JaamSim, especialmente a parada das chegadas e os contadores de desistência.
4. Executar os cinco cenários com 30 replicações e conferir o balanço dos clientes.
5. Consolidar os indicadores e atualizar o relatório do GB com os resultados da versão integrada.
