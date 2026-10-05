import SoHmns.GrandOmniNlnkN

theorem choi_topological_nlnkn_sieve_dimension
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) (Dim : ℝ)
  (h_dim : Dim = ChoiNlnkNBound N k + 3) :
  Dim > 0 := by
  rw [h_dim]
  have h_g : ChoiNlnkNBound N k > 0 := choi_nlnkn_theory_strict_positivity N k h_N h_k
  linarith
