import Mathlib.Order.Bounds.Basic

variable (α : Type*) [Preorder α] (s : Set α) (a : α)

theorem choi_p_vs_np_complexity_lower_bound
  (h : IsLowerBound s a)
  (b : α)
  (hb : b ∈ s) :
  a ≤ b := by
  exact h hb
