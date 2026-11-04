# Alterações necessárias no relatório atual do GB

Referência: PDF recebido de 12 páginas, preservado em [relatorio_GB_recebido.pdf](references/relatorio_GB_recebido.pdf). Este roteiro não é uma edição do PDF. Os números novos vêm exclusivamente das 150 replicações auditadas em results/runs. Aplicar ao documento editável; depois da Pessoa 3, recalcular novamente.

## Texto e método: substituições por página

| Página/seção | Trecho ou conteúdo atual | Alteração necessária |
|---|---|---|
| 1, perguntas | C5 “elimina o aumento ... observado no cenário 2” | Tratar como hipótese a verificar. Na conclusão, dizer reduz substancialmente, não espera zero. |
| 2, §2.1 | todo cliente sai somente após pagamento; fluxo começa diretamente na fila | Acrescentar classificação por cliente e Branch por QueueLength>5, antes da fila; acrescentar saída exclusiva dos desistentes e contador. |
| 3, Figura 1 | ACD sem tipo/desistência | Atualizar com o fluxo de MODELO_CONCEITUAL.md; incluir filas únicas e servidores paralelos. |
| 3, §2.2 | simulação terminal de 90 min que termina no horizonte | Distinguir demanda de 90 min e simulação de 150 min; os 60 min finais esvaziam o sistema. |
| 3–4, §2.3 | processo Poisson e parâmetros da planilha | Explicitar primeira chegada determinística em t=0, preservada da base, seguida de EXPO(90 s). Dados são sintéticos, e os novos tipos são premissas do GB, não ajuste empírico. |
| 4, Tabela 1 | montagem única TRIA(60,105,200 s) | Substituir por três linhas: 40% TRIA(45,70,110), 45% TRIA(75,110,160), 15% TRIA(120,170,240), em segundos. Incluir TipoPedido. Preservar tostagem/pagamento/chegada. |
| 4, após Tabela 1 | “uma única distribuição ... montagem” | Substituir por distribuição condicionada ao TipoPedido, definido uma vez; TempoMontagem é armazenado e usado no servidor. |
| 4, hipótese 2 | “Não são consideradas desistências” | Desistência imediata ao encontrar 6 ou mais aguardando; não há abandono após aceitação; pessoas em serviço não contam. |
| 5, hipótese 8 | modelo não diferencia quantidade/ingredientes | Diferencia complexidade (simples/tradicional/complexo); múltiplos sanduíches continuam fora desta etapa. |
| 5, hipótese 10 | chegadas ativas por 2,5 h; MaxNumber=999 | Chegadas em [0,5400) s por TimeSeriesThreshold/ImmediateThresholdList; atendimento até 9000 s; MaxNumber não controla tempo. |
| 5–6, §3 | descrição dos recursos e probabilidades | Preservar os cinco cenários; acrescentar que todos compartilham a mesma regra de tipos, montagem e desistência. |
| 6–7, §4.1 | indicador principal muda entre C1–C3 e C4–C5 | Usar Wq balcão como principal comum aos cinco; lead time como complementar. IC95% = média ± t(0,975;29)×DP/√30. Informar streams e substream por replicação; denominador temporal 9000 s. |
| 7–8, Tabelas 2 e 3 | números de versões/janelas diferentes | Substituir integralmente pelas tabelas abaixo. Incluir desistências, conservação, P90 e vazão; DP, n e limites completos em apêndice/CSV. |
| 8–10, §§4.3–4.7 | análises numéricas antigas | Reescrever todas; usar respostas quantitativas novas abaixo. C4 passa a ter redução conclusiva de lead time frente a C1. |
| 10, §4.8 | Lei de Little com taxa/janela anteriores | Verificar por replicação: Lq = (admitidos/9000 s) × Wq balcão; excluir desistentes da taxa da fila. Calcular média dos produtos, não produto das médias. Área dos logs coincide com Lq. |
| 10, §4.9/Tabela 4 | cinco respostas antigas | Substituir pela tabela de respostas abaixo e respeitar a sobreposição de IC. Não traduzir IC sobreposto como igualdade nem “diferença não significativa” sem teste. |
| 11, §4.10 | chegadas por 2,5 h “garantem” todos concluídos | Remover: prolongar chegadas até o fim não elimina censura. A nova execução encerra chegadas em 90 min e observou zero remanescentes em 150/150 replicações. |
| 11–12, §5 | todas as conclusões, percentuais e recomendação C5 | Recalcular; distinguir melhor tempo de serviço de melhor decisão econômica, pois não há custos. Não afirmar gargalo somente por aumento de espera. |
| 12, limitações | modelo “não considera desistências” | Remover essa limitação; manter ausência de bloqueios, panes, pausas e múltiplos itens, além de dados sintéticos e início vazio. |
| Referências/método | versão e IA | Informar JaamSim 2026-08, JAR com SHA, Python/Scipy da análise; incluir declaração de uso de IA conforme enunciado. |

## Números antigos que devem ser retirados

Cada célula abaixo representa C1/C2/C3/C4/C5, nessa ordem. Todos são históricos e não devem permanecer como resultado da integração.

| Local/indicador | Série antiga |
|---|---|
| Tabela 2, Wq balcão, s | 44,7±17,0 / 7,7±3,5 / 44,7±17,0 / 58,1±10,3 / 9,9±2,1 |
| Tabela 2, Lq balcão | 0,538 / 0,094 / 0,538 / 0,667 / 0,114 |
| Tabela 2, máximo médio balcão | 4,0 / 2,4 / 4,0 / 5,6 / 3,4 |
| Tabela 2, espera tostagem, s | 1,45 / 2,73 / 1,93 / 1,45 / 2,73 |
| Tabela 2, Wq caixa, s | 13,9±4,0 / 25,7±13,0 / 13,2±3,9 / 0,1±0,1 / 1,0±1,0 |
| Tabela 2, Lq caixa | 0,154 / 0,296 / 0,147 / 0,001 / 0,010 |
| Tabela 2, utilização balcão | 0,660 / 0,445 / 0,660 / 0,668 / 0,446 |
| Tabela 2, utilização tostadeira | 0,179 / 0,181 / 0,252 / 0,190 / 0,190 |
| Tabela 2, utilização caixa | 0,532 / 0,536 / 0,530 / 0,270 / 0,271 |
| Tabela 3, W, s | 242,9±20,8 / 219,8±16,6 / 249,7±21,8 / 247,4±10,7 / 200,7±2,6 |
| Tabela 3, chegados | 61,5 / 61,5 / 61,5 / 97,4 / 97,9 |
| Tabela 3, concluídos | 57,2 / 57,9 / 57,3 / 96,3 / 96,8 |
| Tabela 3, remanescentes | 4,3 / 3,6 / 4,2 / 1,1 / 1,1 |
| §§4.4–5, percentuais e limites | 82,7%; 82,5%; 9,5%; 2,8%; 17,4%; 8,7%; IC [27,7;61,7], [236,7;258,1], [7,8;12,0], [198,2;203,3] e todas as repetições desses números |
| §4.10 | aproximadamente 100 chegadas por replicação, 61,5 do GA e garantia de eliminação de censura com chegadas ativas até o fim |

Há inconsistências já antes da Pessoa 2: os DAT da Pessoa 1 dão Wq balcão C1=58,109 s e W=259,432 s, enquanto o PDF usa 44,7 s e 242,9 s. O PDF diz que C4 mantém indicadores do balcão de C1, mas sua própria tabela exibe 58,1 versus 44,7 s. No texto de C5, 97,9 é chamado de atendidos, mas aparece como chegados na Tabela 3. Isso reforça a substituição integral, sem aproveitar células isoladas.

## Nova Tabela 2 — filas e utilização

Média ± semi-amplitude IC95%; n=30 em todas as células. Utilizações em fração, medidas em 9000 s; para porcentagem, multiplicar média e intervalo por 100.

| Indicador | C1 | C2 | C3 | C4 | C5 |
|---|---:|---:|---:|---:|---:|
| Wq balcão (s) | 35.695 ± 6.998 | 6.618 ± 1.662 | 35.695 ± 6.998 | 35.695 ± 6.998 | 6.618 ± 1.662 |
| Lq balcão (clientes) | 0.2455 ± 0.0545 | 0.0461 ± 0.0128 | 0.2455 ± 0.0545 | 0.2455 ± 0.0545 | 0.0461 ± 0.0128 |
| Média do máximo da fila (clientes) | 4.367 ± 0.465 | 2.633 ± 0.444 | 4.367 ± 0.465 | 4.367 ± 0.465 | 2.633 ± 0.444 |
| Espera tostadeira (s) | 1.822 ± 0.405 | 2.800 ± 0.597 | 2.435 ± 0.411 | 1.822 ± 0.405 | 2.800 ± 0.597 |
| Wq caixa (s) | 17.741 ± 4.192 | 28.415 ± 5.981 | 16.703 ± 3.942 | 0.339 ± 0.130 | 1.322 ± 0.359 |
| Lq caixa (clientes) | 0.1223 ± 0.0313 | 0.1962 ± 0.0464 | 0.1153 ± 0.0305 | 0.0023 ± 0.0009 | 0.0093 ± 0.0028 |
| Utilização média dos balcões (fração) | 0.3641 ± 0.0170 | 0.2433 ± 0.0115 | 0.3641 ± 0.0170 | 0.3641 ± 0.0170 | 0.2433 ± 0.0115 |
| Utilização tostadeira (fração) | 0.1126 ± 0.0076 | 0.1129 ± 0.0076 | 0.1544 ± 0.0079 | 0.1126 ± 0.0076 | 0.1129 ± 0.0076 |
| Utilização média dos caixas (fração) | 0.3316 ± 0.0172 | 0.3320 ± 0.0174 | 0.3316 ± 0.0172 | 0.1658 ± 0.0086 | 0.1660 ± 0.0087 |

## Nova Tabela 3 — sistema e perdas

| Indicador | C1 | C2 | C3 | C4 | C5 |
|---|---:|---:|---:|---:|---:|
| Lead time (s) | 231.217 ± 8.851 | 213.419 ± 7.039 | 237.268 ± 8.481 | 213.815 ± 7.336 | 186.326 ± 2.698 |
| Gerados (clientes) | 59.867 ± 2.938 | 59.867 ± 2.938 | 59.867 ± 2.938 | 59.867 ± 2.938 | 59.867 ± 2.938 |
| Atendidos (clientes) | 59.767 ± 2.908 | 59.867 ± 2.938 | 59.767 ± 2.908 | 59.767 ± 2.908 | 59.867 ± 2.938 |
| Desistentes (clientes) | 0.100 ± 0.150 | 0.000 ± 0.000 | 0.100 ± 0.150 | 0.100 ± 0.150 | 0.000 ± 0.000 |
| Remanescentes (clientes) | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P90 por replicação (s) | 340.411 ± 17.189 | 303.599 ± 14.600 | 344.566 ± 17.121 | 313.508 ± 16.354 | 253.509 ± 5.164 |
| Vazão em 2,5 h (clientes/h) | 23.907 ± 1.163 | 23.947 ± 1.175 | 23.907 ± 1.163 | 23.907 ± 1.163 | 23.947 ± 1.175 |

Desistências totais em 30 replicações: C1=3, C2=0, C3=3, C4=3, C5=0. São os mesmos padrões de chegadas em cada cenário; não somar os cinco cenários como cinco amostras independentes. Os tipos foram conferidos em 1796 chegadas distintas: 717 simples (39,922%), 791 tradicionais (44,042%) e 288 complexos (16,036%).

Os IC t de desistências raras podem incluir valores negativos (limite inferior -0.0503); isso é limitação da aproximação para a média e não uma contagem negativa. Relatar também totais e replicações com evento. Zero observado não comprova probabilidade real zero.

## Nova Tabela 4 — respostas às perguntas

| Pergunta | Evidência nova | Resposta e limite da conclusão |
|---|---|---|
| 1: C1 abaixo de 300 s? | Wq=35.69 s; IC95% [28.70; 42.69] s | Sim, inclusive o limite superior está abaixo da meta de média. Isso não significa que todo cliente espera menos de 300 s. |
| 2: C2 reduz Wq em pelo menos 40%? | 35.69 → 6.62 s; redução pontual 81.46%; ICs de médias separados | Sim na estimativa; diferença conclusiva pelo critério de IC. O percentual é razão de médias, não um IC de redução percentual. |
| 3: C3 aumenta W em mais de 20%? | 231.22 → 237.27 s; aumento pontual 2.62% | Não na estimativa. ICs de W se sobrepõem: não concluir diferença por inspeção. O IC pareado complementar mostra diferença de 6,05 s [4,74;7,36], sem substituir a regra. |
| 4: C4 reduz W frente a C1? | 231.22 → 213.82 s; ICs [222.37; 240.07] e [206.48; 221.15] s | Sim; intervalos sem sobreposição. A antiga resposta negativa deve ser removida. |
| 5: C5 resolve aumento de espera no caixa de C2? | Wq caixa 28.41 → 1.32 s; W 213.42 → 186.33 s; Wq balcão idêntico 6.62 s | Reduz substancialmente a espera no caixa e o lead time, com ICs separados, sem perda no balcão. Não afirmar fila sempre nula. |

## Conclusão substituta e figuras

Sob as premissas sintéticas atuais, C1 já cumpre a meta de espera média de 300 s, com 35.69 s e IC95% [28.70; 42.69] s. C2/C5 reduzem essa espera para 6.62 s. C5 apresenta o menor lead time médio, 186.33 s, com IC95% [183.63; 189.02] s, usando três balcões e dois caixas. C2 e C4 têm lead times próximos, 213.42 e 213.82 s, e ICs sobrepostos. Não é possível escolher economicamente entre configurações sem custos de pessoal/equipamento e metas adicionais. Houve somente 3 desistências em 1796 chegadas nos cenários com dois balcões; zero nos de três balcões, sem evidência suficiente para afirmar risco nulo. Todas as 150 replicações terminaram esvaziadas.

Incluir `results/figures/fila_balcao_degraus.png` (C1, replicação 28; tempos exatos dos eventos), `espera_balcao_ic95.png` (indicador principal) e `lead_time_ic95.png` (complementar). Todos possuem título, eixos e unidades. O gráfico de uma replicação ilustra comportamento; as conclusões usam as 30 replicações.

Acrescentar seção de validação com a falha de sintaxe recebida, correção do horário, teste fila 5/6, exclusão de desistentes do lead time, auditoria de 8980 registros de chegada em cinco cenários e conservação independente. A versão final do relatório deve declarar que múltiplos itens/Pessoa 3, revisão visual nativa e vídeo ainda não estão concluídos nesta etapa.
