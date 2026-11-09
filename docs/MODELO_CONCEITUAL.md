# Modelo conceitual e contrato de integração

## Entidade, fluxo e fronteira

A entidade é o cliente/pedido. Cada pedido tem uma QuantidadeLanches (1, 2 ou 3 sanduíches); a chegada é registrada antes de qualquer fila. Há duplicação das entidades de produção e reunião dos lanches antes do pagamento: o pedido entra uma vez, é produzido em vários lanches em paralelo e volta a ser um só para pagar.

```mermaid
flowchart TD
  A["Chegada em 0 ≤ t < 5400 s"] --> B["Sorteia TipoPedido, QuantidadeLanches, ClienteID e tempo de montagem"]
  B --> C{"Mais de 5 lanches aguardando no balcão?"}
  C -->|Sim| D["Contar desistência e sair (não gera lanches)"]
  C -->|Não| E["Duplicar: gera QuantidadeLanches lanches do pedido"]
  E --> F["Fila única do balcão"]
  F --> G["2 ou 3 balcões em paralelo (montagem por lanche)"]
  G --> H["FilaReuniao: espera o lote do pedido (sem recurso ocupado)"]
  H --> I["Combine: reúne os lanches pelo ClienteID em um só pedido"]
  I --> J{"Precisa tostar?"}
  J -->|55% ou 75%| K["Fila e tostadeira"]
  J -->|45% ou 25%| L["Fila única do caixa"]
  K --> L
  L --> M["1 ou 2 caixas em paralelo"]
  M --> N["Medir lead time e sair"]
```

O balcão é liberado antes da tostagem; não há bloqueio entre etapas. Os dois caixas dos cenários 4/5 retiram pedidos da mesma FilaCaixa. A decisão condicional é imediata, sem abandono posterior de quem já entrou na fila, e é avaliada uma única vez por cliente, antes da duplicação. Entidades em serviço não são contadas em QueueLength. Após a reunião há um pedido por cliente: tostagem, pagamento, lead time e atendimento são medidos uma vez por pedido, nunca por lanche.

## Distribuições e justificativas

| Variável | Distribuição | Parâmetros | Stream |
|---|---|---|---:|
| Intervalo de chegada | Exponencial | média 90 s | 1 |
| TipoPedido | Discreta | 1:40%; 2:45%; 3:15% | 9 |
| QuantidadeLanches | Discreta | 1:70%; 2:22%; 3:8% | 13 |
| Montagem simples | Triangular | mínimo 45 s; moda 70 s; máximo 110 s | 10 |
| Montagem tradicional | Triangular | mínimo 75 s; moda 110 s; máximo 160 s | 11 |
| Montagem complexa | Triangular | mínimo 120 s; moda 170 s; máximo 240 s | 12 |
| Tostagem | Triangular | mínimo 20 s; moda 30 s; máximo 45 s | 3 |
| Pagamento | Triangular | mínimo 18 s; moda 38 s; máximo 95 s | 4 |
| Rota de tostagem | Discreta | 55/45% ou 75/25% | 5 |

As distribuições originais são premissas sintéticas de projeto, documentadas na aba Fontes da planilha do GA; os parâmetros da aba Resumo não foram ajustados novamente nem usados para substituir a base. A exponencial representa intervalos independentes; a triangular representa uma duração limitada com mínimo, valor mais provável e máximo. Os três tipos e suas probabilidades são decisões de modelagem fornecidas para a Pessoa 2, não estimativas empíricas extraídas de clientes reais. A média teórica da mistura de montagem é 108,25 s, frente a 121,67 s na distribuição única anterior.

Preserva-se uma chegada em t=0 (`FirstArrivalTime=0`), seguida de intervalos EXPO(90 s). Portanto o número esperado antes de 5400 s é aproximadamente 61 (1 + 5400/90), e não se deve descrever a primeira chegada como exponencial. O sistema inicia vazio imediatamente antes dessa primeira chegada.

## Atributos e indicadores

TipoPedido é definido exatamente uma vez na chegada, inclusive para clientes que depois desistem. O ternário de SorteiaMontagem consulta somente a distribuição correspondente. TempoMontagem armazena uma duração única que todos os balcões usam em ServiceTime; não há novo sorteio pelo servidor. HoraChegada nunca é reiniciada. FilaNaChegada registra uma fotografia da fila antes da decisão.

TotalDesistencias é um CustomOutput numérico de Simulation que lê SaidaDesistencia.NumberAdded. Usar o contador nativo do destino evita um contador manual divergente e garante reinício por replicação. Lead time é `SimTime - HoraChegada`, coletado em EstatSistema depois do pagamento, somente na rota dos atendidos. Os logs verificam a decomposição em esperas e serviços.

ClientesAindaNoSistema é uma medida independente: soma das três filas e NumberInProgress de todos os balcões, da tostadeira e dos caixas. Não se usa apenas gerados menos saídas para afirmar conservação; o balanço é comparado com a ocupação medida. O intervalo pendente do gerador após o fechamento não é um cliente criado e não entra no estoque.

| Indicador | Unidade e medição | Meta ou papel |
|---|---|---|
| Espera média no balcão (principal) | segundos, entrada em FilaBalcao até início da montagem | média inferior a 300 s; comparar redução C2/C1 |
| TotalDesistencias | clientes, chegadas desviadas diretamente à saída própria | acompanhar perdas; menor é preferível, sem inventar meta numérica adicional |
| Lead time | segundos, criação do cliente até conclusão do pagamento | comparar serviço completo, somente atendidos |
| P90 do lead time | segundos, percentil empírico por replicação, interpolação linear | avaliar a cauda; resumir os 30 P90s |
| Vazão | clientes/h, atendidos ÷ 2,5 h | janela completa; exportação adicional divide por 1,5 h e é rotulada separadamente |

Utilizações e comprimentos médios são integrais no intervalo [0,9000] s. A diluição pela hora final ociosa é esperada. As esperas são médias dos clientes que passaram por cada fila. O esvaziamento observado permite relacionar a área de fila com a soma das esperas sem censura final.

## Sementes e comparação

RandomSeed identifica streams distintos. GlobalSubstreamSeed permanece no padrão do JaamSim: número da replicação, de 1 a 30. Entre cenários, a auditoria confirmou os mesmos instantes de chegada, tipos e tempos sorteados para cada cliente de mesma posição na replicação. Tostagem e pagamento consomem seus streams conforme a ordem dos serviços; não se presume pareamento perfeito desses serviços por identidade do cliente.

As 30 replicações, e não os clientes individuais, são a unidade para IC das médias. O principal é comum aos cinco cenários (Wq balcão); W é complementar. Usa-se t(0,975;29) × s/√30. ICs não sobrepostos indicam diferença segundo a disciplina; ICs sobrepostos não autorizam concluir diferença pela inspeção. O IC pareado da diferença é apresentado separadamente, sem ajuste de comparações múltiplas, como complemento exploratório.

## Contrato para a Pessoa 3

1. Manter o cliente como proprietário do pedido, do TipoPedido e da HoraChegada.
2. Cada item criado no futuro recebe o TipoPedido do cliente; não sortear complexidade independente para sanduíches.
3. Se houver tempos por item, cada item pode sortear sua duração na distribuição correspondente ao tipo herdado; não confundir igualdade de classificação com obrigação de durações idênticas.
4. Avaliar desistência uma vez, antes de criar itens; cliente desistente não gera lanches nem chega ao caixa.
5. Após a futura reunião dos itens, registrar pagamento/lead time e atendimento uma vez por cliente. Não contar itens como clientes no balanço.
6. Preservar identidade do cliente, tempo inicial e streams documentados; ampliar a auditoria para relacionar itens e pedidos.
7. Reexecutar as 150 replicações após essa integração. Estes resultados são válidos para Pessoa 1 + Pessoa 2, antes da Pessoa 3.

Os servidores em paralelo existentes são preservados. A adequação do requisito específico de lotes/duplicações à solução da Pessoa 3 continua a cargo dessa etapa.

## Implementação da Pessoa 3 (pedidos múltiplos, duplicação e reunião)

A camada da Pessoa 3 está no gerador `scripts/build_models.py` e aparece nos cinco `models/cenarioN.cfg`. Ela cumpre o contrato acima item a item.

### Atributo QuantidadeLanches

`QuantidadeLanches` é sorteado uma vez por cliente em `ClassificaPedido`, por `QtdLanchesDist` (stream 13, 1:70%; 2:22%; 3:8%), inclusive para quem depois desiste. A média da mistura é 1,38 lanche por pedido. As probabilidades são premissas sintéticas de projeto, no mesmo espírito de TipoPedido: a maioria dos pedidos tem um sanduíche, uma parcela menor dois e poucos três. `ClienteID` recebe `[ChegadaClientes].NumberGenerated`, identificando o pedido para o casamento na reunião. Ambos os atributos, e as distribuições, são declarados antes de `ClassificaPedido`, para que a unidade (DimensionlessUnit) já esteja resolvida quando o atributo é usado.

### Duplicação das entidades de produção

Quem entra (decisão de desistência avaliada antes, uma vez) vai ao `Duplicate` `DuplicaLanches`, que gera `QuantidadeLanches - 1` cópias; original e cópias representam os lanches do pedido e seguem todos para a `FilaBalcao`. Cada lanche é montado por um balcão (`ServiceTime = TempoMontagem`), de modo que mais lanches ocupam mais os 2 ou 3 balcões — a duplicação respeita a capacidade instalada, sem criar servidores novos. As cópias herdam automaticamente `TipoPedido`, `ClienteID`, `HoraChegada` e `TempoMontagem` do pedido; nenhuma complexidade independente é sorteada por lanche.

### Reunião antes do pagamento

A `FilaReuniao` agrupa os lanches por `Match { this.obj.ClienteID }`. O `Combine` `ReuneLanches` usa uma única fila de espera com `MatchRequired { TRUE }` e `NumberRequired { [FilaReuniao].QueueLength > 0 ? [FilaReuniao].QueueList(1).QuantidadeLanches : 1 }`: ele exige exatamente a quantidade de lanches do pedido que está à frente da fila e devolve **uma** entidade por pedido — a própria entidade-cliente, que conserva `HoraChegada` e `TipoPedido`; as cópias são consumidas. Assim, pagamento, lead time e atendimento são medidos uma vez por cliente, nunca por lanche. O `Pack`/`EntityContainer` foi testado e descartado para a reunião por cliente: ele agrupa pela ordem da fila, ignorando o `Match`, e misturaria lanches de clientes diferentes na mesma bandeja; o `Combine` com `MatchRequired` é o objeto correto para reunir itens de um mesmo pedido.

A espera na `FilaReuniao` é a "espera do lote" da Aula 14: tempo parado que não ocupa recurso nenhum, medido por `[FilaReuniao].AverageQueueTime` (indicador `EsperaReuniao_s`). A reunião é FIFO por pedido: o pedido à frente só sai quando todos os seus lanches chegam, o que pode fazer um pedido completo esperar o pedido da frente — exatamente a espera sem recurso que a aula discute.

### Balanços e indicadores

O balanço de pedidos usa o gerador e as saídas: `ClientesAindaNoSistema = ClientesGerados - ClientesAtendidos - TotalDesistencias`, que vai a zero com o sistema vazio. O balanço de itens usa os balcões e a reunião: `SanduichesNoSistema` soma `FilaBalcao`, os balcões em serviço e a `FilaReuniao`; `SanduichesMontados` é a soma de `NumberProcessed` dos balcões; `PedidosReunidos = [ReuneLanches].NumberProcessed`. Não se conta lanche como cliente. Como a `FilaBalcao` passou a conter lanches, a desistência (`FilaBalcao.QueueLength > 5`) e a espera média no balcão passam a ser medidas em lanches, e não em clientes — mudança a destacar na releitura dos indicadores.

### Verificação e próximos passos

Os cinco cenários foram regenerados e executados headless (1 replicação cada) sem erros, com conservação confirmada: zero lanches e zero pedidos remanescentes, `ClientesGerados = ClientesAtendidos + TotalDesistencias` e `PedidosReunidos = ClientesAtendidos`. A reexecução das 150 replicações, o recálculo das médias/IC95% e os gráficos finais (fila em degraus e lead time com barras de erro) são da Pessoa 4; os resultados em `results/` ainda refletem Pessoa 1 + Pessoa 2 e devem ser refeitos após esta integração.

### Animação

A cena de cada cenário tem título do cenário, relógio da simulação, indicadores em texto com unidade (atendidos em pedidos, desistências em clientes, lead time médio em s, fila do balcão e lanches montados em lanches, espera de reunião em s) e o gráfico de estado em tempo real `GraficoFila`, com eixos rotulados, mostrando em degraus os lanches aguardando montagem e os lanches em reunião. Os objetos `DuplicaLanches`, `FilaReuniao` e `ReuneLanches` têm posição na cena para que o novo fluxo seja visível durante a rodada.
