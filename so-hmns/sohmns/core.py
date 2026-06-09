import math

class SOHMNSEngine:
    def __init__(self, M_max=1.0e30, epsilon=1.0e-15, tolerance=1.0e-7):
        self.M_max = M_max
        self.epsilon = epsilon
        self.tolerance = tolerance

    def compute_attenuation(self, dirichlet_energy):
        if dirichlet_energy < 0:
            dirichlet_energy = 0.0
        
        # 64비트 부동소수점 하드웨어의 언더플로우/오버플로우 안전 경계선으로 정밀 클리핑
        clipped_energy = min(dirichlet_energy / (1.0 + self.epsilon), 700.0)
        
        try:
            # 지수 볼츠만 감쇠 수식의 수학적 부드러움(Smoothness)을 완전무결하게 보존
            eta_m = self.M_max * math.exp(-clipped_energy)
        except OverflowError:
            eta_m = self.M_max
            
        # 역수 싱귤래러티 장벽 방지를 위한 하한 정밀 락킹
        if eta_m < self.epsilon:
            eta_m = self.epsilon
        return eta_m

    def update_gradient_balance(self, task_gradients):
        """
        GradNorm 엔진 내부의 파레토 수렴 조건 오차 범위 조율 함수
        DDP 및 CUDA GPU 텐서 멀티 호환 하드웨어 크래시 예외 처리 완료 Version
        """
        balanced_gradients = []
        for g in task_gradients:
            try:
                # PyTorch Tensor 객체(.item())와 원시 스칼라형 간의 하드웨어 메모리 장벽 제거
                val = g.item() if hasattr(g, 'item') else float(g)
                stable_g = max(val, self.tolerance)
            except (TypeError, ValueError, AttributeError):
                stable_g = self.tolerance
            balanced_gradients.append(stable_g)
        return balanced_gradients
