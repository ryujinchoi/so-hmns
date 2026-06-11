from so_hmns_ultimate import UltimateSpectralOperatorEngine
import sys

class UniversalHMNSSolver:
    def __init__(self, default_n=10000):
        self.default_n = default_n
        
    def solve_for_delta(self, delta: float):
        engine = UltimateSpectralOperatorEngine(N_cutoff=self.default_n, delta=delta)
        return engine.verify()

if __name__ == "__main__":
    solver = UniversalHMNSSolver()
    # 경계 조건 테스트 (delta = 0.3)
    print("=== SOLVER EDGE CONDITION TEST (Delta = 0.3) ===")
    print(solver.solve_for_delta(0.3))
