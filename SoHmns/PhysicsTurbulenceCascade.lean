import Mathlib.Analysis.Complex.Basic

def ChoiTurbulenceScale (n : ℕ) : ℝ := (n : ℝ) * 10^(-5)

theorem choi_turbulence_cascade_strict_positivity
  (n : ℕ)
  (h_pos : n > 0) :
  ChoiTurbulenceScale n > 0 := by
  by omega
