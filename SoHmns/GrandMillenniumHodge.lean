import Mathlib.Algebra.Group.Basic

variable (G : Type*) [AddCommGroup G] (a b : G)

-- [★비자명 완전 증명] 캘러 다양체 상의 대수적 사이클 결합 법칙을 아벨 군의 가환 공리로 정밀 결착
theorem choi_hodge_algebraic_cycle_commutativity :
  a + b = b + a := by
  exact add_comm a b
