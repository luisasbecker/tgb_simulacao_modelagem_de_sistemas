#!/usr/bin/env python3
"""Run the official JaamSim JAR; never equate exit code 0 with success."""
from pathlib import Path
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import re

ROOT=Path(__file__).resolve().parents[1]
JAR=ROOT/'tools/JaamSim2026-08.jar'
SHA='83e87bcde04b5dc8c06bac8dfb665e120fa6306aebe6ed6d49fb2ed1835223bf'

def run_model(cfg, timeout=180):
    cfg=Path(cfg).resolve()
    if hashlib.sha256(JAR.read_bytes()).hexdigest()!=SHA:
        raise RuntimeError('JaamSim JAR checksum mismatch')
    env=os.environ.copy()
    java=shutil.which('java')
    if not java: raise RuntimeError('Java not found')
    # Some minimal runners do not configure the dynamic loader for the JRE.
    java_root=Path(java).resolve().parents[1]
    libs=[java_root/'lib',java_root/'lib/server']
    env['LD_LIBRARY_PATH']=':'.join(str(p) for p in libs if p.exists())+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
    tmp=cfg.parent/'.tmp';tmp.mkdir(exist_ok=True)
    command=[java,f'-Djava.io.tmpdir={tmp}', '-Xmx1g','-jar',str(JAR),str(cfg),'-h']
    for suffix in ('.dat','.rep'):
        cfg.with_suffix(suffix).unlink(missing_ok=True)
    result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=timeout)
    (cfg.parent/'console.log').write_text(result.stdout+result.stderr)
    # JaamSim may return 0 on a parsing error; inspect the main log and outputs.
    log=cfg.with_suffix('.log')
    errors=log.read_text(errors='replace') if log.exists() else ''
    if result.returncode or any(x in errors for x in ['*** INPUT ERROR','*** ERROR','Validation Error','Input Error:','Runtime Error']):
        raise RuntimeError(f'JaamSim failed: {cfg}; see {log} and console.log')
    if not cfg.with_suffix('.dat').exists() or not cfg.with_suffix('.rep').exists():
        raise RuntimeError(f'Missing .dat/.rep for {cfg}')
    from result_io import read_log_replications
    reps=int(re.findall(r'Simulation\s+NumberOfReplications\s*\{\s*(\d+)\s*\}',cfg.read_text())[-1])
    report=cfg.with_suffix('.rep').read_text()
    reported=[int(float(x)) for x in re.findall(r'Simulation\tReplicationNumber\t([^\t]+)\t',report)]
    if reported!=list(range(1,reps+1)):
        raise RuntimeError(f'Incomplete .rep: {cfg}: {reported}')
    for name in ['LogChegadas','LogDesistencias','LogMontagem','LogAtendidos','LogEstado']:
        groups=read_log_replications(cfg.with_name(cfg.stem+'-'+name+'.log'))
        if set(groups)!=set(range(1,reps+1)):
            raise RuntimeError(f'Incomplete {name}: {cfg}')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cfg',type=Path);a=p.parse_args()
    run_model(a.cfg);print(f'JaamSim completed: {a.cfg}')
