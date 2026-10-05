import Mathlib.Topology.Homeomorph

variable (X Y : Type*) [TopologicalSpace X] [TopologicalSpace Y]

-- X가 컴팩트 공간이고 X, Y가 위상동형이면 Y도 컴팩트 공간임을 Mathlib 정리를 통해 실증
theorem choi_poincare_topological_compactness_preservation
  [hX : CompactSpace X]
  (e : X ≃ₜ Y) :
  CompactSpace Y := by
  exact Homeomorph.compactSpace e
