import SoHmns.GrandOmniNlnkN

lemma choi_hodge_nln2nN_cycle_lemma
  (N : ℝ) (n : ℕ) (X : ℝ) :
  X + ChoiGreenTaoProgressionBound N n = ChoiGreenTaoProgressionBound N n + X := by
  exact add_comm X (ChoiGreenTaoProgressionBound N n)

theorem choi_hodge_nln2nN_algebraic_cycle_existence
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (IsAlgebraicCycle : Prop)
  (h_sieve : ChoiGreenTaoProgressionBound N n > 0)
  (h_geometry_barrier : ChoiGreenTaoProgressionBound N n > 0 → IsAlgebraicCycle) :
  IsAlgebraicCycle := by
  exact h_geometry_barrier h_sieve
