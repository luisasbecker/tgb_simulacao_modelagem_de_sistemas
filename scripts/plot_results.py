#!/usr/bin/env python3
"""Export publication figures from audited real JaamSim output."""
from pathlib import Path
import argparse
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from result_io import read_log_replications
from run_model import ROOT

def main():
    p=argparse.ArgumentParser();p.add_argument('results',type=Path,nargs='?',default=ROOT/'results');a=p.parse_args()
    out=a.results/'figures';out.mkdir(exist_ok=True)
    rows=list(csv.DictReader((a.results/'resumo_ic95.csv').open()))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','savefig.dpi':180})
    for metric,title,filename in [('EsperaBalcao_s','Espera média no balcão — 30 replicações por cenário','espera_balcao_ic95'),('LeadTime_medio_s','Lead time dos clientes atendidos — 30 replicações por cenário','lead_time_ic95')]:
        data=[r for r in rows if r['indicador']==metric]
        means=[float(r['media']) for r in data];halves=[float(r['semi_amplitude']) for r in data]
        fig,ax=plt.subplots(figsize=(9,5.2),layout='constrained')
        ax.errorbar(range(1,6),means,yerr=halves,fmt='o',capsize=7,markersize=8,color='#1f5e93',elinewidth=1.8)
        ax.set(xticks=range(1,6),xticklabels=[f'Cenário {i}' for i in range(1,6)],ylabel='Tempo médio (s)',xlabel='Configuração do atendimento',title=title,ylim=(0,max(m+h for m,h in zip(means,halves))*1.24))
        ax.grid(axis='y',alpha=.2)
        ax.set_xlim(.5,5.5)
        for x,m,h in zip(range(1,6),means,halves):ax.annotate(f'{m:.2f} ± {h:.2f} s',(x,m+h),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10)
        fig.supxlabel('Barras: IC95% t de Student, 29 graus de liberdade. Chegadas: 90 min; execução: 150 min.',fontsize=9)
        for ext in ('png','svg'):fig.savefig(out/f'{filename}.{ext}')
        plt.close(fig)
    # Replication 28 includes the boundary q=6 and rejections. Use exact event times.
    logs=read_log_replications(a.results/'runs/cenario1/cenario1-LogEstado.log')[28]
    t=[v['this.SimTime/1[s]']/60 for v in logs]+[150]
    q=[v['[FilaBalcao].QueueLength'] for v in logs]+[logs[-1]['[FilaBalcao].QueueLength']]
    fig,ax=plt.subplots(figsize=(10,4.7),layout='constrained')
    ax.step(t,q,where='post',color='#1f5e93',linewidth=1.6)
    ax.axvline(90,color='#725c16',linestyle='--',linewidth=1.5,label='Fim das chegadas: 90 min')
    ax.set(xlim=(0,150),ylim=(-.1,6.8),xticks=[0,30,60,90,120,150],yticks=range(7),xlabel='Tempo desde o início da replicação (min)',ylabel='Clientes aguardando no balcão',title='Evolução da fila do balcão — cenário 1, replicação 28')
    ax.grid(axis='y',alpha=.18);ax.legend(loc='upper right',frameon=False)
    for ext in ('png','svg'):fig.savefig(out/f'fila_balcao_degraus.{ext}')
    plt.close(fig)
    print(f'Charts saved to {out}')

if __name__=='__main__':main()
