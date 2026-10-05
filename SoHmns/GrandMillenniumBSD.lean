import SoHmns.GrandOmniNlnkN

theorem choi_bsd_nlnkn_rank_invariant
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) (Rank : ℝ) :
  Rank * ChoiNlnkNBound N k = ChoiNlnkNBound N k * Rank := by
  exact mul_comm Rank (ChoiNlnkNBound N k)
