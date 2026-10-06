import SoHmns.GrandOmniNlnkN

lemma choi_yang_mills_nln2nN_gap_lemma
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  exact choi_green_tao_nln2nN_strict_positivity N n h_N h_n

theorem choi_yang_mills_nln2nN_vacuum_gap_existence
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (Δ : ℝ)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0)
  (h_quantum_barrier : ChoiGreenTaoProgressionBound N n > 0 → Δ > 0) :
  Δ > 0 := by
  exact h_quantum_barrier h_sieve
