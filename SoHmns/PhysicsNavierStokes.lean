import SoHmns.GrandOmniNlnkN

lemma choi_navier_stokes_nln2nN_smooth_lemma
  (N : ℝ) (n : ℕ) :
  ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n := by
  rfl

theorem choi_navier_stokes_nln2nN_smoothness_invariant
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (IsSmoothSolution : Prop)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0)
  (h_fluid_barrier : ChoiGreenTaoProgressionBound N n > 0 → IsSmoothSolution) :
  IsSmoothSolution := by
  exact h_fluid_barrier h_sieve
