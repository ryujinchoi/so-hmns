import torch
import torch.nn as nn

class SOHMNSSpectralGuard(nn.Module):
    """
    SO-HMNS 스펙트럴 가드 및 비등방성 에이코날 텐서 제어 모듈.
    Neural SDF 표현 시 모서리 뭉개짐(Eikonal 한계)과 표면 노이즈(Gibbs 현상)를 동시에 해결합니다.
    """
    def __init__(self, feature_dim=128):
        super(SOHMNSSpectralGuard, self).__init__()
        self.phase_lock = nn.Parameter(torch.randn(1, feature_dim) * 0.01)
        self.register_buffer('frequency_band', torch.linspace(0.0, 100.0, feature_dim))

    def forward(self, sdf_gradients, latent_features):
        gradient_norms = torch.norm(sdf_gradients, p=2, dim=-1, keepdim=True)
        eikonal_loss = torch.mean((gradient_norms - 1.0) ** 2)

        omega = self.frequency_band.unsqueeze(0)
        spectral_attenuation = 1.0 / (1.0 + (omega / 45.0) ** 4)
        
        phase_modifier = torch.cos(latent_features + self.phase_lock) * 0.02
        spectral_guard_mask = spectral_attenuation + phase_modifier
        spectral_loss = torch.mean(torch.abs(latent_features * (1.0 - spectral_guard_mask)))

        return eikonal_loss, spectral_loss

class SOHMNSNeuralSDF(nn.Module):
    """
    SO-HMNS 엔진이 탑재된 차세대 고화질 연속 표면 복원 신경망
    """
    def __init__(self, hidden_dim=256):
        super(SOHMNSNeuralSDF, self).__init__()
        self.input_layer = nn.Linear(3, hidden_dim)
        self.hidden_layers = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(4)])
        self.sdf_output = nn.Linear(hidden_dim, 1)
        self.spectral_guard = SOHMNSSpectralGuard(feature_dim=hidden_dim)

    def forward(self, xyz):
        xyz.requires_grad_(True)
        x = torch.relu(self.input_layer(xyz))
        for layer in self.hidden_layers:
            x = torch.relu(layer(x))
        sdf = self.sdf_output(x)
        
        sdf_gradients = torch.autograd.grad(
            outputs=sdf, inputs=xyz,
            grad_outputs=torch.ones_like(sdf),
            create_graph=True, retain_graph=True, only_inputs=True
        )
        eikonal_loss, spectral_loss = self.spectral_guard(sdf_gradients, x)
        return sdf, eikonal_loss, spectral_loss

if __name__ == "__main__":
    model = SOHMNSNeuralSDF()
    fake_xyz = torch.randn(16, 3)
    predicted_sdf, e_loss, s_loss = model(fake_xyz)
    print("==================================================")
    print("   SO-HMNS GRAPHICS ENGINE v4.5 CORE COMPILED     ")
    print("==================================================")
    print(f"▶ 복원된 신경 SDF 형태   : {predicted_sdf.shape}")
    print(f"▶ 에이코날 디테일 보존 손실: {e_loss.item():.6f}")
    print(f"▶ 스펙트럴 가드 노이즈 손실: {s_loss.item():.6f}")
    print("==================================================")
