import unittest
import json
import os
import sys
from fractions import Fraction

sys.set_int_max_str_digits(0)

class QuantumMeasurementSolver:
    def __init__(self, dimension: int):
        self.dim = dimension

    def multiply_matrix_vector(self, matrix, vector):
        result = [Fraction(0, 1)] * self.dim
        for i in range(self.dim):
            for j in range(self.dim):
                result[i] += matrix[i][j] * vector[j]
        return result

    def multiply_matrices(self, m1, m2):
        result = [[Fraction(0, 1) for _ in range(self.dim)] for _ in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    result[i][j] += m1[i][k] * m2[k][j]
        return result

    def verify_idempotency(self, projector_matrix):
        p_squared = self.multiply_matrices(projector_matrix, projector_matrix)
        for i in range(self.dim):
            for j in range(self.dim):
                if p_squared[i][j] != projector_matrix[i][j]:
                    return False
        return True

class TestQuantumMeasurementInvariants(unittest.TestCase):
    def setUp(self):
        self.solver = QuantumMeasurementSolver(dimension=2)
        self.initial_psi = [Fraction(1, 3), Fraction(2, 3)]
        self.projector = [
            [Fraction(1, 1), Fraction(0, 1)],
            [Fraction(0, 1), Fraction(0, 1)]
        ]

    def test_projector_idempotency_axiom(self):
        is_idempotent = self.solver.verify_idempotency(self.projector)
        self.assertTrue(is_idempotent)

    def test_wave_function_deterministic_lock(self):
        collapsed_psi = self.solver.multiply_matrix_vector(self.projector, self.initial_psi)
        secondary_psi = self.solver.multiply_matrix_vector(self.projector, collapsed_psi)
        self.assertEqual(secondary_psi, collapsed_psi)

        payload = {
            "dimension": 2,
            "verification_type": "Quantum_Measurement_Idempotency",
            "matrix": [
                [{"num": elem.numerator, "den": elem.denominator} for elem in row]
                for row in self.projector
            ],
            "determinant": {"num": 0, "den": 1}
        }
        with open("matrix_output.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

if __name__ == "__main__":
    # Infuse buffer=True to silence streaming outputs during multi-node validations
    unittest.main(buffer=True)
