import Mathlib.LinearAlgebra.Dimension.LinearMap

variable (K V W : Type*) [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]

theorem choi_bsd_algebraic_rank_sum
  [FiniteDimensional K V] [FiniteDimensional K W] :
  FiniteDimensional.finrank K (V × W) = FiniteDimensional.finrank K V + FiniteDimensional.finrank K W := by
  exact FiniteDimensional.finrank_prod K V W
