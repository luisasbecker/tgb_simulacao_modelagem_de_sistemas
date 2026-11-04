"""Strict readers for JaamSim tab-separated output (including empty CI columns)."""
from pathlib import Path
import csv
import math
import re

def read_dat(path, allow_nonfinite=False):
    with Path(path).open(newline='') as f: rows=list(csv.reader(f,delimiter='\t'))
    if not rows or rows[0][:2]!=['Scenario','Replication']:
        raise ValueError(f'Unexpected .dat header: {path}')
    columns=[(i,h.replace('[Simulation].','')) for i,h in enumerate(rows[0]) if h]
    data=[]
    for r in rows[1:]:
        # Summary row has an EMPTY replication cell. Do not remove blank cells.
        if len(r)<2 or not re.fullmatch(r'\d+',r[1]):continue
        out={k:float(r[i]) for i,k in columns}
        if not allow_nonfinite and not all(math.isfinite(x) for x in out.values()):raise ValueError(f'Nonfinite data: {path}')
        data.append(out)
    return data

def read_logger(path):
    lines=Path(path).read_text().splitlines()
    start=next(i for i,l in enumerate(lines) if l.startswith('this.SimTime/1[s]\t'))
    rows=list(csv.reader(lines[start:],delimiter='\t'))
    # Duplicate headers occur in ExpressionLogger; keep positional access available.
    return rows[0], rows[1:]

def numeric_logger(path):
    h,rows=read_logger(path)
    return [{k:float(v) if k not in ('this.obj','this.obj.Name') else v for k,v in zip(h,r)} for r in rows]

def read_log_replications(path):
    groups={}
    rep=1
    header=None
    for line in Path(path).read_text().splitlines():
        if (m:=re.search(r'##### SCENARIO \d+ - REPLICATION (\d+) #####',line)):
            rep=int(m[1]);groups.setdefault(rep,[]);header=None;continue
        if line.startswith('this.SimTime/1[s]\t'):
            header=line.split('\t');groups.setdefault(rep,[]);continue
        if not line or header is None:continue
        cells=line.split('\t')
        if len(cells)!=len(header):raise ValueError(f'Malformed log row: {path}: {line}')
        groups[rep].append({k:float(v) if k not in ('this.obj','this.obj.Name') else v for k,v in zip(header,cells)})
    return groups
