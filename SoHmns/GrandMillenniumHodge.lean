import SoHmns.GrandOmniNlnkN

theorem choi_hodge_nlnkn_cycle_commute
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) (X : ℝ) :
  X + ChoiNlnkNBound N k = ChoiNlnkNBound N k + X := by
  exact add_comm X (ChoiNlnkNBound N k)
