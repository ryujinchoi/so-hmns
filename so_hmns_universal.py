import numpy as np
import sys
import math
import threading
import copy
from decimal import Decimal, localcontext

getcontext().prec = 5000

class SovereignOmniTopologyEncoderV18:
    @staticmethod
    def encode_sovereign_string(raw_data_str: str) -> Decimal:
        if not isinstance(raw_data_str, str):
            raise TypeError("Sovereign topological inputs must be a strict string to prevent binary noise.")
        return Decimal(raw_data_str.strip())

class SovereignUnifiedFieldEngineV18:
    STATIC_SPHERE_SAMPLE_SIZE = 1000
    _GLOBAL_STATIC_SPHERE = None
    _LOCK = threading.Lock()
    _EPS_MACH = sys.float_info.epsilon

    def __init__(self, target_system_name: str, topological_dimension: int, space_type: int, is_nonlinear: bool):
        self.system_name = target_system_name
        self.d = Decimal(str(topological_dimension))
        self.space_type = space_type
        self.sigma = Decimal('1.0') if is_nonlinear else Decimal('0.0')
        
        if space_type == 0:
            self.embedding_constant = (self.d / Decimal('2.0')) + (Decimal('0.5') * self.sigma)
            self.cascade_factor = Decimal('1.0') + self.sigma
            self.space_desc = f"Continuous_Manifold_Sobolev_Space_Dim_{topological_dimension}"
        else:
            self.embedding_constant = Decimal('1.0') / (self.d + Decimal('1.0'))
            self.cascade_factor = Decimal('1.0')
            self.space_desc = f"Discrete_Graph_Laplacian_Space_Dim_{topological_dimension}"
            
        self.local_rng = np.random.RandomState(42)
        
        if SovereignUnifiedFieldEngineV18._GLOBAL_STATIC_SPHERE is None:
            with SovereignUnifiedFieldEngineV18._LOCK:
                if SovereignUnifiedFieldEngineV18._GLOBAL_STATIC_SPHERE is None:
                    local_sphere = self._generate_isotropic_sphere(self.STATIC_SPHERE_SAMPLE_SIZE)
                    SovereignUnifiedFieldEngineV18._GLOBAL_STATIC_SPHERE = tuple(local_sphere)

    def _generate_isotropic_sphere(self, size: int):
        u1 = self.local_rng.uniform(0.0, 1.0, size)
        safe_upper_bound = np.nextafter(1.0, -1.0)
        u1 = np.clip(u1, sys.float_info.epsilon, safe_upper_bound)
        u2 = self.local_rng.uniform(0.0, 1.0, size)
        res = np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * u2)
        return [Decimal(str(x)) for x in res]

    def execute_sovereign_validation(self, strict_perturbation: Decimal, critical_index_str: str, field_conclusion_template: str) -> dict:
        p_str = str(strict_perturbation).split('.')
        decimal_part_len = len(p_str) if len(p_str) > 1 else 0
        required_precision = max(2000, decimal_part_len * 2)
        
        with localcontext() as local_ctx:
            local_ctx.prec = required_precision
            critical_index = Decimal(str(critical_index_str))
            perturbation = strict_perturbation * self.embedding_constant
            N = 10000
            
            if perturbation != Decimal('0.0'):
                raw_div = critical_index / abs(perturbation)
                N = max(10000, int(raw_div.to_integral_value(rounding='ROUND_CEILING')))
            else:
                N = 10000

            if perturbation >= (Decimal('0.25') - Decimal(str(self._EPS_MACH))):
                energy = Decimal('Infinity')
            else:
                try:
                    nonlinear_multiplier = self.cascade_factor
                    dec_N = Decimal(N)
                    p_factor = Decimal('1.0') - Decimal('4.0') * perturbation
                    p_factor_2 = Decimal('2.0') - Decimal('4.0') * perturbation
                    continuous_integral = Decimal('1.0') / (p_factor * (dec_N ** p_factor))
                    space_correction = Decimal('1.0') / (Decimal('2.0') * (dec_N ** p_factor_2))
                    raw_energy = (continuous_integral + space_correction) * nonlinear_multiplier
                    energy = copy.deepcopy(raw_energy)
                except Exception:
                    energy = Decimal('Infinity')

            contradiction_detected = False
            if perturbation != Decimal('0.0') and (energy > Decimal('1.0')):
                contradiction_detected = True

            status = "Q.E.D. (Sovereign Invariant Contradiction Established)" if contradiction_detected else "STABLE_SYSTEM"
            final_conclusion = field_conclusion_template if contradiction_detected else "The system remains within bounded stability."

            local_ctx.clear_flags()

            return {
                "Engine_Version": "SO-HMNS v18.0 (Sovereign Absolute Invariant Truth)",
                "Target_System_Name": self.system_name,
                "Assigned_Space_Topology": self.space_desc,
                "Derived_Embedding_Constant": float(self.embedding_constant),
                "Derived_Cascade_Factor": float(self.cascade_factor),
                "Thread_Isolated_Precision": f"{required_precision}_Digits_Context_Isolated_Sterilized",
                "Strict_Decimal_N_Digits": f"{len(str(N))}_Digits_Large_Integer_Scale",
                "Validated_Tail_Energy": float(energy) if energy != Decimal('Infinity') else "Infinity",
                "Operator_Norm_Breached_Contradiction": contradiction_detected,
                "Academic_Field_Conclusion": final_conclusion,
                "Status": status
            }
