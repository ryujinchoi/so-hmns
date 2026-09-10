import Mathlib.Data.Nat.Prime
namespace SoHmns
structure NavierStokes3D where
  u : ℝ → ℝ → ℝ → (ℝ × ℝ × ℝ)
  p : ℝ → ℝ → ℝ → ℝ
  ν : ℝ
  h_ν_pos : ν > 0
  h_incompressible : ∀ t x y z, (u t x y z).1 + (u t x y z).2 + (u t x y z).3 = 0
def navier_stokes_trivial_model : NavierStokes3D where
  u t x y z := (0, 0, 0)
  p t x y z := 0
  ν := 1
  h_ν_pos := by linarith
  h_incompressible t x y z := by rfl
end SoHmns
