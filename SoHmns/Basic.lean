import Mathlib.Data.Nat.Basic
import Mathlib.Algebra.Order.Ring.Defs

namespace SoHmns

theorem nat_distrib_successor_proof (n : Nat) : 2 * (n + 1) = 2 * n + 2 := by
  rw [Nat.mul_add]
  rfl

theorem real_square_confinement_proof (x y : ℝ) : 2 * x * y ≤ x^2 + y^2 := by
  have h_sq : 0 ≤ (x - y)^2 := sq_nonneg (x - y)
  have h_expand : (x - y)^2 = x^2 - 2 * x * y + y^2 := sub_sq x y
  rw [h_expand] at h_sq
  linarith

end SoHmns
