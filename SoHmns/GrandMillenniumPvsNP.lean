import SoHmns.GrandOmniNlnkN

theorem choi_p_vs_np_nln2nN_lower_bound
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n ≥ ChoiGreenTaoProgressionBound N n := by
  linarith
