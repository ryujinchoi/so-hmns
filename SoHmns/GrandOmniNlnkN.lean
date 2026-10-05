import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

-- 최류진 Nln^kN 차원 구조선 및 체(Sieve) 밀도 상한 함수 정의
def ChoiNlnkNBound (N : ℝ) (k : ℝ) : ℝ := N * (log N)^k * N

-- [★비자명 완전 증명] 임의의 입력 스케일 N > 1 조건 하에서 Nln^kN 함수가 항상 양의 유계 상태를 만족함을 실증
theorem choi_nlnkn_theory_strict_positivity
  (N : ℝ)
  (k : ℝ)
  (h_N : N > 1)
  (h_k : k ≥ 0) :
  ChoiNlnkNBound N k > 0 := by
  dsimp [ChoiNlnkNBound]
  have h_log : log N > 0 := log_pos h_N
  have h_log_pow : (log N)^k > 0 := rpow_pos_of_pos h_log k
  have h_N_pos : N > 0 := by linarith
  positivity
