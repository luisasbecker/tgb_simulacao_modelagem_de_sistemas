# Resultados — versão final (Pessoas 1 a 4)

JaamSim 2026-08; 30 replicações por cenário; 9000 s por replicação; chegadas em [0, 5400) s. Valores: média entre replicações ± semi-amplitude do IC95% t de Student (29 graus de liberdade).

Indicador principal (definido no relatório): **espera média no balcão**, em segundos por lanche, da entrada na fila do balcão ao início da montagem; meta: média inferior a 300 s. Indicador obrigatório complementar: **lead time do pedido**, em segundos, medido da chegada do cliente (`HoraChegada`) até o fim do pagamento; exclui desistentes. Contagem específica: **desistências**, em clientes por replicação, medida na chegada quando há mais de cinco lanches aguardando no balcão.

## Indicadores principais

| Indicador | Unidade | C1 | C2 | C3 | C4 | C5 |
|---|---|---:|---:|---:|---:|---:|
| Lead time médio do pedido | s | 305.99 ± 13.11 | 239.68 ± 8.26 | 312.37 ± 13.22 | 292.50 ± 12.48 | 217.21 ± 6.72 |
| P90 do lead time | s | 481.74 ± 20.80 | 358.59 ± 17.73 | 485.23 ± 20.76 | 463.63 ± 20.60 | 318.96 ± 14.13 |
| Espera média no balcão (por lanche) | s | 109.59 ± 11.50 | 34.66 ± 6.21 | 109.59 ± 11.50 | 109.59 ± 11.50 | 34.66 ± 6.21 |
| Espera de reunião (por pedido) | s | 20.55 ± 2.04 | 10.00 ± 1.30 | 20.55 ± 2.04 | 20.55 ± 2.04 | 10.00 ± 1.30 |
| Espera média no caixa | s | 13.87 ± 2.86 | 23.58 ± 4.84 | 12.79 ± 2.55 | 0.38 ± 0.18 | 1.11 ± 0.32 |
| Fila média do balcão | lanches | 0.96 ± 0.13 | 0.33 ± 0.07 | 0.96 ± 0.13 | 0.96 ± 0.13 | 0.33 ± 0.07 |
| Fila máxima do balcão | lanches | 7.17 ± 0.30 | 5.90 ± 0.49 | 7.17 ± 0.30 | 7.17 ± 0.30 | 5.90 ± 0.49 |
| Desistências | clientes | 3.43 ± 1.09 | 0.53 ± 0.32 | 3.43 ± 1.09 | 3.43 ± 1.09 | 0.53 ± 0.32 |
| Taxa de desistência | fracao | 0.054 ± 0.016 | 0.008 ± 0.005 | 0.054 ± 0.016 | 0.054 ± 0.016 | 0.008 ± 0.005 |
| Vazão | pedidos/h | 22.57 ± 0.94 | 23.73 ± 1.14 | 22.57 ± 0.94 | 22.57 ± 0.94 | 23.73 ± 1.14 |
| Pedidos atendidos | pedidos | 56.43 ± 2.35 | 59.33 ± 2.84 | 56.43 ± 2.35 | 56.43 ± 2.35 | 59.33 ± 2.84 |

A fila do balcão e a espera no balcão são medidas em **lanches** (após a duplicação da Pessoa 3). A vazão usa a janela total de 2,5 h. O P90 é calculado dentro de cada replicação e depois resumido. IC de desistências pode ter limite inferior negativo devido à raridade do evento; não representa contagem negativa.

## Respostas às perguntas do estudo

| Pergunta | Evidência | Resposta |
|---:|---|---|
| 1 | C1 = 109.59 s, IC95% [98.09; 121.10] s | sim |
| 2 | 109.59 s -> 34.66 s (-68.4%); diferenca_conclusiva | sim |
| 3 | 305.99 s -> 312.37 s (+2.1%); inconclusivo_por_sobreposicao | nao |
| 4 | 305.99 s -> 292.50 s (-4.4%); inconclusivo_por_sobreposicao | nao conclusivo |
| 5 | caixa 23.58 -> 1.11 s (diferenca_conclusiva); lead time 239.68 -> 217.21 s (diferenca_conclusiva); balcao 34.66 -> 34.66 s (inconclusivo_por_sobreposicao) | sim |

## Comparações entre cenários (lead time)

Critério da disciplina: ICs que não se sobrepõem indicam diferença conclusiva. A diferença pareada é complementar.

| A | B | Média A (s) | Média B (s) | Variação B vs A | Critério | Diferença pareada B−A, IC95% (s) |
|---:|---:|---:|---:|---:|---|---|
| 1 | 2 | 305.99 | 239.68 | -21.7% | diferenca_conclusiva | -66.31 [-73.84; -58.78] |
| 1 | 3 | 305.99 | 312.37 | +2.1% | inconclusivo_por_sobreposicao | 6.38 [5.14; 7.63] |
| 1 | 4 | 305.99 | 292.50 | -4.4% | inconclusivo_por_sobreposicao | -13.49 [-16.23; -10.75] |
| 1 | 5 | 305.99 | 217.21 | -29.0% | diferenca_conclusiva | -88.78 [-97.45; -80.11] |
| 2 | 3 | 239.68 | 312.37 | +30.3% | diferenca_conclusiva | 72.69 [64.73; 80.65] |
| 2 | 4 | 239.68 | 292.50 | +22.0% | diferenca_conclusiva | 52.82 [45.02; 60.61] |
| 2 | 5 | 239.68 | 217.21 | -9.4% | diferenca_conclusiva | -22.47 [-27.10; -17.84] |
| 3 | 4 | 312.37 | 292.50 | -6.4% | inconclusivo_por_sobreposicao | -19.87 [-22.81; -16.94] |
| 3 | 5 | 312.37 | 217.21 | -30.5% | diferenca_conclusiva | -95.16 [-104.05; -86.27] |
| 4 | 5 | 292.50 | 217.21 | -25.7% | diferenca_conclusiva | -75.29 [-82.95; -67.62] |

Demais indicadores comparados: [comparacoes_ic95.csv](comparacoes_ic95.csv).

## Lead time por tamanho do pedido (descritivo, agregado)

| Cenário | Lanches | Pedidos | Lead time médio (s) | P90 (s) |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1192 | 293.68 | 481.03 |
| 1 | 2 | 368 | 325.00 | 507.76 |
| 1 | 3 | 133 | 387.41 | 546.65 |
| 2 | 1 | 1250 | 237.57 | 374.54 |
| 2 | 2 | 390 | 244.19 | 371.31 |
| 2 | 3 | 140 | 266.09 | 378.47 |
| 3 | 1 | 1192 | 301.13 | 488.62 |
| 3 | 2 | 368 | 329.31 | 505.68 |
| 3 | 3 | 133 | 390.91 | 560.42 |
| 4 | 1 | 1192 | 276.68 | 458.33 |
| 4 | 2 | 368 | 318.14 | 505.93 |
| 4 | 3 | 133 | 382.27 | 543.02 |
| 5 | 1 | 1250 | 211.35 | 317.88 |
| 5 | 2 | 390 | 227.40 | 348.17 |
| 5 | 3 | 140 | 254.49 | 357.50 |

## Todos os indicadores

| Cenário | Indicador | Unidade | Média | DP | n | IC95% inferior | IC95% superior | Semi-amplitude |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | ClientesGerados | pedidos | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 1 | ClientesAtendidos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 1 | TotalDesistencias | clientes | 3.433333 | 2.932380 | 30 | 2.338365 | 4.528302 | 1.094969 |
| 1 | ClientesAindaNoSistema | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 1 | SanduichesMontados | lanches | 77.566667 | 8.282442 | 30 | 74.473952 | 80.659381 | 3.092715 |
| 1 | PedidosReunidos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 1 | SanduichesNoSistema | lanches | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 1 | PedidosNoPagamento | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 1 | EsperaReuniao_s | s | 18.679959 | 4.710471 | 30 | 16.921040 | 20.438878 | 1.758919 |
| 1 | FilaReuniao_media | lanches | 0.162380 | 0.048219 | 30 | 0.144375 | 0.180385 | 0.018005 |
| 1 | EsperaBalcao_s | s | 109.593509 | 30.807280 | 30 | 98.089882 | 121.097136 | 11.503627 |
| 1 | FilaBalcao_media | lanches | 0.960481 | 0.336822 | 30 | 0.834710 | 1.086253 | 0.125772 |
| 1 | FilaBalcao_max | lanches | 7.166667 | 0.791478 | 30 | 6.871124 | 7.462209 | 0.295543 |
| 1 | EsperaCaixa_s | s | 13.867758 | 7.651396 | 30 | 11.010680 | 16.724836 | 2.857078 |
| 1 | FilaCaixa_media | pedidos | 0.089345 | 0.055825 | 30 | 0.068500 | 0.110191 | 0.020845 |
| 1 | EsperaTostagem_s | s | 2.317347 | 1.827940 | 30 | 1.634783 | 2.999911 | 0.682564 |
| 1 | FilaTostagem_media | pedidos | 0.008000 | 0.006455 | 30 | 0.005590 | 0.010411 | 0.002410 |
| 1 | UtilizacaoBalcoes | fracao | 0.470520 | 0.050453 | 30 | 0.451681 | 0.489360 | 0.018840 |
| 1 | UtilizacaoTostadeira | fracao | 0.106294 | 0.018819 | 30 | 0.099267 | 0.113321 | 0.007027 |
| 1 | UtilizacaoCaixas | fracao | 0.313177 | 0.038958 | 30 | 0.298630 | 0.327724 | 0.014547 |
| 1 | LeadTime_medio_s | s | 305.991680 | 35.118397 | 30 | 292.878255 | 319.105105 | 13.113425 |
| 1 | LeadTime_dp_s | s | 128.028186 | 17.189255 | 30 | 121.609613 | 134.446759 | 6.418573 |
| 1 | LeadTime_max_s | s | 625.866670 | 75.115898 | 30 | 597.817932 | 653.915407 | 28.048737 |
| 1 | Vazao_h | pedidos/h | 22.573333 | 2.520390 | 30 | 21.632204 | 23.514463 | 0.941129 |
| 1 | VazaoLanches_h | lanches/h | 31.026667 | 3.312977 | 30 | 29.789581 | 32.263753 | 1.237086 |
| 1 | AmostrasLeadTime | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 1 | ClientesMontados | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 1 | ClientesTostados | pedidos | 30.166667 | 5.324526 | 30 | 28.178456 | 32.154877 | 1.988211 |
| 1 | ClientesPagos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 1 | UtilizacaoBalcao1 | fracao | 0.497030 | 0.043301 | 30 | 0.480862 | 0.513199 | 0.016169 |
| 1 | UtilizacaoBalcao2 | fracao | 0.444010 | 0.060520 | 30 | 0.421412 | 0.466609 | 0.022599 |
| 1 | UtilizacaoCaixa | fracao | 0.313177 | 0.038958 | 30 | 0.298630 | 0.327724 | 0.014547 |
| 1 | P90_lead_time_s | s | 481.742408 | 55.697590 | 30 | 460.944586 | 502.540230 | 20.797822 |
| 1 | TaxaDesistencia | fracao | 0.054120 | 0.043052 | 30 | 0.038044 | 0.070196 | 0.016076 |
| 1 | VazaoJanelaDemanda_h | pedidos/h | 37.622222 | 4.200651 | 30 | 36.053673 | 39.190771 | 1.568549 |
| 1 | LanchesPorPedido | lanches/pedido | 1.376624 | 0.065737 | 30 | 1.352077 | 1.401171 | 0.024547 |
| 1 | EsperaReuniaoPedido_s | s | 20.553761 | 5.473736 | 30 | 18.509834 | 22.597687 | 2.043926 |
| 1 | PedidosMultiplos | pedidos | 16.700000 | 2.692903 | 30 | 15.694454 | 17.705546 | 1.005546 |
| 2 | ClientesGerados | pedidos | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 2 | ClientesAtendidos | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 2 | TotalDesistencias | clientes | 0.533333 | 0.860366 | 30 | 0.212067 | 0.854599 | 0.321266 |
| 2 | ClientesAindaNoSistema | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 2 | SanduichesMontados | lanches | 81.666667 | 10.209304 | 30 | 77.854450 | 85.478883 | 3.812217 |
| 2 | PedidosReunidos | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 2 | SanduichesNoSistema | lanches | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 2 | PedidosNoPagamento | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 2 | EsperaReuniao_s | s | 9.081797 | 3.056344 | 30 | 7.940540 | 10.223055 | 1.141257 |
| 2 | FilaReuniao_media | lanches | 0.083568 | 0.033715 | 30 | 0.070979 | 0.096157 | 0.012589 |
| 2 | EsperaBalcao_s | s | 34.663273 | 16.636723 | 30 | 28.451019 | 40.875528 | 6.212254 |
| 2 | FilaBalcao_media | lanches | 0.326075 | 0.180869 | 30 | 0.258537 | 0.393612 | 0.067537 |
| 2 | FilaBalcao_max | lanches | 5.900000 | 1.322224 | 30 | 5.406274 | 6.393726 | 0.493726 |
| 2 | EsperaCaixa_s | s | 23.578642 | 12.966354 | 30 | 18.736926 | 28.420358 | 4.841716 |
| 2 | FilaCaixa_media | pedidos | 0.159280 | 0.094673 | 30 | 0.123929 | 0.194632 | 0.035351 |
| 2 | EsperaTostagem_s | s | 3.192798 | 2.142638 | 30 | 2.392723 | 3.992872 | 0.800074 |
| 2 | FilaTostagem_media | pedidos | 0.011995 | 0.009111 | 30 | 0.008593 | 0.015397 | 0.003402 |
| 2 | UtilizacaoBalcoes | fracao | 0.331046 | 0.041013 | 30 | 0.315731 | 0.346360 | 0.015314 |
| 2 | UtilizacaoTostadeira | fracao | 0.111701 | 0.019709 | 30 | 0.104341 | 0.119060 | 0.007359 |
| 2 | UtilizacaoCaixas | fracao | 0.329347 | 0.045221 | 30 | 0.312461 | 0.346233 | 0.016886 |
| 2 | LeadTime_medio_s | s | 239.683792 | 22.133751 | 30 | 231.418913 | 247.948670 | 8.264879 |
| 2 | LeadTime_dp_s | s | 87.168618 | 17.073131 | 30 | 80.793406 | 93.543830 | 6.375212 |
| 2 | LeadTime_max_s | s | 478.593034 | 72.750779 | 30 | 451.427446 | 505.758621 | 27.165587 |
| 2 | Vazao_h | pedidos/h | 23.733333 | 3.046913 | 30 | 22.595597 | 24.871069 | 1.137736 |
| 2 | VazaoLanches_h | lanches/h | 32.666667 | 4.083722 | 30 | 31.141780 | 34.191553 | 1.524887 |
| 2 | AmostrasLeadTime | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 2 | ClientesMontados | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 2 | ClientesTostados | pedidos | 31.766667 | 5.685331 | 30 | 29.643729 | 33.889604 | 2.122937 |
| 2 | ClientesPagos | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 2 | UtilizacaoBalcao1 | fracao | 0.403064 | 0.034106 | 30 | 0.390329 | 0.415800 | 0.012735 |
| 2 | UtilizacaoBalcao2 | fracao | 0.331939 | 0.044989 | 30 | 0.315140 | 0.348738 | 0.016799 |
| 2 | UtilizacaoBalcao3 | fracao | 0.258134 | 0.054012 | 30 | 0.237965 | 0.278302 | 0.020168 |
| 2 | UtilizacaoCaixa | fracao | 0.329347 | 0.045221 | 30 | 0.312461 | 0.346233 | 0.016886 |
| 2 | P90_lead_time_s | s | 358.585641 | 47.475159 | 30 | 340.858125 | 376.313157 | 17.727516 |
| 2 | TaxaDesistencia | fracao | 0.008419 | 0.013784 | 30 | 0.003272 | 0.013566 | 0.005147 |
| 2 | VazaoJanelaDemanda_h | pedidos/h | 39.555556 | 5.078188 | 30 | 37.659329 | 41.451782 | 1.896227 |
| 2 | LanchesPorPedido | lanches/pedido | 1.378205 | 0.061778 | 30 | 1.355136 | 1.401273 | 0.023068 |
| 2 | EsperaReuniaoPedido_s | s | 10.001136 | 3.494457 | 30 | 8.696285 | 11.305988 | 1.304852 |
| 2 | PedidosMultiplos | pedidos | 17.666667 | 3.043742 | 30 | 16.530115 | 18.803219 | 1.136552 |
| 3 | ClientesGerados | pedidos | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 3 | ClientesAtendidos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 3 | TotalDesistencias | clientes | 3.433333 | 2.932380 | 30 | 2.338365 | 4.528302 | 1.094969 |
| 3 | ClientesAindaNoSistema | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 3 | SanduichesMontados | lanches | 77.566667 | 8.282442 | 30 | 74.473952 | 80.659381 | 3.092715 |
| 3 | PedidosReunidos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 3 | SanduichesNoSistema | lanches | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 3 | PedidosNoPagamento | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 3 | EsperaReuniao_s | s | 18.679959 | 4.710471 | 30 | 16.921040 | 20.438878 | 1.758919 |
| 3 | FilaReuniao_media | lanches | 0.162380 | 0.048219 | 30 | 0.144375 | 0.180385 | 0.018005 |
| 3 | EsperaBalcao_s | s | 109.593509 | 30.807280 | 30 | 98.089882 | 121.097136 | 11.503627 |
| 3 | FilaBalcao_media | lanches | 0.960481 | 0.336822 | 30 | 0.834710 | 1.086253 | 0.125772 |
| 3 | FilaBalcao_max | lanches | 7.166667 | 0.791478 | 30 | 6.871124 | 7.462209 | 0.295543 |
| 3 | EsperaCaixa_s | s | 12.786088 | 6.822848 | 30 | 10.238395 | 15.333781 | 2.547693 |
| 3 | FilaCaixa_media | pedidos | 0.082746 | 0.052227 | 30 | 0.063244 | 0.102248 | 0.019502 |
| 3 | EsperaTostagem_s | s | 3.491187 | 1.755940 | 30 | 2.835508 | 4.146865 | 0.655679 |
| 3 | FilaTostagem_media | pedidos | 0.016135 | 0.008298 | 30 | 0.013037 | 0.019233 | 0.003098 |
| 3 | UtilizacaoBalcoes | fracao | 0.470520 | 0.050453 | 30 | 0.451681 | 0.489360 | 0.018840 |
| 3 | UtilizacaoTostadeira | fracao | 0.145229 | 0.018663 | 30 | 0.138260 | 0.152198 | 0.006969 |
| 3 | UtilizacaoCaixas | fracao | 0.313177 | 0.038958 | 30 | 0.298630 | 0.327724 | 0.014547 |
| 3 | LeadTime_medio_s | s | 312.374344 | 35.397888 | 30 | 299.156555 | 325.592132 | 13.217789 |
| 3 | LeadTime_dp_s | s | 127.257599 | 17.879615 | 30 | 120.581241 | 133.933957 | 6.676358 |
| 3 | LeadTime_max_s | s | 631.539198 | 82.339524 | 30 | 600.793114 | 662.285281 | 30.746084 |
| 3 | Vazao_h | pedidos/h | 22.573333 | 2.520390 | 30 | 21.632204 | 23.514463 | 0.941129 |
| 3 | VazaoLanches_h | lanches/h | 31.026667 | 3.312977 | 30 | 29.789581 | 32.263753 | 1.237086 |
| 3 | AmostrasLeadTime | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 3 | ClientesMontados | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 3 | ClientesTostados | pedidos | 41.266667 | 5.085024 | 30 | 39.367887 | 43.165446 | 1.898779 |
| 3 | ClientesPagos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 3 | UtilizacaoBalcao1 | fracao | 0.497030 | 0.043301 | 30 | 0.480862 | 0.513199 | 0.016169 |
| 3 | UtilizacaoBalcao2 | fracao | 0.444010 | 0.060520 | 30 | 0.421412 | 0.466609 | 0.022599 |
| 3 | UtilizacaoCaixa | fracao | 0.313177 | 0.038958 | 30 | 0.298630 | 0.327724 | 0.014547 |
| 3 | P90_lead_time_s | s | 485.228685 | 55.589444 | 30 | 464.471246 | 505.986125 | 20.757440 |
| 3 | TaxaDesistencia | fracao | 0.054120 | 0.043052 | 30 | 0.038044 | 0.070196 | 0.016076 |
| 3 | VazaoJanelaDemanda_h | pedidos/h | 37.622222 | 4.200651 | 30 | 36.053673 | 39.190771 | 1.568549 |
| 3 | LanchesPorPedido | lanches/pedido | 1.376624 | 0.065737 | 30 | 1.352077 | 1.401171 | 0.024547 |
| 3 | EsperaReuniaoPedido_s | s | 20.553761 | 5.473736 | 30 | 18.509834 | 22.597687 | 2.043926 |
| 3 | PedidosMultiplos | pedidos | 16.700000 | 2.692903 | 30 | 15.694454 | 17.705546 | 1.005546 |
| 4 | ClientesGerados | pedidos | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 4 | ClientesAtendidos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 4 | TotalDesistencias | clientes | 3.433333 | 2.932380 | 30 | 2.338365 | 4.528302 | 1.094969 |
| 4 | ClientesAindaNoSistema | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 4 | SanduichesMontados | lanches | 77.566667 | 8.282442 | 30 | 74.473952 | 80.659381 | 3.092715 |
| 4 | PedidosReunidos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 4 | SanduichesNoSistema | lanches | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 4 | PedidosNoPagamento | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 4 | EsperaReuniao_s | s | 18.679959 | 4.710471 | 30 | 16.921040 | 20.438878 | 1.758919 |
| 4 | FilaReuniao_media | lanches | 0.162380 | 0.048219 | 30 | 0.144375 | 0.180385 | 0.018005 |
| 4 | EsperaBalcao_s | s | 109.593509 | 30.807280 | 30 | 98.089882 | 121.097136 | 11.503627 |
| 4 | FilaBalcao_media | lanches | 0.960481 | 0.336822 | 30 | 0.834710 | 1.086253 | 0.125772 |
| 4 | FilaBalcao_max | lanches | 7.166667 | 0.791478 | 30 | 6.871124 | 7.462209 | 0.295543 |
| 4 | EsperaCaixa_s | s | 0.376026 | 0.489317 | 30 | 0.193312 | 0.558740 | 0.182714 |
| 4 | FilaCaixa_media | pedidos | 0.002431 | 0.003271 | 30 | 0.001210 | 0.003652 | 0.001221 |
| 4 | EsperaTostagem_s | s | 2.317347 | 1.827940 | 30 | 1.634783 | 2.999911 | 0.682564 |
| 4 | FilaTostagem_media | pedidos | 0.008000 | 0.006455 | 30 | 0.005590 | 0.010411 | 0.002410 |
| 4 | UtilizacaoBalcoes | fracao | 0.470520 | 0.050453 | 30 | 0.451681 | 0.489360 | 0.018840 |
| 4 | UtilizacaoTostadeira | fracao | 0.106294 | 0.018819 | 30 | 0.099267 | 0.113321 | 0.007027 |
| 4 | UtilizacaoCaixas | fracao | 0.156588 | 0.019479 | 30 | 0.149315 | 0.163862 | 0.007274 |
| 4 | LeadTime_medio_s | s | 292.499948 | 33.432698 | 30 | 280.015973 | 304.983923 | 12.483975 |
| 4 | LeadTime_dp_s | s | 124.326040 | 18.826113 | 30 | 117.296254 | 131.355826 | 7.029786 |
| 4 | LeadTime_max_s | s | 600.582269 | 86.783848 | 30 | 568.176648 | 632.987891 | 32.405621 |
| 4 | Vazao_h | pedidos/h | 22.573333 | 2.520390 | 30 | 21.632204 | 23.514463 | 0.941129 |
| 4 | VazaoLanches_h | lanches/h | 31.026667 | 3.312977 | 30 | 29.789581 | 32.263753 | 1.237086 |
| 4 | AmostrasLeadTime | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 4 | ClientesMontados | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 4 | ClientesTostados | pedidos | 30.166667 | 5.324526 | 30 | 28.178456 | 32.154877 | 1.988211 |
| 4 | ClientesPagos | pedidos | 56.433333 | 6.300976 | 30 | 54.080510 | 58.786156 | 2.352823 |
| 4 | UtilizacaoBalcao1 | fracao | 0.497030 | 0.043301 | 30 | 0.480862 | 0.513199 | 0.016169 |
| 4 | UtilizacaoBalcao2 | fracao | 0.444010 | 0.060520 | 30 | 0.421412 | 0.466609 | 0.022599 |
| 4 | UtilizacaoCaixa1 | fracao | 0.230300 | 0.022348 | 30 | 0.221956 | 0.238645 | 0.008345 |
| 4 | UtilizacaoCaixa2 | fracao | 0.082877 | 0.024782 | 30 | 0.073623 | 0.092130 | 0.009254 |
| 4 | P90_lead_time_s | s | 463.629578 | 55.154669 | 30 | 443.034486 | 484.224669 | 20.595092 |
| 4 | TaxaDesistencia | fracao | 0.054120 | 0.043052 | 30 | 0.038044 | 0.070196 | 0.016076 |
| 4 | VazaoJanelaDemanda_h | pedidos/h | 37.622222 | 4.200651 | 30 | 36.053673 | 39.190771 | 1.568549 |
| 4 | LanchesPorPedido | lanches/pedido | 1.376624 | 0.065737 | 30 | 1.352077 | 1.401171 | 0.024547 |
| 4 | EsperaReuniaoPedido_s | s | 20.553761 | 5.473736 | 30 | 18.509834 | 22.597687 | 2.043926 |
| 4 | PedidosMultiplos | pedidos | 16.700000 | 2.692903 | 30 | 15.694454 | 17.705546 | 1.005546 |
| 5 | ClientesGerados | pedidos | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 5 | ClientesAtendidos | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 5 | TotalDesistencias | clientes | 0.533333 | 0.860366 | 30 | 0.212067 | 0.854599 | 0.321266 |
| 5 | ClientesAindaNoSistema | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 5 | SanduichesMontados | lanches | 81.666667 | 10.209304 | 30 | 77.854450 | 85.478883 | 3.812217 |
| 5 | PedidosReunidos | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 5 | SanduichesNoSistema | lanches | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 5 | PedidosNoPagamento | pedidos | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 5 | EsperaReuniao_s | s | 9.081797 | 3.056344 | 30 | 7.940540 | 10.223055 | 1.141257 |
| 5 | FilaReuniao_media | lanches | 0.083568 | 0.033715 | 30 | 0.070979 | 0.096157 | 0.012589 |
| 5 | EsperaBalcao_s | s | 34.663273 | 16.636723 | 30 | 28.451019 | 40.875528 | 6.212254 |
| 5 | FilaBalcao_media | lanches | 0.326075 | 0.180869 | 30 | 0.258537 | 0.393612 | 0.067537 |
| 5 | FilaBalcao_max | lanches | 5.900000 | 1.322224 | 30 | 5.406274 | 6.393726 | 0.493726 |
| 5 | EsperaCaixa_s | s | 1.109281 | 0.849097 | 30 | 0.792223 | 1.426339 | 0.317058 |
| 5 | FilaCaixa_media | pedidos | 0.007655 | 0.006582 | 30 | 0.005197 | 0.010112 | 0.002458 |
| 5 | EsperaTostagem_s | s | 3.192798 | 2.142638 | 30 | 2.392723 | 3.992872 | 0.800074 |
| 5 | FilaTostagem_media | pedidos | 0.011995 | 0.009111 | 30 | 0.008593 | 0.015397 | 0.003402 |
| 5 | UtilizacaoBalcoes | fracao | 0.331046 | 0.041013 | 30 | 0.315731 | 0.346360 | 0.015314 |
| 5 | UtilizacaoTostadeira | fracao | 0.111701 | 0.019709 | 30 | 0.104341 | 0.119060 | 0.007359 |
| 5 | UtilizacaoCaixas | fracao | 0.164674 | 0.022610 | 30 | 0.156231 | 0.173116 | 0.008443 |
| 5 | LeadTime_medio_s | s | 217.214431 | 18.009696 | 30 | 210.489500 | 223.939362 | 6.724931 |
| 5 | LeadTime_dp_s | s | 75.541614 | 14.719947 | 30 | 70.045095 | 81.038132 | 5.496519 |
| 5 | LeadTime_max_s | s | 430.912093 | 64.721885 | 30 | 406.744544 | 455.079642 | 24.167549 |
| 5 | Vazao_h | pedidos/h | 23.733333 | 3.046913 | 30 | 22.595597 | 24.871069 | 1.137736 |
| 5 | VazaoLanches_h | lanches/h | 32.666667 | 4.083722 | 30 | 31.141780 | 34.191553 | 1.524887 |
| 5 | AmostrasLeadTime | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 5 | ClientesMontados | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 5 | ClientesTostados | pedidos | 31.766667 | 5.685331 | 30 | 29.643729 | 33.889604 | 2.122937 |
| 5 | ClientesPagos | pedidos | 59.333333 | 7.617282 | 30 | 56.488993 | 62.177673 | 2.844340 |
| 5 | UtilizacaoBalcao1 | fracao | 0.403064 | 0.034106 | 30 | 0.390329 | 0.415800 | 0.012735 |
| 5 | UtilizacaoBalcao2 | fracao | 0.331939 | 0.044989 | 30 | 0.315140 | 0.348738 | 0.016799 |
| 5 | UtilizacaoBalcao3 | fracao | 0.258134 | 0.054012 | 30 | 0.237965 | 0.278302 | 0.020168 |
| 5 | UtilizacaoCaixa1 | fracao | 0.232771 | 0.022252 | 30 | 0.224462 | 0.241080 | 0.008309 |
| 5 | UtilizacaoCaixa2 | fracao | 0.096576 | 0.026237 | 30 | 0.086779 | 0.106373 | 0.009797 |
| 5 | P90_lead_time_s | s | 318.960858 | 37.840174 | 30 | 304.831105 | 333.090612 | 14.129753 |
| 5 | TaxaDesistencia | fracao | 0.008419 | 0.013784 | 30 | 0.003272 | 0.013566 | 0.005147 |
| 5 | VazaoJanelaDemanda_h | pedidos/h | 39.555556 | 5.078188 | 30 | 37.659329 | 41.451782 | 1.896227 |
| 5 | LanchesPorPedido | lanches/pedido | 1.378205 | 0.061778 | 30 | 1.355136 | 1.401273 | 0.023068 |
| 5 | EsperaReuniaoPedido_s | s | 10.001136 | 3.494457 | 30 | 8.696285 | 11.305988 | 1.304852 |
| 5 | PedidosMultiplos | pedidos | 17.666667 | 3.043742 | 30 | 16.530115 | 18.803219 | 1.136552 |
