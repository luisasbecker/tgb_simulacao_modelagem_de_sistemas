#!/usr/bin/env python3
"""Static preservation contract; engine parsing is validated separately."""
from pathlib import Path
import json
import re
from build_models import ROOT

def records(text):
    text='\n'.join(l.split('#')[0] for l in text.splitlines())
    entries={}
    pos=0
    pattern=re.compile(r'(?m)^([\w-]+)\s+([\w-]+)\s*\{')
    while (m:=pattern.search(text,pos)):
        start=m.end();pos=start;depth=1
        while depth and pos<len(text):
            depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
        if depth:raise AssertionError('Unbalanced braces')
        entries[m[1],m[2]]=' '.join(text[start:pos-1].split())
    return entries

def validate():
    report=[]
    for n in range(1,6):
        base=records((ROOT/f'docs/baselines/pessoa1/tgb_subway_cenario{n}.cfg').read_text())
        p=ROOT/f'models/cenario{n}.cfg';text=p.read_text();cfg=records(text)
        balcoes=[f'Balcao{i}' for i in range(1,4 if n in (2,5) else 3)]
        caixas=['Caixa1','Caixa2'] if n in (4,5) else ['Caixa']
        allowed={('ChegadaClientes','NextComponent'),('ChegadaClientes','FirstArrivalTime'),('EstatSistema','SampleValue'),('EstatSistema','NextComponent'),('Simulation','RunOutputList')}
        allowed|={(b,k) for b in balcoes for k in ['NextComponent','ServiceTime']}
        # Multiple Define records are grouped by type, so compare object declarations separately.
        changes=[]
        for key,value in base.items():
            if key[0]=='Define':continue
            assert key in cfg,(n,'removed input',key)
            if cfg[key]!=value:
                assert key in allowed,(n,'unexpected base change',key,value,cfg[key])
                changes.append({'object':key[0],'keyword':key[1],'before':value,'after':cfg[key]})
        original={(kind,name) for kind,names in re.findall(r'Define\s+(\w+)\s*\{([^}]+)\}',(ROOT/f'docs/baselines/pessoa1/tgb_subway_cenario{n}.cfg').read_text()) for name in names.split()}
        final={(kind,name) for kind,names in re.findall(r'Define\s+(\w+)\s*\{([^}]+)\}',text) for name in names.split()}
        assert original<=final
        assert {name for kind,name in final if kind=='Server'}==set(balcoes+caixas+['Tostadeira'])
        assert cfg['Simulation','RunDuration']=='2.5 h'
        assert cfg['Simulation','NumberOfReplications']=='30'
        assert cfg['RotaDist','ProbabilityList']==('0.75 0.25' if n==3 else '0.55 0.45')
        assert all(cfg[c,'WaitQueue']=='FilaCaixa' for c in caixas)
        assert all(cfg[b,'WaitQueue']=='FilaBalcao' for b in balcoes)
        assert cfg['ChegadaClientes','ImmediateThresholdList']=='HorarioPico'
        assert cfg['JanelaChegadas','Value']=='{ 0 s 1 } { 5400 s 0 }'
        assert ('ChegadaClientes','OperatingThresholdList') not in cfg
        assert cfg['DecisaoDesistencia','Choice']=="'[FilaBalcao].QueueLength > 5 ? 2 : 1'"
        assert cfg['DecisaoDesistencia','NextComponentList']=='FilaBalcao LogDesistencias'
        assert cfg['TipoPedidoDist','ProbabilityList']=='0.40 0.45 0.15'
        assert all(cfg[b,'ServiceTime']=="'this.obj.TempoMontagem'" for b in balcoes)
        for tipo,values in [('Simples',(45,70,110)),('Tradicional',(75,110,160)),('Complexo',(120,170,240))]:
            for k,v in zip(['MinValue','Mode','MaxValue'],values):assert cfg[f'Montagem{tipo}Dist',k]==f'{v} s'
        assert 'this.obj.TipoPedido ==' in cfg['SorteiaMontagem','AttributeAssignmentList']
        assert cfg['EstatSistema','SampleValue']=="'this.SimTime - this.obj.HoraChegada'"
        report.append({'scenario':n,'passed':True,'base_inputs_changed':changes})
    out=ROOT/'results/validation/static_validation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2))
    print('Static preservation contract: 5 scenarios passed (not an engine execution).')
    return report

if __name__=='__main__':validate()
