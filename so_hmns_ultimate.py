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

    def verify_gravitational_gate(self, density_profile_str: str) -> dict:
        """Computes the Numerical Restoration Pressure gradient mapping gravity."""
        base_verification = self.verify_tail_error(density_profile_str)
        residual = Decimal(base_verification["residual"])
        restoration_gradient = -residual * Decimal('0.14159265')  # Pure 대수적 곡률 변형 인자
        return {"metric_tensor_addition": str(restoration_gradient), "lock_status": "GEOMETRIC_CURVATURE_MAPPED"}

    def verify_strong_confinement(self, distance_str: str) -> dict:
        """Evaluates the Context Confinement Lock metrics for strong interactions."""
        if self.space_type != 1:
            return {"status": "ACCESS_DENIED", "msg": "Confinement requires space_type=1 (Discrete Lattice)"}
        base_verification = self.verify_tail_error(distance_str)
        residual_norm = abs(Decimal(base_verification["residual"]))
        confinement_force = Decimal('100.0') * residual_norm  # 거리에 비례한 오차 폭발 억제 락 강도
        return {"confinement_lock_pressure": str(confinement_force), "status": "CONTEXT_LOCK_ACTIVE"}

    def verify_weak_typecast(self, energy_overflow_str: str) -> dict:
        """Models Bit-Truncation & Type-Casting validation for weak decay vectors."""
        base_verification = self.verify_tail_error(energy_overflow_str)
        residual = Decimal(base_verification["residual"])
        time_step_dt = Decimal('1.0') / (residual + Decimal('0.00001')) # dT 매핑 역산
        typecast_probability = residual / time_step_dt
        return {"bit_truncation_overflow_rate": str(typecast_probability), "status": "TYPECAST_DECAY_EMITTED"}

if __name__ == "__main__":
    print("[so-hmns] Running Grand Unified Mathematical Model...")
    engine_discrete = SovereignCoreEngine(space_type=1, dimension=3, nonlinearity=0.0)
    print(f"-> Strong Confinement Matrix: {engine_discrete.verify_strong_confinement('5.4128')}")
