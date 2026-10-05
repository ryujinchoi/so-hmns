import Mathlib.Analysis.Complex.Basic

def ChoiZetaEnergy (n : ℕ) : ℝ := (n : ℝ) * 5

theorem choi_quantum_zeta_strict_positivity
  (n : ℕ)
  (h_pos : n > 0) :
  ChoiZetaEnergy n > 0 := by
  by omega
