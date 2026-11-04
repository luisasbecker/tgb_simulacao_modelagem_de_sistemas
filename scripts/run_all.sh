#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/download_jaamsim.sh
python3 scripts/run_all.py "$@"
