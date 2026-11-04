#!/usr/bin/env python3
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
from run_model import ROOT,run_model,SHA
from validate_cfg import validate
from result_io import read_dat

def main():
    p=argparse.ArgumentParser();p.add_argument('--replications',type=int,choices=[1,30],default=30);p.add_argument('--output',type=Path,default=ROOT/'results/runs');a=p.parse_args()
    validate()
    a.output=a.output.resolve()
    if a.output.exists() and any(a.output.iterdir()):raise SystemExit(f'Refusing to overwrite results: {a.output}; choose a new --output.')
    a.output.mkdir(parents=True,exist_ok=True)
    manifest={'jaamsim_version':'2026-08','jar_sha256':SHA,'replications_per_scenario':a.replications,'models':[]}
    for n in range(1,6):
        src=ROOT/f'models/cenario{n}.cfg';work=a.output/f'cenario{n}';work.mkdir()
        dst=work/src.name;shutil.copy2(src,dst)
        if a.replications!=30:
            with dst.open('a') as f:f.write(f'\nSimulation NumberOfReplications {{ {a.replications} }}\n')
        print(f'Running scenario {n}: {a.replications} replication(s)',flush=True)
        run_model(dst)
        rows=read_dat(dst.with_suffix('.dat'))
        assert [int(r['Replication']) for r in rows]==list(range(1,a.replications+1))
        for r in rows:
            assert r['ClientesGerados']==r['ClientesAtendidos']+r['TotalDesistencias']+r['ClientesAindaNoSistema']
            assert r['TempoFinal_s']==9000 and r['TempoGeradorAberto_s']==5400
            assert r['UltimaChegada_s']<5400
        manifest['models'].append({'scenario':n,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'executed_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'replications':len(rows)})
    (a.output/'execution_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(f'Completed {5*a.replications} real JaamSim replications.')
    if a.replications==30:
        import subprocess,sys
        subprocess.run([sys.executable,str(ROOT/'scripts/analyze_results.py'),str(a.output)],check=True)

if __name__=='__main__':main()
