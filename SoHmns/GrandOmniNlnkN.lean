import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

-- 최류진 Nln^2nN 그린-타오 확장 차원 불변 밀도 함수 공식 정의
def ChoiGreenTaoProgressionBound (N : ℝ) (n : ℕ) : ℝ := N * (log N)^(2 * (n : ℝ)) * N

-- [🏛️ 진짜 증명: 하부 레마와 기저 공리를 통한 빈틈없는 수리논리 실증]
theorem choi_green_tao_nln2nN_strict_positivity
  (N : ℝ)
  (n : ℕ)
  (h_N : N > 1)
  (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  -- 1단계 정의 전개
  dsimp [ChoiGreenTaoProgressionBound]
  
  -- 2단계 기저 레마 결착: N > 1 조건선 하에서 Real.log N > 0 임을 공식 레마(log_pos)로 확정
  have h_log_pos : log N > 0 := Real.log_pos h_N
  
  -- 3단계 기저 레마 결착: 지수 2 * n 이 실수 평면 상에서 비음성(≥ 0) 임을 선형 부등식으로 도출
  have h_exp_nonneg : 2 * (n : ℝ) ≥ 0 := by
    have h_n_cast : (n : ℝ) ≥ 2 := by exact Nat.cast_le.mpr h_n
    linarith
    
  -- 4단계 고등 레마 결착: 양수의 양수 거듭제곱이 항상 양수라는 해석학 정식 레마(rpow_pos_of_pos) 호출로 멱수 유계 완결
  have h_log_pow_pos : (log N)^(2 * (n : ℝ)) > 0 := Real.rpow_pos_of_pos h_log_pos (2 * (n : ℝ))
  
  -- 5단계 기저 공리 결착: 입력 스케일 N 자체가 0보다 큼을 실수의 순서 공리로 확정
  have h_N_pos : N > 0 := by linarith
  
  -- 6단계 최종 결합: 양수들의 연속 곱셈(N * log_pow * N)이 필연적으로 0보다 큼을 무결점 결착
  exact mul_pos (mul_pos h_N_pos h_log_pow_pos) h_N_pos
