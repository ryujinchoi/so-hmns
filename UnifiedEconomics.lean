import data.rat.basic
import data.matrix.basic
import algebra.big_operators.basic

open_locale big_operators

constant TotalEconomicAgents : ℕ
axiom agent_dimension_lock : TotalEconomicAgents ≥ 2

def MarketLiquidityTensor := matrix (fin TotalEconomicAgents) (fin TotalEconomicAgents) ℚ

def IsInflationShielded (M : MarketLiquidityTensor) : Prop :=
  M.trace = 0 ∧ (∀ i j, M i j ∈ (set.univ : set ℚ))

def IsValueConserved (M : MarketLiquidityTensor) : Prop :=
  ∀ i, ∑ j, M i j = 0

axiom economy_equilibrium_closure (M : MarketLiquidityTensor) (A : MarketLiquidityTensor) :
  IsInflationShielded M ∧ IsValueConserved M → IsInflationShielded (M + A)

theorem nash_market_kernel_stability (M : MarketLiquidityTensor) (h1 : IsInflationShielded M) (h2 : IsValueConserved M) :
  ∃ (K : set (fin TotalEconomicAgents → ℚ)), ∀ (v ∈ K), M.mul_vec v = 0 :=
begin
  sorry,
end
