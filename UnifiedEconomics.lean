import data.rat.basic
import data.matrix.basic

constant TotalEconomicAgents : ℕ
axiom agent_dimension_lock : TotalEconomicAgents ≥ 2

def MarketLiquidityTensor := matrix (fin TotalEconomicAgents) (fin TotalEconomicAgents) ℚ

def IsInflationShielded (M : MarketLiquidityTensor) : Prop :=
  M.trace = 0 ∧ (∀ i j, M i j ∈ (set.univ : set ℚ))

axiom economy_equilibrium_closure (M : MarketLiquidityTensor) (A : MarketLiquidityTensor) :
  IsInflationShielded M → IsInflationShielded (M + A)

theorem nash_market_kernel_stability (M : MarketLiquidityTensor) (h : IsInflationShielded M) :
  ∃ (K : set (fin TotalEconomicAgents → ℚ)), ∀ (v ∈ K), M.mul_vec v = 0 :=
begin
  sorry,
end
