# Base preservada antes da integração

Fonte oficial: ZIP `Trabalho GB - Ana, Emanuele, Gabriela e Luisa.zip`, cinco CFG da Pessoa 1. Cópias intactas em `docs/baselines/pessoa1/`; manifesto SHA-256 de todos os membros dos quatro ZIPs em `docs/archive_manifest.json`.

| Cenário | Balcões | Tostadeiras | Caixas | P(tostar) | P(direto) |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 1 | 55% | 45% |
| 2 | 3 | 1 | 1 | 55% | 45% |
| 3 | 2 | 1 | 1 | 75% | 25% |
| 4 | 2 | 1 | 2 | 55% | 45% |
| 5 | 3 | 1 | 2 | 55% | 45% |

Preservar: filas FIFO compartilhadas; liberação do balcão antes da tostagem; ausência de bloqueio; EXPO(90 s); TRIA(20,30,45 s) da tostagem; TRIA(18,38,95 s) do pagamento; streams 1,3,4,5; primeira chegada em t=0 (padrão original); início vazio; aquecimento zero; 9000 s; 30 replicações; saídas dos clientes concluídos; posições dos objetos originais.

Correção autorizada: MaxNumber=999 é limite de quantidade e NÃO encerra chegadas em 5400 s. A intenção da janela de demanda será implementada por horário explícito. O limite 999 permanece, sem ser usado como relógio.

Alteração solicitada: substituir o uso de MontagemDist nos balcões pelas três distribuições condicionadas por TipoPedido. A declaração original permanece como referência sem uso. Atributos e registros são acrescentados sem duplicar clientes ou desenvolver pedidos com múltiplos sanduíches.

Comparações integrais antes de alterações: `docs/comparisons/ga_pessoa1_c*.diff` e `pessoa1_pessoa2_c*.diff`. Os modelos do ambiente online são idênticos aos da tentativa Pessoa 2. GA C1/C2 são idênticos nas duas fontes ZIP; GA C3 tem uma versão regravada pela interface no ZIP da Pessoa 1 (layout/ordenação), além da versão original do OneDrive. Nenhuma é tomada como substituta da base oficial do GB.
