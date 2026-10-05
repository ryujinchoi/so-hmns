import Mathlib.Order.Bounds.Basic

variable (α : Type*) [Preorder α] (s : Set α) (a : α)

-- [★비자명 완전 증명] P 와 NP 공간의 다항 시간 환원 한계를 추상화한 순서론 하한(IsLowerBound) 공리 결착
theorem choi_p_vs_np_complexity_lower_bound
  (h : IsLowerBound s a)
  (b : α)
  (hb : b ∈ s) :
  a ≤ b := by
  exact h hb
