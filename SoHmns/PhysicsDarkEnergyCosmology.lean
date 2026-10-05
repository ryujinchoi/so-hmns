import SoHmns.GrandOmniNlnkN

theorem choi_dark_energy_nln2nN_lambda_bound
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Lambda : ℝ) 
  (h_lambda : Lambda = ChoiGreenTaoProgressionBound N n + 2) :
  Lambda > 0 := by
  rw [h_lambda]
  have h_g : ChoiGreenTaoProgressionBound N n > 0 := choi_green_tao_nln2nN_strict_positivity N n h_N h_n
  linarith
