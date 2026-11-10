# Pessoa 4 — Indicadores, experimentação e análise estatística

Este documento resume o que a Pessoa 4 implementou e por quê. A responsabilidade, conforme a divisão do grupo, é a medição e comparação dos resultados: configurar os indicadores de lead time, desistências, vazão e tamanho da fila; preparar a extração das 30 replicações por cenário; calcular médias, IC95% e comparações entre cenários; produzir os dois gráficos obrigatórios.

## 1. Indicadores configurados no modelo

Todas as mudanças estão no gerador [`scripts/build_models.py`](../scripts/build_models.py); os cinco `models/cenarioN.cfg` foram regenerados.

| Indicador | Definição | Unidade | Onde |
|---|---|---|---|
| Lead time do pedido (obrigatório pelo enunciado) | da chegada (`HoraChegada`) ao fim do pagamento, por pedido; exclui desistentes | s | `LeadTime_medio_s`, `LeadTime_dp_s`, `LeadTime_max_s` (novos: DP e máximo) |
| P90 do lead time | percentil 90 dentro de cada replicação, calculado a partir de `LogAtendidos` | s | análise Python |
| Desistências (contagem específica) | clientes que encontram mais de cinco lanches aguardando no balcão | clientes/replicação | `TotalDesistencias`; `TaxaDesistencia` na análise |
| Vazão | pedidos atendidos e lanches montados por hora na janela de 2,5 h | pedidos/h, lanches/h | `Vazao_h`, `VazaoLanches_h` (novo) |
| Tamanho da fila | fila do balcão (média ponderada no tempo e máximo), fila do caixa, fila de reunião | lanches / pedidos | `FilaBalcao_media`, `FilaBalcao_max`, `FilaCaixa_media`, `FilaReuniao_media` |

Também foram acrescentados:

- `ClienteID` e `QuantidadeLanches` em todos os registros de pedido (`LogChegadas`, `LogDesistencias`, `LogMontagem`, `LogAtendidos`);
- o estado `EsperaReuniao` em `LogAtendidos`, para que a soma dos estados feche exatamente o lead time;
- um novo registro por lanche, `LogLanches` (objeto `EntityLogger`, tempo zero), entre os balcões e a `FilaReuniao`. Ele permite auditar a duplicação e a reunião item a item.

Nenhuma distribuição, semente, rota ou capacidade foi alterada: o `LogLanches` só registra. A validação estática ([`scripts/validate_cfg.py`](../scripts/validate_cfg.py)) continua garantindo os parâmetros das Pessoas 1 a 3.

## 2. Descoberta na integração: o Combine nem sempre devolve o cliente original

O registro por lanche mostrou que o `Combine` devolve a **primeira entidade da fila de reunião**, que muitas vezes é uma cópia (`Cliente5_Dup1`), e não a entidade original. Isso não altera os resultados, porque as cópias herdam todos os atributos (`ClienteID`, `HoraChegada`, `TipoPedido`, `QuantidadeLanches`) e o lead time continua sendo um por pedido. Porém, a auditoria antiga identificava clientes pelo nome da entidade e falharia. A identidade passou a ser `ClienteID` em toda a análise. Nas 150 replicações, a quantidade de pedidos entregues por uma cópia está em `results/validation_summary.json` (`pedidos_entregues_pela_copia`).

## 3. Extração e auditoria das replicações

[`scripts/analyze_results.py`](../scripts/analyze_results.py) foi reescrito. Para cada uma das 150 replicações, ele confere, entre outros:

- balanço de pedidos (gerados = atendidos + desistentes + remanescentes) e de lanches (montados = soma de `QuantidadeLanches` dos atendidos);
- **reunião correta**: cada pedido sai do `Combine` uma única vez, com exatamente `QuantidadeLanches` lanches do próprio `ClienteID`, e só depois do último lanche montado;
- herança de atributos por todos os lanches e tempo de montagem igual a `TempoMontagem`;
- lead time = soma dos estados (montagem, esperas no balcão, reunião, tostagem, caixa e pagamento);
- espera no balcão e utilizações reconstruídas pelos registros individuais;
- áreas das filas (balcão, caixa, reunião) recalculadas a partir do registro de estado por evento;
- desistência coerente com a regra `FilaBalcao.QueueLength > 5`;
- números aleatórios comuns: chegadas, tipos e quantidades idênticos nos cinco cenários;
- testes de aderência das entradas (qui-quadrado para `TipoPedido` e `QuantidadeLanches`; KS para as montagens).

## 4. Estatística

- IC95% t de Student com 29 graus de liberdade sobre as 30 médias de replicação, para todos os indicadores (`results/resumo_ic95.csv`).
- Comparação dos 10 pares de cenários em lead time, P90, espera no balcão, espera no caixa, fila do balcão, desistências e vazão (`results/comparacoes_ic95.csv`), com: variação percentual, **critério da disciplina** (sobreposição de ICs) e, como complemento, IC t pareado da diferença (válido pelas sementes comuns).
- Respostas automáticas às cinco perguntas do estudo (`results/respostas_perguntas.csv`).
- Tabela descritiva de lead time por tamanho do pedido (`results/lead_time_por_tamanho.csv`).

## 5. Gráficos obrigatórios

[`scripts/plot_results.py`](../scripts/plot_results.py) gera PNG e SVG em `results/figures/`:

- `espera_balcao_ic95` — espera média no balcão por cenário, barras com IC95% como barras de erro (indicador principal, conforme o relatório);
- `lead_time_ic95` — lead time médio por cenário, mesmo formato (indicador obrigatório, pedido na divisão do grupo);
- `fila_balcao_degraus` — evolução da fila do balcão em degraus, com tempos exatos de evento, cenário 1 contra cenário 2 na mesma replicação (mesmas chegadas). A replicação é escolhida automaticamente: a de mais desistências no cenário 1, para mostrar a decisão condicional no limite de cinco lanches;
- extra: `desistencias_ic95`.

Todos têm título, eixos rotulados, unidades e nota sobre o IC. Cores: par categórico validado para daltonismo.

## 6. Resultados principais

| Indicador | C1 | C2 | C3 | C4 | C5 |
|---|---:|---:|---:|---:|---:|
| Lead time (s) | 305.99 ± 13.11 | 239.68 ± 8.26 | 312.37 ± 13.22 | 292.50 ± 12.48 | 217.21 ± 6.72 |
| Espera no balcão (s/lanche) | 109.59 ± 11.50 | 34.66 ± 6.21 | 109.59 ± 11.50 | 109.59 ± 11.50 | 34.66 ± 6.21 |
| Desistências (clientes/replicação) | 3.43 ± 1.09 | 0.53 ± 0.32 | 3.43 ± 1.09 | 3.43 ± 1.09 | 0.53 ± 0.32 |

| Pergunta | Resposta |
|---:|---|
| 1 | sim: espera no balcão em C1 = 109.59 s, IC95% [98.09; 121.10] s, abaixo de 300 s |
| 2 | sim: redução de 68.4% (109.59 para 34.66 s), ICs separados |
| 3 | não: lead time +2.1% (305.99 para 312.37 s), ICs sobrepostos |
| 4 | não conclusivo: lead time −4.4% (305.99 para 292.50 s), ICs sobrepostos |
| 5 | sim: caixa 23.58 para 1.11 s e lead time 239.68 para 217.21 s, ambos conclusivos; balcão inalterado |

Mudanças em relação à versão Pessoa 2, explicadas pela duplicação: a fila e a espera do balcão agora contam lanches (1,38 por pedido), então a espera no balcão subiu e as desistências passaram de 3 para 103 em C1 (30 replicações), já que o limite de cinco é atingido mais cedo.

## 7. Reproduzir

```bash
python3 scripts/validate_cfg.py
python3 tests/test_runtime.py
python3 scripts/run_all.py --output results/reexecutions/minha_execucao/runs
python3 scripts/plot_results.py results/reexecutions/minha_execucao
```

A reexecução feita para esta entrega reproduziu `results/resumo_ic95.csv` byte a byte.

## Arquivos alterados

| Arquivo | Mudança |
|---|---|
| `scripts/build_models.py` | `LogLanches`, `ClienteID`/`QuantidadeLanches`/`EsperaReuniao` nos registros, `LeadTime_dp_s`, `LeadTime_max_s`, `VazaoLanches_h` |
| `models/cenario1.cfg` a `cenario5.cfg` | regenerados |
| `scripts/run_model.py` | lista única de registros (`LOGS`), incluindo `LogLanches` |
| `scripts/validate_cfg.py` | contrato estático com o registro por lanche |
| `scripts/analyze_results.py` | auditoria por `ClienteID`, novos indicadores, comparações e respostas |
| `scripts/plot_results.py` | gráficos obrigatórios e extras |
| `tests/test_runtime.py` | auditoria completa também no teste da reunião |
| `results/` | 150 replicações novas, CSVs, resumo e figuras |
| `README.md` | status e resultados finais |

## Pendências fora da Pessoa 4

- `scripts/make_documentation.py` gera o README a partir de um modelo da Pessoa 2; está desatualizado e não deve ser executado.
- Revisão visual da animação e gravação do vídeo MP4.
- O relatório foi atualizado por completo com o modelo final e estes resultados; falta a revisão do grupo.
