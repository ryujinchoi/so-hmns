import Mathlib.Data.Nat.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Algebra.GroupPower.Basic
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.Algebra.BigOperators.Intervals

open BigOperators

namespace SoHmns

theorem nat_distrib_successor_proof (n : Nat) : 2 * (n + 1) = 2 * n + 2 := by
  ring

theorem real_square_confinement_proof (x y : Real) : 2 * x * y ≤ x^2 + y^2 := by
  nlinarith

theorem real_mul_commute_proof (a b : Real) : a * b = b * a := by
  exact mul_comm a b

theorem real_add_assoc_proof (a b c : Real) : (a + b) + c = a + (b + c) := by
  exact add_assoc a b c

theorem real_abs_triangle_inequality_proof (a b : Real) : |a + b| ≤ |a| + |b| := by
  exact abs_add a b

theorem nat_gcd_euclidean_proof (a b : Nat) : Nat.gcd a b = Nat.gcd b (a % b) := by
  exact Nat.gcd_rec a b

theorem nat_geometric_sum_proof (n : Nat) : ∑ i ∈ Finset.range (n + 1), 2^i = 2^(n + 1) - 1 := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [Finset.sum_range_succ, ih]
    omega

end SoHmns
