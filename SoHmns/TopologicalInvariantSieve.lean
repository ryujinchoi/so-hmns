import Mathlib.Analysis.Complex.Basic

def ChoiTopologicalDimension (n : ℕ) : ℝ := (n : ℝ) + 3

theorem choi_topological_dimension_strict_positivity
  (n : ℕ)
  (h_pos : n > 0) :
  ChoiTopologicalDimension n > 0 := by
  by omega
