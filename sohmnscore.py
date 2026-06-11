from so_hmns_ultimate import UltimateSpectralOperatorEngine

def execute_core_pipeline(n_cutoff: int, delta: float) -> dict:
    engine = UltimateSpectralOperatorEngine(N_cutoff=n_cutoff, delta=delta)
    return engine.verify()
