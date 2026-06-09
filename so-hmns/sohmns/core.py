import math

class SOHMNSEngine:
    def __init__(self, M_max=1.0e30, epsilon=1.0e-15, tolerance=1.0e-7):
        self.M_max = M_max
        self.epsilon = epsilon
        self.tolerance = tolerance

    def compute_attenuation(self, dirichlet_energy):
        if dirichlet_energy < 0:
            dirichlet_energy = 0.0
        clipped_energy = min(dirichlet_energy / (1.0 + self.epsilon), 700.0)
        try:
            eta_m = self.M_max * math.exp(-clipped_energy)
        except OverflowError:
            eta_m = self.M_max
        if eta_m < self.epsilon:
            eta_m = self.epsilon
        return eta_m

    def update_gradient_balance(self, task_gradients):
        balanced_gradients = []
        for g in task_gradients:
            try:
                stable_g = max(float(g), self.tolerance)
            except (TypeError, ValueError):
                stable_g = self.tolerance
            balanced_gradients.append(stable_g)
        return balanced_gradients
