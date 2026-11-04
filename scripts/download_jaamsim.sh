#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
JAR="tools/JaamSim2026-08.jar"
SHA="83e87bcde04b5dc8c06bac8dfb665e120fa6306aebe6ed6d49fb2ed1835223bf"
mkdir -p tools
if [[ ! -f "$JAR" ]]; then
  curl -fL --retry 3 'https://github.com/jaamsim/jaamsim/releases/download/v2026-08/JaamSim2026-08.jar' -o "$JAR.part"
  printf '%s  %s\n' "$SHA" "$JAR.part" | sha256sum -c -
  mv "$JAR.part" "$JAR"
fi
# Verify existing files too; an earlier partial download is never accepted.
printf '%s  %s\n' "$SHA" "$JAR" | sha256sum -c -
