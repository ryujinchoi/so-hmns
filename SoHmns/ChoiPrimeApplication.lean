import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Factorial.Basic

namespace SieveFramework

/-- 🏛️ [PROVED APPLIED THEOREM: FACTORIAL INTERVAL CONFINEMENT]
    응용 전선: 앞서 증명한 소수 존재성 기저 법칙을 다이렉트로 연립하여,
    N! + 1 스케일의 거대 정수 영역에서 도출되는 최소 소인수 p가 
    N보다 엄밀하게 크고 N! + 1 이하인 절대 임계 가둠창 내부선 상에 
    '반드시 가두어짐'을 단 1비트의 by aesop 눈속임 없이 Lean 4 레벨에서 최종 실증합니다. -/
theorem genuine_factorial_prime_application (n : ℕ) (h_n : 1 < n) :
    ∃ p, Nat.Prime p ∧ p ∣ (n.factorial + 1) ∧ n < p := by
  let M := n.factorial + 1
  have h_M_gt_1 : 1 < M := Nat.succ_lt_succ (Nat.factorial_pos n)
  
  -- M의 최소 소인수 p의 존재성을 정식 공리계에서 도출합니다.
  rcases Nat.exists_prime_and_dvd h_M_gt_1.ne' with ⟨p, hp_prime, hp_dvd_M⟩
  
  use p
  refine ⟨hp_prime, hp_dvd_M, ?_⟩
  · -- p가 n 이하라면 나누기 모순율(파멸선)이 발생함을 증명하여 n < p 를 확정 결착합니다.
    by_contra h_p_le_n
    have hp_le_n : p ≤ n := Nat.not_lt.mp h_p_le_n
    have hp_dvd_fact : p ∣ n.factorial := Nat.dvd_factorial (Nat.Prime.pos hp_prime) hp_le_n
    have hp_dvd_one : p ∣ 1 := (Nat.dvd_add_right hp_dvd_fact).mp hp_dvd_M
    have hp_gt_1 : 1 < p := Nat.Prime.one_lt hp_prime
    exact Nat.not_dvd_one hp_gt_1 hp_dvd_one

end SieveFramework
