#!/usr/bin/env python3
from pathlib import Path
import csv, math, re, statistics, sys

root = Path(sys.argv[1] if len(sys.argv)>1 else "results/runs")
out_dir = root.parent if root.name == "runs" else root
out_dir.mkdir(parents=True, exist_ok=True)
# t(0.975, 29), apropriado ao requisito de 30 replicações.
T_29 = 2.045229642132703

rows=[]
problems=[]
for dat in sorted(root.glob("tgb_subway_cenario*/tgb_subway_cenario*.dat")):
    scenario=int(re.search(r"cenario(\d+)", dat.name).group(1))
    with dat.open(encoding="utf-8-sig", newline="") as f:
        reader=csv.reader(f, delimiter="\t")
        raw=list(reader)
    if not raw:
        problems.append(f"C{scenario}: .dat vazio"); continue
    header=[x.strip() for x in raw[0] if x.strip()]
    data=[]
    for r in raw[1:]:
        vals=[x.strip() for x in r if x.strip()]
        if len(vals) < 3: continue
        # Linhas de replicação têm Scenario e Replication numéricos.
        try:
            rep=int(float(vals[1]))
        except Exception:
            continue
        if rep < 1: continue
        data.append(vals)
    if len(data) != 30:
        problems.append(f"C{scenario}: {len(data)} replicações, esperado 30")
    # header sem colunas vazias casa com vals filtrados.
    idx={h:i for i,h in enumerate(header)}
    def find_col(substr):
        for h,i in idx.items():
            if substr in h: return i,h
        return None,None
    i_w,wname=find_col("[EstatSistema].SampleAverage")
    i_served,sname=find_col("[Saida].NumberAdded")
    i_des,dname=find_col("[SaidaDesistencia].NumberAdded")
    i_gen,gname=find_col("[ChegadaClientes].NumberGenerated")
    i_q,qname=find_col("[FilaBalcao].AverageQueueTime")
    if None in [i_w,i_served,i_des,i_gen,i_q]:
        problems.append(f"C{scenario}: colunas esperadas não encontradas")
        continue
    def col(i): return [float(r[i]) for r in data]
    w=col(i_w); served=col(i_served); des=col(i_des); gen=col(i_gen); q=col(i_q)
    gaps=[g-s-d for g,s,d in zip(gen,served,des)]
    def ci95(x):
        n=len(x); mean=statistics.fmean(x)
        if n<2: return mean, float('nan')
        se=statistics.stdev(x)/math.sqrt(n)
        t=T_29 if n==30 else 1.96
        return mean,t*se
    mw,hw=ci95(w); mq,hq=ci95(q); md,hd=ci95(des); mg,hg=ci95(gen); ms,hs=ci95(served)
    rows.append({
        "cenario":scenario,"n":len(data),
        "lead_time_mean_s":mw,"lead_time_ci95_half_s":hw,
        "fila_balcao_mean_s":mq,"fila_balcao_ci95_half_s":hq,
        "desistencias_mean":md,"desistencias_ci95_half":hd,
        "gerados_mean":mg,"atendidos_mean":ms,
        "remanescentes_mean":statistics.fmean(gaps),"remanescentes_max":max(gaps),
    })

summary=out_dir/"summary.csv"
if rows:
    with summary.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    md=out_dir/"summary.md"
    with md.open("w",encoding="utf-8") as f:
        f.write("# Resumo dos experimentos\n\n")
        f.write("| Cenário | n | Lead time médio (s) ± IC95% | Espera balcão (s) ± IC95% | Desistências/rodada | Gerados | Atendidos | Remanescentes máx. |\n")
        f.write("|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for r in rows:
            f.write(f"| {r['cenario']} | {r['n']} | {r['lead_time_mean_s']:.2f} ± {r['lead_time_ci95_half_s']:.2f} | {r['fila_balcao_mean_s']:.2f} ± {r['fila_balcao_ci95_half_s']:.2f} | {r['desistencias_mean']:.2f} | {r['gerados_mean']:.2f} | {r['atendidos_mean']:.2f} | {r['remanescentes_max']:.0f} |\n")
        f.write("\nCritério de integridade: gerados − atendidos − desistentes = remanescentes ao fim da rodada. O ideal é zero em todas as replicações.\n")
    print(md.read_text(encoding="utf-8"))
if problems:
    print("\nPROBLEMAS:")
    for p in problems: print("-",p)
    sys.exit(1)
if not rows:
    print("Nenhum .dat encontrado.", file=sys.stderr); sys.exit(2)
