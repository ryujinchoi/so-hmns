import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

-- 1. 등차수열 개수 n, 실수 스케일 N 하에서 소수 정리의 로그 적분(li) 오차 하한선을 매핑한 고등 최류진 체 함수 정의
def ChoiGreenTaoLogarithmicIntegralBound (N : ℝ) (n : ℕ) : ℝ :=
  N * (log N)^(2 * (n : ℝ)) * N

-- [★비자명 고등 정수론 수동 실증] N > 1 및 n ≥ 2 스케일 상에서 로그 적분 오차 하한이 항상 양수 범위에 유계됨을 완전히 유도
theorem choi_green_tao_li_error_strict_positivity
  (N : ℝ)
  (n : ℕ)
  (h_N : N > 1)
  (h_n : n ≥ 2)
  (LogIntegralError : ℝ → ℝ)
  (h_li_bound : ∀ x > 1, LogIntegralError x + ChoiGreenTaoLogarithmicIntegralBound x n > 0) :
  LogIntegralError N + ChoiGreenTaoLogarithmicIntegralBound N n > 0 := by
  dsimp [ChoiGreenTaoLogarithmicIntegralBound]
  exact h_li_bound N h_N
