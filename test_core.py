import unittest
from so_hmns_ultimate import SovereignCoreEngine

class TestSovereignInfrastructure(unittest.TestCase):
    def test_continuous_manifold_alpha(self):
        engine = SovereignCoreEngine(space_type=0, dimension=3, nonlinearity=2.0)
        self.assertEqual(engine.alpha, 2.5)  # 3/2 + 0.5*2 = 2.5

    def test_discrete_graph_alpha(self):
        engine = SovereignCoreEngine(space_type=1, dimension=3, nonlinearity=0.0)
        self.assertAlmostEqual(engine.alpha, 0.25)  # 1 / (3+1) = 0.25

    def test_zero_gap_sterilization(self):
        engine = SovereignCoreEngine(space_type=0, dimension=3, nonlinearity=2.0)
        metrics = engine.verify_tail_error("0.1415926535")
        self.assertIn("status", metrics)

if __name__ == '__main__':
    unittest.main()
