#!/usr/bin/env python3
"""Integrate Pessoa 2 onto the unchanged, versioned Pessoa 1 configurations."""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]

def set_input(text, entity, keyword, value):
    pattern = re.compile(rf'(?m)^{re.escape(entity)}\s+{re.escape(keyword)}\s*\{{')
    match = pattern.search(text)
    if not match:
        return text + f'\n{entity} {keyword} {{ {value} }}\n'
    depth = 1
    pos = match.end()
    while depth:
        depth += (text[pos] == '{') - (text[pos] == '}')
        pos += 1
    return text[:match.start()] + f'{entity} {keyword} {{ {value} }}' + text[pos:]

def build(n):
    base = ROOT / f'docs/baselines/pessoa1/tgb_subway_cenario{n}.cfg'
    # Retain all active base inputs, including graphical layout and unused MontagemDist.
    text = '\n'.join(l for l in base.read_text().splitlines() if not l.lstrip().startswith('#'))
    text = re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'
    text = f'# Cenario {n}: base integral da Pessoa 1 + integracao validada da Pessoa 2.\n# Fonte preservada em docs/baselines/pessoa1/. Ver docs/ALTERACOES.md.\n# MontagemDist permanece como referencia historica, sem uso pelos balcoes.\n' + text
    balcoes = [f'Balcao{i}' for i in range(1, 4 if n in (2, 5) else 3)]
    caixas = ['Caixa1','Caixa2'] if n in (4,5) else ['Caixa']
    text = set_input(text,'ChegadaClientes','NextComponent','ClassificaPedido')
    for b in balcoes:
        text = set_input(text,b,'ServiceTime',"'this.obj.TempoMontagem'")
        # Pessoa 3: cada lanche montado segue para a fila de reuniao do pedido.
        # Pessoa 4: passa antes por LogLanches (registro por item, tempo zero).
        text = set_input(text,b,'NextComponent','LogLanches')
    text = set_input(text,'EstatSistema','NextComponent','LogAtendidos')
    text = set_input(text,'EstatSistema','SampleValue',"'this.SimTime - this.obj.HoraChegada'")
    text = set_input(text,'Simulation','RunOutputList','')
    text += '''
# ---- Pessoa 2: uma classificacao por CLIENTE, inclusive desistentes ----
Define Assign { ClassificaPedido SorteiaMontagem }
Define Branch { DecisaoDesistencia }
Define EntitySink { SaidaDesistencia }
Define DiscreteDistribution { TipoPedidoDist }
Define TriangularDistribution { MontagemSimplesDist MontagemTradicionalDist MontagemComplexoDist }
Define TimeSeries { JanelaChegadas }
Define TimeSeriesThreshold { HorarioPico }
Define EntityLogger { LogChegadas LogDesistencias LogMontagem LogAtendidos }
Define ExpressionLogger { LogEstado }
Define OverlayText { TextoAtendidos TextoDesistencias TextoLeadTime TextoFila }
Define Graph { GraficoFila }

Cliente AttributeDefinitionList {
 { TipoPedido 0 } { TempoMontagem 0[s] } { HoraChegada 0[s] } { FilaNaChegada 0 }
}
TipoPedidoDist UnitType { DimensionlessUnit }
TipoPedidoDist RandomSeed { 9 }
TipoPedidoDist ValueList { 1 2 3 }
TipoPedidoDist ProbabilityList { 0.40 0.45 0.15 }
# Pessoa 3: distribuicao de QuantidadeLanches, definida ANTES de ClassificaPedido
# para que a unidade (DimensionlessUnit) ja esteja resolvida no uso do atributo.
Define DiscreteDistribution { QtdLanchesDist }
QtdLanchesDist UnitType { DimensionlessUnit }
QtdLanchesDist RandomSeed { 13 }
QtdLanchesDist ValueList { 1 2 3 }
QtdLanchesDist ProbabilityList { 0.70 0.22 0.08 }
'''
    for name,seed,low,mode,high in [('Simples',10,45,70,110),('Tradicional',11,75,110,160),('Complexo',12,120,170,240)]:
        text += f'''Montagem{name}Dist UnitType {{ TimeUnit }}
Montagem{name}Dist RandomSeed {{ {seed} }}
Montagem{name}Dist MinValue {{ {low} s }}
Montagem{name}Dist Mode {{ {mode} s }}
Montagem{name}Dist MaxValue {{ {high} s }}
'''
    text += '''
# Fechamento agendado EXATAMENTE em 5400 s, sem concluir intervalo pendente.
JanelaChegadas UnitType { DimensionlessUnit }
JanelaChegadas Value { { 0 s 1 } { 5400 s 0 } }
HorarioPico UnitType { DimensionlessUnit }
HorarioPico TimeSeries { JanelaChegadas }
HorarioPico MinOpenLimit { 0.5 }
ChegadaClientes ImmediateThresholdList { HorarioPico }
# FirstArrivalTime continua no padrao da base: primeira chegada em t=0.
ChegadaClientes FirstArrivalTime { 0 s }

ClassificaPedido AttributeAssignmentList {
 { 'this.obj.HoraChegada = this.SimTime' }
 { 'this.obj.TipoPedido = [TipoPedidoDist].Value' }
 { 'this.obj.FilaNaChegada = [FilaBalcao].QueueLength' }
}
ClassificaPedido NextComponent { SorteiaMontagem }
SorteiaMontagem AttributeAssignmentList {
 'this.obj.TempoMontagem = this.obj.TipoPedido == 1 ? [MontagemSimplesDist].Value : this.obj.TipoPedido == 2 ? [MontagemTradicionalDist].Value : [MontagemComplexoDist].Value'
}
SorteiaMontagem NextComponent { LogChegadas }
LogChegadas NextComponent { DecisaoDesistencia }
DecisaoDesistencia Choice { '[FilaBalcao].QueueLength > 5 ? 2 : 1' }
DecisaoDesistencia NextComponentList { FilaBalcao LogDesistencias }
LogDesistencias NextComponent { SaidaDesistencia }
LogMontagem NextComponent { RotaTostagem }
LogAtendidos NextComponent { Saida }

# Estados permitem verificar tempos realizados, sem alterar duracoes ou rotas.
FilaBalcao StateAssignment { EsperaBalcao }
FilaTostagem StateAssignment { EsperaTostagem }
FilaCaixa StateAssignment { EsperaCaixa }
Tostadeira StateAssignment { Tostagem }
'''
    for b in balcoes: text += f'{b} StateAssignment {{ Montagem }}\n'
    for c in caixas: text += f'{c} StateAssignment {{ Pagamento }}\n'
    # Pessoa 4: ClienteID e QuantidadeLanches identificam o pedido em todos os
    # registros; o Combine pode devolver uma copia (ClienteN_Dup1) como entidade
    # do pedido, entao a auditoria usa ClienteID e nao o nome da entidade.
    log_fields = ['this.obj.Name','this.obj.ClienteID','this.obj.QuantidadeLanches','this.obj.TipoPedido','this.obj.TempoMontagem/1[s]','this.obj.HoraChegada/1[s]','this.obj.FilaNaChegada']
    for log in ['LogChegadas','LogDesistencias','LogMontagem','LogAtendidos']:
        fields = log_fields.copy()
        if log in ['LogMontagem','LogAtendidos']:
            fields += ['(this.SimTime-this.obj.HoraChegada)/1[s]', 'this.obj.StateTimes("Montagem")/1[s]']
        if log == 'LogAtendidos':
            fields += [f'this.obj.StateTimes("{state}")/1[s]' for state in ['EsperaBalcao','EsperaReuniao','EsperaTostagem','Tostagem','EsperaCaixa','Pagamento']]
        text += f"{log} DataSource {{ " + ' '.join("{ '"+f+"' }" for f in fields) + ' }\n'

    # ---- Pessoa 4: registro de cada lanche montado (item), antes da reuniao ----
    lanche_fields = ['this.obj.Name','this.obj.ClienteID','this.obj.QuantidadeLanches','this.obj.TipoPedido','this.obj.TempoMontagem/1[s]','this.obj.HoraChegada/1[s]','this.obj.StateTimes("EsperaBalcao")/1[s]','this.obj.StateTimes("Montagem")/1[s]']
    text += '\nDefine EntityLogger { LogLanches }\n'
    text += 'LogLanches NextComponent { FilaReuniao }\n'
    text += 'LogLanches DataSource { ' + ' '.join("{ '"+f+"' }" for f in lanche_fields) + ' }\n'
    text += 'LogLanches Position { -0.6 0.5 0 m }\n'

    # ---- Pessoa 3: pedidos com multiplos lanches, duplicacao e reuniao ----
    # QuantidadeLanches (atributo com significado) decide quantas entidades de
    # producao o pedido gera; o Duplicate cria os lanches extras, os balcoes os
    # montam em paralelo (respeitando a capacidade instalada) e o Combine reune
    # todos os lanches do mesmo cliente antes do pagamento, devolvendo UMA
    # entidade por pedido. ClienteID identifica o pedido para o casamento (Match).
    text += '''
Define Duplicate { DuplicaLanches }
Define Queue { FilaReuniao }
Define Combine { ReuneLanches }
Define OverlayText { TextoLanches TextoReuniao }

# Duplicacao das entidades de producao: 1 original + (QuantidadeLanches - 1) copias.
DuplicaLanches NextComponent { FilaBalcao }
DuplicaLanches TargetComponentList { FilaBalcao }
DuplicaLanches NumberOfDuplicates { 'this.obj.QuantidadeLanches - 1' }

# Reuniao antes do pagamento: o Combine agrupa pelo ClienteID (Match na fila) e
# exige exatamente QuantidadeLanches lanches do pedido lider; mantem a entidade
# cliente (com HoraChegada/TipoPedido) e consome as copias. A espera na
# FilaReuniao e a "espera do lote", que nao ocupa nenhum recurso.
FilaReuniao Match { 'this.obj.ClienteID' }
FilaReuniao StateAssignment { EsperaReuniao }
ReuneLanches WaitQueueList { FilaReuniao }
ReuneLanches MatchRequired { TRUE }
ReuneLanches NumberRequired { '[FilaReuniao].QueueLength > 0 ? [FilaReuniao].QueueList(1).QuantidadeLanches : 1' }
ReuneLanches NextComponent { LogMontagem }
'''
    # Atributos do cliente: acrescenta ClienteID e QuantidadeLanches, preservando
    # os da Pessoa 2. O cliente continua dono do pedido durante todo o fluxo.
    text = set_input(text,'Cliente','AttributeDefinitionList',
        '{ TipoPedido 0 } { TempoMontagem 0[s] } { HoraChegada 0[s] } { FilaNaChegada 0 } { ClienteID 0 } { QuantidadeLanches 1 }')
    # ClienteID e QuantidadeLanches sorteados uma vez por cliente, inclusive
    # desistentes, antes de qualquer duplicacao (contrato da Pessoa 3).
    text = set_input(text,'ClassificaPedido','AttributeAssignmentList',
        "{ 'this.obj.HoraChegada = this.SimTime' } "
        "{ 'this.obj.ClienteID = [ChegadaClientes].NumberGenerated' } "
        "{ 'this.obj.TipoPedido = [TipoPedidoDist].Value' } "
        "{ 'this.obj.QuantidadeLanches = [QtdLanchesDist].Value' } "
        "{ 'this.obj.FilaNaChegada = [FilaBalcao].QueueLength' }")
    # Quem entra segue para a duplicacao; o desistente nao gera lanches.
    text = set_input(text,'DecisaoDesistencia','NextComponentList','DuplicaLanches LogDesistencias')

    # Balancos: pedidos (ordem) usam o gerador e as saidas; itens (lanches) usam
    # os balcoes e a fila de reuniao. Nao se conta lanche como cliente.
    sandus = ' + '.join(f'[{s}].NumberInProgress' for s in balcoes) + ' + [FilaBalcao].QueueLength + [FilaReuniao].QueueLength'
    pagamento = '[FilaTostagem].QueueLength + [Tostadeira].NumberInProgress + [FilaCaixa].QueueLength + ' + ' + '.join(f'[{c}].NumberInProgress' for c in caixas)
    montados = ' + '.join(f'[{b}].NumberProcessed' for b in balcoes)
    metrics = {
        'ClientesGerados': '[ChegadaClientes].NumberGenerated',
        'ClientesAtendidos': '[Saida].NumberAdded',
        'TotalDesistencias': '[SaidaDesistencia].NumberAdded',
        'ClientesAindaNoSistema': '[ChegadaClientes].NumberGenerated - [Saida].NumberAdded - [SaidaDesistencia].NumberAdded',
        'SanduichesMontados': montados,
        'PedidosReunidos': '[ReuneLanches].NumberProcessed',
        'SanduichesNoSistema': sandus,
        'PedidosNoPagamento': pagamento,
        'EsperaReuniao_s': '[FilaReuniao].AverageQueueTime/1[s]',
        'FilaReuniao_media': '[FilaReuniao].QueueLengthAverage',
        'EsperaBalcao_s': '[FilaBalcao].AverageQueueTime/1[s]',
        'FilaBalcao_media': '[FilaBalcao].QueueLengthAverage',
        'FilaBalcao_max': '[FilaBalcao].QueueLengthMaximum',
        'EsperaCaixa_s': '[FilaCaixa].AverageQueueTime/1[s]',
        'FilaCaixa_media': '[FilaCaixa].QueueLengthAverage',
        'EsperaTostagem_s': '[FilaTostagem].AverageQueueTime/1[s]',
        'FilaTostagem_media': '[FilaTostagem].QueueLengthAverage',
        'UtilizacaoBalcoes': '('+' + '.join(f'[{b}].Utilisation' for b in balcoes)+f')/{len(balcoes)}',
        'UtilizacaoTostadeira': '[Tostadeira].Utilisation',
        'UtilizacaoCaixas': '('+' + '.join(f'[{c}].Utilisation' for c in caixas)+f')/{len(caixas)}',
        'LeadTime_medio_s': '[EstatSistema].SampleAverage/1[s]',
        # Pessoa 4: dispersao e maximo do lead time dentro da replicacao.
        'LeadTime_dp_s': '[EstatSistema].SampleStandardDeviation/1[s]',
        'LeadTime_max_s': '[EstatSistema].SampleMaximum/1[s]',
        # Vazao em pedidos/h e lanches/h sobre a janela total (2,5 h).
        'Vazao_h': '[Saida].NumberAdded/(this.SimTime/1[h])',
        'VazaoLanches_h': '(' + montados + ')/(this.SimTime/1[h])',
        'UltimaChegada_s': '[LogChegadas].LogTime/1[s]',
        'TempoFinal_s': 'this.SimTime/1[s]',
        'AmostrasLeadTime': '[EstatSistema].NumberAdded',
        'ClientesMontados': '[RotaTostagem].NumberAdded',
        'ClientesTostados': '[Tostadeira].NumberProcessed',
        'ClientesPagos': ' + '.join(f'[{c}].NumberProcessed' for c in caixas),
        'TempoGeradorAberto_s': '[HorarioPico].OpenFraction*this.SimTime/1[s]',
        'Substream': 'this.ReplicationNumber',
    }
    for s in balcoes+caixas: metrics['Utilizacao'+s] = f'[{s}].Utilisation'
    text += '\n# Indicadores numericos; definidos ANTES de RunOutputList.\nSimulation CustomOutputList {\n'
    text += '\n'.join(f" {{ {k} '{v}' DimensionlessUnit }}" for k,v in metrics.items())+'\n}\n'
    text += "Simulation RunOutputList {\n"+'\n'.join(f" {{ '[Simulation].{k}' }}" for k in metrics)+'\n}\n'
    text += '''
# Serie temporal por mudanca de estado; preserva degraus, sem amostragem arbitraria.
LogEstado Interval { }
LogEstado ValueTraceList { { [FilaBalcao].QueueLength } { [FilaCaixa].QueueLength } { [HorarioPico].Open } }
LogEstado DataSource { { [FilaBalcao].QueueLength } { [FilaCaixa].QueueLength } { [ChegadaClientes].NumberGenerated } { [Saida].NumberAdded } { [SaidaDesistencia].NumberAdded } { [Simulation].ClientesAindaNoSistema } }

# Complementos visuais. Os objetos originais mantem seu layout.
ClassificaPedido Position { -7 2 0 m }
SorteiaMontagem Position { -5.8 2 0 m }
LogChegadas Position { -4.6 2 0 m }
DecisaoDesistencia Position { -3.5 2 0 m }
LogDesistencias Position { -3.5 3.2 0 m }
SaidaDesistencia Position { -1.8 3.2 0 m }
LogMontagem Position { 0 2.5 0 m }
LogAtendidos Position { 9 1.8 0 m }
DuplicaLanches Position { -2.6 1.3 0 m }
FilaReuniao Position { 0.2 0.5 0 m }
ReuneLanches Position { 0.7 0.5 0 m }
QtdLanchesDist Position { 2 -5 0 m }
JanelaChegadas Position { -7 -3 0 m }
HorarioPico Position { -5 -3 0 m }
TipoPedidoDist Position { -7 -4 0 m }
MontagemSimplesDist Position { -4 -4 0 m }
MontagemTradicionalDist Position { -2 -4 0 m }
MontagemComplexoDist Position { 0 -4 0 m }
LogEstado Position { 2 -4 0 m }

TextoAtendidos ScreenPosition { 15 45 }
TextoAtendidos Format { 'Atendidos: %.0f pedidos' }
TextoAtendidos DataSource { [Saida].NumberAdded }
TextoDesistencias ScreenPosition { 15 65 }
TextoDesistencias Format { 'Desistencias: %.0f clientes' }
TextoDesistencias DataSource { [SaidaDesistencia].NumberAdded }
TextoLeadTime ScreenPosition { 15 85 }
TextoLeadTime Format { 'Lead time medio: %.1f s' }
TextoLeadTime DataSource { '[EstatSistema].SampleAverage/1[s]' }
TextoFila ScreenPosition { 15 105 }
TextoFila Format { 'Fila balcao: %.0f lanches aguardando' }
TextoFila DataSource { [FilaBalcao].QueueLength }
TextoLanches ScreenPosition { 15 125 }
TextoLanches Format { 'Lanches montados: %.0f lanches' }
TextoLanches DataSource { '[Simulation].SanduichesMontados' }
TextoReuniao ScreenPosition { 15 145 }
TextoReuniao Format { 'Espera de reuniao: %.1f s' }
TextoReuniao DataSource { '[FilaReuniao].AverageQueueTime/1[s]' }
GraficoFila Position { 5 -3 0 m }
GraficoFila Size { 7 3 m }
GraficoFila Title { 'Estado em tempo real: lanches no balcao e pedidos em reuniao' }
GraficoFila UnitType { DimensionlessUnit }
GraficoFila DataSource { { [FilaBalcao].QueueLength } { [FilaReuniao].QueueLength } }
GraficoFila LineColours { { blue } { orange } }
GraficoFila XAxisTitle { 'Tempo relativo ao instante atual (min)' }
GraficoFila XAxisUnit { min }
GraficoFila XAxisStart { -90 min }
GraficoFila XAxisEnd { 0 min }
GraficoFila XAxisInterval { 15 min }
GraficoFila YAxisTitle { 'Itens (lanches)' }
GraficoFila YAxisStart { 0 }
GraficoFila YAxisEnd { 10 }
GraficoFila YAxisInterval { 2 }
GraficoFila NumberOfPoints { 901 }
'''
    traces = ['[FilaBalcao].QueueLength','[FilaReuniao].QueueLength','[FilaCaixa].QueueLength','[HorarioPico].Open'] + [f'[{s}].NumberInProgress' for s in balcoes+['Tostadeira']+caixas]
    state_data = ['[FilaBalcao].QueueLength','[FilaReuniao].QueueLength','[FilaCaixa].QueueLength','[ChegadaClientes].NumberGenerated','[Saida].NumberAdded','[SaidaDesistencia].NumberAdded','[Simulation].ClientesAindaNoSistema','[Simulation].SanduichesMontados']+[f'[{s}].NumberInProgress' for s in balcoes+['Tostadeira']+caixas]
    text=set_input(text,'LogEstado','ValueTraceList',' '.join('{ '+f+' }' for f in traces))
    text=set_input(text,'LogEstado','DataSource',' '.join('{ '+f+' }' for f in state_data))
    # JaamSim resolves entity references at input time: declare all objects first.
    lines=text.splitlines()
    definitions=[l for l in lines if l.startswith('Define ')]
    lines=[l for l in lines if not l.startswith('Define ')]
    text='\n'.join(lines).replace('Simulation RunOutputList {  }\n','').replace('RecordEdits','RecordEdits\n\n'+'\n'.join(definitions),1)
    return text+'\n'

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--scenario',type=int,choices=range(1,6));a=p.parse_args()
    for n in ([a.scenario] if a.scenario else range(1,6)):
        out=ROOT/f'models/cenario{n}.cfg';out.write_text(build(n));print(out.relative_to(ROOT))
