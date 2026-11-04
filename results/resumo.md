# Resultados reais da versão Pessoa 1 + Pessoa 2

JaamSim 2026-08; 30 replicações por cenário; 9000 s por replicação; chegadas em [0,5400) s. Valores abaixo são médias entre replicações ± semi-amplitude IC95% t de Student (29 graus de liberdade).

| Cenário | Espera balcão (s) | Lead time (s) | P90 por replicação (s) | Atendidos | Desistentes | Remanescentes | Vazão (clientes/h em 2,5 h) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 35.695 ± 6.998 | 231.217 ± 8.851 | 340.411 ± 17.189 | 59.767 ± 2.908 | 0.100 ± 0.150 | 0.000 ± 0.000 | 23.907 ± 1.163 |
| 2 | 6.618 ± 1.662 | 213.419 ± 7.039 | 303.599 ± 14.600 | 59.867 ± 2.938 | 0.000 ± 0.000 | 0.000 ± 0.000 | 23.947 ± 1.175 |
| 3 | 35.695 ± 6.998 | 237.268 ± 8.481 | 344.566 ± 17.121 | 59.767 ± 2.908 | 0.100 ± 0.150 | 0.000 ± 0.000 | 23.907 ± 1.163 |
| 4 | 35.695 ± 6.998 | 213.815 ± 7.336 | 313.508 ± 16.354 | 59.767 ± 2.908 | 0.100 ± 0.150 | 0.000 ± 0.000 | 23.907 ± 1.163 |
| 5 | 6.618 ± 1.662 | 186.326 ± 2.698 | 253.509 ± 5.164 | 59.867 ± 2.938 | 0.000 ± 0.000 | 0.000 ± 0.000 | 23.947 ± 1.175 |

O indicador principal comum aos cinco cenários é a espera média no balcão. Lead time é indicador complementar. P90 é calculado por replicação (interpolação linear) e depois resumido; não é um percentil de médias nem um agrupamento dos 150 experimentos.

Utilização e comprimentos médios de fila usam toda a janela de 9000 s, inclusive o esvaziamento. VazaoJanelaDemanda_h usa 1,5 h como denominador e está separada no CSV. Não comparar utilizações destas tabelas com números antigos medidos em outra janela.

ICs sobrepostos não permitem concluir diferença pelo critério da disciplina. O CSV de comparações também fornece IC t pareado da diferença como análise complementar, sem substituir esse critério. IC t da média de desistências pode apresentar limite inferior negativo devido à raridade do evento; não representa contagem negativa e não deve ser truncado silenciosamente.

## Todos os indicadores

| Cenário | Indicador | Unidade | Média | DP | n | IC95% inferior | IC95% superior | Semi-amplitude |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | ClientesGerados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 1 | ClientesAtendidos | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 1 | TotalDesistencias | clientes | 0.100000 | 0.402578 | 30 | -0.050325 | 0.250325 | 0.150325 |
| 1 | ClientesAindaNoSistema | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 1 | EsperaBalcao_s | s | 35.694596 | 18.741828 | 30 | 28.696282 | 42.692909 | 6.998314 |
| 1 | FilaBalcao_media | clientes | 0.245517 | 0.145903 | 30 | 0.191036 | 0.299998 | 0.054481 |
| 1 | FilaBalcao_max | clientes | 4.366667 | 1.245221 | 30 | 3.901694 | 4.831640 | 0.464973 |
| 1 | EsperaCaixa_s | s | 17.741395 | 11.227265 | 30 | 13.549065 | 21.933725 | 4.192330 |
| 1 | FilaCaixa_media | clientes | 0.122266 | 0.083814 | 30 | 0.090969 | 0.153563 | 0.031297 |
| 1 | EsperaTostagem_s | s | 1.822009 | 1.084285 | 30 | 1.417130 | 2.226888 | 0.404879 |
| 1 | FilaTostagem_media | clientes | 0.006771 | 0.004535 | 30 | 0.005078 | 0.008464 | 0.001693 |
| 1 | UtilizacaoBalcoes | fracao | 0.364136 | 0.045567 | 30 | 0.347121 | 0.381151 | 0.017015 |
| 1 | UtilizacaoTostadeira | fracao | 0.112639 | 0.020297 | 30 | 0.105060 | 0.120218 | 0.007579 |
| 1 | UtilizacaoCaixas | fracao | 0.331619 | 0.046192 | 30 | 0.314371 | 0.348868 | 0.017248 |
| 1 | LeadTime_medio_s | s | 231.217495 | 23.704347 | 30 | 222.366146 | 240.068844 | 8.851349 |
| 1 | Vazao_h | clientes/h | 23.906667 | 3.115582 | 30 | 22.743289 | 25.070044 | 1.163377 |
| 1 | AmostrasLeadTime | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 1 | ClientesMontados | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 1 | ClientesTostados | clientes | 32.033333 | 5.863289 | 30 | 29.843945 | 34.222722 | 2.189388 |
| 1 | ClientesPagos | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 1 | UtilizacaoBalcao1 | fracao | 0.410339 | 0.036697 | 30 | 0.396636 | 0.424042 | 0.013703 |
| 1 | UtilizacaoBalcao2 | fracao | 0.317933 | 0.059667 | 30 | 0.295653 | 0.340213 | 0.022280 |
| 1 | UtilizacaoCaixa | fracao | 0.331619 | 0.046192 | 30 | 0.314371 | 0.348868 | 0.017248 |
| 1 | P90_lead_time_s | s | 340.411467 | 46.032814 | 30 | 323.222532 | 357.600403 | 17.188935 |
| 1 | TaxaDesistencia | fracao | 0.001500 | 0.006026 | 30 | -0.000750 | 0.003750 | 0.002250 |
| 1 | VazaoJanelaDemanda_h | clientes/h | 39.844444 | 5.192636 | 30 | 37.905482 | 41.783407 | 1.938962 |
| 2 | ClientesGerados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 2 | ClientesAtendidos | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 2 | TotalDesistencias | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 2 | ClientesAindaNoSistema | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 2 | EsperaBalcao_s | s | 6.618425 | 4.452003 | 30 | 4.956020 | 8.280831 | 1.662405 |
| 2 | FilaBalcao_media | clientes | 0.046088 | 0.034242 | 30 | 0.033302 | 0.058874 | 0.012786 |
| 2 | FilaBalcao_max | clientes | 2.633333 | 1.188547 | 30 | 2.189523 | 3.077144 | 0.443811 |
| 2 | EsperaCaixa_s | s | 28.414830 | 16.017952 | 30 | 22.433628 | 34.396031 | 5.981201 |
| 2 | FilaCaixa_media | clientes | 0.196165 | 0.124181 | 30 | 0.149795 | 0.242535 | 0.046370 |
| 2 | EsperaTostagem_s | s | 2.799527 | 1.597636 | 30 | 2.202960 | 3.396094 | 0.596567 |
| 2 | FilaTostagem_media | clientes | 0.010505 | 0.007110 | 30 | 0.007850 | 0.013160 | 0.002655 |
| 2 | UtilizacaoBalcoes | fracao | 0.243290 | 0.030755 | 30 | 0.231806 | 0.254774 | 0.011484 |
| 2 | UtilizacaoTostadeira | fracao | 0.112880 | 0.020360 | 30 | 0.105277 | 0.120482 | 0.007603 |
| 2 | UtilizacaoCaixas | fracao | 0.332045 | 0.046479 | 30 | 0.314690 | 0.349401 | 0.017355 |
| 2 | LeadTime_medio_s | s | 213.419037 | 18.851865 | 30 | 206.379635 | 220.458439 | 7.039402 |
| 2 | Vazao_h | clientes/h | 23.946667 | 3.147384 | 30 | 22.771414 | 25.121919 | 1.175252 |
| 2 | AmostrasLeadTime | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 2 | ClientesMontados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 2 | ClientesTostados | clientes | 32.100000 | 5.885986 | 30 | 29.902137 | 34.297863 | 2.197863 |
| 2 | ClientesPagos | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 2 | UtilizacaoBalcao1 | fracao | 0.353217 | 0.030455 | 30 | 0.341845 | 0.364589 | 0.011372 |
| 2 | UtilizacaoBalcao2 | fracao | 0.243019 | 0.040617 | 30 | 0.227852 | 0.258186 | 0.015167 |
| 2 | UtilizacaoBalcao3 | fracao | 0.133634 | 0.036197 | 30 | 0.120118 | 0.147150 | 0.013516 |
| 2 | UtilizacaoCaixa | fracao | 0.332045 | 0.046479 | 30 | 0.314690 | 0.349401 | 0.017355 |
| 2 | P90_lead_time_s | s | 303.598726 | 39.098565 | 30 | 288.999082 | 318.198370 | 14.599644 |
| 2 | TaxaDesistencia | fracao | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 2 | VazaoJanelaDemanda_h | clientes/h | 39.911111 | 5.245639 | 30 | 37.952357 | 41.869865 | 1.958754 |
| 3 | ClientesGerados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 3 | ClientesAtendidos | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 3 | TotalDesistencias | clientes | 0.100000 | 0.402578 | 30 | -0.050325 | 0.250325 | 0.150325 |
| 3 | ClientesAindaNoSistema | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 3 | EsperaBalcao_s | s | 35.694596 | 18.741828 | 30 | 28.696282 | 42.692909 | 6.998314 |
| 3 | FilaBalcao_media | clientes | 0.245517 | 0.145903 | 30 | 0.191036 | 0.299998 | 0.054481 |
| 3 | FilaBalcao_max | clientes | 4.366667 | 1.245221 | 30 | 3.901694 | 4.831640 | 0.464973 |
| 3 | EsperaCaixa_s | s | 16.703103 | 10.558128 | 30 | 12.760633 | 20.645573 | 3.942470 |
| 3 | FilaCaixa_media | clientes | 0.115327 | 0.081756 | 30 | 0.084799 | 0.145856 | 0.030528 |
| 3 | EsperaTostagem_s | s | 2.435110 | 1.100591 | 30 | 2.024143 | 2.846078 | 0.410968 |
| 3 | FilaTostagem_media | clientes | 0.012256 | 0.006671 | 30 | 0.009766 | 0.014747 | 0.002491 |
| 3 | UtilizacaoBalcoes | fracao | 0.364136 | 0.045567 | 30 | 0.347121 | 0.381151 | 0.017015 |
| 3 | UtilizacaoTostadeira | fracao | 0.154426 | 0.021040 | 30 | 0.146569 | 0.162282 | 0.007856 |
| 3 | UtilizacaoCaixas | fracao | 0.331619 | 0.046192 | 30 | 0.314371 | 0.348868 | 0.017248 |
| 3 | LeadTime_medio_s | s | 237.268173 | 22.711258 | 30 | 228.787650 | 245.748697 | 8.480523 |
| 3 | Vazao_h | clientes/h | 23.906667 | 3.115582 | 30 | 22.743289 | 25.070044 | 1.163377 |
| 3 | AmostrasLeadTime | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 3 | ClientesMontados | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 3 | ClientesTostados | clientes | 43.766667 | 5.805368 | 30 | 41.598907 | 45.934427 | 2.167760 |
| 3 | ClientesPagos | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 3 | UtilizacaoBalcao1 | fracao | 0.410339 | 0.036697 | 30 | 0.396636 | 0.424042 | 0.013703 |
| 3 | UtilizacaoBalcao2 | fracao | 0.317933 | 0.059667 | 30 | 0.295653 | 0.340213 | 0.022280 |
| 3 | UtilizacaoCaixa | fracao | 0.331619 | 0.046192 | 30 | 0.314371 | 0.348868 | 0.017248 |
| 3 | P90_lead_time_s | s | 344.566226 | 45.850121 | 30 | 327.445510 | 361.686943 | 17.120717 |
| 3 | TaxaDesistencia | fracao | 0.001500 | 0.006026 | 30 | -0.000750 | 0.003750 | 0.002250 |
| 3 | VazaoJanelaDemanda_h | clientes/h | 39.844444 | 5.192636 | 30 | 37.905482 | 41.783407 | 1.938962 |
| 4 | ClientesGerados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 4 | ClientesAtendidos | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 4 | TotalDesistencias | clientes | 0.100000 | 0.402578 | 30 | -0.050325 | 0.250325 | 0.150325 |
| 4 | ClientesAindaNoSistema | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 4 | EsperaBalcao_s | s | 35.694596 | 18.741828 | 30 | 28.696282 | 42.692909 | 6.998314 |
| 4 | FilaBalcao_media | clientes | 0.245517 | 0.145903 | 30 | 0.191036 | 0.299998 | 0.054481 |
| 4 | FilaBalcao_max | clientes | 4.366667 | 1.245221 | 30 | 3.901694 | 4.831640 | 0.464973 |
| 4 | EsperaCaixa_s | s | 0.339067 | 0.347561 | 30 | 0.209285 | 0.468849 | 0.129782 |
| 4 | FilaCaixa_media | clientes | 0.002339 | 0.002422 | 30 | 0.001435 | 0.003243 | 0.000904 |
| 4 | EsperaTostagem_s | s | 1.822009 | 1.084285 | 30 | 1.417130 | 2.226888 | 0.404879 |
| 4 | FilaTostagem_media | clientes | 0.006771 | 0.004535 | 30 | 0.005078 | 0.008464 | 0.001693 |
| 4 | UtilizacaoBalcoes | fracao | 0.364136 | 0.045567 | 30 | 0.347121 | 0.381151 | 0.017015 |
| 4 | UtilizacaoTostadeira | fracao | 0.112639 | 0.020297 | 30 | 0.105060 | 0.120218 | 0.007579 |
| 4 | UtilizacaoCaixas | fracao | 0.165810 | 0.023096 | 30 | 0.157185 | 0.174434 | 0.008624 |
| 4 | LeadTime_medio_s | s | 213.815167 | 19.646608 | 30 | 206.479003 | 221.151331 | 7.336164 |
| 4 | Vazao_h | clientes/h | 23.906667 | 3.115582 | 30 | 22.743289 | 25.070044 | 1.163377 |
| 4 | AmostrasLeadTime | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 4 | ClientesMontados | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 4 | ClientesTostados | clientes | 32.033333 | 5.863289 | 30 | 29.843945 | 34.222722 | 2.189388 |
| 4 | ClientesPagos | clientes | 59.766667 | 7.788955 | 30 | 56.858223 | 62.675110 | 2.908444 |
| 4 | UtilizacaoBalcao1 | fracao | 0.410339 | 0.036697 | 30 | 0.396636 | 0.424042 | 0.013703 |
| 4 | UtilizacaoBalcao2 | fracao | 0.317933 | 0.059667 | 30 | 0.295653 | 0.340213 | 0.022280 |
| 4 | UtilizacaoCaixa1 | fracao | 0.236843 | 0.022737 | 30 | 0.228353 | 0.245333 | 0.008490 |
| 4 | UtilizacaoCaixa2 | fracao | 0.094776 | 0.029709 | 30 | 0.083683 | 0.105870 | 0.011094 |
| 4 | P90_lead_time_s | s | 313.508138 | 43.795890 | 30 | 297.154484 | 329.861792 | 16.353654 |
| 4 | TaxaDesistencia | fracao | 0.001500 | 0.006026 | 30 | -0.000750 | 0.003750 | 0.002250 |
| 4 | VazaoJanelaDemanda_h | clientes/h | 39.844444 | 5.192636 | 30 | 37.905482 | 41.783407 | 1.938962 |
| 5 | ClientesGerados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 5 | ClientesAtendidos | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 5 | TotalDesistencias | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 5 | ClientesAindaNoSistema | clientes | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 5 | EsperaBalcao_s | s | 6.618425 | 4.452003 | 30 | 4.956020 | 8.280831 | 1.662405 |
| 5 | FilaBalcao_media | clientes | 0.046088 | 0.034242 | 30 | 0.033302 | 0.058874 | 0.012786 |
| 5 | FilaBalcao_max | clientes | 2.633333 | 1.188547 | 30 | 2.189523 | 3.077144 | 0.443811 |
| 5 | EsperaCaixa_s | s | 1.322139 | 0.961608 | 30 | 0.963068 | 1.681209 | 0.359071 |
| 5 | FilaCaixa_media | clientes | 0.009284 | 0.007503 | 30 | 0.006483 | 0.012086 | 0.002802 |
| 5 | EsperaTostagem_s | s | 2.799527 | 1.597636 | 30 | 2.202960 | 3.396094 | 0.596567 |
| 5 | FilaTostagem_media | clientes | 0.010505 | 0.007110 | 30 | 0.007850 | 0.013160 | 0.002655 |
| 5 | UtilizacaoBalcoes | fracao | 0.243290 | 0.030755 | 30 | 0.231806 | 0.254774 | 0.011484 |
| 5 | UtilizacaoTostadeira | fracao | 0.112880 | 0.020360 | 30 | 0.105277 | 0.120482 | 0.007603 |
| 5 | UtilizacaoCaixas | fracao | 0.166023 | 0.023239 | 30 | 0.157345 | 0.174700 | 0.008678 |
| 5 | LeadTime_medio_s | s | 186.326345 | 7.225587 | 30 | 183.628267 | 189.024424 | 2.698079 |
| 5 | Vazao_h | clientes/h | 23.946667 | 3.147384 | 30 | 22.771414 | 25.121919 | 1.175252 |
| 5 | AmostrasLeadTime | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 5 | ClientesMontados | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 5 | ClientesTostados | clientes | 32.100000 | 5.885986 | 30 | 29.902137 | 34.297863 | 2.197863 |
| 5 | ClientesPagos | clientes | 59.866667 | 7.868459 | 30 | 56.928536 | 62.804797 | 2.938131 |
| 5 | UtilizacaoBalcao1 | fracao | 0.353217 | 0.030455 | 30 | 0.341845 | 0.364589 | 0.011372 |
| 5 | UtilizacaoBalcao2 | fracao | 0.243019 | 0.040617 | 30 | 0.227852 | 0.258186 | 0.015167 |
| 5 | UtilizacaoBalcao3 | fracao | 0.133634 | 0.036197 | 30 | 0.120118 | 0.147150 | 0.013516 |
| 5 | UtilizacaoCaixa1 | fracao | 0.234035 | 0.022298 | 30 | 0.225709 | 0.242361 | 0.008326 |
| 5 | UtilizacaoCaixa2 | fracao | 0.098010 | 0.029109 | 30 | 0.087141 | 0.108880 | 0.010870 |
| 5 | P90_lead_time_s | s | 253.509247 | 13.828411 | 30 | 248.345634 | 258.672861 | 5.163614 |
| 5 | TaxaDesistencia | fracao | 0.000000 | 0.000000 | 30 | 0.000000 | 0.000000 | 0.000000 |
| 5 | VazaoJanelaDemanda_h | clientes/h | 39.911111 | 5.245639 | 30 | 37.952357 | 41.869865 | 1.958754 |
