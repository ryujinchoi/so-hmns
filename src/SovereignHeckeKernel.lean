import Mathlib.NumberTheory.Padics.PadicNumbers
import Mathlib.Algebra.Ring.Basic

structure SovereignHeckeKernel (p : ℕ) [h : Fact (Nat.Prime p)] where
	hecke_spectrum_tensor : PadicInt p
	serre_modularity_coefficient : ℚ
	profinite_density_guard : ℚ
	zero_leakage_hecke : profinite_density_guard > 0 → serre_modularity_coefficient = 1 → hecke_spectrum_tensor ≠ 0
