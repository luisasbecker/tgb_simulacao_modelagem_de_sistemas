# Evidências de validação técnica

## Separação dos níveis

| Nível | O que foi feito | O que não permite afirmar sozinho |
|---|---|---|
| Estático | comparação de entradas da base, objetos, recursos, rotas, distribuição, corte e conservação configurada | não prova que o parser ou a simulação funcionam |
| Execução real | JAR oficial JaamSim 2026-08, Java 17; smoke de 600 s; testes de limites; uma execução completa de cada cenário; 30 replicações por cenário | não substitui auditoria dos números e logs |
| Auditoria | DAT, REP, registros por cliente, estado e ocupação; checks com falha explícita | não transforma as premissas sintéticas em dados reais do Subway |
| Estatística | 30 valores por indicador/cenário; média, DP amostral, n, IC t95%, P90 e IC da diferença | não prova equivalência quando ICs se sobrepõem nem ótima escolha econômica |

## Checklist dos 17 pontos solicitados

| Item | Evidência e resultado |
|---|---|
| 1. Abre sem erro de parsing | cinco modelos aceitos pelo motor, sem log principal de erro na execução final |
| 2–3. Referências e objetos | declarações antes das referências; contrato estático preserva todos os objetos originais; execução não apresenta referências quebradas |
| 4. Começa normalmente | smoke de 600 s: 8 gerados, 6 atendidos, 2 remanescentes esperados; balanço satisfeito |
| 5. Para chegadas em 5400 s | limiar agendado aberto por exatamente 5400 s em 150/150; última chegada global 5399,491566 s; testes com primeira chegada exatamente em 5400 e intervalo pendente bloqueados |
| 6. Continua até 9000 s | TempoFinal_s=9000 nas 150 linhas e nos 150 blocos REP |
| 7. Sorteio real de TipoPedido | todos os 8980 registros de chegada carregam 1/2/3; atributo permanece igual até saída |
| 8. Proporções | 1796 chegadas distintas: 717 simples, 791 tradicionais, 288 complexos; 39,922%/44,042%/16,036%; diagnóstico qui-quadrado p=0,438 |
| 9. Distribuição correta | limites e streams conferidos; média por tipo 75,560/115,509/178,892 s; toda montagem realizada coincide com TempoMontagem dentro de 2 microssegundos; tipo preservado |
| 10. Desistência somente fila>5 | teste com 10 chegadas: 8 atendidos e 2 desistentes; os dois encontraram 6; cliente que encontrou 5 foi atendido; testes reais conferem a regra por cliente |
| 11. Desistente não chega ao caixa | IDs de desistentes disjuntos dos montados e atendidos; pagos=atendidos=amostras de lead time |
| 12. Contagem de desistências | contador nativo da saída própria coincide com log: 3/0/3/3/0 em C1/C2/C3/C4/C5 |
| 13. Lead time só concluídos | EstatSistema recebe somente após caixa; auditoria de entrada/saída e soma das seis parcelas de espera/serviço |
| 14. Conservação | gerados=atendidos+desistentes+ocupação medida; conferência em cada replicação e em cada observação do estado; zero remanescentes nas 150 |
| 15. Dois caixas paralelos | C4/C5 preservam WaitQueue=FilaCaixa; logs registram ambos com NumberInProgress=1 simultaneamente em todas as 30 replicações |
| 16. C3 75% tostados | ProbabilityList=0.75/0.25 preservada; contagem dos clientes tostados conferida com tempo no estado Tostagem; probabilidade é parâmetro, proporção empírica flutua |
| 17. Trinta replicações | DAT aceita exatamente replicações 1–30; REP e logs possuem as mesmas 30 seções em cada cenário |

As proporções de tipos usam C1 uma única vez porque os mesmos sorteios são reutilizados entre cenários. Não se aumenta artificialmente a amostra para 8980. Testes de aderência são diagnósticos das amostras; não demonstram validade empírica das distribuições para o estabelecimento.

## Sementes, integridade e reprodução

O JAR oficial tem SHA-256 `83e87bcde04b5dc8c06bac8dfb665e120fa6306aebe6ed6d49fb2ed1835223bf`. Nenhuma classe do motor foi alterada. O executor usa `java ... -jar JaamSim2026-08.jar cenarioN.cfg -h` e não simula a fila em Python. Python só lê arquivos, comanda processos, verifica resultados, calcula IC e desenha gráficos.

O manifesto em results/runs/execution_manifest.json contém hashes dos CFG finais e executados, do JAR e das saídas. Os arquivos models/cenarioN.cfg e os CFG de results/runs são idênticos. Substreams 1–30; streams fixos por distribuição. As chegadas, tipos e tempos sorteados são idênticos por cliente/replicação entre os cenários.

O ambiente marcou os logs com data de host diferente do contexto da sessão. Essas marcas foram mantidas sem editar os arquivos do motor; não são usadas para cálculos nem como data de coleta de campo.

## Falhas encontradas e tratamento

- O modelo recebido falhou pela declaração de unidade no atributo; ver received/received.log. O ambiente também tinha problema de cache temporário de ícones, isolado reproduzindo um exemplo oficial; ver received/environment_init_errors.log.
- Após corrigir só a unidade, a tentativa executou mas manteve o fechamento temporal inadequado e exportou o contador manual como texto; seus resultados são diagnósticos, não entram no resumo.
- A primeira gravação do cenário 4 teve DAT completo, mas REP e logs incompletos; foi arquivada e excluída da análise. Reexecução com o mesmo CFG gerou DAT idêntico e logs completos. O mecanismo de incompletude não foi determinado. O runner passou a verificar explicitamente REP e todos os logs.
- As fixtures de corte geram zero ou um cliente; indicadores de filas sem amostras produzem NaN, resultado esperado nesses testes. O analisador da produção exige valores finitos e não usa essas fixtures nas 150 replicações.

## Arquivos para conferir

- results/validation/static_validation.json: preservação da base.
- results/validation/runtime_tests.json: limites e smoke.
- results/validation/all_scenarios/: uma execução completa de cada cenário antes da produção.
- results/validation/received/: erro e diagnóstico da tentativa recebida.
- results/runs/: evidência bruta final aceita.
- results/validation_summary.json e results/conservacao.csv: auditoria final.
- results/replicacoes.csv: dados por replicação, inclusive P90.
- results/resumo_ic95.csv: estatísticas completas, sem reaproveitar números antigos.
- results/comparacoes_ic95.csv: regra da disciplina e complemento pareado.

## Limites restantes

A configuração visual nativa é validada pelo parser/headless, mas não foi revisada em janela gráfica. Os três gráficos externos foram renderizados e inspecionados. O vídeo MP4, os slides, a edição do PDF e a implementação da Pessoa 3 ficam para as etapas seguintes. O workflow/devcontainer foram preparados; não se afirma que rodaram em GitHub Actions/Codespaces. A conexão GitHub não tinha permissão de escrita, e nenhuma publicação remota ocorreu.
