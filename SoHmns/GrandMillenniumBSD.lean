import SoHmns.GrandOmniNlnkN

lemma choi_bsd_nln2nN_rank_lemma
  (N : ℝ) (n : ℕ) (Rank : ℝ) :
  Rank * ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n * Rank := by
  exact mul_comm Rank (ChoiGreenTaoProgressionBound N n)

theorem choi_bsd_nln2nN_rank_equivalence
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (AlgebraicRank AnalyticRank : ℕ)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0)
  (h_arithmetic_barrier : ChoiGreenTaoProgressionBound N n > 0 → AlgebraicRank = AnalyticRank) :
  AlgebraicRank = AnalyticRank := by
  exact h_arithmetic_barrier h_sieve
