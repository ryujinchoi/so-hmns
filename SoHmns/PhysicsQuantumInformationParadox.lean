import Mathlib.Analysis.Complex.Basic

def ChoiEntropyBound (n : ℕ) : ℝ := (n : ℝ) * 10^(-20)

theorem choi_quantum_information_strict_positivity
  (n : ℕ)
  (h_pos : n > 0) :
  ChoiEntropyBound n > 0 := by
  by omega
