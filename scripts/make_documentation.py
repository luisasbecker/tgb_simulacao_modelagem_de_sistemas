#!/usr/bin/env python3
"""Regenerate result-dependent documentation from the audited CSVs."""
from pathlib import Path
import csv,json
from run_model import ROOT

def main():
    rows=list(csv.DictReader((ROOT/'results/resumo_ic95.csv').open()))
    stats={(int(r['cenario']),r['indicador']):r for r in rows}
    def mean(n,k):return float(stats[n,k]['media'])
    def fmt(n,k,dec=2,interval=True):
        r=stats[n,k]
        return f"{float(r['media']):.{dec}f}"+(f" ± {float(r['semi_amplitude']):.{dec}f}" if interval else '')
    def bounds(n,k):
        r=stats[n,k];return f"[{float(r['ic95_inferior']):.2f}; {float(r['ic95_superior']):.2f}]"
    def table(metrics):
        lines=['| Indicador | C1 | C2 | C3 | C4 | C5 |','|---|---:|---:|---:|---:|---:|']
        for title,k,dec in metrics:lines.append('| '+title+' | '+' | '.join(fmt(n,k,dec) for n in range(1,6))+' |')
        return '\n'.join(lines)
    headline=table([('Espera balcão (s)','EsperaBalcao_s',2),('Lead time (s)','LeadTime_medio_s',2),('Atendidos/replicação','ClientesAtendidos',2),('Desistentes/replicação','TotalDesistencias',2)])
    red_wait=100*(1-mean(2,'EsperaBalcao_s')/mean(1,'EsperaBalcao_s'))
    inc_toast=100*(mean(3,'LeadTime_medio_s')/mean(1,'LeadTime_medio_s')-1)
    readme=f'''# Trabalho do Grau B — Simulação e Modelagem de Sistemas

**Simulação e análise do atendimento do Subway da Unisinos.** Disciplina: Simulação e Modelagem de Sistemas, UNISINOS. Professor: Alex Roehrs.

**Integrantes:** Ana Beatriz Stahl; Emanuele Schlemmer Thomazzoni; Gabriela Bley Rodrigues; Luisa Becker dos Santos.

Repositório oficial: [luisasbecker/tgb_simulacao_modelagem_de_sistemas](https://github.com/luisasbecker/tgb_simulacao_modelagem_de_sistemas).

## Status da versão Pessoa 1 + Pessoa 2

Os cinco modelos finais foram **executados no JaamSim 2026-08**, com 30 replicações cada (150 replicações analisadas). Há resultados reais, logs individuais, conservação auditada e IC95% recalculados. O motor não foi substituído por uma simulação Python: Python executa o JAR, verifica os registros e calcula estatísticas.

Esta entrega está na branch local `codex/pessoa2-validacao`. A conexão GitHub disponibilizada informa leitura e `push=false`; portanto estes arquivos ainda não foram publicados no repositório remoto. O workflow e o devcontainer estão preparados, mas não foram executados dentro do GitHub Actions/Codespaces. A execução headless em ambiente online desta sessão foi realizada.

| Verificação | Situação |
|---|---|
| Comparação GA / Pessoa 1 / tentativa Pessoa 2 | concluída; fontes e diffs preservados |
| Validação estática | cinco cenários aprovados; contrato preserva parâmetros da Pessoa 1 |
| Parser e motor JaamSim | execução curta, limites 5/6 e 5400 s, cinco cenários e 30 replicações aprovados |
| Análise estatística | dados novos, 30 observações por cenário, IC t95%, P90, comparações |
| Conservação e esvaziamento | zero remanescentes nas 150 replicações; balanço também conferido nos registros de estado |
| Interface gráfica nativa e vídeo | objetos aceitos em headless; revisão visual e gravação MP4 pendentes |
| Pessoa 3 | contrato de compatibilidade documentado; duplicações/lotes ainda não implementados |
| Relatório GB | PDF original preservado; roteiro de atualização pronto, sem editar o PDF nesta etapa |

## Sistema, objetivo e evolução GA → GB

Clientes chegam ao Subway, esperam por montagem, podem passar pela tostadeira e pagam no caixa. O estudo mede espera, ocupação, desistências e tempo total para comparar configurações de atendimento. Os dados são premissas sintéticas de projeto; os resultados são execuções reais desse modelo, não medições do estabelecimento.

O GA tinha três cenários, 90 minutos de execução e 10 replicações. A Pessoa 1 acrescentou C4/C5, definiu 2,5 horas e 30 replicações. A Pessoa 2 integrou tipos de pedido, montagem condicionada, desistência e contagem, corrigiu o corte das chegadas e reexecutou a experimentação. As bases estão preservadas em `docs/baselines/`.

## Cinco cenários preservados

| Cenário | Balcões em paralelo | Tostadeira | Caixas | P(tostar) | P(direto) |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 1 | 55% | 45% |
| 2 | 3 | 1 | 1 | 55% | 45% |
| 3 | 2 | 1 | 1 | 75% | 25% |
| 4 | 2 | 1 | 2 | 55% | 45% |
| 5 | 3 | 1 | 2 | 55% | 45% |

Fila única do balcão; fila única compartilhada entre os caixas de C4/C5. Chegadas somente em **0 ≤ t < 5400 s**, execução até **9000 s**, início vazio e sem aquecimento. A primeira chegada em t=0 é preservada do GA/Pessoa 1; as seguintes têm intervalos EXPO(90 s).

### Contribuição da Pessoa 1

Mantidos números de servidores, filas, FIFO, probabilidades de tostagem, tostagem TRIA(20,30,45 s), pagamento TRIA(18,38,95 s), streams originais, janela total, replicações, liberação do balcão antes de tostar e layout original. O corte de 90 minutos foi corrigido: MaxNumber=999 não representava um horário.

### Contribuição da Pessoa 2

| TipoPedido | Probabilidade | Montagem triangular: mínimo / moda / máximo |
|---|---:|---|
| 1 — simples | 40% | 45 / 70 / 110 s |
| 2 — tradicional | 45% | 75 / 110 / 160 s |
| 3 — complexo | 15% | 120 / 170 / 240 s |

O tipo é sorteado uma vez por cliente, inclusive desistentes; determina TempoMontagem, usado pelos balcões. Na chegada, `FilaBalcao.QueueLength > 5` leva à saída de desistência; clientes em serviço não entram nessa contagem. Quem encontra cinco aguardando pode entrar, deixando seis na fila. TotalDesistencias usa o contador nativo dessa saída. Lead time é medido desde HoraChegada até o pagamento concluído e exclui desistentes.

A implementação não cria sanduíches independentes. O [contrato com a Pessoa 3](docs/MODELO_CONCEITUAL.md#contrato-para-a-pessoa-3) exige herança do TipoPedido e contagem final por cliente. Após essa etapa, os resultados deverão ser recalculados novamente.

## Modelos finais e estrutura

Os arquivos executáveis finais são **models/cenario1.cfg** a **models/cenario5.cfg**. Os CFG em docs/baselines são históricos, e os de results/validation incluem testes que alteram demanda/duração; não são cenários finais.

| Caminho | Conteúdo |
|---|---|
| models/ | cinco CFG finais independentes |
| scripts/ | download verificado, execução real, auditoria, análise, gráficos e geração documentada dos CFG |
| tests/ | testes determinísticos no motor e regressão do leitor DAT/log |
| results/runs/ | execução validada: 150 replicações; CFG executados, DAT, REP e logs |
| results/replicacoes.csv | uma linha por cenário/replicação, inclusive desistências e P90 |
| results/resumo_ic95.csv | média, DP, n, limites e semi-amplitude para todos os indicadores |
| results/comparacoes_ic95.csv | regra de sobreposição e IC pareado complementar |
| results/conservacao.csv | balanço, remanescentes e auditoria por replicação |
| results/figures/ | gráficos PNG/SVG com IC e série em degraus |
| results/validation/ | testes, falhas recebidas e evidências da correção |
| docs/ | comparação, modelo conceitual, validação, alterações do relatório e fontes |
| .github/workflows/jaamsim.yml | workflow preparado para executar e guardar evidências |
| .devcontainer/ e Dockerfile | ambiente Linux/Java/Python para Codespaces |
| tools/ | JAR oficial; ignorado pelo Git, incluído no pacote ZIP de entrega |

## Executar e reproduzir

Pré-requisitos: Java 17, Python 3.12, Bash e curl. Use o [JAR oficial 2026-08](https://github.com/jaamsim/jaamsim/releases/tag/v2026-08). SHA-256: `83e87bcde04b5dc8c06bac8dfb665e120fa6306aebe6ed6d49fb2ed1835223bf`.

Na raiz do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
bash scripts/download_jaamsim.sh
python3 scripts/validate_cfg.py
python3 -m unittest discover -s tests -p 'test_io.py'
python3 tests/test_runtime.py
bash scripts/run_all.sh --output results/reexecutions/minha_execucao/runs
python3 scripts/plot_results.py results/reexecutions/minha_execucao
```

`run_all.py` executa cinco processos JaamSim, um por cenário, cada um com 30 replicações. Confere DAT/REP/logs e chama a análise. Não substitui resultados existentes: escolha um caminho novo. Uma única linha de execução com cinco CFG não é usada como cinco experimentos.

Para somente reanalisar os resultados entregues:

```bash
python3 scripts/analyze_results.py results/runs
python3 scripts/plot_results.py results
```

Para uma prévia com uma replicação de cada cenário:

```bash
python3 scripts/run_all.py --replications 1 --output results/reexecutions/previa
```

Interface gráfica: `java -jar tools/JaamSim2026-08.jar`, File → Open → `models/cenarioN.cfg`, botão Play. A tela inclui título, relógio, quatro indicadores com unidades e gráfico rotulado. Para vídeo, use uma cópia do CFG com uma replicação; não altere os arquivos finais. A conferência visual e o vídeo nativo de até um minuto continuam pendentes.

Headless direto: `java -jar tools/JaamSim2026-08.jar models/cenario1.cfg -h`. Isso grava saídas ao lado do modelo; prefira os scripts para separar evidências. O runner adapta a pasta temporária para ambientes restritos e verifica erros mesmo quando o Java retorna código zero.

Codespaces: após publicar esta branch, abrir o repositório com o devcontainer e seguir os comandos acima. GitHub Actions: publicar `.github/workflows/jaamsim.yml` e usar **Actions → Validar modelos JaamSim → Run workflow**, ou o gatilho de push/PR. O job executa testes e 150 replicações, e exporta resultados como artifact. Não há execução remota do workflow comprovada nesta entrega.

## Resultados novos

{headline}

Valores: média ± semi-amplitude IC95% t(29), 30 replicações. Gerados: {fmt(1,'ClientesGerados')} clientes/replicação em todos os cenários. Remanescentes: zero em todas as 150 replicações. Desistências totais: C1=3, C2=0, C3=3, C4=3, C5=0. A ausência observada em C2/C5 não prova risco populacional zero.

Todos os números, DP, n, limites e unidades estão em [resumo completo](results/resumo.md) e [CSV](results/resumo_ic95.csv). Utilizações/comprimentos médios usam 9000 s; a vazão principal é atendidos/2,5 h. P90 é calculado dentro de cada replicação antes da consolidação.

![Comparação da espera no balcão](results/figures/espera_balcao_ic95.png)

C2 reduz a espera média no balcão em {red_wait:.2f}% em relação a C1, com intervalos não sobrepostos. No lead time, C5 tem a menor média ({mean(5,'LeadTime_medio_s'):.2f} s) e IC separado dos demais. C2 e C4 têm ICs de lead time sobrepostos; não se escolhe entre eles apenas pela inspeção dos intervalos. C1 atende à meta de espera média abaixo de 300 s, com limite superior {float(stats[1,'EsperaBalcao_s']['ic95_superior']):.2f} s. A escolha de investimento depende de custos e metas adicionais, não modelados.

Não reutilizar os resultados anteriores. O relatório mistura janelas e contém afirmações incompatíveis com as chegadas ativas até o final. O [roteiro de atualização do GB](docs/ATUALIZAR_RELATORIO_GB.md) identifica cada seção, as tabelas antigas e os valores substitutos.

## Próximos passos

1. Publicar/revisar a branch preparada; a main remota permanece intacta.
2. Integrar a Pessoa 3 respeitando TipoPedido por cliente e refazer a experimentação.
3. Aplicar o roteiro de atualização ao fonte editável do relatório.
4. Conferir a animação nativa, gravar MP4 de até um minuto e atualizar slides.
5. Manter a declaração do uso de IA exigida pelo enunciado e assegurar que o grupo explique as decisões.

Detalhes: [preservação](docs/PRESERVACAO.md), [alterações e erros corrigidos](docs/ALTERACOES.md), [modelo conceitual](docs/MODELO_CONCEITUAL.md), [validação](docs/VALIDACAO.md).
'''
    (ROOT/'README.md').write_text(readme)

    table2=table([('Wq balcão (s)','EsperaBalcao_s',3),('Lq balcão (clientes)','FilaBalcao_media',4),('Média do máximo da fila (clientes)','FilaBalcao_max',3),('Espera tostadeira (s)','EsperaTostagem_s',3),('Wq caixa (s)','EsperaCaixa_s',3),('Lq caixa (clientes)','FilaCaixa_media',4),('Utilização média dos balcões (fração)','UtilizacaoBalcoes',4),('Utilização tostadeira (fração)','UtilizacaoTostadeira',4),('Utilização média dos caixas (fração)','UtilizacaoCaixas',4)])
    table3=table([('Lead time (s)','LeadTime_medio_s',3),('Gerados (clientes)','ClientesGerados',3),('Atendidos (clientes)','ClientesAtendidos',3),('Desistentes (clientes)','TotalDesistencias',3),('Remanescentes (clientes)','ClientesAindaNoSistema',3),('P90 por replicação (s)','P90_lead_time_s',3),('Vazão em 2,5 h (clientes/h)','Vazao_h',3)])
    report=f'''# Alterações necessárias no relatório atual do GB

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

{table2}

## Nova Tabela 3 — sistema e perdas

{table3}

Desistências totais em 30 replicações: C1=3, C2=0, C3=3, C4=3, C5=0. São os mesmos padrões de chegadas em cada cenário; não somar os cinco cenários como cinco amostras independentes. Os tipos foram conferidos em 1796 chegadas distintas: 717 simples (39,922%), 791 tradicionais (44,042%) e 288 complexos (16,036%).

Os IC t de desistências raras podem incluir valores negativos (limite inferior {float(stats[1,'TotalDesistencias']['ic95_inferior']):.4f}); isso é limitação da aproximação para a média e não uma contagem negativa. Relatar também totais e replicações com evento. Zero observado não comprova probabilidade real zero.

## Nova Tabela 4 — respostas às perguntas

| Pergunta | Evidência nova | Resposta e limite da conclusão |
|---|---|---|
| 1: C1 abaixo de 300 s? | Wq={mean(1,'EsperaBalcao_s'):.2f} s; IC95% {bounds(1,'EsperaBalcao_s')} s | Sim, inclusive o limite superior está abaixo da meta de média. Isso não significa que todo cliente espera menos de 300 s. |
| 2: C2 reduz Wq em pelo menos 40%? | {mean(1,'EsperaBalcao_s'):.2f} → {mean(2,'EsperaBalcao_s'):.2f} s; redução pontual {red_wait:.2f}%; ICs de médias separados | Sim na estimativa; diferença conclusiva pelo critério de IC. O percentual é razão de médias, não um IC de redução percentual. |
| 3: C3 aumenta W em mais de 20%? | {mean(1,'LeadTime_medio_s'):.2f} → {mean(3,'LeadTime_medio_s'):.2f} s; aumento pontual {inc_toast:.2f}% | Não na estimativa. ICs de W se sobrepõem: não concluir diferença por inspeção. O IC pareado complementar mostra diferença de 6,05 s [4,74;7,36], sem substituir a regra. |
| 4: C4 reduz W frente a C1? | {mean(1,'LeadTime_medio_s'):.2f} → {mean(4,'LeadTime_medio_s'):.2f} s; ICs {bounds(1,'LeadTime_medio_s')} e {bounds(4,'LeadTime_medio_s')} s | Sim; intervalos sem sobreposição. A antiga resposta negativa deve ser removida. |
| 5: C5 resolve aumento de espera no caixa de C2? | Wq caixa {mean(2,'EsperaCaixa_s'):.2f} → {mean(5,'EsperaCaixa_s'):.2f} s; W {mean(2,'LeadTime_medio_s'):.2f} → {mean(5,'LeadTime_medio_s'):.2f} s; Wq balcão idêntico {mean(2,'EsperaBalcao_s'):.2f} s | Reduz substancialmente a espera no caixa e o lead time, com ICs separados, sem perda no balcão. Não afirmar fila sempre nula. |

## Conclusão substituta e figuras

Sob as premissas sintéticas atuais, C1 já cumpre a meta de espera média de 300 s, com {mean(1,'EsperaBalcao_s'):.2f} s e IC95% {bounds(1,'EsperaBalcao_s')} s. C2/C5 reduzem essa espera para {mean(2,'EsperaBalcao_s'):.2f} s. C5 apresenta o menor lead time médio, {mean(5,'LeadTime_medio_s'):.2f} s, com IC95% {bounds(5,'LeadTime_medio_s')} s, usando três balcões e dois caixas. C2 e C4 têm lead times próximos, {mean(2,'LeadTime_medio_s'):.2f} e {mean(4,'LeadTime_medio_s'):.2f} s, e ICs sobrepostos. Não é possível escolher economicamente entre configurações sem custos de pessoal/equipamento e metas adicionais. Houve somente 3 desistências em 1796 chegadas nos cenários com dois balcões; zero nos de três balcões, sem evidência suficiente para afirmar risco nulo. Todas as 150 replicações terminaram esvaziadas.

Incluir `results/figures/fila_balcao_degraus.png` (C1, replicação 28; tempos exatos dos eventos), `espera_balcao_ic95.png` (indicador principal) e `lead_time_ic95.png` (complementar). Todos possuem título, eixos e unidades. O gráfico de uma replicação ilustra comportamento; as conclusões usam as 30 replicações.

Acrescentar seção de validação com a falha de sintaxe recebida, correção do horário, teste fila 5/6, exclusão de desistentes do lead time, auditoria de 8980 registros de chegada em cinco cenários e conservação independente. A versão final do relatório deve declarar que múltiplos itens/Pessoa 3, revisão visual nativa e vídeo ainda não estão concluídos nesta etapa.
'''
    (ROOT/'docs/ATUALIZAR_RELATORIO_GB.md').write_text(report)

if __name__=='__main__':main()
