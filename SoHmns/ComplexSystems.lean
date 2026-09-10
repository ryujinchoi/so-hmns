namespace SoHmns
structure SupplyChainNetwork where
  cargo_flow : ℝ → ℝ → (ℝ × ℝ)
  node_capacity : ℝ
  supply_disruption : ℝ → ℝ
  h_flow_conservation : ∀ t x, (cargo_flow t x).1 + (cargo_flow t x).2 = 0
  h_bottleneck_free : ∀ t, supply_disruption t < node_capacity
end SoHmns
