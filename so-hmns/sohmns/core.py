import torch
import torch.nn as nn
import torch.nn.functional as F
from .utils import compute_graph_laplacian

class SOHMNSOptimizer(nn.Module):
    def __init__(self, alpha_grad=0.1, tau=1.0, kappa=1.0, eta_0=0.01):
        super(SOHMNSOptimizer, self).__init__()
        self.alpha_grad = alpha_grad
        self.tau = tau
        self.kappa = kappa
        self.eta_0 = eta_0
        
        # 1. We hold internal values as native Python floats to avoid PyTorch autograd tracking conflict
        self.l1_val = 1.0
        self.l2_val = 1.0

    def compute_free_energy_lr(self, loss_val):
        return self.eta_0 * torch.exp(-loss_val / self.kappa)

    def compute_manifold_loss(self, Z, L_sym):
        dirichlet_energy = torch.trace(torch.mm(torch.mm(Z.t(), L_sym), Z))
        r_shape = torch.exp(-self.tau * dirichlet_energy)
        return 1.0 - r_shape

    def compute_topology_kld(self, X, Z):
        n = X.size(0)
        dist_X = torch.cdist(X, X, p=2)
        P = F.softmax(-dist_X ** 2, dim=1) + 1e-8
        
        dist_Z = torch.cdist(Z, Z, p=2)
        Q_unnorm = 1.0 / (1.0 + dist_Z ** 2)
        Q = Q_unnorm / (torch.sum(Q_unnorm, dim=1, keepdim=True) + 1e-8) + 1e-8
        
        kld = torch.sum(P * torch.log(P / Q)) / n
        return kld

    def forward(self, L_task, X, Z, shared_weights):
        L_manifold = self.compute_manifold_loss(Z, compute_graph_laplacian(X))
        L_entropy = self.compute_topology_kld(X, Z)
        
        # 2. Combine objectives using static snapshots of the balancing scales
        L_total = L_task + self.l1_val * L_manifold + self.l2_val * L_entropy
        
        # 3. Calculate gradients (returned as tuples)
        grad_task_tuple = torch.autograd.grad(L_task, shared_weights, retain_graph=True, allow_unused=True)
        grad_manifold_tuple = torch.autograd.grad(L_manifold, shared_weights, retain_graph=True, allow_unused=True)
        grad_entropy_tuple = torch.autograd.grad(L_entropy, shared_weights, retain_graph=True, allow_unused=True)
        
        # 4. Extract the gradient tensors and compute the norms safely
        if grad_task_tuple is not None and grad_manifold_tuple is not None and grad_entropy_tuple is not None:
            G_task = torch.norm(grad_task_tuple[0], p=2)
            G_manifold = torch.norm(self.l1_val * grad_manifold_tuple[0], p=2)
            G_entropy = torch.norm(self.l2_val * grad_entropy_tuple[0], p=2)
            G_mean = (G_task + G_manifold + G_entropy) / 3.0
            
            # 5. Perform the GradNorm balancing update strictly outside the PyTorch graph
            with torch.no_grad():
                new_l1 = self.l1_val + self.alpha_grad * ((G_manifold / (G_mean + 1e-6)) - 1.0)
                new_l2 = self.l2_val + self.alpha_grad * ((G_entropy / (G_mean + 1e-6)) - 1.0)
                self.l1_val = float(max(1e-3, new_l1.item()))
                self.l2_val = float(max(1e-3, new_l2.item()))
                
        return L_total, self.compute_free_energy_lr(L_total.detach())
