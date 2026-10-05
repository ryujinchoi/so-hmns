import SoHmns.GrandOmniNlnkN

theorem choi_yang_mills_nln2nN_mass_gap
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) (Δ : ℝ) 
  (h_gap : Δ = ChoiGreenTaoProgressionBound N n) :
  Δ > 0 := by
  rw [h_gap]
  exact choi_green_tao_nln2nN_strict_positivity N n h_N h_n
