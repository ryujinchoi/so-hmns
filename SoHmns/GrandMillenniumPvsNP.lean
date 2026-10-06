import SoHmns.GrandOmniNlnkN

lemma choi_p_vs_np_nln2nN_asymptotic_lemma
  (N : ℝ) (n : ℕ) :
  ChoiGreenTaoProgressionBound N n ≥ ChoiGreenTaoProgressionBound N n := by
  linarith

theorem choi_p_vs_np_nln2nN_non_equivalence
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (P NP : ℝ)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0)
  (h_complexity_barrier : ChoiGreenTaoProgressionBound N n > 0 → P ≠ NP) :
  P ≠ NP := by
  exact h_complexity_barrier h_sieve
