import Mathlib.Topology.Homeomorph

variable (X Y : Type*) [TopologicalSpace X] [TopologicalSpace Y]

theorem choi_poincare_topological_compactness_preservation
  [CompactSpace X]
  (e : X ≃ₜ Y) :
  CompactSpace Y := by
  exact Homeomorph.compactSpace e
