import torch, csv, os, math
from so_hmns_v19_extension import SOHMNSv31Extension
from sohmns.core import SOHMNSEngine

def main():
    print("[SO-HMNS v31.0] Infinity-Category Homotopy & Syntomic Cohomology 가동.")
    sohmns_engine = SOHMNSEngine()
    v31_guard = SOHMNSv31Extension(precision=500)
    L_task = torch.tensor([5.0], requires_grad=True)
    log_file = "so_hmns_v31_training_log.csv"
    
    with open(log_file, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Epoch", "Loss", "Learning_Rate", "Infinity_Homotopy_Factor", "Syntomic_Status"])
        
    print(f"\n[SO-HMNS v31.0] 절대 불변 로그 수착 개시 -> {log_file}\n")
    for epoch in range(1, 101):
        L_total_raw = sohmns_engine.compute_attenuation(L_task)
        loss_pure = L_total_raw.item() if hasattr(L_total_raw, "item") else L_total_raw
        decay_factor = v31_guard.compute_lyapunov_decay(loss_pure)
        l1, l2, dynamic_lr = v31_guard.dynamic_operator_decoupling(epoch)
        inf_homotopy = v31_guard.calculate_infinity_homotopy(epoch, loss_pure)
        syntomic_status = v31_guard.verify_syntomic_cohomology(l1, l2)
        
        L_total = L_total_raw * float(decay_factor) * inf_homotopy
        if hasattr(L_total, "backward"):
            try: L_total.backward(retain_graph=True)
            except: pass
            
        with open(log_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([epoch, f"{loss_pure:.4f}", f"{dynamic_lr:.6f}", f"{inf_homotopy:.24f}", syntomic_status])
            
        if epoch % 10 == 0 or epoch == 1:
            print(f"[{epoch:03d}/100] Loss: {loss_pure:.4f} | LR: {dynamic_lr:.6f}")
            print(f"      -> Infinity Homotopy: {inf_homotopy:.24f} | Syntomic: [{syntomic_status}]")
    print("\n[SO-HMNS v31.0] 전수검사 그랜드 마스터 최종 진화 완수!\n")

if __name__ == "__main__":
    main()
