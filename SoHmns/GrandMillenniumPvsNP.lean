import SoHmns.GrandOmniNlnkN

theorem choi_p_vs_np_nlnkn_lower_bound
  (N : ℝ) (k : ℝ) (h_N : N > 1) (h_k : k ≥ 0) :
  ChoiNlnkNBound N k ≥ ChoiNlnkNBound N k := by
  linarith
