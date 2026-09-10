import Mathlib.Data.Nat.Basic
import Mathlib.Algebra.Order.Ring.Defs
import Mathlib.Algebra.Order.AbsoluteValue
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Data.Nat.Pow

open BigOperators

namespace SoHmns

-- [정리 1: 자연수 분배 법칙 및 Successor 결착]
theorem nat_distrib_successor_proof (n : Nat) : 2 * (n + 1) = 2 * n + 2 := by
  rw [Nat.mul_add]
  rfl

-- [정리 2: 완전 제곱식 하반연속 대수 격벽]
theorem real_square_confinement_proof (x y : ℝ) : 2 * x * y ≤ x^2 + y^2 := by
  have h_sq : 0 ≤ (x - y)^2 := sq_nonneg (x - y)
  have h_expand : (x - y)^2 = x^2 - 2 * x * y + y^2 := sub_sq x y
  rw [h_expand] at h_sq
  linarith

-- [정리 3: 실수의 곱셈 교환 대칭성]
theorem real_mul_commute_proof (a b : ℝ) : a * b = b * a := by
  exact mul_comm a b

-- [정리 4: 실수의 선형 덧셈 결합 법칙]
theorem real_add_assoc_proof (a b c : ℝ) : (a + b) + c = a + (b + c) := by
  exact add_assoc a b c

-- [정리 5: 실수의 절댓값 삼각부등식]
theorem real_abs_triangle_inequality_proof (a b : ℝ) : |a + b| ≤ |a| + |b| := by
  exact abs_add a b

-- [정리 6: 유클리드 최대공약수 불변 정리]
theorem nat_gcd_euclidean_proof (a b : Nat) : Nat.gcd a b = Nat.gcd b (a % b) := by
  exact Nat.gcd_rec a b

-- [정리 7: 수학적 귀납법 기반 등비수열 합 공식]
theorem nat_geometric_sum_proof (n : Nat) : ∑ i ∈ Finset.range (n + 1), 2^i = 2^(n + 1) - 1 := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [Finset.sum_range_succ, ih]
    omega

end SoHmns
