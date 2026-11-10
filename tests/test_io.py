import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from result_io import read_dat,read_log_replications
ROOT=Path(__file__).resolve().parents[1]

class ReadersTest(unittest.TestCase):
    def test_replication_row_not_summary(self):
        rows=read_dat(ROOT/'results/runs/cenario1/cenario1.dat')
        self.assertEqual([r['Replication'] for r in rows],list(range(1,31)))
        self.assertEqual(rows[0]['ClientesGerados'],52)
        self.assertEqual(rows[-1]['ClientesGerados'],47)
    def test_empty_rejection_sections_are_preserved(self):
        # Replicacoes sem desistencia geram secoes vazias no log; o leitor deve
        # preserva-las (30 grupos) e cada grupo deve bater com TotalDesistencias.
        groups=read_log_replications(ROOT/'results/runs/cenario2/cenario2-LogDesistencias.log')
        rows=read_dat(ROOT/'results/runs/cenario2/cenario2.dat')
        self.assertEqual(set(groups),set(range(1,31)))
        self.assertTrue(any(not v for v in groups.values()))
        self.assertEqual([len(groups[int(r['Replication'])]) for r in rows],[int(r['TotalDesistencias']) for r in rows])

if __name__=='__main__':unittest.main()
