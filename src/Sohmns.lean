import Mathlib.Data.Real.Basic

lemma invariant_manifold_stability (x y : ℝ) (h : x = y) : x - y = 0 := by
  rw [h, sub_self]

theorem absolute_truth_continuity (x : ℝ) : x = x := by
  rfl
