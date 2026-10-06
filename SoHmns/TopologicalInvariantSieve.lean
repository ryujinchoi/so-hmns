import SoHmns.GrandOmniNlnkN

lemma choi_topological_nln2nN_lemma
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  exact choi_green_tao_nln2nN_strict_positivity N n h_N h_n

theorem choi_topological_nln2nN_sieve_dimension
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Dim : ℝ)
  (h_dim : Dim = ChoiGreenTaoProgressionBound N n + 3)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0) :
  Dim > 0 := by
  rw [h_dim]
  have h_g : ChoiGreenTaoProgressionBound N n > 0 := choi_topological_nln2nN_lemma N n h_N h_n
  linarith
