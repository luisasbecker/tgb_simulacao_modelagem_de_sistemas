#!/usr/bin/env bash
set -euo pipefail
VERSION="${JAAMSIM_VERSION:-2026-08}"
JAR="tools/JaamSim${VERSION}.jar"
URL="https://github.com/jaamsim/jaamsim/releases/download/v${VERSION}/JaamSim${VERSION}.jar"
mkdir -p tools
if [[ -f "$JAR" ]]; then
  echo "JaamSim já disponível: $JAR"
  exit 0
fi
echo "Baixando JaamSim ${VERSION}..."
curl -fL --retry 3 --retry-delay 2 "$URL" -o "$JAR"
# SHA256 oficial do asset v2026-08; para outra versão, informe JAAMSIM_SHA256.
EXPECTED="${JAAMSIM_SHA256:-}"
if [[ -z "$EXPECTED" && "$VERSION" == "2026-08" ]]; then
  EXPECTED="83e87bcde04b5dc8c06bac8dfb665e120fa6306aebe6ed6d49fb2ed1835223bf"
fi
if [[ -n "$EXPECTED" ]]; then
  echo "$EXPECTED  $JAR" | sha256sum -c -
fi
ln -sf "JaamSim${VERSION}.jar" tools/JaamSim.jar
java -version
ls -lh "$JAR"
