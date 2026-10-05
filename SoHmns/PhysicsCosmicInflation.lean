import SoHmns.GrandOmniNlnkN

theorem choi_cosmic_inflation_nlnkn_bound
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) (Scale : ℝ) 
  (h_scale : Scale = ChoiNlnkNBound N k) :
  Scale > 0 := by
  rw [h_scale]
  exact choi_nlnkn_theory_strict_positivity N k h_N h_k
