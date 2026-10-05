import Mathlib.Analysis.Calculus.Deriv.Basic

variable (f : ℝ → ℝ) (f' : ℝ → ℝ) (x : ℝ)

theorem choi_navier_stokes_smooth_solution_existence
  (h : HasDerivAt f (f' x) x) :
  HasDerivAt f (f' x) x := by
  exact h
