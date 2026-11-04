# Comparação e registro de alterações

## Fontes e ordem de trabalho

Foi inspecionado o repositório oficial no commit `0b75aabbb866bcfeb8a565665c643164e2ed6a51`, que continha apenas README.md. A branch local `codex/pessoa2-validacao` deriva desse commit. O GitHub informa permissão de leitura e `push=false`; nenhuma alteração foi publicada ou enviada à branch main.

Os quatro ZIPs foram inventariados com tamanho e SHA-256 de todos os seus membros antes de editar modelos. Os dois relatórios anexados, o enunciado interno, os CFG, scripts, saídas anteriores e a planilha do GA foram inspecionados. Os vídeos/slides do GA foram identificados como material histórico, sem reaproveitá-los como demonstração da versão nova. A cópia integral do README anterior está em docs/baselines/README_anterior.md.

## GA → Pessoa 1 → tentativa Pessoa 2

| Aspecto | GA original | Pessoa 1 oficial | Tentativa Pessoa 2 recebida | Integração final |
|---|---|---|---|---|
| Cenários | 3 | 5; C4/C5 com dois caixas | mesmos 5 | preservados |
| Duração/replicações | 1,5 h / 10 | 2,5 h / 30 | 2,5 h / 30 | preservadas |
| Chegadas | até encerrar o GA | MaxNumber=999 não impõe 90 min | ExpressionThreshold + OperatingThresholdList | TimeSeriesThreshold + ImmediateThresholdList em 5400 s |
| Montagem | TRIA(60,105,200 s) | igual GA | três tipos e distribuições | três tipos realmente usados pelos balcões |
| Tipo do desistente | ausente | ausente | não sorteado antes da saída | sorteado uma vez para todo cliente |
| Desistência | ausente | ausente | Branch QueueLength > 5 | preservada a regra; validada nos limites 5/6 |
| Contagem | saída atendida | saída atendida | contador manual + saída de desistência | contador nativo de saída exposto como TotalDesistencias |
| Lead time | TotalTime dos atendidos | igual GA | mesma rota atendida | SimTime-HoraChegada; auditado por estados |
| Observação individual | ausente | ausente | ausente | logs de chegada, montagem, desistência e conclusão |
| Conservação | não auditada | não auditada | diferença entre contagens sugerida | balanço contra ocupação independente, por evento e replicação |

GA C1/C2 são idênticos nos dois ZIPs. GA C3 no ZIP da Pessoa 1 foi regravado pelo editor: ordenação, formatação e elementos gráficos diferem do OneDrive. A comparação semântica está em ga_variantes_semanticas.json. Os cinco CFG do pacote online são byte a byte iguais aos da tentativa Pessoa 2. Diffs integrais estão em docs/comparisons/. O teste estático registra cada entrada alterada da base em results/validation/static_validation.json; rejeita mudanças não autorizadas e remoção de objetos originais.

## Defeitos e correções

1. **MaxNumber não é tempo:** na Pessoa 1, chegadas permaneciam ativas até o término. O arquivo de log antigo ainda registra uma tentativa com `EndTime`, keyword inválida para EntityGenerator. O CFG atual da Pessoa 1 já não tinha EndTime, mas tampouco tinha corte temporal.
2. **Atributo com unidade inválida:** `TempoMontagem 105 s` falha no parser. A forma final é `TempoMontagem 0[s]`; cada cliente recebe o sorteio antes da fila. Foi reproduzido o erro no motor, não apenas detectado por regex.
3. **Limiar temporal inadequado:** ExpressionThreshold baseado em SimTime depende de eventos. Na tentativa recebida, corrigindo apenas a sintaxe, HorarioPico ficou aberto até 5427,766429 s na replicação 1; o gerador registrou estado Working até 5811,018617 s. Não se usa isso como prova de chegada tardia naquela replicação: a última chegada foi 5393,339016 s. A solução final agenda fechamento em 5400 s e interrompe imediatamente o intervalo pendente; testes com primeira chegada/intervalo exatamente no limite confirmam ausência de criação em t=5400.
4. **Contador exportado como texto:** ao corrigir só a sintaxe, a coluna `[ContadorDesistencias].TotalDesistencias` saiu como texto literal no DAT. A declaração aparecia depois de RunOutputList. A solução define os CustomOutputs numéricos antes de exportá-los e usa o contador nativo do sink de desistência.
5. **Classificação incompleta:** a tentativa classificava apenas quem era aceito. Agora todos os clientes são classificados antes da decisão, mantendo uma classificação por pedido e amostras pareáveis entre cenários. Isso não consome tempo simulado.
6. **Validação anterior insuficiente:** o verificador original aprovava regex/chaves, apesar do erro de sintaxe. A validação agora separa contrato estático, execução do parser/motor, testes determinísticos, auditoria individual e estatística.
7. **Leitor DAT incorreto:** o analisador anterior eliminava colunas vazias, podendo interpretar a linha agregada final como uma replicação adicional. O leitor novo mantém as posições e só aceita inteiro na célula Replication; exige exatamente 1–30, sem duplicações.
8. **Saídas/indicadores faltantes:** adicionados comprimento médio do caixa, utilização individual, vazão, P90 por replicação, tipos observados, lead time decomposto e ocupação independente para conservação.
9. **Execução não destrutiva:** o runner novo recusa sobrescrever uma pasta de experimento existente. Não usa o `rm -rf results/runs` do pacote anterior. Verifica hash do JAR existente, erros de parsing mesmo com retorno zero, presença e completude de DAT/REP/logs.
10. **Ambiente desta sessão:** o Java exigiu LD_LIBRARY_PATH para localizar libjli/libjvm; o cache temporário de imagens exigiu java.io.tmpdir em pasta gravável. Os 108 erros de ícones iniciais também afetavam exemplo oficial, e eram do ambiente. O runner corrige esses dois pontos sem modificar o JAR.
11. **Primeira gravação do C4 incompleta:** embora o DAT tivesse 30 replicações, o REP e logs estavam incompletos. Evidência preservada em results/validation/initial_c4_incomplete_logs/. Reexecutado o mesmo CFG com o mesmo SHA/streams; o DAT é byte a byte idêntico, agora com REP e logs completos. A causa da gravação incompleta não foi estabelecida. Esse incidente motivou a verificação explícita de completude; nenhum resultado foi inventado para completar logs.

## Mudanças gráficas e limites de validação

Foram mantidos o título, relógio e posições da base e acrescentados textos de atendidos (clientes), desistências (clientes), lead time (s), fila (clientes) e Graph com eixos rotulados. Os objetos gráficos foram aceitos pelo parser e pelo motor em modo headless. A apresentação visual nativa e o vídeo MP4 ainda precisam ser conferidos/gravados na interface gráfica; não se afirma validação visual da animação por execução headless. Os gráficos externos PNG/SVG foram renderizados e inspecionados.

## Referências técnicas consultadas

- [Release oficial JaamSim 2026-08](https://github.com/jaamsim/jaamsim/releases/tag/v2026-08), JAR e SHA-256.
- [Manual oficial](https://jaamsim.com/docs/JaamSim%20User%20Manual%202021-04.pdf), §§ 6.2, 7, 10.1, 14.3, 14.4 e 16; ajuda e exemplos contidos no próprio JAR.
- [Código da versão executada](https://github.com/jaamsim/jaamsim/tree/v2026-08), comportamento de parsing, logs e execução headless.

O código do simulador não foi alterado. Os novos resultados substituem integralmente os números antigos para esta versão, mas ainda precisarão ser recalculados após a Pessoa 3.
