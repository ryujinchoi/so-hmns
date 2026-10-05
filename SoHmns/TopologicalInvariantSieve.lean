import SoHmns.GrandOmniNlnkN

theorem choi_topological_nln2nN_sieve_dimension
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Dim : ℝ)
  (h_dim : Dim = ChoiGreenTaoProgressionBound N n + 3) :
  Dim > 0 := by
  rw [h_dim]
  have h_g : ChoiGreenTaoProgressionBound N n > 0 := choi_green_tao_nln2nN_strict_positivity N n h_N h_n
  linarith
