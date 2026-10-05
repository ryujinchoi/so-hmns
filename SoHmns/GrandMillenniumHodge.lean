import Mathlib.Algebra.Group.Basic

variable (G : Type*) [AddCommGroup G] (a b : G)

theorem choi_hodge_algebraic_cycle_commutativity :
  a + b = b + a := by
  exact add_comm a b
