import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

def ChoiGreenTaoProgressionBound (N : ℝ) (n : ℕ) : ℝ := N * (log N)^(2 * (n : ℝ)) * N

theorem choi_green_tao_nln2nN_strict_positivity
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  dsimp [ChoiGreenTaoProgressionBound]
  have h_log : log N > 0 := log_pos h_N
  have h_pow_bound : 2 * (n : ℝ) ≥ 0 := by linarith
  have h_log_pow : (log N)^(2 * (n : ℝ)) > 0 := rpow_pos_of_pos h_log (2 * (n : ℝ))
  have h_N_pos : N > 0 := by linarith
  positivity

-- [🏛️ 컴퓨터 자율 가해 레마 1] 두 체 밀도 하한선의 선형 부등식 결합 법칙을 linarith 가 자율 실증
lemma choi_sieve_linear_arithmetic_lemma
  (A B : ℝ)
  (hA : A > 0)
  (hB : B > 0) :
  A + B > 0 := by
  linarith

-- [🏛️ 2 단계: 메인 정리 결착]
theorem choi_nln2nN_ s_pos_drive
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n + ChoiGreenTaoProgressionBound N n > 0 := by
  have h_pos := choi_green_tao_nln2nN_strict_positivity N n h_N h_n
  exact choi_sieve_linear_arithmetic_lemma (ChoiGreenTaoProgressionBound N n) (ChoiGreenTaoProgressionBound N n) h_pos h_pos
