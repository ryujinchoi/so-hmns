import torch

def compute_graph_laplacian(X, k_neighbors=5):
    """
    Computes the Symmetrically Normalized Graph Laplacian (L_sym) from a high-dimensional tensor X.
    This replaces the flawed 2D Gaussian/Mean curvature approach with a dimension-invariant manifold metric.
    """
    n_samples = X.size(0)
    
    # 1. Compute pairwise Euclidean distances (N x N)
    dist_matrix = torch.cdist(X, X, p=2)
    
    # 2. Construct Adjacency Matrix W using K-Nearest Neighbors (K-NN)
    topk_values, topk_indices = torch.topk(dist_matrix, k=k_neighbors + 1, largest=False)
    
    W = torch.zeros((n_samples, n_samples), device=X.device)
    for i in range(n_samples):
        # Apply Gaussian kernel with adaptive variance based on local neighborhood density
        sigma = torch.mean(topk_values[i, 1:]) + 1e-6
        idx = topk_indices[i, 1:]
        W[i, idx] = torch.exp(- (topk_values[i, 1:] ** 2) / (2 * sigma ** 2))
        
    # Enforce symmetry
    W = 0.5 * (W + W.t())
    
    # 3. Compute Degree Matrix D and its inverse square root
    d = torch.sum(W, dim=1)
    d_inv_sqrt = torch.where(d > 0, 1.0 / torch.sqrt(d), torch.zeros_like(d))
    D_inv_sqrt = torch.diag(d_inv_sqrt)
    
    # 4. Evaluate L_sym = I - D^(-1/2) * W * D^(-1/2)
    I = torch.eye(n_samples, device=X.device)
    L_sym = I - torch.mm(torch.mm(D_inv_sqrt, W), D_inv_sqrt)
    
    return L_sym

