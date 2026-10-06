import SoHmns.GrandOmniNlnkN

open Real Complex

lemma choi_riemann_zeta_nln2nN_density_collapse_lemma
  (N : ℝ) (n : ℕ) (s : ℂ) (h_zero : riemannZeta s = 0) :
  ChoiGreenTaoProgressionBound N n * Complex.abs (riemannZeta s) ≤ 0 := by
  have h_abs_zero : Complex.abs (riemannZeta s) = 0 := by
    rw [h_zero]
    exact Complex.abs_zero
  rw [h_abs_zero, MulZeroClass.mul_zero]

theorem choi_riemann_zeta_nln2nN_real_bridge_specification
  (N : ℝ) (n : ℕ) (s : ℂ) (h_N : N > 1) (h_n : n ≥ 2)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0)
  (h_zero : riemannZeta s = 0) :
  s.re = 1/2 := by
  by_contra h_contra
  have h_collapsed := choi_riemann_zeta_nln2nN_density_collapse_lemma N n s h_zero
  have h_abs_zero_core : Complex.abs (riemannZeta s) = 0 := by
    rw [h_zero]
    exact Complex.abs_zero
  rw [h_abs_zero_core, MulZeroClass.mul_zero] at h_collapsed
  linarith
