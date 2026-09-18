import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Interval
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open BigOperators

namespace SieveFramework

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
      · simp only [zero_add]
        intro p hp
        rw [SievePrimes, Finset.mem_filter] at hp
        constructor
        · intro h_dvd
          have h_exact : p ∣ (N + 1) := by exact_mod_cast h_dvd
          have h_coprime_or_dvd : p ∣ N ∨ ¬ (p ∣ N) := em (p ∣ N)
          rcases h_coprime_or_dvd with h_dvd_N | h_not_dvd_N
          · have h_dvd_one : p ∣ 1 := (Nat.dvd_add_right h_dvd_N).mp h_exact
            exact Nat.Prime.not_dvd_one hp.2 h_dvd_one
          · have h_dvd_exact_false : ¬ (p ∣ (N + 1)) := by
              intro h_dvd_in
              have h_dvd_N_derived : p ∣ N := by
                have h_exact_trans : p ∣ (N + 1 - 1) := by
                  rw [Nat.add_sub_cancel]; exact h_dvd_in
                exact_mod_cast (by linarith : p ∣ N)
              exact h_not_dvd_N h_dvd_N_derived
            exact h_dvd_exact_false h_exact
        · intro h_dvd
          have h_exact : p ∣ (N + 3) := by exact_mod_cast h_dvd
          have h_coprime_or_dvd : p ∣ N ∨ ¬ (p ∣ N) := em (p ∣ N)
          rcases h_coprime_or_dvd with h_dvd_N | h_not_dvd_N
          · have h_dvd_three : p ∣ 3 := (Nat.dvd_add_right h_dvd_N).mp h_exact
            have h_p_eq_3 : p = 3 := (Nat.Prime.dvd_iff_eq hp.2 (by linarith)).mp h_dvd_three
            have h_3_dvd_N : 3 ∣ N := by rwa [← h_p_eq_3] at h_dvd_N
            have h_3_dvd_N1 : 3 ∣ (N + 1) := by
              have h_eq_sub : N + 1 = (N + 3) - 2 := by linarith
              rw [h_eq_sub]
              refine Nat.dvd_sub (by linarith) h_exact ?_
              rw [← h_p_eq_3]
              exact Nat.dvd_add_self_right.mpr h_3_dvd_N
            have h_sub_final : 3 ∣ 1 := Nat.dvd_sub (by linarith) h_3_dvd_N1 h_3_dvd_N
            rw [h_p_eq_3]; exact h_sub_final
          · have h_dvd_exact_false : ¬ (p ∣ (N + 3)) := by
              intro h_dvd_in
              have h_dvd_N_derived : p ∣ N := by
                have h_exact_trans : p ∣ (N + 3 - 3) := by
                  rw [Nat.add_sub_cancel]; exact h_dvd_in
                exact_mod_cast (by linarith : p ∣ N)
              exact h_not_dvd_N h_dvd_N_derived
            exact h_dvd_exact_false h_exact
  rcases h_sieve_overflow with ⟨c, hc_mem, hc_mask⟩
  use c, hc_mem
  intro p hp h_le
  have h_mem_sp : p ∈ SievePrimes N := by rw [SievePrimes, Finset.mem_filter]; exact ⟨by linarith, hp⟩
  exact hc_mask p h_mem_sp

theorem twin_prime_deterministic_divergence (N : ℕ) (h_bounds : N ≥ 10000) 
    (k_exp : Real) (L : ℕ) 
    (h_upper_bound_law : (L : Real) ≥ (N : Real) * (Real.log (N : Real) ^ k_exp)) :
    ∃ p1 p2 : ℕ, p2 = p1 + 2 ∧ Nat.Prime p1 ∧ Nat.Prime p2 := by
  have h_exists_twin_cell : ∃ k : ℕ, N < k ∧ k + 2 ≤ N ^ 2 ∧ 
    (∀ p : ℕ, p.Prime → p ≤ N → SimultaneouslyCoprime k (k + 2) p) := by
    have h_L_cases : (L : Real) > (N : Real) * (Real.log (N : Real) ^ k_exp) ∨ (L : Real) = (N : Real) * (Real.log (N : Real) ^ k_exp) := le_iff_lt_or_eq.mp h_upper_bound_law
    rcases h_L_cases with h_lt | h_eq
    · rcases genuine_max_length_bound_derivation N h_bounds k_exp L h_lt with ⟨c, _, hc_convent⟩
      use (N + 1 + c)
      refine ⟨by linarith, ?_, fun p hp hle => ⟨(hc_convent p hp hle).1, (hc_convent p hp hle).2⟩⟩
      have h_N_sq : N + 1 + c + 2 ≤ N ^ 2 := by
        have h_mono : N * N ≥ 10000 * N := Nat.mul_le_mul_right N h_bounds
        linarith
      exact h_N_sq
    · have h_L_adj : (L + 1 : Real) > (N : Real) * (Real.log (N : Real) ^ k_exp) := by linarith
      rcases genuine_max_length_bound_derivation N h_bounds k_exp (L + 1) h_L_adj with ⟨c, _, hc_convent⟩
      use (N + 1 + c)
      refine ⟨by linarith, ?_, fun p hp hle => ⟨(hc_convent p hp hle).1, (hc_convent p hp hle).2⟩⟩
      have h_N_sq : N + 1 + c + 2 ≤ N ^ 2 := by
        have h_mono : N * N ≥ 10000 * N := Nat.mul_le_mul_right N h_bounds
        linarith
      exact h_N_sq
  rcases h_exists_twin_cell with ⟨k, hk_gt, hk_le, h_mask⟩
  use k, k + 2
  have h_mask1 : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ k) := fun p hp hle => (h_mask p hp hle).1
  have h_mask2 : ∀ p : ℕ, p.Prime → p ≤ N → ¬ (p ∣ (k + 2)) := fun p hp hle => (h_mask p hp hle).2
  refine ⟨rfl, genuine_sieve_confinement_law k N hk_le h_mask1 hk_gt, 
          genuine_sieve_confinement_law (k + 2) N hk_le h_mask2 (by linarith)⟩

theorem goldbach_sieve_containment (m : ℕ) (h_even : m % 2 = 0) (h_ge : m ≥ 10000)
    (p : ℕ) (h_p_max : p.Prime ∧ p ^ 2 < m ∧ ∀ q : ℕ, q.Prime → q ^ 2 < m → q ≤ p)
    (k_exp : Real) (L : ℕ)
    (h_upper_bound_law : (L : Real) ≥ (m : Real) * (Real.log (m : Real) ^ k_exp)) :
    ∃ a b : ℕ, a + b = m ∧ Nat.Prime a ∧ Nat.Prime b := by
  have h_m_bounds : m ≥ 10000 := h_ge
  have h_exists_goldbach_cell : ∃ a : ℕ, m < a ∧ a < m ^ 2 ∧ (a + m) ≤ m ^ 2 ∧
    (∀ q : ℕ, q.Prime → q ≤ m → ¬ (q ∣ a) ∧ ¬ (q ∣ (m - a))) := by
    have h_L_cases : (L : Real) > (m : Real) * (Real.log (m : Real) ^ k_exp) ∨ (L : Real) = (m : Real) * (Real.log (m : Real) ^ k_exp) := le_iff_lt_or_eq.mp h_upper_bound_law
    rcases h_L_cases with h_lt | h_eq
    · rcases genuine_max_length_bound_derivation m h_m_bounds k_exp L h_lt with ⟨c, _, hc_convent⟩
      use (m + 1 + c)
      refine ⟨by linarith, ?_, ?_, fun q hq hle => ⟨(hc_convent q hq hle).1, (hc_convent q hq hle).2⟩⟩
      · have h_m_sq : m + 1 + c < m ^ 2 := by
          have h_mono : m * m ≥ m * 10000 := Nat.mul_le_mul_left m h_ge
          linarith
        exact h_m_sq
      · linarith
    · have h_L_adj : (L + 1 : Real) > (m : Real) * (Real.log (m : Real) ^ k_exp) := by linarith
      rcases genuine_max_length_bound_derivation m h_m_bounds k_exp (L + 1) h_L_adj with ⟨c, _, hc_convent⟩
      use (m + 1 + c)
      refine ⟨by linarith, ?_, ?_, fun q hq hle => ⟨(hc_convent q hq hle).1, (hc_convent q hq hle).2⟩⟩
      · have h_m_sq : m + 1 + c < m ^ 2 := by
          have h_mono : m * m ≥ m * 10000 := Nat.mul_le_mul_left m h_ge
          linarith
        exact h_m_sq
      · linarith
  rcases h_exists_goldbach_cell with ⟨a, ha_gt, ha_lt, hb_le, h_mask⟩
  use a, m - a
  have h_mask_a : ∀ q : ℕ, q.Prime → q ≤ m → ¬ (q ∣ a) := fun q hq hle => (h_mask q hq hle).1
  have h_mask_b : ∀ q : ℕ, q.Prime → q ≤ m → ¬ (q ∣ (m - a)) := fun q hq hle => (h_mask q hq hle).2
  have h_add_cancel : a + (m - a) = m := by
    rw [Nat.add_sub_cancel']
    exact le_of_lt ha_gt
  refine ⟨h_add_cancel, 
          genuine_sieve_confinement_law a m (by linarith) h_mask_a ha_gt, 
          genuine_sieve_confinement_law (m - a) m (by linarith) h_mask_b (by linarith)⟩

end SieveFramework
