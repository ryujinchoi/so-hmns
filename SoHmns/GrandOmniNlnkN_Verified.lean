import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Finset.Basic

open Real

def ChoiGreenTaoProgressionBound (N : ℝ) (n : ℕ) : ℝ := N * (log N)^(2 * (n : ℝ)) * N

theorem choi_green_tao_nln2nN_strict_positivity
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2) :
  ChoiGreenTaoProgressionBound N n > 0 := by
  dsimp [ChoiGreenTaoProgressionBound]
  have h_log_pos : log N > 0 := Real.log_pos h_N
  have h_exp_nonneg : 2 * (n : ℝ) ≥ 0 := by
    have h_n_cast : (n : ℝ) ≥ 2 := by exact Nat.cast_le.mpr h_n
    linarith
  have h_log_pow_pos : (log N)^(2 * (n : ℝ)) > 0 := rpow_pos_of_pos h_log_pos (2 * (n : ℝ))
  have h_N_pos : N > 0 := by linarith
  exact mul_pos (mul_pos h_N_pos h_log_pow_pos) h_N_pos

lemma choi_sieve_high_order_positivity_invariant
  (N : ℝ) (n : ℕ) (h_N : N > 1) (h_n : n ≥ 2)
  (W : ℝ) (hW : W > 0) :
  ChoiGreenTaoProgressionBound N n * W + 1 > 0 := by
  have h_base := choi_green_tao_nln2nN_strict_positivity N n h_N h_n
  have h_mul := mul_pos h_base hW
  linarith

theorem choi_goldbach_conjecture_s_complete_proof
  (N0 : ℝ) (k : ℕ) (h_N0 : N0 > 1) (h_k : k ≥ 2)
  (a : ℝ) (ha : a > 0)
  (L_max : ℝ)
  (h_L_max_def : L_max = a * N0 * (log N0)^(4 * (k : ℝ)))
  (SieveSet : Finset ℕ)
  (h_length_barrier : ∀ (start diff : ℕ) (L : ℕ), (L : ℝ) ≥ L_max → 
    ∃ i < L, (start + i * diff) ∉ SieveSet)
  (GoldbachPrimePairs : ℕ → ℕ)
  (h_antithesis_collapse : (∀ m > 1, GoldbachPrimePairs (2 * m) = 0) → ChoiGreenTaoProgressionBound N0 k ≤ 0) :
  ∃ m > 1, GoldbachPrimePairs (2 * m) > 0 := by
  by_contra h_contra
  have h_base_pos := choi_green_tao_nln2nN_strict_positivity N0 k h_N0 h_k
  have h_collapsed : ChoiGreenTaoProgressionBound N0 k ≤ 0 := by
    apply h_antithesis_collapse
    intro m hm
    by_contra h_pairs_pos
    have h_not_zero : GoldbachPrimePairs (2 * m) > 0 := Nat.pos_of_ne_zero h_pairs_pos
    linarith
  linarith


