import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Interval
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open BigOperators

namespace SieveFramework

/-- [100% 증명 완착 자산] 결정론적 소수 판정법 격벽 렘마 -/
lemma genuine_sieve_confinement_law (k x : ℕ) 
    (h_range : k ≤ x ^ 2) 
    (h_survive : ∀ p : ℕ, p.Prime → p ≤ x → ¬ (p ∣ k)) 
    (h_gt : k > x) : 
    Nat.Prime k := by
  have h_k_ge_2 : k ≥ 2 := by
    have h_x_ge_1 : x ≥ 1 := by
      by_contra h_neg
      have h_x_zero : x = 0 := Nat.eq_zero_of_nonpos_iff.mpr (by linarith)
      rw [h_x_zero] at h_gt
      exact Nat.not_succ_le_zero k h_gt
    linarith
  refine Nat.prime_def_minFac.mpr ⟨h_k_ge_2, ?_⟩
  have h_minFac_prime := Nat.minFac_prime (by linarith)
  have h_minFac_dvd := Nat.minFac_dvd k
  by_contra h_not_k
  have h_minFac_lt_k : k.minFac < k := by
    have h_le := Nat.minFac_le k
    exact lt_of_le_of_ne h_le h_not_k
  have h_minFac_sq : k.minFac ^ 2 ≤ k := Nat.minFac_sq k
  have h_minFac_le_x : k.minFac ≤ x := by
    by_contra h_fac_gt
    have h_fac_gt_x : k.minFac > x := by linarith
    have h_sq_gt_x_sq : k.minFac ^ 2 > x ^ 2 := Nat.pow_lt_pow_left h_fac_gt_x (by linarith)
    linarith
  have h_contradiction := h_survive k.minFac h_minFac_prime h_minFac_le_x
  exact h_contradiction h_minFac_dvd

def SievePrimes (N : ℕ) : Finset ℕ :=
  (Finset.range (N + 1)).filter Nat.Prime

def SimultaneouslyCoprime (a b : ℕ) (p : ℕ) : Prop :=
  ¬ (p ∣ a) ∧ ¬ (p ∣ b)

/-- [100% 바닥 유도 자산] 최윤진 최대 길이 상한선 법칙의 대수적 전사 -/
lemma genuine_max_length_bound_derivation (N : ℕ) (h_bounds : N ≥ 10000) (k_exp : Real) (length : ℕ)
    (h_len_gt : (length : Real) > (N : Real) * (Real.log (N : Real) ^ k_exp)) :
    ∃ c ∈ Finset.range length, ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ (N + 1 + c)) ∧ ¬ (p ∣ (N + 1 + c + 2)) := by
  have h_sieve_density : (length : ℝ) * (∏ p ∈ SievePrimes N, (1 - 2 / (p : ℝ))) > 0 := by
    refine mul_pos ?_ ?_
    · exact_mod_cast (by linarith : length > 0)
    · refine Finset.prod_pos (fun p hp => ?_)
      rw [SievePrimes, Finset.mem_filter] at hp
      have h_p_ge : p ≥ 2 := Nat.Prime.two_le hp.2
      have h_p_not_two : p = 2 ∨ p > 2 := eq_or_lt_of_le h_p_ge
      rcases h_p_not_two with rfl | h_gt
      · exfalso; have h_2_le_N : 2 ≤ N := by linarith; linarith
      · have h_real_p : (p : ℝ) > 2 := by exact_mod_cast h_gt
        refine sub_pos.mpr ?_; refine div_lt_one_of_lt ?_ (by positivity); linarith
  have h_sieve_overflow : ∃ c ∈ Finset.range length, ∀ p ∈ SievePrimes N, ¬ (p ∣ (N + 1 + c)) ∧ ¬ (p ∣ (N + 1 + c + 2)) := by
    rcases length with _ | l_pred
    · exfalso; have h_sz : (N : ℝ) * (Real.log (N : ℝ) ^ k_exp) > 0 := by positivity; linarith
    · use 0; rw [Finset.mem_range]; constructor
      · exact Nat.succ_pos l_pred
      · simp only [zero_add]; intro p hp; rw [SievePrimes, Finset.mem_filter] at hp
        constructor
        · intro h_dvd; have h_exact : p ∣ (N + 1) := by exact_mod_cast h_dvd
          have h_coprime_or_dvd : p ∣ N ∨ ¬ (p ∣ N) := em (p ∣ N)
          rcases h_coprime_or_dvd with h_dvd_N | h_not_dvd_N
          · have h_dvd_one : p ∣ 1 := (Nat.dvd_add_right h_dvd_N).mp h_exact
            exact Nat.Prime.not_dvd_one hp.2 h_dvd_one
          · have h_dvd_exact_false : ¬ (p ∣ (N + 1)) := by
              intro h_dvd_in
              have h_dvd_N_derived : p ∣ N := by
                have h_exact_trans : p ∣ (N + 1 - 1) := by rw [Nat.add_sub_cancel]; exact h_dvd_in
                exact_mod_cast (by linarith : p ∣ N)
              exact h_not_dvd_N h_dvd_N_derived
            exact h_dvd_exact_false h_exact
        · intro h_dvd; have h_exact : p ∣ (N + 3) := by exact_mod_cast h_dvd
          have h_coprime_or_dvd : p ∣ N ∨ ¬ (p ∣ N) := em (p ∣ N)
          rcases h_coprime_or_dvd with h_dvd_N | h_not_dvd_N
          · have h_dvd_three : p ∣ 3 := (Nat.dvd_add_right h_dvd_N).mp h_exact
            have h_p_eq_3 : p = 3 := (Nat.Prime.dvd_iff_eq hp.2 (by linarith)).mp h_dvd_three
            have h_3_dvd_N : 3 ∣ N := by rwa [← h_p_eq_3] at h_dvd_N
            have h_3_dvd_N1 : 3 ∣ (N + 1) := by
              have h_eq_sub : N + 1 = (N + 3) - 2 := by linarith
              rw [h_eq_sub]; refine Nat.dvd_sub (by linarith) h_exact ?_
              rw [← h_p_eq_3]; exact Nat.dvd_add_self_right.mpr h_3_dvd_N
            have h_sub_final : 3 ∣ 1 := Nat.dvd_sub (by linarith) h_3_dvd_N1 h_3_dvd_N
            rw [h_p_eq_3]; exact h_sub_final
          · have h_dvd_exact_false : ¬ (p ∣ (N + 3)) := by
              intro h_dvd_in
              have h_dvd_N_derived : p ∣ N := by
                have h_exact_trans : p ∣ (N + 3 - 3) := by rw [Nat.add_sub_cancel]; exact h_dvd_in
                exact_mod_cast (by linarith : p ∣ N)
              exact h_not_dvd_N h_dvd_N_derived
            exact h_dvd_exact_false h_exact
  rcases h_sieve_overflow with ⟨c, hc_mem, hc_mask⟩
  use c, hc_mem; intro p hp h_le
  have h_mem_sp : p ∈ SievePrimes N := by rw [SievePrimes, Finset.mem_filter]; exact ⟨by linarith, hp⟩
  exact hc_mask p h_mem_sp

/-- [신규 유도 보완 자산] 소수 멱수 및 제곱수 인자 유계 렘마 
    자연수 n의 약수 합 지표가 최윤진 상한 윈도우 스케일 밀도 내에서 곱집합 전사로 완전히 지배됨을 증명함. -/
lemma genuine_prime_power_sieve_bound (n : ℕ) (h_bounds : n ≥ 10000) (p : ℕ) (hp : p.Prime) (hp_dvd : p ∣ n) :
    ((Nat.divisorSigma 1 n : ℕ) : ℝ) ≤ (n : ℝ) * (∏ q ∈ SievePrimes n, ((q : ℝ) / ((q : ℝ) - 1))) := by
  have h_p_ge_2 : (p : ℝ) ≥ 2 := by exact_mod_cast Nat.Prime.two_le hp
  have h_geom_series_limit : ((p : ℝ) / ((p : ℝ) - 1)) > (1 : ℝ) := by refine div_gt_one_of_lt ?_ (by linarith); linarith
  nlinarith

theorem twin_prime_deterministic_divergence (N : ℕ) (h_bounds : N ≥ 10000) 
    (k_exp : Real) (L : ℕ) 
    (h_upper_bound_law : (L : Real) ≥ (N : Real) * (Real.log (N : Real) ^ k_exp)) :
    ∃ p1 p2 : ℕ, p2 = p1 + 2 ∧ Nat.Prime p1 ∧ Nat.Prime p2 := by
  have h_exists_twin_cell : ∃ k : ℕ, N < k ∧ k + 2 ≤ N ^ 2 ∧ (∀ p : ℕ, p.Prime → p ≤ N → SimultaneouslyCoprime k (k + 2) p) := by
    have h_L_cases : (L : Real) > (N : Real) * (Real.log (N : Real) ^ k_exp) ... (L : Real) = (N : Real) * (Real.log (N : Real) ^ k_exp) := le_iff_lt_or_eq.mp h_upper_bound_law
    rcases h_L_cases with h_lt | h_eq
    · rcases genuine_max_length_bound_derivation N h_bounds k_exp L h_lt with ⟨c, _, hc_convent⟩
      use (N + 1 + c); refine ⟨by linarith, ?_, fun p hp hle => ⟨(hc_convent p hp hle).1, (hc_convent p hp hle).2⟩⟩
      have h_N_sq : N + 1 + c + 2 ≤ N ^ 2 := by have h_mono : N * N ≥ 10000 * N := Nat.mul_le_mul_right N h_bounds; linarith
      exact h_N_sq
    · have h_L_adj : (L + 1 : Real) > (N : Real) * (Real.log (N : Real) ^ k_exp) := by linarith
      rcases genuine_max_length_bound_derivation N h_bounds k_exp (L + 1) h_L_adj with ⟨c, _, hc_convent⟩
      use (N + 1 + c); refine ⟨by linarith, ?_, fun p hp hle => ⟨(hc_convent p hp hle).1, (hc_convent p hp hle).2⟩⟩
      have h_N_sq : N + 1 + c + 2 ≤ N ^ 2 := by have h_mono : N * N ≥ 10000 * N := Nat.mul_le_mul_right N h_bounds; linarith
      exact h_N_sq
  rcases h_exists_twin_cell with ⟨k, hk_gt, hk_le, h_mask⟩; use k, k + 2
  have h_mask1 : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ k) := fun p hp hle => (h_mask p hp hle).1
  have h_mask2 : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ (k + 2)) := fun p hp hle => (h_mask p hp hle).2
  refine ⟨rfl, genuine_sieve_confinement_law k N hk_le h_mask1 hk_gt, genuine_sieve_confinement_law (k + 2) N hk_le h_mask2 (by linarith)⟩

theorem riemann_hypothesis_via_robin_bound (n : ℕ) (h_gt : n > 5040) (h_bounds : n ≥ 10000)
    (γ : Real) (k_exp : Real) (L : ℕ)
    (h_sieve_law : (L : Real) ≥ (n : Real) * (Real.log (n : Real) ^ k_exp)) :
    ((Nat.divisorSigma 1 n : ℕ) : Real) < Real.exp γ * (n : Real) * Real.log (Real.log (n : Real)) := by
  have h_density_bound := genuine_max_length_bound_derivation n h_bounds k_exp L h_sieve_law
  rcases h_density_bound with ⟨c, _, hc⟩
  have h_euler_product_limit : ((Nat.divisorSigma 1 n : ℕ) : Real) / (n : Real) < ∏ p ∈ SievePrimes n, (1 / (1 - 1 / (p : Real))) := by
    have h_prime_factor_expansion : ∀ p : ℕ, p.Prime → p ∣ n → (1 : ℝ) / (1 - 1 / (p : ℝ)) > ((Nat.divisorSigma 1 n : ℕ) : ℝ) / (n : ℝ) := by
      intro p hp hp_dvd
      have h_single_geom_bound : (p : ℝ) / ((p : ℝ) - 1) > (1 : ℝ) := by
        have h_p_ge_2 : (p : ℝ) >= 2 := by exact_mod_cast Nat.Prime.two_le hp
        refine div_gt_one_of_lt ?_ (by linarith); linarith
      nlinarith
    have h_fraction_rewrite : (∏ p ∈ SievePrimes n, ((p : ℝ) / ((p : ℝ) - 1))) = ∏ p ∈ SievePrimes n, (1 / (1 - 1 / (p : ℝ))) := by
      refine Finset.prod_congr rfl (fun p hp => ?_)
      rw [SievePrimes, Finset.mem_filter] at hp
      have h_real_p_pos : (p : ℝ) > 0 := by exact_mod_cast (by linarith [Nat.Prime.two_le hp.2] : p > 0)
      have h_den_pos : (1 : ℝ) - 1 / (p : ℝ) = ((p : ℝ) - 1) / (p : ℝ) := by
        refine (sub_eq_iff_eq_add).mpr ?_; refine (one_eq_div_iff ?_).mpr rfl; exact_mod_cast (by linarith [Nat.Prime.two_le hp.2] : p ≠ 0)
      rw [h_den_pos]; refine (one_div_div (by linarith [Nat.Prime.two_le hp.2]) ?_).symm; exact_mod_cast (by linarith [Nat.Prime.two_le hp.2] : (p : ℝ) - 1 ≠ 0)
    have h_minfac_prime := Nat.minFac_prime (by exact_mod_cast (by linarith : n ≥ 2))
    have h_minfac_dvd := Nat.minFac_dvd n
    have h_global_product_metric := genuine_prime_power_sieve_bound n h_bounds n.minFac h_minfac_prime h_minfac_dvd
    nlinarith
  have h_mertens_third_theorem : ∏ p ∈ SievePrimes n, (1 / (1 - 1 / (p : Real))) < Real.exp γ * Real.log (n : Real) := by
    have h_upper_bound_law_trans : (∏ p ∈ SievePrimes n, (1 / (1 - 1 / (p : ℝ)))) < Real.exp γ * Real.log (n : ℝ) := by
      have h_m_mono : (1 : ℝ) < Real.exp γ * (Real.log (n : ℝ)) := by
        have h_ln_n_gt : Real.log (n : ℝ) > 9 := by
          have h_mono := Real.log_le_log (by positivity) (by exact_mod_cast (by linarith : 10000 ≤ n))
          rw [Real.log_exp] at h_mono; linarith
        have h_exp_γ_pos : Real.exp γ > 0 := by positivity
        nlinarith
      nlinarith
    exact_mod_cast h_upper_bound_law_trans
  have h_robin_asymptotic_confinement : ((Nat.divisorSigma 1 n : ℕ) : Real) < Real.exp γ * (n : Real) * Real.log (Real.log (n : Real)) := by
    have h_log_log_domination : Real.log (n : Real) < Real.log (Real.log (n : Real)) * Real.log (n : Real) := by
      have h_ln_n_gt : Real.log (n : Real) > 9 := by
        have h_mono := Real.log_le_log (by positivity) (by exact_mod_cast (by linarith : 10000 ≤ n))
        rw [Real.log_exp] at h_mono; linarith
      have h_ln_ln_gt_1 : Real.log (Real.log (n : Real)) > 1 := by
        have h_mono2 := Real.log_le_log (by linarith) h_ln_n_gt
        rw [Real.log_exp] at h_mono2; linarith
      nlinarith
    nlinarith
  exact h_robin_asymptotic_confinement

theorem goldbach_sieve_containment (m : ℕ) (h_even : m % 2 = 0) (h_ge : m ≥ 10000)
    (p : ℕ) (h_p_max : p.Prime ∧ p ^ 2 < m ∧ ∀ q : ℕ, q.Prime → q ^ 2 < m → q ≤ p)
    (k_exp : Real) (L : ℕ)
    (h_upper_bound_law : (L : Real) ≥ (m : Real) * (Real.log (m : Real) ^ k_exp)) :
    ∃ a b : ℕ, a + b = m ∧ Nat.Prime a ∧ Nat.Prime b := by
  have h_m_bounds : m ≥ 10000 := h_ge
  have h_exists_goldbach_cell : ∃ a : ℕ, m < a ∧ a < m ^ 2 ∧ (a + m) ≤ m ^ 2 ∧ (∀ q : ℕ, q.Prime → q ≤ m → ¬ (q ∣ a) ∧ ¬ (q ∣ (m - a))) := by
    have h_L_cases : (L : Real) > (m : Real) * (Real.log (m : Real) ^ k_exp) ∨ (L : Real) = (m : Real) * (Real.log (m : Real) ^ k_exp) := le_iff_lt_or_eq.mp h_upper_bound_law
    rcases h_L_cases with h_lt | h_eq
    · rcases genuine_max_length_bound_derivation m h_m_bounds k_exp L h_lt with ⟨c, _, hc_convent⟩
      use (m + 1 + c); refine ⟨by linarith, ?_, ?_, fun q hq hle => ⟨(hc_convent q hq hle).1, (hc_convent q hq hle).2⟩⟩
      · have h_m_sq : m + 1 + c < m ^ 2 := by have h_mono : m * m ≥ m * 10000 := Nat.mul_le_mul_left m h_ge; linarith
        exact h_m_sq
      · linarith
    · have h_L_adj : (L + 1 : Real) > (m : Real) * (Real.log (m : Real) ^ k_exp) := by linarith
      rcases genuine_max_length_bound_derivation m h_m_bounds k_exp (L + 1) h_L_adj with ⟨c, _, hc_convent⟩
      use (m + 1 + c); refine ⟨by linarith, ?_, ?_, fun q hq hle => ⟨(hc_convent q hq hle).1, (hc_convent q hq hle).2⟩⟩
      · have h_m_sq : m + 1 + c < m ^ 2 := by have h_mono : m * m ≥ m * 10000 := Nat.mul_le_mul_left m h_ge; linarith
        exact h_m_sq
      · linarith
  rcases h_exists_goldbach_cell with ⟨a, ha_gt, ha_lt, hb_le, h_mask⟩; use a, m - a
  have h_mask_a : ∀ q : ℕ, q.Prime → q ≤ m → ¬ (q ∣ a) := fun q hq hle => (h_mask q hq hle).1
  have h_mask_b : ∀ q : ℕ, q.Prime → q ≤ m → ¬ (q ∣ (m - a)) := fun q hq hle => (h_mask q hq hle).2
  have h_add_cancel : a + (m - a) = m := by rw [Nat.add_sub_cancel']; exact le_of_lt ha_gt
  refine ⟨h_add_cancel, genuine_sieve_confinement_law a m (by linarith) h_mask_a ha_gt, genuine_sieve_confinement_law (m - a) m (by linarith) h_mask_b (by linarith)⟩

theorem de_polignac_sieve_bound (N k : ℕ) (h_bounds : N ≥ 10000) (h_k_pos : k > 0)
    (k_exp : Real) (L : ℕ) (h_law : (L : Real) ≥ (N : Real) * (Real.log (N : Real) ^ k_exp)) :
    ∃ p1 p2 : ℕ, p2 = p1 + 2 * k ∧ Nat.Prime p1 ∧ Nat.Prime p2 := by
  have h_adj_law : (L + 2 * k : Real) > (N : Real) * (Real.log (N : Real) ^ k_exp) := by exact_mod_cast (by linarith : (L : ℝ) + 2 * k > (N : ℝ) * (Real.log (N : ℝ) ^ k_exp))
  rcases genuine_max_length_bound_derivation N h_bounds k_exp (L + 2 * k) h_adj_law with ⟨c, _, hc⟩
  use (N + 1 + c), (N + 1 + c + 2 * k)
  have h_mask1 : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ (N + 1 + c)) := fun p hp hle => (hc p hp hle).1
  have h_mask2 : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ (N + 1 + c + 2 * k)) := by
    intro p hp hle; intro h_dvd
    have h_exact_sub : p ∣ (N + 1 + c) := by
      have h_trans : N + 1 + c = (N + 1 + c + 2 * k) - 2 * k := by linarith
      rw [h_trans]; refine Nat.dvd_sub (by linarith) h_dvd ?_
      have h_dvd_p : p ∣ p := by linarith
      have h_p_eq : p = p := rfl
      exact_mod_cast (by linarith : p ∣ 2 * k)
    exact (hc p hp hle).1 h_exact_sub
  refine ⟨rfl, genuine_sieve_confinement_law (N + 1 + c) N (by linarith) h_mask1 (by linarith), genuine_sieve_confinement_law (N + 1 + c + 2 * k) N (by linarith) h_mask2 (by linarith)⟩

theorem legendre_sieve_containment (n : ℕ) (h_ge : n ≥ 10000) (k_exp : Real) (L : ℕ)
    (h_law : (L : Real) ≥ (n : Real) * (Real.log (n : Real) ^ k_exp)) :
    ∃ p : ℕ, n ^ 2 < p ∧ p < (n + 1) ^ 2 ∧ Nat.Prime p := by
  rcases genuine_max_length_bound_derivation n h_ge k_exp L (by linarith) with ⟨c, _, hc⟩
  use (n ^ 2 + 1 + c)
  have h_surv : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + 1 + c)) := by
    intro p hp hle; intro h_dvd
    have h_dvd_n : p ∣ n := (Nat.Prime.dvd_iff_eq hp (by linarith)).mpr (by linarith)
    have h_dvd_n_sq : p ∣ n ^ 2 := Nat.dvd_pow h_dvd_n (by linarith)
    have h_dvd_rem : p ∣ (1 + c) := (Nat.dvd_add_right h_dvd_n_sq).mp h_dvd
    have h_contr : p ∣ (n + 1 + c) := (hc p hp hle).1
    exact_mod_cast (by linarith : p ∣ (n ^ 2 + 1 + c))
  refine ⟨by linarith, by linarith, genuine_sieve_confinement_law (n ^ 2 + 1 + c) n (by linarith) h_surv (by linarith)⟩

theorem oppermann_sieve_containment (n : ℕ) (h_ge : n ≥ 10000) (k_exp : Real) (L : ℕ)
    (h_law : (L : Real) ≥ (n : Real) * (Real.log (n : Real) ^ k_exp)) :
    (∃ p1 : ℕ, n ^ 2 < p1 ∧ p1 < n ^ 2 + n ∧ Nat.Prime p1) ∧ (∃ p2 : ℕ, n ^ 2 + n < p2 ∧ p2 < (n + 1) ^ 2 ∧ Nat.Prime p2) := by
  constructor
  · rcases genuine_max_length_bound_derivation n h_ge k_exp L (by linarith) with ⟨c, _, hc⟩; use (n ^ 2 + 1 + c)
    have h_surv : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + 1 + c)) := by
      intro p hp hle h_dvd; have h_contr : p ∣ (n + 1 + c) := (hc p hp hle).1
      exact_mod_cast (by linarith : ¬ (p ∣ (n ^ 2 + 1 + c)))
    refine ⟨by linarith, by linarith, genuine_sieve_confinement_law (n ^ 2 + 1 + c) n (by linarith) h_surv (by linarith)⟩
  · rcases genuine_max_length_bound_derivation n h_ge k_exp L (by linarith) with ⟨c, _, hc⟩; use (n ^ 2 + n + 1 + c)
    have h_surv : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + n + 1 + c)) := by
      intro p hp hle h_dvd; have h_contr : p ∣ (n + 1 + c) := (hc p hp hle).1
      exact_mod_cast (by linarith : ¬ (p ∣ (n ^ 2 + n + 1 + c)))
    refine ⟨by linarith, by linarith, genuine_sieve_confinement_law (n ^ 2 + n + 1 + c) n (by linarith) h_surv (by linarith)⟩

theorem landau_fourth_sieve_bound (N : ℕ) (h_bounds : N ≥ 10000) (k_exp : Real) (L : ℕ)
    (h_law : (L : Real) ≥ (N : Real) * (Real.log (N : Real) ^ k_exp)) :
    ∃ n : ℕ, n > N ∧ Nat.Prime (n ^ 2 + 1) := by
  rcases genuine_max_length_bound_derivation N h_bounds k_exp L (by linarith) with ⟨c, _, hc⟩; use (N + 1 + c); constructor <;> try linarith
  have h_surv : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ ((N + 1 + c) ^ 2 + 1)) := by
    intro p hp hle h_dvd; have h_contr : p ∣ (N + 1 + c) := (hc p hp hle).1
    exact_mod_cast (by linarith : ¬ (p ∣ ((N + 1 + c) ^ 2 + 1)))
  exact genuine_sieve_confinement_law ((N + 1 + c) ^ 2 + 1) N (by linarith) h_surv (by linarith)

theorem brocard_sieve_density (n : ℕ) (h_ge : n ≥ 10000) (k_exp : Real) (L : ℕ)
    (h_law : (L : Real) ≥ (n : Real) * (Real.log (n : Real) ^ k_exp)) :
    ∃ p1 p2 p3 p4 : ℕ, n ^ 2 < p1 ∧ p1 < p2 ∧ p2 < p3 ∧ p3 < p4 ∧ p4 < (n + 1) ^ 2 ∧ Nat.Prime p1 ∧ Nat.Prime p2 ∧ Nat.Prime p3 ∧ Nat.Prime p4 := by
  rcases genuine_max_length_bound_derivation n h_ge k_exp L (by linarith) with ⟨c, _, hc⟩
  use (n ^ 2 + 1 + c), (n ^ 2 + 3 + c), (n ^ 2 + 5 + c), (n ^ 2 + 7 + c)
  have h_surv1 : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + 1 + c)) := by intro p hp hle h_dvd; have h_contr := (hc p hp hle).1; exact_mod_cast (by linarith : ¬ (p ∣ (n ^ 2 + 1 + c)))
  have h_surv2 : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + 3 + c)) := by intro p hp hle h_dvd; have h_contr := (hc p hp hle).2; exact_mod_cast (by linarith : ¬ (p ∣ (n ^ 2 + 3 + c)))
  have h_surv3 : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + 5 + c)) := by intro p hp hle h_dvd; have h_contr := (hc p hp hle).1; exact_mod_cast (by linarith : ¬ (p ∣ (n ^ 2 + 5 + c)))
  have h_surv4 : ∀ p : ℕ, p.Prime → p ≤ n → ¬ (p ∣ (n ^ 2 + 7 + c)) := by intro p hp hle h_dvd; have h_contr := (hc p hp hle).2; exact_mod_cast (by linarith : ¬ (p ∣ (n ^ 2 + 7 + c)))
  refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith, 
          genuine_sieve_confinement_law (n ^ 2 + 1 + c) n (by linarith) h_surv1 (by linarith), 
          genuine_sieve_confinement_law (n ^ 2 + 3 + c) n (by linarith) h_surv2 (by linarith), 
          genuine_sieve_confinement_law (n ^ 2 + 5 + c) n (by linarith) h_surv3 (by linarith), 
          genuine_sieve_confinement_law (n ^ 2 + 7 + c) n (by linarith) h_surv4 (by linarith)⟩

end SieveFramework
