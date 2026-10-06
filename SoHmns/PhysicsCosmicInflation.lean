import SoHmns.GrandOmniNlnkN

lemma choi_cosmic_inflation_nln2nN_lemma
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  exact choi_green_tao_nln2nN_strict_positivity N n h_N h_n

theorem choi_cosmic_inflation_nln2nN_bound
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Scale : ℝ) 
  (h_scale : Scale = ChoiGreenTaoProgressionBound N n)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0) :
  Scale > 0 := by
  rw [h_scale]
  exact choi_cosmic_inflation_nln2nN_lemma N n h_N h_n
