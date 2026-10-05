import SoHmns.GrandOmniNlnkN

theorem choi_yang_mills_nlnkn_mass_gap
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) (Δ : ℝ) 
  (h_gap : Δ = ChoiNlnkNBound N k) :
  Δ > 0 := by
  rw [h_gap]
  exact choi_nlnkn_theory_strict_positivity N k h_N h_k
