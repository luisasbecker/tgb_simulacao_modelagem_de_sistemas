#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
./scripts/download_jaamsim.sh
rm -rf results/runs
mkdir -p results/runs
for cfg in models/tgb_subway_cenario*.cfg; do
  name="$(basename "$cfg" .cfg)"
  work="results/runs/$name"
  mkdir -p "$work"
  cp "$cfg" "$work/$name.cfg"
  echo "===== Executando $name ====="
  (
    cd "$work"
    java -Xmx2g -jar "$ROOT/tools/JaamSim.jar" "$name.cfg" -h 2>&1 | tee run.log
  )
  if [[ ! -f "$work/$name.dat" ]]; then
    echo "ERRO: $name não gerou .dat" >&2
    exit 2
  fi
  if [[ ! -f "$work/$name.rep" ]]; then
    echo "ERRO: $name não gerou .rep" >&2
    exit 3
  fi
done
python3 scripts/analyze_results.py results/runs
