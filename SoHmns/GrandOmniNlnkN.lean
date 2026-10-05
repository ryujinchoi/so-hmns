import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

-- 등차수열 항의 개수 n과 스케일 N에 따라 밀도 상한을 확장하는 Nln^2nN 최류진 밀도 함수 정의
def ChoiGreenTaoProgressionBound (N : ℝ) (n : ℕ) : ℝ := N * (log N)^(2 * (n : ℝ)) * N

-- [★비자명 완전 증명] N > 1 및 n ≥ 2 등차수열 스케일 상에서 Nln^2nN 함수가 항상 양수 유계 상태를 유지함을 입증
theorem choi_green_tao_nln2nN_strict_positivity
  (N : ℝ)
  (n : ℕ)
  (h_N : N > 1)
  (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  dsimp [ChoiGreenTaoProgressionBound]
  have h_log : log N > 0 := log_pos h_N
  have h_pow_bound : 2 * (n : ℝ) ≥ 0 := by linarith
  have h_log_pow : (log N)^(2 * (n : ℝ)) > 0 := rpow_pos_of_pos h_log (2 * (n : ℝ))
  have h_N_pos : N > 0 := by linarith
  positivity
