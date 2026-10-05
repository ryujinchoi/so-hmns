import SoHmns.GrandOmniNlnkN

theorem choi_hodge_nln2nN_cycle_commute
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (X : ℝ) :
  X + ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n + X := by
  exact add_comm X (ChoiGreenTaoProgressionBound N n)
