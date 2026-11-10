#!/usr/bin/env python3
"""Pessoa 4: export the required figures from audited real JaamSim output.

1. espera_balcao_ic95 — principal indicator (report) per scenario, bars with IC95% error bars;
   lead_time_ic95     — lead time per scenario, same layout (required indicator).
2. fila_balcao_degraus — counter queue over time (step plot, exact event times), C1 vs C2,
                         same replication (common random numbers: identical arrivals).
Extra: desistencias_ic95 with the same layout.
"""
from pathlib import Path
import argparse
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from result_io import read_log_replications, read_dat
from run_model import ROOT

BLUE, ORANGE = '#2a78d6', '#eb6834'  # validated categorical pair (CVD dE 24.7)
INK, MUTED, GRID = '#262624', '#6b6a63', '#e4e3dd'
CONFIG = {1: '2 balcões · 1 caixa', 2: '3 balcões · 1 caixa', 3: '2 balcões · 1 caixa\n75% tostados',
          4: '2 balcões · 2 caixas', 5: '3 balcões · 2 caixas'}


def style():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'text.color': INK, 'axes.labelcolor': INK,
                         'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.edgecolor': MUTED,
                         'axes.spines.top': False, 'axes.spines.right': False, 'axes.titleweight': 'bold',
                         'savefig.dpi': 200, 'savefig.facecolor': 'white'})


def save(fig, out, name):
    for ext in ('png', 'svg'):
        fig.savefig(out / f'{name}.{ext}', bbox_inches='tight', pad_inches=.15)
    plt.close(fig)


def bar_ic(rows, metric, title, ylabel, unit, out, name, reps, digits=1):
    data = sorted((r for r in rows if r['indicador'] == metric), key=lambda r: int(r['cenario']))
    means = [float(r['media']) for r in data]
    halves = [float(r['semi_amplitude']) for r in data]
    x = range(1, 6)
    fig, ax = plt.subplots(figsize=(9, 5.4), layout='constrained')
    ax.bar(x, means, width=.6, color=BLUE, zorder=2)
    ax.errorbar(x, means, yerr=halves, fmt='none', ecolor=INK, elinewidth=1.4, capsize=8, capthick=1.4, zorder=3)
    top = max(m + h for m, h in zip(means, halves))
    for i, m, h in zip(x, means, halves):
        ax.annotate(f'{m:.{digits}f} ± {h:.{digits}f} {unit}'.replace('.', ','), (i, m + h), xytext=(0, 6), textcoords='offset points',
                    ha='center', va='bottom', fontsize=10, color=INK)
    ax.set_xticks(list(x), [f'Cenário {i}\n{CONFIG[i]}' for i in x], fontsize=9.5)
    ax.set(ylabel=ylabel, xlabel='Configuração do atendimento', ylim=(min(0, min(m - h for m, h in zip(means, halves)) * 1.15), top * 1.15), xlim=(.4, 5.6))
    ax.set_title(title, loc='left')
    ax.grid(axis='y', color=GRID, linewidth=.8, zorder=0)
    ax.axhline(0, color=MUTED, linewidth=.8)
    fig.text(.01, -.01, f'Barras de erro: IC 95% t de Student, {reps} replicações por cenário ({reps - 1} g.l.). '
                        'Chegadas por 90 min; execução de 150 min.', fontsize=8.5, color=MUTED)
    save(fig, out, name)


def queue_series(log):
    t = [v['this.SimTime/1[s]'] / 60 for v in log] + [150]
    q = [v['[FilaBalcao].QueueLength'] for v in log]
    return t, q + [q[-1]]


def step_chart(results, out):
    runs = results / 'runs'
    dat = read_dat(runs / 'cenario1/cenario1.dat')
    # Replication with the most balking in C1: shows the conditional decision at the queue limit.
    rep = int(max(dat, key=lambda r: (r['TotalDesistencias'], r['FilaBalcao_max'], -r['Replication']))['Replication'])
    d1 = next(r for r in dat if r['Replication'] == rep)
    d2 = next(r for r in read_dat(runs / 'cenario2/cenario2.dat') if r['Replication'] == rep)
    fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
    for n, color, d in [(1, BLUE, d1), (2, ORANGE, d2)]:
        log = read_log_replications(runs / f'cenario{n}/cenario{n}-LogEstado.log')[rep]
        t, q = queue_series(log)
        ax.step(t, q, where='post', color=color, linewidth=2,
                label=f'Cenário {n} ({CONFIG[n]}): {d["TotalDesistencias"]:.0f} desistências')
    ax.axvline(90, color=MUTED, linestyle='--', linewidth=1.2)
    ax.text(90.8, 9.4, 'fim das chegadas (90 min)', color=MUTED, fontsize=9, va='top')
    ax.axhline(5, color=MUTED, linestyle=':', linewidth=1.2)
    ax.text(150, 5.15, 'limite: acima de 5 lanches o cliente desiste', color=MUTED, fontsize=9, ha='right', va='bottom')
    ax.set(xlim=(0, 150), ylim=(0, 10), xticks=range(0, 151, 15), yticks=range(0, 11, 2),
           xlabel='Tempo de simulação (min)', ylabel='Fila do balcão (lanches aguardando)')
    ax.set_title(f'Evolução da fila do balcão em degraus — replicação {rep}', loc='left')
    ax.grid(axis='y', color=GRID, linewidth=.8)
    ax.legend(loc='upper left', frameon=False, fontsize=9.5)
    fig.text(.01, -.01, 'Valores registrados a cada mudança de estado (sem amostragem). Mesma replicação = mesmas chegadas nos dois cenários.',
             fontsize=8.5, color=MUTED)
    save(fig, out, 'fila_balcao_degraus')
    return rep


def main():
    p = argparse.ArgumentParser()
    p.add_argument('results', type=Path, nargs='?', default=ROOT / 'results')
    a = p.parse_args()
    out = a.results / 'figures'
    out.mkdir(exist_ok=True)
    style()
    rows = list(csv.DictReader((a.results / 'resumo_ic95.csv').open()))
    reps = int(rows[0]['n'])
    bar_ic(rows, 'LeadTime_medio_s', 'Lead time médio do pedido por cenário', 'Lead time médio (s)', 's', out, 'lead_time_ic95', reps)
    bar_ic(rows, 'EsperaBalcao_s', 'Espera média na fila do balcão por cenário', 'Espera média por lanche (s)', 's', out, 'espera_balcao_ic95', reps)
    bar_ic(rows, 'TotalDesistencias', 'Desistências por replicação e cenário', 'Desistências (clientes/replicação)', 'clientes', out, 'desistencias_ic95', reps, 2)
    rep = step_chart(a.results, out)
    print(f'Charts saved to {out} (step chart: replication {rep})')


if __name__ == '__main__':
    main()
