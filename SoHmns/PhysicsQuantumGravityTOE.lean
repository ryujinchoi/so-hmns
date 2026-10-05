import Mathlib.Analysis.Complex.Basic

def ChoiPlanckScale (n : ℕ) : ℝ := (n : ℝ) * 10^(-35)

theorem choi_quantum_gravity_strict_positivity
  (n : ℕ)
  (h_pos : n > 0) :
  ChoiPlanckScale n > 0 := by
  by omega
