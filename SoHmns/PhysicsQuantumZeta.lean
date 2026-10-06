import SoHmns.GrandOmniNlnkN

lemma choi_quantum_zeta_nln2nN_lemma
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n := by
  rfl

theorem choi_quantum_zeta_nln2nN_energy
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0) :
  ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n := by
  exact choi_quantum_zeta_nln2nN_lemma N n h_N h_n
