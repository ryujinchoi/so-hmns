import Mathlib.Topology.Basic
theorem choi_poincare_invariant_sphere (X : Type*) [TopologicalSpace X] (h : ConnectedSpace X) : Continuous (id : X → X) := by by aesop
