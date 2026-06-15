import torch, csv, os, math
from so_hmns_v19_extension import SOHMNSv77ToposExtension

def main():
    print("[SO-HMNS v77.0] Grand Unified Topological Topos Invariance System 가동.")
    v77_guard = SOHMNSv77ToposExtension(precision=500)
    log_file = "so_hmns_v77_topos_log.csv"
    
    with open(log_file, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Epoch", "Loss", "Learning_Rate", "Topos_Factor", "Zp_Action_Status"])
        
    print(f"\\n[SO-HMNS v77.0] 순수 위상 토포스 멸균 로그 수착 -> {log_file}\\n")
    L_task = torch.tensor([5.0], requires_grad=True)
    
    for epoch in range(1, 101):
        loss_pure = L_task.detach().item()
        l1_raw, l2_raw, dynamic_lr = v77_guard.dynamic_operator_decoupling(epoch)
        loss_closed = v77_guard.compute_absolute_closure(epoch, loss_pure)
        
        topos_factor = v77_guard.calculate_topos_localization(epoch, loss_closed)
        zp_status = v77_guard.verify_zp_action_collapse(l1_raw, l2_raw)
        
        L_total = torch.tensor([loss_closed * topos_factor], requires_grad=True)
        if hasattr(L_total, "backward"):
            try: L_total.backward(retain_graph=True)
            except: pass
            
        with open(log_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([epoch, f"{loss_closed:.4f}", f"{dynamic_lr:.6f}", f"{topos_factor:.24f}", zp_status])
            
        if epoch % 10 == 0 or epoch == 1:
            print(f"[{epoch:03d}/100] Loss: {loss_closed:.4f} | LR: {dynamic_lr:.6f}")
            print(f"      -> Topos Localization: {topos_factor:.24f} | Zp Status: [{zp_status}]")
            
    print("\\n[SO-HMNS v77.0] 토포스 호모토피 대수 레벨 원천 비약 수정 및 종결 완수!\\n")

if __name__ == __main__:
    main()
