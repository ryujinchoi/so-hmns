import Mathlib.Analysis.Complex.Basic

def ChoiInflationScale (n : ℕ) : ℝ := (n : ℝ) * 10^(-30)

theorem choi_cosmic_inflation_strict_positivity
  (n : ℕ)
  (h_pos : n > 0) :
  ChoiInflationScale n > 0 := by
  by omega
