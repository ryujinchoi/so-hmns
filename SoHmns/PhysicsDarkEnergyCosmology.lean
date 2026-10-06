import SoHmns.GrandOmniNlnkN

lemma choi_dark_energy_nln2nN_lemma
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  exact choi_green_tao_nln2nN_strict_positivity N n h_N h_n

theorem choi_dark_energy_nln2nN_lambda_bound
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Lambda : ℝ) 
  (h_lambda : Lambda = ChoiGreenTaoProgressionBound N n + 2)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0) :
  Lambda > 0 := by
  rw [h_lambda]
  have h_g : ChoiGreenTaoProgressionBound N n > 0 := choi_dark_energy_nln2nN_lemma N n h_N h_n
  linarith
