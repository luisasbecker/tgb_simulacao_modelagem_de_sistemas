#!/usr/bin/env python3
"""Pessoa 4: audit every order/sandwich trace, then compute replication-level Student t intervals.

Identity rule (Pessoa 3 model): an order is identified by ClienteID, never by the entity name.
The Combine may return a copy (``ClienteN_Dup1``) as the order entity; copies inherit every
attribute (ClienteID, HoraChegada, TipoPedido, QuantidadeLanches), so lead time stays per order.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter, defaultdict
import argparse
import csv
import json
import math
import statistics
import numpy as np
from scipy import stats
from result_io import read_dat, read_log_replications
from run_model import ROOT, LOGS

RUN_S = 9000
DEMAND_S = 5400
MONTAGEM = {1: (45, 70, 110), 2: (75, 110, 160), 3: (120, 170, 240)}
TIPO_P = {1: .40, 2: .45, 3: .15}
QTD_P = {1: .70, 2: .22, 3: .08}
LEAD_STATES = ['Montagem', 'EsperaBalcao', 'EsperaReuniao', 'EsperaTostagem', 'Tostagem', 'EsperaCaixa', 'Pagamento']
CID = 'this.obj.ClienteID'
QTD = 'this.obj.QuantidadeLanches'
TIME = 'this.SimTime/1[s]'
LEAD = '(this.SimTime-this.obj.HoraChegada)/1[s]'
ST = 'this.obj.StateTimes("{}")/1[s]'.format

# Indicators reported in the main table / compared between scenarios (principal first).
MAIN = ['LeadTime_medio_s', 'P90_lead_time_s', 'EsperaBalcao_s', 'EsperaReuniaoPedido_s', 'EsperaCaixa_s',
        'FilaBalcao_media', 'FilaBalcao_max', 'TotalDesistencias', 'TaxaDesistencia', 'Vazao_h', 'ClientesAtendidos']
COMPARED = ['LeadTime_medio_s', 'P90_lead_time_s', 'EsperaBalcao_s', 'EsperaCaixa_s', 'FilaBalcao_media',
            'TotalDesistencias', 'Vazao_h']
LABEL = {
    'LeadTime_medio_s': 'Lead time médio do pedido',
    'P90_lead_time_s': 'P90 do lead time',
    'EsperaBalcao_s': 'Espera média no balcão (por lanche)',
    'EsperaReuniaoPedido_s': 'Espera de reunião (por pedido)',
    'EsperaCaixa_s': 'Espera média no caixa',
    'FilaBalcao_media': 'Fila média do balcão',
    'FilaBalcao_max': 'Fila máxima do balcão',
    'TotalDesistencias': 'Desistências',
    'TaxaDesistencia': 'Taxa de desistência',
    'Vazao_h': 'Vazão',
    'ClientesAtendidos': 'Pedidos atendidos',
}
SKIP = {'Scenario', 'Replication', 'cenario', 'Substream', 'UltimaChegada_s', 'TempoFinal_s', 'TempoGeradorAberto_s'}


def write_csv(path, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with Path(path).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def ci(values):
    n = len(values)
    mean = statistics.fmean(values)
    sd = statistics.stdev(values)
    half = float(stats.t.ppf(.975, n - 1)) * sd / math.sqrt(n)
    return {'media': mean, 'desvio_padrao': sd, 'n': n, 'ic95_inferior': mean - half,
            'ic95_superior': mean + half, 'semi_amplitude': half}


def unit(k):
    if k == 'VazaoLanches_h':
        return 'lanches/h'
    if k.endswith('_h'):
        return 'pedidos/h'
    if k.endswith('_s'):
        return 's'
    if k.startswith('Utilizacao') or k == 'TaxaDesistencia':
        return 'fracao'
    if k == 'LanchesPorPedido':
        return 'lanches/pedido'
    if k.startswith(('FilaBalcao', 'FilaReuniao', 'Sanduiches')):
        return 'lanches'
    if k == 'TotalDesistencias':
        return 'clientes'
    return 'pedidos'


def close(a, b, tol=2e-6):
    assert abs(a - b) <= tol, (a, b, abs(a - b))


def balcoes(n):
    return 3 if n in (2, 5) else 2


def caixas(n):
    return 2 if n in (4, 5) else 1


def audit_rep(n, r, logs):
    """Independent checks of one replication; adds derived indicators to ``r``."""
    rep = int(r['Replication'])
    a, d, lan, m, s, e = [logs[x][rep] for x in LOGS]
    cids = lambda rows: [int(v[CID]) for v in rows]
    A, D, M, S = (set(cids(x)) for x in (a, d, m, s))
    # Order level: one record per order in every order log.
    assert len(a) == len(A) == r['ClientesGerados']
    assert sorted(A) == list(range(1, len(a) + 1))
    assert len(d) == len(D) == r['TotalDesistencias']
    assert len(s) == len(S) == r['ClientesAtendidos'] == r['AmostrasLeadTime'] == r['ClientesPagos']
    assert len(m) == len(M) == r['ClientesMontados'] == r['PedidosReunidos']
    assert D.isdisjoint(S | M | set(cids(lan)))
    assert D | S <= A and S <= M
    assert r['ClientesGerados'] == r['ClientesAtendidos'] + r['TotalDesistencias'] + r['ClientesAindaNoSistema']
    assert r['TempoFinal_s'] == RUN_S and r['TempoGeradorAberto_s'] == DEMAND_S
    assert r['Substream'] == rep
    assert all(v[TIME] < DEMAND_S for v in a)
    assert r['UltimaChegada_s'] == max(v[TIME] for v in a)
    # Conditional balking: evaluated once per order on sandwiches waiting at the counter.
    assert all(v['this.obj.FilaNaChegada'] >= 6 for v in d)
    assert all(v['this.obj.FilaNaChegada'] <= 5 for v in s)
    assert D == {int(v[CID]) for v in a if v['this.obj.FilaNaChegada'] > 5}
    arrival = {int(v[CID]): v for v in a}
    for v in a:
        low, _, high = MONTAGEM[int(v['this.obj.TipoPedido'])]
        assert low <= v['this.obj.TempoMontagem/1[s]'] <= high
        assert v[QTD] in (1, 2, 3)
        close(v[TIME], v['this.obj.HoraChegada/1[s]'])
    attrs = ['this.obj.TipoPedido', 'this.obj.TempoMontagem/1[s]', 'this.obj.HoraChegada/1[s]', QTD]
    # Item level: every sandwich inherits its order attributes and is mounted for TempoMontagem.
    per_order = defaultdict(list)
    for v in lan:
        per_order[int(v[CID])].append(v)
        assert all(v[k] == arrival[int(v[CID])][k] for k in attrs)
        close(v[ST('Montagem')], v['this.obj.TempoMontagem/1[s]'])
    assert len(lan) == r['SanduichesMontados']
    # Join: each order leaves the Combine once, with ALL and ONLY its own sandwiches, after the last one.
    for v in m:
        c = int(v[CID])
        assert len(per_order[c]) == int(arrival[c][QTD]), (n, rep, c)
        assert v[TIME] >= max(x[TIME] for x in per_order[c]) - 1e-9
    for v in m + s:
        assert all(v[k] == arrival[int(v[CID])][k] for k in attrs)
    for v in s:
        lead = v[LEAD]
        close(lead, v[TIME] - v['this.obj.HoraChegada/1[s]'])
        close(lead, sum(v[ST(state)] for state in LEAD_STATES))
    leads = [v[LEAD] for v in s]
    close(statistics.fmean(leads), r['LeadTime_medio_s'])
    close(statistics.stdev(leads), r['LeadTime_dp_s'], 1e-4)
    close(max(leads), r['LeadTime_max_s'])
    emptied = r['ClientesAindaNoSistema'] == 0
    if emptied:
        assert A == D | S and M == S
        assert r['SanduichesNoSistema'] == 0 and r['PedidosNoPagamento'] == 0
        assert len(lan) == sum(int(arrival[c][QTD]) for c in S)
        close(statistics.fmean(v[ST('EsperaBalcao')] for v in lan), r['EsperaBalcao_s'])
        close(statistics.fmean(v[ST('EsperaCaixa')] for v in s), r['EsperaCaixa_s'])
        close(sum(v[ST('Montagem')] for v in lan) / RUN_S / balcoes(n), r['UtilizacaoBalcoes'])
        close(sum(v[ST('Tostagem')] for v in s) / RUN_S, r['UtilizacaoTostadeira'])
        close(sum(v[ST('Pagamento')] for v in s) / RUN_S / caixas(n), r['UtilizacaoCaixas'])
        assert sum(v[ST('Tostagem')] > 0 for v in s) == r['ClientesTostados']
    # Event-complete state log: order balance and exact time-weighted queue areas.
    for v in e:
        assert v['[ChegadaClientes].NumberGenerated'] == v['[Saida].NumberAdded'] + v['[SaidaDesistencia].NumberAdded'] + v['[Simulation].ClientesAindaNoSistema']
    for queue, metric in [('FilaBalcao', 'FilaBalcao_media'), ('FilaCaixa', 'FilaCaixa_media'), ('FilaReuniao', 'FilaReuniao_media')]:
        area = sum(v[f'[{queue}].QueueLength'] * ((e[i + 1][TIME] if i + 1 < len(e) else RUN_S) - v[TIME]) for i, v in enumerate(e))
        close(area / RUN_S, r[metric])
    assert max(v['[FilaBalcao].QueueLength'] for v in e) == r['FilaBalcao_max']
    parallel = sum(v.get('[Caixa1].NumberInProgress', 0) == 1 and v.get('[Caixa2].NumberInProgress', 0) == 1 for v in e)
    if n in (4, 5):
        assert parallel > 0
    # Derived indicators (computed per replication, summarised later across replications).
    r['P90_lead_time_s'] = float(np.quantile(leads, .9, method='linear'))
    r['TaxaDesistencia'] = len(d) / len(a)
    r['VazaoJanelaDemanda_h'] = len(s) / (DEMAND_S / 3600)
    r['LanchesPorPedido'] = len(lan) / len(s)
    r['EsperaReuniaoPedido_s'] = statistics.fmean(v[ST('EsperaReuniao')] for v in s)
    r['PedidosMultiplos'] = sum(int(v[QTD]) > 1 for v in s)
    return {'cenario': n, 'replicacao': rep, 'conservacao': True, 'remanescentes': r['ClientesAindaNoSistema'],
            'lanches_remanescentes': r['SanduichesNoSistema'], 'reconstrucao_totais_aplicavel': emptied,
            'ultima_chegada_s': r['UltimaChegada_s'], 'pedidos_auditados': len(a), 'lanches_auditados': len(lan),
            'desistentes': len(d), 'pedidos_entregues_pela_copia': sum('_Dup' in v['this.obj.Name'] for v in s),
            'observacoes_caixas_simultaneos': parallel, 'eventos_estado_auditados': len(e)}


def compare(data, lookup, metric, left, right):
    x, y = lookup[left, metric], lookup[right, metric]
    nonoverlap = x['ic95_superior'] < y['ic95_inferior'] or y['ic95_superior'] < x['ic95_inferior']
    diffs = [b[metric] - a[metric] for a, b in zip(data[left], data[right])]
    diff = ci(diffs) if any(diffs) else {'media': 0.0, 'ic95_inferior': 0.0, 'ic95_superior': 0.0}
    return {'indicador': metric, 'unidade': unit(metric), 'cenario_A': left, 'cenario_B': right,
            'media_A': x['media'], 'media_B': y['media'],
            'variacao_percentual_B_vs_A': 100 * (y['media'] - x['media']) / x['media'] if x['media'] else float('nan'),
            'criterio_disciplina': 'diferenca_conclusiva' if nonoverlap else 'inconclusivo_por_sobreposicao',
            'diferenca_B_menos_A': diff['media'], 'ic95_diferenca_inferior': diff['ic95_inferior'],
            'ic95_diferenca_superior': diff['ic95_superior'],
            'metodo_complementar': 't pareado por replicacao (sementes comuns); sem correcao de multiplicidade'}


def questions(lookup, comp):
    """Numbers that answer the five study questions (see report, introduction)."""
    g = lambda c, k: lookup[c, k]
    q = []
    w = g(1, 'EsperaBalcao_s')
    q.append({'pergunta': 1, 'pergunta_texto': 'C1: espera media no balcao < 300 s?',
              'evidencia': f"C1 = {w['media']:.2f} s, IC95% [{w['ic95_inferior']:.2f}; {w['ic95_superior']:.2f}] s",
              'resposta': 'sim' if w['ic95_superior'] < 300 else 'nao'})
    c = comp['EsperaBalcao_s', 1, 2]
    q.append({'pergunta': 2, 'pergunta_texto': 'C2 reduz a espera no balcao em pelo menos 40% vs C1?',
              'evidencia': f"{c['media_A']:.2f} s -> {c['media_B']:.2f} s ({c['variacao_percentual_B_vs_A']:.1f}%); {c['criterio_disciplina']}",
              'resposta': 'sim' if c['variacao_percentual_B_vs_A'] <= -40 and c['criterio_disciplina'] == 'diferenca_conclusiva' else 'nao'})
    c = comp['LeadTime_medio_s', 1, 3]
    q.append({'pergunta': 3, 'pergunta_texto': 'C3 aumenta o lead time em mais de 20% vs C1?',
              'evidencia': f"{c['media_A']:.2f} s -> {c['media_B']:.2f} s ({c['variacao_percentual_B_vs_A']:+.1f}%); {c['criterio_disciplina']}",
              'resposta': 'sim' if c['variacao_percentual_B_vs_A'] > 20 else 'nao'})
    c = comp['LeadTime_medio_s', 1, 4]
    q.append({'pergunta': 4, 'pergunta_texto': 'C4 reduz o lead time vs C1?',
              'evidencia': f"{c['media_A']:.2f} s -> {c['media_B']:.2f} s ({c['variacao_percentual_B_vs_A']:+.1f}%); {c['criterio_disciplina']}",
              'resposta': 'sim' if c['media_B'] < c['media_A'] and c['criterio_disciplina'] == 'diferenca_conclusiva' else 'nao conclusivo'})
    cx, lt, bal = comp['EsperaCaixa_s', 2, 5], comp['LeadTime_medio_s', 2, 5], comp['EsperaBalcao_s', 2, 5]
    ok = (cx['media_B'] < cx['media_A'] and cx['criterio_disciplina'] == 'diferenca_conclusiva'
          and lt['media_B'] < lt['media_A'] and lt['criterio_disciplina'] == 'diferenca_conclusiva'
          and bal['criterio_disciplina'] == 'inconclusivo_por_sobreposicao')
    q.append({'pergunta': 5, 'pergunta_texto': 'C5 elimina o aumento da espera no caixa de C2 sem perda no balcao?',
              'evidencia': (f"caixa {cx['media_A']:.2f} -> {cx['media_B']:.2f} s ({cx['criterio_disciplina']}); "
                            f"lead time {lt['media_A']:.2f} -> {lt['media_B']:.2f} s ({lt['criterio_disciplina']}); "
                            f"balcao {bal['media_A']:.2f} -> {bal['media_B']:.2f} s ({bal['criterio_disciplina']})"),
              'resposta': 'sim' if ok else 'parcial'})
    return q


def main():
    p = argparse.ArgumentParser()
    p.add_argument('runs', type=Path, nargs='?', default=ROOT / 'results/runs')
    a = p.parse_args()
    out = a.runs.parent
    data, all_logs, audits = {}, {}, []
    for n in range(1, 6):
        folder = a.runs / f'cenario{n}'
        rows = read_dat(folder / f'cenario{n}.dat')
        reps = list(range(1, len(rows) + 1))
        assert len(rows) >= 30 and [r['Replication'] for r in rows] == reps
        logs = {name: read_log_replications(folder / f'cenario{n}-{name}.log') for name in LOGS}
        assert all(set(g) == set(reps) for g in logs.values())
        for r in rows:
            audits.append(audit_rep(n, r, logs))
            r['cenario'] = n
        data[n], all_logs[n] = rows, logs
    R = len(data[1])
    assert all(len(rows) == R for rows in data.values())
    # Common random numbers: identical arrivals and order attributes in every scenario.
    keys = [CID, QTD, 'this.obj.TipoPedido', 'this.obj.TempoMontagem/1[s]', 'this.obj.HoraChegada/1[s]']
    for n in range(2, 6):
        for rep in range(1, R + 1):
            assert [[v[k] for k in keys] for v in all_logs[1]['LogChegadas'][rep]] == [[v[k] for k in keys] for v in all_logs[n]['LogChegadas'][rep]]
    # Input checks on the independent arrivals of scenario 1 (other scenarios share them).
    all_a = [v for group in all_logs[1]['LogChegadas'].values() for v in group]
    discrete = []
    for attr, probs in [('TipoPedido', TIPO_P), ('QuantidadeLanches', QTD_P)]:
        counts = Counter(int(v[f'this.obj.{attr}']) for v in all_a)
        chi = stats.chisquare([counts[k] for k in probs], np.array(list(probs.values())) * len(all_a))
        for k, prob in probs.items():
            discrete.append({'atributo': attr, 'valor': k, 'n': counts[k], 'fracao_observada': counts[k] / len(all_a),
                             'fracao_definida': prob, 'chi2': float(chi.statistic), 'chi2_p': float(chi.pvalue)})
    sample_checks = []
    for tipo, (low, mode, high) in MONTAGEM.items():
        values = [v['this.obj.TempoMontagem/1[s]'] for v in all_a if v['this.obj.TipoPedido'] == tipo]
        ks = stats.kstest(values, 'triang', args=((mode - low) / (high - low), low, high - low))
        sample_checks.append({'tipo': tipo, 'n': len(values), 'media_observada_s': statistics.fmean(values),
                              'media_teorica_s': (low + mode + high) / 3, 'min_amostra_s': min(values),
                              'max_amostra_s': max(values), 'ks_D': float(ks.statistic), 'ks_p': float(ks.pvalue)})
    # Descriptive: lead time by order size, pooled over replications (not used for IC decisions).
    by_size = []
    for n in range(1, 6):
        pooled = defaultdict(list)
        for group in all_logs[n]['LogAtendidos'].values():
            for v in group:
                pooled[int(v[QTD])].append(v[LEAD])
        for k in sorted(pooled):
            by_size.append({'cenario': n, 'quantidade_lanches': k, 'pedidos': len(pooled[k]),
                            'lead_time_medio_s': statistics.fmean(pooled[k]),
                            'p90_lead_time_s': float(np.quantile(pooled[k], .9, method='linear'))})
    summary = []
    for n, rows in data.items():
        for k in rows[0]:
            if k in SKIP:
                continue
            values = [r[k] for r in rows]
            stat = ci(values) if any(v != values[0] for v in values) else {
                'media': values[0], 'desvio_padrao': 0.0, 'n': len(values), 'ic95_inferior': values[0],
                'ic95_superior': values[0], 'semi_amplitude': 0.0}
            summary.append({'cenario': n, 'indicador': k, 'unidade': unit(k), **stat})
    lookup = {(r['cenario'], r['indicador']): r for r in summary}
    comps = [compare(data, lookup, metric, left, right) for metric in COMPARED for left, right in combinations(range(1, 6), 2)]
    comp = {(c['indicador'], c['cenario_A'], c['cenario_B']): c for c in comps}
    answers = questions(lookup, comp)
    write_csv(out / 'replicacoes.csv', [r for rows in data.values() for r in rows])
    write_csv(out / 'resumo_ic95.csv', summary)
    write_csv(out / 'comparacoes_ic95.csv', comps)
    write_csv(out / 'conservacao.csv', audits)
    write_csv(out / 'distribuicoes_discretas.csv', discrete)
    write_csv(out / 'montagem_amostras.csv', sample_checks)
    write_csv(out / 'lead_time_por_tamanho.csv', by_size)
    write_csv(out / 'respostas_perguntas.csv', answers)
    (out / 'tipos_pedido.csv').unlink(missing_ok=True)  # replaced by distribuicoes_discretas.csv
    validation = {
        'passed': True, 'replicacoes_por_cenario': R, 'replicacoes': len(audits),
        'total_pedidos_auditados': sum(x['pedidos_auditados'] for x in audits),
        'total_lanches_auditados': sum(x['lanches_auditados'] for x in audits),
        'chegadas_independentes_para_teste_distribuicao': len(all_a),
        'distribuicoes_discretas': discrete, 'montagem': sample_checks,
        'max_pedidos_remanescentes': max(x['remanescentes'] for x in audits),
        'max_lanches_remanescentes': max(x['lanches_remanescentes'] for x in audits),
        'pedidos_entregues_pela_copia': sum(x['pedidos_entregues_pela_copia'] for x in audits),
        'ultima_chegada_global_s': max(x['ultima_chegada_s'] for x in audits),
        'seeds_pareados_confirmados': True,
        'total_desistencias_por_cenario': {n: int(sum(r['TotalDesistencias'] for r in rows)) for n, rows in data.items()},
        'respostas': answers,
    }
    (out / 'validation_summary.json').write_text(json.dumps(validation, indent=2, ensure_ascii=False))
    write_markdown(out, R, lookup, comps, answers, summary, by_size)
    print(json.dumps({k: validation[k] for k in ['passed', 'replicacoes', 'total_pedidos_auditados', 'total_lanches_auditados', 'max_pedidos_remanescentes', 'max_lanches_remanescentes', 'total_desistencias_por_cenario']}, indent=2))
    for q in answers:
        print(f"P{q['pergunta']}: {q['resposta']} — {q['evidencia']}")


def fmt(r, digits=2):
    return f"{r['media']:.{digits}f} ± {r['semi_amplitude']:.{digits}f}"


def write_markdown(out, R, lookup, comps, answers, summary, by_size):
    lines = ['# Resultados — versão final (Pessoas 1 a 4)', '',
             f'JaamSim 2026-08; {R} replicações por cenário; 9000 s por replicação; chegadas em [0, 5400) s. '
             f'Valores: média entre replicações ± semi-amplitude do IC95% t de Student ({R - 1} graus de liberdade).', '',
             'Indicador principal (definido no relatório): **espera média no balcão**, em segundos por lanche, da entrada na fila do balcão ao início da montagem; meta: média inferior a 300 s. '
             'Indicador obrigatório complementar: **lead time do pedido**, em segundos, medido da chegada do cliente (`HoraChegada`) até o fim do pagamento; exclui desistentes. '
             'Contagem específica: **desistências**, em clientes por replicação, medida na chegada quando há mais de cinco lanches aguardando no balcão.', '',
             '## Indicadores principais', '',
             '| Indicador | Unidade | C1 | C2 | C3 | C4 | C5 |',
             '|---|---|---:|---:|---:|---:|---:|']
    for k in MAIN:
        digits = 3 if k == 'TaxaDesistencia' else 2
        lines.append(f"| {LABEL[k]} | {unit(k)} | " + ' | '.join(fmt(lookup[n, k], digits) for n in range(1, 6)) + ' |')
    lines += ['', 'A fila do balcão e a espera no balcão são medidas em **lanches** (após a duplicação da Pessoa 3). '
              'A vazão usa a janela total de 2,5 h. O P90 é calculado dentro de cada replicação e depois resumido. '
              'IC de desistências pode ter limite inferior negativo devido à raridade do evento; não representa contagem negativa.', '',
              '## Respostas às perguntas do estudo', '', '| Pergunta | Evidência | Resposta |', '|---:|---|---|']
    lines += [f"| {q['pergunta']} | {q['evidencia']} | {q['resposta']} |" for q in answers]
    lines += ['', '## Comparações entre cenários (lead time)', '',
              'Critério da disciplina: ICs que não se sobrepõem indicam diferença conclusiva. A diferença pareada é complementar.', '',
              '| A | B | Média A (s) | Média B (s) | Variação B vs A | Critério | Diferença pareada B−A, IC95% (s) |',
              '|---:|---:|---:|---:|---:|---|---|']
    for c in comps:
        if c['indicador'] != 'LeadTime_medio_s':
            continue
        lines.append(f"| {c['cenario_A']} | {c['cenario_B']} | {c['media_A']:.2f} | {c['media_B']:.2f} | {c['variacao_percentual_B_vs_A']:+.1f}% | "
                     f"{c['criterio_disciplina']} | {c['diferenca_B_menos_A']:.2f} [{c['ic95_diferenca_inferior']:.2f}; {c['ic95_diferenca_superior']:.2f}] |")
    lines += ['', 'Demais indicadores comparados: [comparacoes_ic95.csv](comparacoes_ic95.csv).', '',
              '## Lead time por tamanho do pedido (descritivo, agregado)', '',
              '| Cenário | Lanches | Pedidos | Lead time médio (s) | P90 (s) |', '|---:|---:|---:|---:|---:|']
    lines += [f"| {b['cenario']} | {b['quantidade_lanches']} | {b['pedidos']} | {b['lead_time_medio_s']:.2f} | {b['p90_lead_time_s']:.2f} |" for b in by_size]
    lines += ['', '## Todos os indicadores', '',
              '| Cenário | Indicador | Unidade | Média | DP | n | IC95% inferior | IC95% superior | Semi-amplitude |',
              '|---:|---|---|---:|---:|---:|---:|---:|---:|']
    lines += [f"| {r['cenario']} | {r['indicador']} | {r['unidade']} | {r['media']:.6f} | {r['desvio_padrao']:.6f} | {r['n']} | "
              f"{r['ic95_inferior']:.6f} | {r['ic95_superior']:.6f} | {r['semi_amplitude']:.6f} |" for r in summary]
    (out / 'resumo.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
