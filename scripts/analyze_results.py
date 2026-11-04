#!/usr/bin/env python3
"""Audit all customer traces, then calculate replication-level Student t intervals."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse
import csv
import json
import math
import statistics
import numpy as np
from scipy import stats
from result_io import read_dat,read_log_replications
from run_model import ROOT

def write_csv(path,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def ci(values):
    n=len(values);mean=statistics.fmean(values);sd=statistics.stdev(values)
    half=float(stats.t.ppf(.975,n-1))*sd/math.sqrt(n)
    return {'media':mean,'desvio_padrao':sd,'n':n,'ic95_inferior':mean-half,'ic95_superior':mean+half,'semi_amplitude':half}

def unit(k):
    if k.endswith('_s'):return 's'
    if k.endswith('_h'):return 'clientes/h'
    if k.startswith('Utilizacao') or k=='TaxaDesistencia':return 'fracao'
    if k=='Substream':return 'indice'
    return 'clientes'

def close(a,b,tol=2e-6):
    assert abs(a-b)<=tol,(a,b,abs(a-b))

def audit_rep(n,r,logs):
    rep=int(r['Replication'])
    a,d,m,s,e=[logs[x][rep] for x in ['LogChegadas','LogDesistencias','LogMontagem','LogAtendidos','LogEstado']]
    ids=lambda rows:{v['this.obj.Name'] for v in rows}
    assert len(a)==len(ids(a))==r['ClientesGerados']
    assert len(d)==len(ids(d))==r['TotalDesistencias']
    assert len(s)==len(ids(s))==r['ClientesAtendidos']==r['AmostrasLeadTime']==r['ClientesPagos']
    assert len(m)==len(ids(m))==r['ClientesMontados']
    assert ids(d).isdisjoint(ids(s)|ids(m))
    assert ids(d)|ids(s)<=ids(a)
    assert r['ClientesGerados']==r['ClientesAtendidos']+r['TotalDesistencias']+r['ClientesAindaNoSistema']
    assert r['TempoFinal_s']==9000 and r['TempoGeradorAberto_s']==5400
    assert r['Substream']==rep
    assert all(v['this.SimTime/1[s]']<5400 for v in a)
    assert r['UltimaChegada_s']==max(v['this.SimTime/1[s]'] for v in a)
    assert all(v['this.obj.FilaNaChegada']>=6 for v in d)
    assert all(v['this.obj.FilaNaChegada']<=5 for v in s)
    assert ids(d)=={v['this.obj.Name'] for v in a if v['this.obj.FilaNaChegada']>5}
    if r['ClientesAindaNoSistema']==0:assert ids(a)==ids(d)|ids(s) and ids(m)==ids(s)
    arrival_map={v['this.obj.Name']:v for v in a}
    for v in a:
        low,high={1:(45,110),2:(75,160),3:(120,240)}[int(v['this.obj.TipoPedido'])]
        assert low<=v['this.obj.TempoMontagem/1[s]']<=high
        close(v['this.SimTime/1[s]'],v['this.obj.HoraChegada/1[s]'])
    for v in m+s:
        for k in ['this.obj.TipoPedido','this.obj.TempoMontagem/1[s]','this.obj.HoraChegada/1[s]']:
            assert v[k]==arrival_map[v['this.obj.Name']][k]
        close(v['this.obj.StateTimes("Montagem")/1[s]'],v['this.obj.TempoMontagem/1[s]'])
    for v in s:
        lead=v['(this.SimTime-this.obj.HoraChegada)/1[s]']
        close(lead,v['this.SimTime/1[s]']-v['this.obj.HoraChegada/1[s]'])
        close(lead,sum(v[f'this.obj.StateTimes("{state}")/1[s]'] for state in ['Montagem','EsperaBalcao','EsperaTostagem','Tostagem','EsperaCaixa','Pagamento']))
    leads=[v['(this.SimTime-this.obj.HoraChegada)/1[s]'] for v in s]
    close(statistics.fmean(leads),r['LeadTime_medio_s'])
    # Served-only traces cannot reconstruct service/queue totals for unfinished clients.
    # Keep the independent conservation audit, and record which equalities are applicable.
    emptied=r['ClientesAindaNoSistema']==0
    if emptied:
        close(statistics.fmean(v['this.obj.StateTimes("EsperaBalcao")/1[s]'] for v in s),r['EsperaBalcao_s'])
        close(statistics.fmean(v['this.obj.StateTimes("EsperaCaixa")/1[s]'] for v in s),r['EsperaCaixa_s'])
        nb=3 if n in (2,5) else 2;nc=2 if n in (4,5) else 1
        for state,metric,count in [('Montagem','UtilizacaoBalcoes',nb),('Tostagem','UtilizacaoTostadeira',1),('Pagamento','UtilizacaoCaixas',nc)]:
            close(sum(v[f'this.obj.StateTimes("{state}")/1[s]'] for v in s)/9000/count,r[metric])
        assert sum(v['this.obj.StateTimes("Tostagem")/1[s]']>0 for v in s)==r['ClientesTostados']
    # Independent occupancy at event-complete observations, and queue area identities.
    for v in e:
        assert v['[ChegadaClientes].NumberGenerated']==v['[Saida].NumberAdded']+v['[SaidaDesistencia].NumberAdded']+v['[Simulation].ClientesAindaNoSistema']
    for queue,metric in [('FilaBalcao','FilaBalcao_media'),('FilaCaixa','FilaCaixa_media')]:
        area=sum(v[f'[{queue}].QueueLength']*((e[i+1]['this.SimTime/1[s]'] if i+1<len(e) else 9000)-v['this.SimTime/1[s]']) for i,v in enumerate(e))
        close(area/9000,r[metric])
    parallel=sum(v.get('[Caixa1].NumberInProgress',0)==1 and v.get('[Caixa2].NumberInProgress',0)==1 for v in e)
    if n in (4,5):assert parallel>0
    r['P90_lead_time_s']=float(np.quantile(leads,.9,method='linear'))
    r['TaxaDesistencia']=len(d)/len(a)
    r['VazaoJanelaDemanda_h']=len(s)/1.5
    return {'cenario':n,'replicacao':rep,'conservacao':True,'remanescentes':r['ClientesAindaNoSistema'],'reconstrucao_totais_por_concluidos_aplicavel':emptied,'ultima_chegada_s':r['UltimaChegada_s'],'clientes_auditados':len(a),'desistentes':len(d),'observacoes_caixas_simultaneos':parallel,'eventos_estado_auditados':len(e)}

def main():
    p=argparse.ArgumentParser();p.add_argument('runs',type=Path,nargs='?',default=ROOT/'results/runs');a=p.parse_args()
    out=a.runs.parent;data={};all_logs={};audits=[];all_rows=[]
    for n in range(1,6):
        folder=a.runs/f'cenario{n}'
        rows=read_dat(folder/f'cenario{n}.dat')
        assert len(rows)==30 and [r['Replication'] for r in rows]==list(range(1,31))
        logs={name:read_log_replications(folder/f'cenario{n}-{name}.log') for name in ['LogChegadas','LogDesistencias','LogMontagem','LogAtendidos','LogEstado']}
        assert all(set(g)==set(range(1,31)) for g in logs.values())
        for r in rows:
            audits.append(audit_rep(n,r,logs));r['cenario']=n
        data[n]=rows;all_logs[n]=logs;all_rows+=rows
    # Shared arrival/type/mounting draws: compare exact per-customer records across scenarios.
    for n in range(2,6):
        for rep in range(1,31):
            keys=['this.obj.Name','this.obj.TipoPedido','this.obj.TempoMontagem/1[s]','this.obj.HoraChegada/1[s]']
            assert [[v[k] for k in keys] for v in all_logs[1]['LogChegadas'][rep]]==[[v[k] for k in keys] for v in all_logs[n]['LogChegadas'][rep]]
    all_a=[v for group in all_logs[1]['LogChegadas'].values() for v in group]
    counts=Counter(int(v['this.obj.TipoPedido']) for v in all_a)
    proportions=[{'tipo':k,'n':counts[k],'fracao_observada':counts[k]/len(all_a),'fracao_definida':prob} for k,prob in [(1,.4),(2,.45),(3,.15)]]
    chi=stats.chisquare([counts[i] for i in (1,2,3)],np.array([.4,.45,.15])*len(all_a))
    sample_checks=[]
    for tipo,(low,mode,high) in {1:(45,70,110),2:(75,110,160),3:(120,170,240)}.items():
        values=[v['this.obj.TempoMontagem/1[s]'] for v in all_a if v['this.obj.TipoPedido']==tipo]
        ks=stats.kstest(values,'triang',args=((mode-low)/(high-low),low,high-low))
        sample_checks.append({'tipo':tipo,'n':len(values),'media_observada_s':statistics.fmean(values),'media_teorica_s':(low+mode+high)/3,'min_amostra_s':min(values),'max_amostra_s':max(values),'ks_D':float(ks.statistic),'ks_p':float(ks.pvalue)})
    summary=[]
    for n,rows in data.items():
        for k in rows[0]:
            if k in ['Scenario','Replication','cenario','Substream','UltimaChegada_s','TempoFinal_s','TempoGeradorAberto_s']:continue
            summary.append({'cenario':n,'indicador':k,'unidade':unit(k),**ci([r[k] for r in rows])})
    lookup={(r['cenario'],r['indicador']):r for r in summary}
    comps=[]
    for metric in ['EsperaBalcao_s','LeadTime_medio_s','EsperaCaixa_s']:
        for left,right in combinations(range(1,6),2):
            x=lookup[left,metric];y=lookup[right,metric]
            nonoverlap=x['ic95_superior']<y['ic95_inferior'] or y['ic95_superior']<x['ic95_inferior']
            diff=ci([b[metric]-a[metric] for a,b in zip(data[left],data[right])])
            comps.append({'indicador':metric,'cenario_A':left,'cenario_B':right,'criterio_disciplina':'diferenca_conclusiva' if nonoverlap else 'inconclusivo_por_sobreposicao','diferenca_B_menos_A':diff['media'],'ic95_diferenca_inferior':diff['ic95_inferior'],'ic95_diferenca_superior':diff['ic95_superior'],'metodo_complementar':'t pareado por replicacao; sem correcao de multiplicidade'})
    write_csv(out/'replicacoes.csv',all_rows);write_csv(out/'resumo_ic95.csv',summary);write_csv(out/'comparacoes_ic95.csv',comps)
    write_csv(out/'conservacao.csv',audits);write_csv(out/'tipos_pedido.csv',proportions);write_csv(out/'montagem_amostras.csv',sample_checks)
    validation={'passed':True,'replicacoes':len(audits),'total_clientes_auditados':sum(r['clientes_auditados'] for r in audits),'chegadas_independentes_para_teste_distribuicao':len(all_a),'tipos':proportions,'chi2':float(chi.statistic),'chi2_p':float(chi.pvalue),'max_remanescentes':max(r['remanescentes'] for r in audits),'ultima_chegada_global_s':max(r['ultima_chegada_s'] for r in audits),'seeds_pareados_confirmados':True,'total_desistencias_por_cenario':{n:int(sum(r['TotalDesistencias'] for r in rows)) for n,rows in data.items()},'montagem':sample_checks}
    (out/'validation_summary.json').write_text(json.dumps(validation,indent=2))
    lines=['# Resultados reais da versão Pessoa 1 + Pessoa 2','','JaamSim 2026-08; 30 replicações por cenário; 9000 s por replicação; chegadas em [0,5400) s. Valores abaixo são médias entre replicações ± semi-amplitude IC95% t de Student (29 graus de liberdade).','','| Cenário | Espera balcão (s) | Lead time (s) | P90 por replicação (s) | Atendidos | Desistentes | Remanescentes | Vazão (clientes/h em 2,5 h) |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for n in range(1,6):
        cells=[str(n)]
        for k in ['EsperaBalcao_s','LeadTime_medio_s','P90_lead_time_s','ClientesAtendidos','TotalDesistencias','ClientesAindaNoSistema','Vazao_h']:
            r=lookup[n,k];cells.append(f"{r['media']:.3f} ± {r['semi_amplitude']:.3f}")
        lines.append('| '+' | '.join(cells)+' |')
    lines += ['', 'O indicador principal comum aos cinco cenários é a espera média no balcão. Lead time é indicador complementar. P90 é calculado por replicação (interpolação linear) e depois resumido; não é um percentil de médias nem um agrupamento dos 150 experimentos.', '', 'Utilização e comprimentos médios de fila usam toda a janela de 9000 s, inclusive o esvaziamento. VazaoJanelaDemanda_h usa 1,5 h como denominador e está separada no CSV. Não comparar utilizações destas tabelas com números antigos medidos em outra janela.', '', 'ICs sobrepostos não permitem concluir diferença pelo critério da disciplina. O CSV de comparações também fornece IC t pareado da diferença como análise complementar, sem substituir esse critério. IC t da média de desistências pode apresentar limite inferior negativo devido à raridade do evento; não representa contagem negativa e não deve ser truncado silenciosamente.', '', '## Todos os indicadores', '', '| Cenário | Indicador | Unidade | Média | DP | n | IC95% inferior | IC95% superior | Semi-amplitude |','|---|---|---|---:|---:|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f"| {r['cenario']} | {r['indicador']} | {r['unidade']} | {r['media']:.6f} | {r['desvio_padrao']:.6f} | {r['n']} | {r['ic95_inferior']:.6f} | {r['ic95_superior']:.6f} | {r['semi_amplitude']:.6f} |")
    (out/'resumo.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(validation,indent=2))

if __name__=='__main__':main()
