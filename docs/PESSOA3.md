# Pessoa 3 — Lotes, duplicações e animação

Este documento resume o que a Pessoa 3 implementou no modelo do TGB, **e por que cada decisão foi tomada**. A responsabilidade da Pessoa 3, conforme a divisão do grupo, é o processamento de pedidos múltiplos e a visualização: atributo `QuantidadeLanches`, duplicação das entidades de produção e sua reunião antes do pagamento, atualização do diagrama conceitual e a animação do modelo.

## Visão geral

Até a Pessoa 2, cada cliente era uma única entidade com um lanche. A Pessoa 3 passou a tratar o pedido como podendo ter mais de um sanduíche: o pedido entra uma vez, é produzido em vários lanches em paralelo nos balcões e volta a ser um só pedido antes de pagar. Isso cumpre o requisito "e) Lotes ou duplicações" do enunciado (ao menos um agrupamento, montagem ou fluxo paralelo coerente com o sistema) e acrescenta um segundo atributo com significado (`QuantidadeLanches`), empregado em rota, tempo e indicador.

Toda a mudança está no gerador único [`scripts/build_models.py`](../scripts/build_models.py); os cinco arquivos `models/cenarioN.cfg` são regenerados a partir dele. Trabalhar no gerador, e não editando cinco `.cfg` à mão, garante que os cenários fiquem consistentes entre si e preserva a parametrização de balcões (2 ou 3) e caixas (1 ou 2) por cenário que a Pessoa 1 já tinha.

## O que foi feito, e por quê

### 1. Atributo `QuantidadeLanches`

**O que:** cada cliente sorteia `QuantidadeLanches` (1, 2 ou 3 sanduíches) uma única vez em `ClassificaPedido`, pela distribuição discreta `QtdLanchesDist` (stream 13; `1:70%`, `2:22%`, `3:8%`; média de 1,38 lanche por pedido). Foi acrescentado também o atributo `ClienteID = [ChegadaClientes].NumberGenerated`.

**Por quê:**

- O enunciado pede um atributo com significado empregado em rota, tempo ou indicador. `QuantidadeLanches` governa quantas entidades de produção o pedido gera (rota), quanta carga vai aos balcões (tempo) e entra nos indicadores de itens.
- O sorteio é feito uma vez e antes de qualquer duplicação porque o contrato da Pessoa 2 para a Pessoa 3 exige avaliar a desistência uma vez e preservar a identidade do pedido; sortear por lanche quebraria a identidade.
- As probabilidades são premissas sintéticas de projeto, no mesmo espírito de `TipoPedido`: a maioria dos pedidos tem um sanduíche, uma parte menor dois e poucos três. Não são medições de clientes reais, e isso está declarado no modelo conceitual.
- `ClienteID` é necessário para o casamento na reunião (ver item 3): ele identifica a qual pedido cada lanche pertence. Usar `NumberGenerated` dá um número único e crescente por cliente, e as cópias herdam esse valor automaticamente.

### 2. Duplicação das entidades de produção

**O que:** quem passa pela decisão de desistência vai ao objeto `Duplicate` `DuplicaLanches`, que cria `QuantidadeLanches - 1` cópias. O original e as cópias representam os lanches do pedido e seguem todos para a `FilaBalcao`; cada lanche é montado por um balcão (`ServiceTime = this.obj.TempoMontagem`).

**Por quê:**

- É a tradução direta de "duplicação das entidades de produção". O `Duplicate` é o objeto que a Aula 14 ensina para "uma entidade torna-se duas" e abre caminhos paralelos.
- Fazer os lanches competirem pelos mesmos 2 ou 3 balcões é o que significa "respeitando a capacidade dos recursos": um pedido de três lanches ocupa os balcões três vezes mais do que um de um lanche, sem que nenhum servidor novo seja criado.
- As cópias herdam `TipoPedido`, `ClienteID`, `HoraChegada` e `TempoMontagem` automaticamente, o que atende ao contrato (cada item recebe o `TipoPedido` do cliente; não se sorteia complexidade independente por lanche).

### 3. Reunião antes do pagamento

**O que:** os lanches montados vão à `FilaReuniao`, que agrupa por `Match { this.obj.ClienteID }`. O objeto `Combine` `ReuneLanches` usa essa fila única com `MatchRequired { TRUE }` e `NumberRequired { [FilaReuniao].QueueLength > 0 ? [FilaReuniao].QueueList(1).QuantidadeLanches : 1 }`. Ele exige exatamente a quantidade de lanches do pedido que está à frente da fila e devolve **uma** entidade por pedido — a própria entidade-cliente, que conserva `HoraChegada` e `TipoPedido`; as cópias são consumidas. A entidade reunida segue para tostagem, caixa, medição de lead time e saída.

**Por quê:**

- O contrato exige registrar pagamento, lead time e atendimento uma vez por cliente, e não contar itens como clientes. O `Combine` devolver uma única entidade por pedido é exatamente isso.
- Preservar a entidade-cliente (em vez de criar um objeto novo) mantém `HoraChegada` e `TipoPedido` sem truques, então a medição de lead time (`this.SimTime - this.obj.HoraChegada`) continua idêntica à da Pessoa 2.
- `NumberRequired` é uma expressão porque a quantidade de lanches varia por pedido. Como todos os lanches de um pedido compartilham `QuantidadeLanches`, basta ler esse valor do pedido líder da fila.
- A espera na `FilaReuniao` é, de propósito, a "espera do lote" da Aula 14: tempo parado que não ocupa recurso nenhum. Ela é medida pelo indicador `EsperaReuniao_s` e ilustra a lição da aula de que a maior espera do modelo pode estar justamente onde nenhum recurso está ocupado.

**Por que não `Pack`/`EntityContainer`:** a primeira tentativa foi reunir os lanches em uma bandeja (`Pack`). Em teste no próprio JaamSim, o `Pack` empacota os primeiros `NumberOfEntities` da fila **na ordem**, ignorando o `Match` — ou seja, misturaria lanches de clientes diferentes na mesma bandeja, com lead time e identidade errados. O `Combine` com `MatchRequired` é o objeto correto para reunir itens de um mesmo pedido, e foi o escolhido.

### 4. Diagrama conceitual

**O que:** o [modelo conceitual](MODELO_CONCEITUAL.md) foi atualizado — fluxograma mermaid refeito com os passos de duplicação e reunião, nova linha de `QuantidadeLanches` na tabela de distribuições e uma seção "Implementação da Pessoa 3" descrevendo o fluxo, os balanços e a animação.

**Por quê:** a divisão pede explicitamente "atualizar o diagrama conceitual com os novos fluxos". Sem isso, o diagrama ainda diria que não há duplicação de sanduíches, contradizendo o modelo.

### 5. Animação

**O que:** a cena de cada cenário tem:

- título do cenário e relógio da simulação (preservados da base);
- indicadores em texto, cada um com a sua unidade: atendidos (pedidos), desistências (clientes), lead time médio (s), fila do balcão (lanches), lanches montados (lanches) e espera de reunião (s);
- `GraficoFila`, gráfico de estado em tempo real, em degraus, com eixos rotulados e duas séries: lanches aguardando no balcão e lanches em reunião;
- posições de cena para `DuplicaLanches`, `FilaReuniao` e `ReuneLanches`, para o novo fluxo ficar visível durante a rodada.

**Por quê:** o requisito "f) Demonstração visual" e a divisão pedem título, relógio, ao menos três indicadores com unidade e um gráfico de estado em tempo real. Acrescentar a série da reunião ao gráfico torna visível justamente a espera do lote introduzida pela Pessoa 3.

## Balanços e efeito nos indicadores

Como a `FilaBalcao` passou a conter **lanches** e não clientes, os balanços foram separados:

| Nível | Indicadores | Como se lê |
|---|---|---|
| Pedido (ordem) | `ClientesGerados`, `ClientesAtendidos`, `TotalDesistencias`, `ClientesAindaNoSistema`, `PedidosReunidos`, `PedidosNoPagamento` | `ClientesAindaNoSistema = ClientesGerados - ClientesAtendidos - TotalDesistencias`, vai a zero com o sistema vazio |
| Item (lanche) | `SanduichesMontados`, `SanduichesNoSistema` | `SanduichesNoSistema` soma `FilaBalcao`, balcões em serviço e `FilaReuniao`; vai a zero quando tudo é reunido |

Dois efeitos colaterais, declarados no modelo conceitual para a releitura dos indicadores:

- a desistência (`[FilaBalcao].QueueLength > 5`) passa a disparar com mais de cinco **lanches** aguardando, e não cinco clientes;
- a espera média no balcão passa a ser média por lanche, e não por cliente.

A reconciliação desses indicadores e a reexecução estatística são da Pessoa 4.

## Verificação

- **Validação estática** ([`scripts/validate_cfg.py`](../scripts/validate_cfg.py), atualizado com o contrato da Pessoa 3): os cinco cenários passam.
- **Testes de runtime no motor** ([`tests/test_runtime.py`](../tests/test_runtime.py)): os sete testes passam. Os fixtures que verificam a desistência e a conservação por cliente foram fixados em `QuantidadeLanches = 1` (via `QtdLanchesDist ProbabilityList { 1 0 0 }`) para isolar o comportamento que testam; foi acrescentado o teste `pessoa3_reuniao`, que força dois lanches por pedido e confirma 5 pedidos → 10 lanches montados, todos reunidos, zero remanescente.
- **Execução headless dos cinco cenários** (1 replicação cada): sem erros, com `ClientesGerados = ClientesAtendidos + TotalDesistencias`, `PedidosReunidos = ClientesAtendidos` e `SanduichesNoSistema = 0`.

## Decisões de ferramenta descobertas por teste no JaamSim 2026-08

- O objeto `Batch` não existe nesta versão; a reunião de um número **variável** de itens por pedido só funciona com `Combine` em fila única, `MatchRequired`, `Match` na fila e `NumberRequired` por expressão.
- A distribuição `QtdLanchesDist` precisa ser declarada **antes** de `ClassificaPedido`. Se declarada depois, a unidade do valor resolve como `UserSpecifiedUnit` e o modelo dá erro de runtime na atribuição do atributo (que espera `DimensionlessUnit`). Por isso ela é emitida junto de `TipoPedidoDist`, e não no bloco posterior da Pessoa 3.

## Fora do escopo da Pessoa 3

- Reexecução das 150 replicações, recálculo de médias e IC95% e os gráficos finais (fila em degraus e lead time com barras de erro) são da Pessoa 4; `results/` ainda reflete Pessoa 1 + Pessoa 2 e deve ser refeito após esta integração.
- A revisão visual da animação e a gravação do vídeo MP4 de até um minuto continuam pendentes.

## Arquivos alterados

| Arquivo | Mudança |
|---|---|
| `scripts/build_models.py` | camada da Pessoa 3: `QuantidadeLanches`, `ClienteID`, `Duplicate`, `Combine`, balanços e animação |
| `models/cenario1.cfg` a `cenario5.cfg` | regenerados a partir do gerador |
| `docs/MODELO_CONCEITUAL.md` | diagrama e seção da Pessoa 3 |
| `scripts/validate_cfg.py` | contrato estático atualizado para o novo fluxo |
| `tests/test_runtime.py` | fixtures ajustados e teste `pessoa3_reuniao` |
| `README.md` | status da Pessoa 3 |
