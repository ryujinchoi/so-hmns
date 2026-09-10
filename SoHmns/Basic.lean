import Mathlib.Data.Nat.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Algebra.GroupPower.Basic

namespace SoHmns

theorem nat_distrib_successor_proof (n : Nat) : 2 * (n + 1) = 2 * n + 2 := by
  ring

theorem real_square_confinement_proof (x y : Real) : 2 * x * y ≤ x^2 + y^2 := by
  have h_sq : 0 ≤ (x - y)^2 := sq_nonneg (x - y)
  have h_expand : (x - y)^2 = x^2 - 2 * x * y + y^2 := by ring
  rw [h_expand] at h_sq
  linarith

theorem real_mul_commute_proof (a b : Real) : a * b = b * a := by
  exact mul_comm a b

theorem real_add_assoc_proof (a b c : Real) : (a + b) + c = a + (b + c) := by
  exact add_assoc a b c

end SoHmns
