import torch
import torch.nn as nn
import torch.optim as optim
from sohmns.core import SOHMNSOptimizer

class DummyModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, latent_dim):
        super(DummyModel, self).__init__()
        # Shared Weights layer used for tracking gradient norms
        self.shared_layer = nn.Linear(input_dim, hidden_dim)
        self.task_head = nn.Linear(hidden_dim, input_dim)
        self.manifold_head = nn.Linear(hidden_dim, latent_dim)
        
    def forward(self, x):
        h = torch.relu(self.shared_layer(x))
        x_recon = self.task_head(h)
        z = self.manifold_head(h)
        return x_recon, z, self.shared_layer.weight

if __name__ == "__main__":
    # Generate high-dimensional dummy vectors (Batch=32, Dim=128)
    X_batch = torch.randn(32, 128)
    
    # Initialize Architecture & SO-HMNS Engine
    model = DummyModel(input_dim=128, hidden_dim=64, latent_dim=10)
    sohmns_engine = SOHMNSOptimizer(alpha_grad=0.1, tau=0.5, kappa=2.0, eta_0=0.01)
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Execute a Single Step Training Optimization Loop
    model.train()
    optimizer.zero_grad()
    
    X_recon, Z_manifold, shared_w = model(X_batch)
    
    # Base Objective Loss (Mean Squared Error)
    L_task = nn.MSELoss()(X_recon, X_batch)
    
    # Fuse Multi-Objectives via SOHMNS and acquire bounded dynamic learning rate
    L_total, dynamic_lr = sohmns_engine(L_task, X_batch, Z_manifold, shared_w)
    
    L_total.backward()
    optimizer.step()
    
    print("=== SO-HMNS Engine Integrity Check ===")
    print(f"1. Fused Comprehensive Loss (L_total): {L_total.item():.4f}")
    print(f"2. Thermodynamic Bounded Learning Rate (eta_m): {dynamic_lr.item():.6f}")
    # 엮여있던 변수 구조를 새 양방향 변수(l1_val, l2_val) 출력 구조로 깔끔하게 매칭 완료
    print(f"3. Dynamic Manifold Balance Scale (lambdas): [{sohmns_engine.l1_val:.4f}, {sohmns_engine.l2_val:.4f}]")
