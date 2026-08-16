import Mathlib.NumberTheory.Padics.PadicNumbers
import Mathlib.Algebra.Ring.Basic

structure SovereignLocalLattice (p : ℕ) [Fact (Nat.Prime p)] where
  local_tensor : PadicInt p
  shield_coefficient : ℚ
  invariant_closure : shield_coefficient ≠ 0 → local_tensor ≠ 0
