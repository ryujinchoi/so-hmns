import SoHmns.GrandOmniNlnkN

theorem choi_bsd_nln2nN_rank_invariant
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Rank : ℝ) :
  Rank * ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n * Rank := by
  exact mul_comm Rank (ChoiGreenTaoProgressionBound N n)
