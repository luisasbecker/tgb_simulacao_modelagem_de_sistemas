# Revisão técnica independente

Snapshot inicial revisado: commit `1dbf54598ad1eeecd9c9589e39321877648c1b49`, comparado com a base oficial `0b75aabbb866bcfeb8a565665c643164e2ed6a51`.

## Padrões e engenharia

A revisão não identificou problema bloqueante nos modelos ou números entregues. Reexecutou a auditoria dos 150 conjuntos de registros e verificou coincidência das médias com os CSVs. Apontou que a reconstrução das utilizações e esperas por logs dos concluídos dependia de esvaziamento, mas era aplicada sem essa condição.

Correção: limitar as igualdades dependentes dos concluídos aos experimentos esvaziados, preservando a contagem independente e a auditoria de conservação sempre. O resultado registra `reconstrucao_totais_por_concluidos_aplicavel`. O teste real remaining_clients deixou seis clientes no sistema, registrou o balanço corretamente e passou. Essa correção não altera os CFG finais nem os números das 150 replicações, que estavam esvaziadas.

## Especificação

A revisão não identificou falha material no escopo Pessoa 1 + Pessoa 2. Conferiu parâmetros preservados, atributos, regras, corte, conservação, caixas paralelos, 30 blocos REP por cenário e identidade dos CFG finais/executados. Recalculou os IC95% dos indicadores principais e confirmou as tabelas e a distinção entre regra da disciplina e IC pareado complementar.

Publicação GitHub, execução no Actions/Codespaces e inspeção da animação nativa permanecem limitações declaradas. A Pessoa 3 e a edição do PDF pertencem às etapas seguintes.
