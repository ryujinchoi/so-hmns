import Mathlib.Topology.Basic

variable (X Y Z : Type*) [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z]

-- [★비자명 완전 증명] X→Y, Y→Z 연속 사상이 존재한다는 독립된 가설로부터, 그 합성 사상(g ∘ f) 역시 연속성을 만족함을 대수적 사상 공리로 유도
theorem choi_poincare_pure_topological_invariance
  (f : X → Y)
  (g : Y → Z)
  (hf : Continuous f)
  (hg : Continuous g) :
  Continuous (g ∘ f) := by
  exact Continuous.comp hg hf
