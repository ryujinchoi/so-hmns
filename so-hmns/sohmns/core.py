import math

class SOHMNSEngine:
    def __init__(self, M_max=1.0e30, epsilon=1.0e-15, tolerance=1.0e-7):
        """
        SO-HMNS 고성능 수치 안정화 코어 엔진 파라미터
        
        M_max: 부동소수점 오버플로우 방지를 위해 안전 마진을 둔 연산 절대 상한 (1e308 방지)
        epsilon: 64비트 Double Precision의 머신 엡실론(1e-16)을 고려하여 분모 0을 완벽 차단하는 정밀 상수
        tolerance: GradNorm 엔진의 파레토 수렴 판단 오차 허용 한계선
        """
        self.M_max = M_max
        self.epsilon = epsilon
        self.tolerance = tolerance

    def compute_attenuation(self, dirichlet_energy):
        """
        지수 볼츠만 감쇠 모델의 언더플로우 방지 및 수치 연산 안정화 함수
        """
        # 수치적 오버플로우 및 NaN 발생을 방지하기 위한 정밀 경계 클리핑 (Clipping)
        if dirichlet_energy < 0:
            dirichlet_energy = 0.0
            
        # 64비트 부동소수점 기준 math.exp(700) 이상은 오버플로우가 발생하므로 경계 제한
        clipped_energy = min(dirichlet_energy / (1.0 + self.epsilon), 700.0)
        
        # 지수 볼츠만 감쇠 수식 연산 안정화 (Exponential Boltzmann Attenuation Factor)
        try:
            eta_m = self.M_max * math.exp(-clipped_energy)
        except OverflowError:
            eta_m = self.M_max

        # 역수(1 / eta_m) 연산 시 0 분모 싱귤래러티가 터지는 것을 막기 위해 하한 경계 잠금
        if eta_m < self.epsilon:
            eta_m = self.epsilon
            
        return eta_m

    def update_gradient_balance(self, task_gradients):
        """
        GradNorm 엔진 내부의 파레토 수렴 조건 오차 범위 조율 함수
        """
        balanced_gradients = []
        for g in task_gradients:
            # 그래디언트 노름이 오차 허용 한계(tolerance)보다 작으면 언더플로우 방지를 위해 하한 고정
            stable_g = g if g > self.tolerance else self.tolerance
            balanced_gradients.append(stable_g)
            
        return balanced_gradients
