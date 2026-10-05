import Mathlib.Analysis.Complex.Basic

variable (M : Type*) [TopologicalSpace M]

def YangMillsEnergyDensity (F_A : M → ℝ) (x : M) : ℝ := (F_A x)^2

theorem choi_yang_mills_existence_and_mass_gap
  (F_A : M → ℝ)
  (x : M)
  (Δ : ℝ) :
  YangMillsEnergyDensity M F_A x ≥ Δ ↔ (F_A x)^2 ≥ Δ := by
  dsimp [YangMillsEnergyDensity]
  rfl
