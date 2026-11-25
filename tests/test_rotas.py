import unittest, itertools, math
import networkx as nx
from src.main import load, astar, cost, plan, read
class TestRotas(unittest.TestCase):
    def test_menor_tempo(self):
        g=load()
        for a,b in itertools.product(g.nodes,repeat=2):
            self.assertTrue(math.isclose(cost(g,astar(g,a,b)),nx.shortest_path_length(g,a,b,weight='min')))
    def test_cobertura(self):
        g=load(); orders=[r['no'] for r in read('pedidos.csv')]; r=plan(g,orders,'auto')
        self.assertEqual(sorted(r['seq'][1:-1]),sorted(orders)); self.assertEqual(r['path'][0],'D'); self.assertEqual(r['path'][-1],'D')
    def test_mao_unica(self):
        g=load(); self.assertTrue(g.has_edge('E','K')); self.assertFalse(g.has_edge('K','E'))
if __name__=='__main__': unittest.main()
