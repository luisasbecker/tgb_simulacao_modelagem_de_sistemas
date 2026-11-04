#!/usr/bin/env python3
"""Deterministic integration tests run through the actual JaamSim engine."""
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_model import run_model, ROOT
from result_io import read_dat, numeric_logger, read_log_replications

def test(name,overrides):
    work=ROOT/'results/validation'/name
    work.mkdir(parents=True,exist_ok=True)
    cfg=work/f'{name}.cfg'
    cfg.write_text((ROOT/'models/cenario1.cfg').read_text()+'\nSimulation NumberOfReplications { 1 }\n'+overrides)
    run_model(cfg)
    # Cutoff fixtures have zero or one client; unused queues have undefined averages.
    result=read_dat(cfg.with_suffix('.dat'),allow_nonfinite=name.startswith('cut_'))
    assert len(result)==1
    return result[0],cfg

def main():
    records=[]
    row,cfg=test('smoke','Simulation RunDuration { 600 s }\n')
    assert row['TempoFinal_s']==600
    assert row['ClientesGerados']==row['ClientesAtendidos']+row['TotalDesistencias']+row['ClientesAindaNoSistema']
    records.append({'test':'smoke','passed':True,'remaining_expected':row['ClientesAindaNoSistema']})
    row,cfg=test('boundary_queue', '''ChegadaClientes InterArrivalTime { 1 s }
ChegadaClientes MaxNumber { 10 }
SorteiaMontagem AttributeAssignmentList { 'this.obj.TempoMontagem = 100[s]' }
''')
    arrivals=numeric_logger(cfg.with_name('boundary_queue-LogChegadas.log'))
    rejected=numeric_logger(cfg.with_name('boundary_queue-LogDesistencias.log'))
    completed=numeric_logger(cfg.with_name('boundary_queue-LogAtendidos.log'))
    assert row['ClientesGerados']==10 and row['ClientesAtendidos']==8 and row['TotalDesistencias']==2
    assert row['ClientesAindaNoSistema']==0 and row['FilaBalcao_max']==6
    assert all(r['this.obj.FilaNaChegada']==6 for r in rejected)
    assert any(r['this.obj.FilaNaChegada']==5 for r in completed)
    assert {r['this.obj.Name'] for r in completed}.isdisjoint(r['this.obj.Name'] for r in rejected)
    assert len(completed)==row['AmostrasLeadTime']==row['ClientesPagos']
    records.append({'test':'boundary_queue','passed':True,'generated':10,'served':8,'rejected':2,'max_queue':6})
    for name,first,inter,expected in [('cut_before',5399,2,1),('cut_exact',5400,1,0),('cut_pending',0,5400,1)]:
        row,cfg=test(name,f'ChegadaClientes FirstArrivalTime {{ {first} s }}\nChegadaClientes InterArrivalTime {{ {inter} s }}\n')
        assert row['ClientesGerados']==expected,(name,row)
        assert row['TempoFinal_s']==9000 and row['TempoGeradorAberto_s']==5400
        arrivals=numeric_logger(cfg.with_name(name+'-LogChegadas.log'))
        assert all(r['this.SimTime/1[s]']<5400 for r in arrivals)
        records.append({'test':name,'passed':True,'generated':expected})
    row,cfg=test('remaining_clients', '''ChegadaClientes InterArrivalTime { 1 s }
ChegadaClientes MaxNumber { 10 }
Caixa ServiceTime { 3600 s }
''')
    # Stress fixture only: long payment intentionally leaves real entities unfinished.
    from analyze_results import audit_rep
    logs={name:read_log_replications(cfg.with_name(cfg.stem+'-'+name+'.log')) for name in ['LogChegadas','LogDesistencias','LogMontagem','LogAtendidos','LogEstado']}
    audit=audit_rep(1,row,logs)
    assert audit['remanescentes']>0 and audit['conservacao']
    assert not audit['reconstrucao_totais_por_concluidos_aplicavel']
    records.append({'test':'remaining_clients','passed':True,'audit':audit})
    out=ROOT/'results/validation/runtime_tests.json';out.write_text(json.dumps(records,indent=2))
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
