import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

def ChoiNlnkNBound (N : ℝ) (k : ℝ) : ℝ := N * (log N)^k * N

theorem choi_nlnkn_theory_strict_positivity
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) :
  ChoiNlnkNBound N k > 0 := by
  dsimp [ChoiNlnkNBound]
  have h_log : log N > 0 := log_pos h_N
  have h_log_pow : (log N)^k > 0 := rpow_pos_of_pos h_log k
  have h_N_pos : N > 0 := by linarith
  positivity
