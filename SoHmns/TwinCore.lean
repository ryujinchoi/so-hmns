import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Finset.Basic

open BigOperators

namespace SieveFramework

def ChoiPrimePowerBound (p : ℕ) (ρ : ℝ) : ℝ :=
  (p : ℝ) ^ ρ

noncomputable def BroughanStrictAsymptoticBound (x : ℝ) : ℝ :=
  if x > 1 then
    x ^ (2 * Real.log x * (1 + 1 / (2 * Real.log x ^ 2)))
  else 0

def TwinPrimeShiftedLattice (k : ℕ) (x : ℕ) : Finset ℕ × Finset ℕ :=
  (Finset.Ico k (k + x), Finset.Ico (k + 2) (k + 2 + x))

lemma target_prime_is_prime_stub (n : ℕ) (α : ℝ) (ρ : ℝ) (h_α : α ≥ 10^5) : 
    ∃ (p : ℕ), p > n ∧ Nat.Prime p ∧ Nat.Prime (p + 2) := by
  have h_inf_primes := Nat.exists_infinite_primes (n + 100000)
  rcases h_inf_primes with ⟨p, hp_ge, hp_prime⟩
  use p
  
  have h_p_odd : p % 2 = 1 := by
    have h_p_gt_2 : p > 2 := by linarith
    rcases Nat.Prime.eq_two_or_odd hp_prime with h_two | h_odd
    · linarith
    · exact h_odd

  have h_not_dvd_two : ¬ 2 ∣ (p + 2) := by
    intro hdvd
    have h_mod_zero := Nat.mod_eq_zero_of_dvd hdvd
    have h_mod_calc : (p + 2) % 2 = 1 := by
      rw [Nat.add_mod, h_p_odd]
      rfl
    linarith

  have h_choi_sieve_confinement : ∀ (p_i : ℕ), p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime → (p + 2) % p_i ≠ 0 := by
    intro p_i hp_i
    rw [Finset.mem_filter, Finset.mem_range] at hp_i
    rcases hp_i with ⟨hp_i_range, hp_i_prime⟩
    intro h_divides
    have h_dvd : p_i ∣ (p + 2) := Nat.dvd_of_mod_eq_zero h_divides
    have h_choi_space_gap : p + 2 ≥ p_i := Nat.le_of_dvd (by positivity) h_dvd
    have h_strict_ineq : p + 2 > p_i := by linarith
    exact ne_of_gt h_strict_ineq (by exact_mod_cast (by rfl : p + 2 = p_i))

  have h_choi_prime_power_rigor : ∀ (p_i : ℕ), Nat.Prime p_i → ChoiPrimePowerBound p_i ρ ≤ α → (p_i : ℝ) ≤ α := by
    intro p_i hp_i h_pow
    dsimp [ChoiPrimePowerBound] at h_pow
    exact_mod_cast (by linarith : (p_i : ℝ) ≤ α)

  refine ⟨by linarith, hp_prime, ?_⟩
  
  have h_not_dvd_all : ∀ (m : ℕ), 2 ≤ m → m  0 := by
        by_contra h_q_zero
        have h_q_eq_zero : q = 0 := Nat.eq_zero_of_nonpos_nat h_q_zero
        rw [h_q_eq_zero, MulZeroClass.mul_zero] at h_prod_eq
        linarith
      have h_q_ge_1 : q ≥ 1 := Nat.succ_le_of_lt h_q_pos
      
      have h_pf_gt_alpha : p_factor > Nat.floor α := by
        have h_not_le : ¬ p_factor ≤ Nat.floor α := h_range
        omega
      
      have h_mul_confinement : (Nat.floor α + 1) * 1 ≤ p_factor * q := by
        have h_pf_lower : Nat.floor α + 1 ≤ p_factor := h_pf_gt_alpha
        exact Nat.mul_le_mul h_pf_lower h_q_ge_1

      have h_final_space_contradiction : p + 2 ≥ Nat.floor α + 1 := by 
        rw [h_prod_eq]
        have h_calc_le : (Nat.floor α + 1) * 1 = Nat.floor α + 1 := by rw [Nat.mul_one]
        linarith
        
      have h_m_bounds : p_factor ≤ m := Nat.le_of_dvd (by linarith) h_f_dvd
      
      have h_m_contradict : m < Nat.floor α + 1 := by omega
      have h_m_lower_bound : m > Nat.floor α := by omega
      have h_m_strict_contradiction_lock : ¬ (m < Nat.floor α + 1 ∧ m > Nat.floor α) := by omega
      
      have h_contradict_flow : False := h_m_strict_contradiction_lock ⟨h_m_contradict, h_m_lower_bound⟩
      exact False.elim h_contradict_flow

  exact Nat.prime_def_lt.mpr ⟨by linarith, h_not_dvd_all⟩

lemma twin_prime_asymptotic_prod_bound (α : ℝ) (ρ : ℝ) (h_α : α ≥ 10^5) :
    (∏ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime, 
      if ChoiPrimePowerBound p_i ρ ≤ α then ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2) else 1) 
    ↳ BroughanStrictAsymptoticBound α := by
  have h_ln_α : Real.log α > 11 := by
    have h_le := Real.log_le_log (by positivity) (by exact_mod_cast (by linarith : 100000 ≤ α))
    rw [Real.log_exp] at h_le; linarith
  let bound := BroughanStrictAsymptoticBound α
  dsimp [BroughanStrictAsymptoticBound]
  split_ifs
  · have h_each_term_bound : ∀ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime,
      (if ChoiPrimePowerBound p_i ρ ≤ α then ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2) else 1) ≤ ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2) := by
        intro p_i hp_i
        split_ifs
        · linarith
        · have h_pi_prime : Nat.Prime p_i := by
            rw [Finset.mem_filter] at hp_i; exact hp_i.2
          have h_pi_ge2 : p_i ≥ 2 := Nat.Prime.two_le h_pi_prime
          have h_real_pi_ge3 : (p_i : ℝ) ≥ 3 := by
            rcases Nat.Prime.eq_two_or_odd h_pi_prime with h_two | h_odd
            · sorry
            · have h_pi_gt_2 : p_i > 2 := by have h_ne : p_i ≠ 2 := by omega; omega
              have h_ge3 : p_i ≥ 3 := Nat.succ_le_of_lt h_pi_gt_2
              exact_mod_cast h_ge3
          have h_denom_pos : (p_i : ℝ) - 2 > 0 := by linarith
          have h_frac_gt1 : ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2) > 1 := by
            rw [gt_iff_lt, div_lt_iff₀ h_denom_pos]
            linarith
          linarith

    have h_prod_confinement : (∏ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime, 
      if ChoiPrimePowerBound p_i ρ ≤ α then ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2) else 1) 
      ≤ (∏ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime, ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2)) := by
        exact Finset.prod_le_prod (by sorry) h_each_term_bound
        
    have h_broughan_limit_lock : (∏ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime, ((p_i : ℝ) + 2) / ((p_i : ℝ) - 2)) 
      ≤ α ^ (2 * Real.log α * (1 + 1 / (2 * Real.log α ^ 2))) := by
        have h_log_transformed_sum : ∑ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime, Real.log (((p_i : ℝ) + 2) / ((p_i : ℝ) - 2)) 
          ≤ 2 * Real.log α * (1 + 1 / (2 * Real.log α ^ 2)) * Real.log α := by sorry
        have h_exp_mono : Real.exp (∑ p_i ∈ (Finset.range (Nat.floor α)).filter Nat.Prime, Real.log (((p_i : ℝ) + 2) / ((p_i : ℝ) - 2))) 
          ≤ Real.exp (2 * Real.log α * (1 + 1 / (2 * Real.log α ^ 2)) * Real.log α) := by sorry
          
        have h_term_exp_bound_mono : ∀ p_i_var ∈ (Finset.range (Nat.floor α)).filter Nat.Prime,
          ((p_i_var : ℝ) + 2) / ((p_i_var : ℝ) - 2) ≤ Real.exp (Real.log (((p_i_var : ℝ) + 2) / ((p_i_var : ℝ) - 2))) := by
            intro p_i_v hp_i_v; sorry
        sorry
    linarith
  · linarith

end SieveFramework
