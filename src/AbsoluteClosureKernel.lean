import Mathlib.NumberTheory.Padics.PadicNumbers
import Mathlib.Algebra.Ring.Basic

structure AbsoluteSovereignKernel (p : ℕ) [Fact (Nat.Prime p)] where
	hermitian_tensor : PadicInt p
	hodge_cycle_coefficient : ℚ
	idelic_haar_normalization : ℚ
	zero_leakage_final : idelic_haar_normalization = 1 → hermitian_tensor.valuation = 0
