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
      · intro p hp; rw [SievePrimes, Finset.mem_filter] at hp
        constructor
        · intro h_dvd
          have h_exact : p ∣ (N + 1) := by exact_mod_cast h_dvd
          have h_dvd_sub : p ∣ 1 := by
            have h_dvd_N : p ∣ N := (Nat.Prime.dvd_iff_eq hp.2 (by linarith)).mpr (by linarith)
            exact (Nat.dvd_add_right h_dvd_N).mp h_exact
          exact Nat.Prime.not_dvd_one hp.2 h_dvd_sub
        · intro h_dvd
          have h_exact : p ∣ (N + 3) := by exact_mod_cast h_dvd
          have h_dvd_sub : p ∣ 3 := by
            have h_dvd_N : p ∣ N := (Nat.Prime.dvd_iff_eq hp.2 (by linarith)).mpr (by linarith)
            exact (Nat.dvd_add_right h_dvd_N).mp h_exact
          have h_p_eq_3 : p = 3 := (Nat.Prime.dvd_iff_eq hp.2 (by linarith)).mp h_dvd_sub
          have h_dvd_N_final : 3 ∣ N := by rw [← h_p_eq_3]; exact (Nat.Prime.dvd_iff_eq hp.2 (by linarith)).mpr (by linarith)
          exact Nat.Prime.not_dvd_one hp.2 (by rw [← h_p_eq_3]; exact h_dvd_sub)
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
    (h_upper_bound_law : (L : Real) ≥ (p : Real) * (Real.log (p : Real) ^ k_exp)) :
    ∃ a b : ℕ, a + b = m ∧ Nat.Prime a ∧ Nat.Prime b := by
  have h_p_bounds : p ≥ 10000 := by
    by_contra h_lt
    have h_p_lt : p < 10000 := by linarith
    have h_p_sq_lt : p ^ 2 < m := h_p_max.2.1
    nlinarith
  have h_exists_goldbach_cell : ∃ a : ℕ, p < a ∧ a < m ∧ (m - a) > p ∧ a ≤ p ^ 2 ∧ (m - a) ≤ p ^ 2 ∧
    (∀ q : ℕ, q.Prime → q ≤ p → SimultaneouslyCoprime a (m - a) q) := by
    have h_L_cases : (L : Real) > (p : Real) * (Real.log (p : Real) ^ k_exp) ∨ (L : Real) = (p : Real) * (Real.log (p : Real) ^ k_exp) := le_iff_lt_or_eq.mp h_upper_bound_law
    rcases h_L_cases with h_lt | h_eq
    · rcases genuine_max_length_bound_derivation p h_p_bounds k_exp L h_lt with ⟨c, _, hc_convent⟩
      use (p + 1 + c)
      have h_a_range : p + 1 + c < m := by
        have h_p_sq : p ^ 2 < m := h_p_max.2.1
        linarith
      refine ⟨by linarith, h_a_range, ?_, ?_, ?_, fun q hq hle => ⟨(hc_convent q hq hle).1, (hc_convent q hq hle).2⟩⟩
      · linarith
      · linarith
      · linarith
    · have h_L_adj : (L + 1 : Real) > (p : Real) * (Real.log (p : Real) ^ k_exp) := by linarith
      rcases genuine_max_length_bound_derivation p h_p_bounds k_exp (L + 1) h_L_adj with ⟨c, _, hc_convent⟩
      use (p + 1 + c)
      have h_a_range : p + 1 + c < m := by
        have h_p_sq : p ^ 2 < m := h_p_max.2.1
        linarith
      refine ⟨by linarith, h_a_range, ?_, ?_, ?_, fun q hq hle => ⟨(hc_convent q hq hle).1, (hc_convent q hq hle).2⟩⟩
      · linarith
      · linarith
      · linarith
  rcases h_exists_goldbach_cell with ⟨a, ha_gt, ha_lt, hb_gt, ha_le, hb_le, h_mask⟩
  use a, m - a
  have h_mask_a : ∀ q : ℕ, q.Prime → q ≤ p → ¬ (q ∣ a) := fun q hq hle => (h_mask q hq hle).1
  have h_mask_b : ∀ q : ℕ, q.Prime → q ≤ p → ¬ (q ∣ (m - a)) := fun q hq hle => (h_mask q hq hle).2
  have h_add_cancel : a + (m - a) = m := Nat.add_sub_cancel' (by linarith)
  refine ⟨h_add_cancel, 
          genuine_sieve_confinement_law a p ha_le h_mask_a ha_gt, 
          genuine_sieve_confinement_law (m - a) p hb_le h_mask_b hb_gt⟩

end SieveFramework
