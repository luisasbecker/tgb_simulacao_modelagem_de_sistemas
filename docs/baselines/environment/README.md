# Ambiente online de teste — Trabalho GB Subway / JaamSim

Este repositório executa os cinco cenários do JaamSim em modo **headless**, com 30 replicações por cenário, e publica os `.dat`, `.rep`, logs e um resumo estatístico como artefato do GitHub Actions.

## Execução online recomendada

1. Coloque esta pasta em um repositório GitHub.
2. Abra **Actions > JaamSim GB - validar e executar > Run workflow**.
3. O workflow baixa o JaamSim 2026-08 oficial, valida os `.cfg`, executa os cinco cenários e cria o artefato `jaamsim-resultados`.
4. O resumo final fica em `results/summary.md` e `results/summary.csv`.

O mesmo repositório pode ser aberto em GitHub Codespaces porque contém `.devcontainer/devcontainer.json`.

## Execução local / Codespaces

```bash
python3 scripts/validate_cfg.py
./scripts/run_all.sh
```

O JaamSim é baixado automaticamente para `tools/` e executado com `-h` (headless).

## Testes automáticos

O validador confere, nos cinco cenários:

- 30 replicações;
- `RunDuration = 2.5 h`;
- interrupção das chegadas em 5400 s;
- quantidade correta de balcões e caixas por cenário;
- 55/45 de tostagem nos cenários 1, 2, 4 e 5 e 75/25 no cenário 3;
- `TipoPedido` 40/45/15;
- três distribuições triangulares de montagem;
- desistência quando a fila tem mais de cinco aguardando;
- uso de `TempoMontagem` pelos balcões;
- saídas de desistência e geração adicionadas ao `RunOutputList`.

Após a simulação, o analisador exige 30 linhas de replicação por cenário e calcula média e IC95% do lead time e da espera no balcão. Também verifica a conservação de clientes:

`gerados - atendidos - desistentes = remanescentes no fim da rodada`.

Se os 60 minutos extras forem suficientes para esvaziar o sistema, `remanescentes` deve ser zero em todas as replicações.

## Observação importante sobre o cutoff de 90 min

Os modelos atuais usam `ExpressionThreshold` com `this.SimTime < 5400[s]`. O JaamSim documenta que condições de `ExpressionThreshold` baseadas diretamente no tempo são reavaliadas em eventos; por isso, o ambiente registra `NumberGenerated` e testa o resultado. Se a execução mostrar comportamento limítrofe indesejado, o cutoff pode ser substituído por um `TimeSeriesThreshold` sem alterar os demais cenários.
