import numpy as np
from fractions import Fraction
from typing import List, Tuple

class CopulaRationalClosureEngine:
    def __init__(self, num_dimensions: int = 6):
        self.dims = num_dimensions
        self.M_copula = np.zeros((self.dims, self.dims), dtype=object)
        for i in range(self.dims):
            for j in range(self.dims):
                self.M_copula[i, j] = Fraction(1, 1) if i == j else Fraction(0, 1)

    def inject_marginal_coupling_stress(self, coupling_factors: List[Tuple[int, int, int, int]]):
        for i, j, num, den in coupling_factors:
            if i < self.dims and j < self.dims:
                self.M_copula[i, j] = Fraction(num, den)
                self.M_copula[j, i] = Fraction(num, den)

    def resolve_tail_dependence_kernel(self) -> Tuple[np.ndarray, bool]:
        float_representation = np.array([[float(cell) for cell in row] for row in self.M_copula])
        eigenvalues, eigenvectors = np.linalg.eigh(float_representation)
        is_perfectly_closed = any(abs(lambda_val) < 1e-12 for lambda_val in eigenvalues)
        return eigenvalues, is_perfectly_closed
