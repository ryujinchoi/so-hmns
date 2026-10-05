import SoHmns.GrandOmniNlnkN

theorem choi_dark_energy_nlnkn_lambda_bound
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) (Lambda : ℝ) 
  (h_lambda : Lambda = ChoiNlnkNBound N k + 2) :
  Lambda > 0 := by
  rw [h_lambda]
  have h_g : ChoiNlnkNBound N k > 0 := choi_nlnkn_theory_strict_positivity N k h_N h_k
  linarith
