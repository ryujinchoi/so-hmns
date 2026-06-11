from so_hmns_ultimate import UltimateSpectralOperatorEngine
import sys

def run_universal_validation():
    print("[SO-HMNS Universal Core v2.1 Activated]")
    # 극소 미세 섭동 케이스 검증 (delta = 0.01) -> 동적 스케일링으로 모순 강제 포착
    engine = UltimateSpectralOperatorEngine(N_cutoff=10000, delta=0.01)
    res = engine.verify()
    print("=== UNIVERSAL SYSTEM RUN RESULT (Delta = 0.01) ===")
    for k, v in res.items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    run_universal_validation()
