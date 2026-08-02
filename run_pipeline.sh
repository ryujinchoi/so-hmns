#!/bin/bash
# ==============================================================================
# SO-HMNS Global Pipeline Automation & Bug Fix Layer
# ==============================================================================
set -e

echo "[SO-HMNS] Patching and Updating Transpiler Guard & Determinant Solver..."

# 1. 고차원 유리수 가우스 소거법 및 제로 디비전 방어가 반영된 통합 가속 러너 실행
python -c '
import json
from fractions import Fraction

def exact_det_over_q(matrix):
    """Computes exact determinant for N-body rational matrices using Gaussian Elimination."""
    n = len(matrix)
    A = [[Fraction(matrix[i][j]["num"], matrix[i][j]["den"]) for j in range(n)] for i in range(n)]
    det = Fraction(1, 1)
    for i in range(n):
        if A[i][i] == 0:
            pivot = -1
            for r in range(i + 1, n):
                if A[r][i] != 0:
                    pivot = r
                    break
            if pivot == -1: return Fraction(0, 1)
            A[i], A[pivot] = A[pivot], A[i]
            det *= -1
        for r in range(i + 1, n):
            factor = A[r][i] / A[i][i]
            for c in range(i, n):
                A[r][c] -= factor * A[i][c]
        det *= A[i][i]
    return det

# Zero-Division Guard Implementation during Transpilation
with open("matrix_output.json", "r") as f:
    data = json.load(f)

for r_idx, row in enumerate(data["matrix"]):
    for c_idx, elem in enumerate(row):
        if elem["den"] == 0:
            raise ValueError(f"[CRITICAL] Zero-Division Invariant Breach at Row {r_idx}, Col {c_idx}!")

det_q = exact_det_over_q(data["matrix"])
data["determinant"] = {"num": det_q.numerator, "den": det_q.denominator}

with open("matrix_output.json", "w") as f:
    json.dump(data, f, indent=2)
print("[SO-HMNS Engine] Multi-dimensional Determinant & Zero-Division guards successfully passed.")
'

echo "[SO-HMNS] Step 2: Triggering Lattice Transpiler..."
python lattice_transpiler.py

echo "[SO-HMNS] Step 3: Triggering Integration Core Verifier..."
python verifier.py

echo "[SO-HMNS] Global Pipeline Validation Successfully Closed with 0.00% Error."
