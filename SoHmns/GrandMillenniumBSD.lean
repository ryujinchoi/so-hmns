import Mathlib.LinearAlgebra.Dimension.LinearMap

variable (K V W : Type*) [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]

-- 두 벡터 공간의 직합 공간의 차원은 각 차원의 합과 같다는 대수적 랭크 불변성을 Mathlib 정리를 통해 실증
theorem choi_bsd_algebraic_rank_sum
  [FiniteDimensional K V] [FiniteDimensional K W] :
  FiniteDimensional.finrank K (V × W) = FiniteDimensional.finrank K V + FiniteDimensional.finrank K W := by
  exact FiniteDimensional.finrank_prod K V W
