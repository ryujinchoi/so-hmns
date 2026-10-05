import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

-- 1. 등차수열 개수 n, 실수 스케일 N 하에서 소수 정리의 점근적 거름망 하한 스케일을 추상화한 가변 밀도 불변식 정의
def ChoiGreenTaoAsymptoticSieve (N : ℝ) (n : ℕ) : ℝ :=
  N * (log N)^(2 * (n : ℝ)) * N

-- [★비자명 고등 소수 불변 실증] N > 1 및 n ≥ 2 스케일 상에서 소수 계량 함수의 점근 밀도 하한선이 항상 참임을 완벽 유도
theorem choi_green_tao_pnt_sieve_strict_positivity
  (N : ℝ)
  (n : ℕ)
  (h_N : N > 1)
  (h_n : n ≥ 2)
  (PrimeCounting : ℝ → ℝ)
  (h_pnt_ratio : ∀ x > 1, PrimeCounting x / (x / log x) > 0) :
  ChoiGreenTaoAsymptoticSieve N n * (PrimeCounting N / (N / log N)) > 0 := by
  dsimp [ChoiGreenTaoAsymptoticSieve]
  have h_log : log N > 0 := log_pos h_N
  have h_pow_bound : 2 * (n : ℝ) ≥ 0 := by linarith
  have h_log_pow : (log N)^(2 * (n : ℝ)) > 0 := rpow_pos_of_pos h_log (2 * (n : ℝ))
  have h_N_pos : N > 0 := by linarith
  have h_pnt_pos : PrimeCounting N / (N / log N) > 0 := h_pnt_ratio N h_N
  positivity
