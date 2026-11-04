#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

expected = {
    1: {"balcoes": {"Balcao1","Balcao2"}, "caixas": {"Caixa"}, "toast": "0.55  0.45"},
    2: {"balcoes": {"Balcao1","Balcao2","Balcao3"}, "caixas": {"Caixa"}, "toast": "0.55  0.45"},
    3: {"balcoes": {"Balcao1","Balcao2"}, "caixas": {"Caixa"}, "toast": "0.75  0.25"},
    4: {"balcoes": {"Balcao1","Balcao2"}, "caixas": {"Caixa1","Caixa2"}, "toast": "0.55  0.45"},
    5: {"balcoes": {"Balcao1","Balcao2","Balcao3"}, "caixas": {"Caixa1","Caixa2"}, "toast": "0.55  0.45"},
}

required_common = [
    r"Simulation\s+RunDuration\s*\{\s*2\.5\s*h\s*\}",
    r"Simulation\s+NumberOfReplications\s*\{\s*30\s*\}",
    r"ChegadaClientes\s+OperatingThresholdList\s*\{\s*HorarioPico\s*\}",
    r"HorarioPico\s+OpenCondition\s*\{\s*'this\.SimTime\s*<\s*5400\[s\]'\s*\}",
    r"TipoPedidoDist\s+ProbabilityList\s*\{\s*0\.40\s+0\.45\s+0\.15\s*\}",
    r"DecisaoDesistencia\s+Choice\s*\{\s*'\[FilaBalcao\]\.QueueLength\s*>\s*5\s*\?\s*2\s*:\s*1'\s*\}",
    r"MontagemSimplesDist\s+MinValue\s*\{\s*45\s*s\s*\}",
    r"MontagemSimplesDist\s+Mode\s*\{\s*70\s*s\s*\}",
    r"MontagemSimplesDist\s+MaxValue\s*\{\s*110\s*s\s*\}",
    r"MontagemTradicionalDist\s+MinValue\s*\{\s*75\s*s\s*\}",
    r"MontagemTradicionalDist\s+Mode\s*\{\s*110\s*s\s*\}",
    r"MontagemTradicionalDist\s+MaxValue\s*\{\s*160\s*s\s*\}",
    r"MontagemComplexoDist\s+MinValue\s*\{\s*120\s*s\s*\}",
    r"MontagemComplexoDist\s+Mode\s*\{\s*170\s*s\s*\}",
    r"MontagemComplexoDist\s+MaxValue\s*\{\s*240\s*s\s*\}",
]

def active_lines(text):
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))

def server_names(text):
    names=set()
    for m in re.finditer(r"Define\s+Server\s*\{([^}]*)\}", text, flags=re.S):
        names.update(m.group(1).split())
    return names

def norm_ws(s):
    return " ".join(s.split())

errors=[]
for n, spec in expected.items():
    p=MODELS/f"tgb_subway_cenario{n}.cfg"
    if not p.exists():
        errors.append(f"C{n}: arquivo ausente")
        continue
    raw=p.read_text(encoding="utf-8")
    text=active_lines(raw)
    if text.count("{") != text.count("}"):
        errors.append(f"C{n}: chaves desbalanceadas")
    for pattern in required_common:
        if not re.search(pattern, text, flags=re.S):
            errors.append(f"C{n}: requisito não encontrado: {pattern}")
    servers=server_names(text)
    balcoes={s for s in servers if s.startswith("Balcao")}
    caixas={s for s in servers if s.startswith("Caixa")}
    if balcoes != spec["balcoes"]:
        errors.append(f"C{n}: balcões {sorted(balcoes)} != esperado {sorted(spec['balcoes'])}")
    if caixas != spec["caixas"]:
        errors.append(f"C{n}: caixas {sorted(caixas)} != esperado {sorted(spec['caixas'])}")
    m=re.search(r"RotaDist\s+ProbabilityList\s*\{([^}]*)\}", text)
    got=norm_ws(m.group(1)) if m else None
    want=norm_ws(spec["toast"])
    if got != want:
        errors.append(f"C{n}: probabilidades tostagem {got!r} != {want!r}")
    for b in spec["balcoes"]:
        if not re.search(rf"{re.escape(b)}\s+ServiceTime\s*\{{\s*'this\.obj\.TempoMontagem'\s*\}}", text):
            errors.append(f"C{n}: {b} não usa TempoMontagem")
    # Três saídas extras da Pessoa 2 devem estar na lista de execução.
    for token in ["[ContadorDesistencias].TotalDesistencias", "[SaidaDesistencia].NumberAdded", "[ChegadaClientes].NumberGenerated"]:
        if token not in text:
            errors.append(f"C{n}: RunOutputList sem {token}")

if errors:
    print("FALHA NA VALIDAÇÃO ESTÁTICA")
    for e in errors: print("-", e)
    sys.exit(1)
print("OK: 5 cenários preservam a Pessoa 1 e contêm as regras da Pessoa 2.")
