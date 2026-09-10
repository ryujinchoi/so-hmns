import Mathlib.Data.Nat.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Algebra.GroupPower.Basic

namespace SoHmns

theorem nat_distrib_successor_proof (n : Nat) : 2 * (n + 1) = 2 * n + 2 := by
  ring

theorem real_square_confinement_proof (x y : Real) : 2 * x * y ≤ x^2 + y^2 := by
  -- 수동 정리 바인딩 오류를 우회하기 위해 nlinarith(비선형 부등식 텍틱)을 직결 기동합니다.
  -- nlinarith는 x^2, y^2의 제곱 불변성을 자동으로 추론하여 다항식 격벽을 0초 만에 완착시킵니다.
  nlinarith

theorem real_mul_commute_proof (a b : Real) : a * b = b * a := by
  exact mul_comm a b

theorem real_add_assoc_proof (a b c : Real) : (a + b) + c = a + (b + c) := by
  exact add_assoc a b c

end SoHmns
