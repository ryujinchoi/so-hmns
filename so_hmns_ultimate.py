import sys
import copy
from decimal import Decimal, getcontext, localcontext
from math import factorial

class SovereignCoreEngine:
    def __init__(self, space_type: int, dimension: int, nonlinearity: float, precision_base: int = 150):
        self.space_type = space_type
        self.d = dimension
        self.sigma = nonlinearity
        self.precision_base = precision_base
        
        if self.space_type == 0:
            self.alpha = float(self.d) / 2.0 + 0.5 * float(self.sigma)
        elif self.space_type == 1:
            self.alpha = 1.0 / (float(self.d) + 1.0)
        else:
            raise ValueError("Invalid space_type. Select 0 or 1.")

    def _get_bernoulli_number(self, n: int) -> Decimal:
        A = [Decimal(1) / Decimal(i + 1) for i in range(n + 1)]
        for j in range(1, n + 1):
            for i in range(n - j + 1):
                A[i] = Decimal(i + 1) * (A[i] - A[i + 1])
        return A

    def verify_tail_error(self, raw_input_str: str) -> dict:
        dynamic_precision = max(self.precision_base, len(raw_input_str) * 2)
        
        with localcontext() as ctx:
            ctx.prec = dynamic_precision
            sterile_input = Decimal(raw_input_str)
            active_tensor = copy.deepcopy(sterile_input)
            residual_accumulator = Decimal(0)
            terms_to_evaluate = 6
            
            try:
                for m in range(1, terms_to_evaluate):
                    b_num = self._get_bernoulli_number(2 * m)
                    fact = Decimal(factorial(2 * m))
                    derivative_factor = active_tensor ** Decimal(-2 * m - self.alpha)
                    term = (b_num / fact) * derivative_factor
                    residual_accumulator += term
                
                is_convergent = residual_accumulator.is_finite() and abs(residual_accumulator) < Decimal('1e-5')
                status_msg = "STABLE_INVARIANT_CONVERGENCE" if is_convergent else "ASYMPTOTIC_TAIL_DIVERGENCE"
                
            except Exception as e:
                status_msg = f"CRITICAL_TOPOLOGICAL_SHEAR: {str(e)}"
                residual_accumulator = Decimal('Infinity')
            
            finally:
                ctx.clear_flags()
        
        return {
            "space_type": self.space_type,
            "guard_index_alpha": self.alpha,
            "residual": str(residual_accumulator),
            "status": status_msg
        }

if __name__ == "__main__":
    print("[so-hmns] Running internal verification matrices...")
    engine = SovereignCoreEngine(space_type=0, dimension=3, nonlinearity=2.5)
    test_run = engine.verify_tail_error("0.00041285913257912431")
    print(f"Result Matrix Target: {test_run}")
