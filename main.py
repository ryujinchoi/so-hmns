import math

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in):
    """
    scipy 없이 동작하는 3차원 비선형 화산 동역학 방정식
    """
    # 1. 압력 변화율
    Q_out = (1.0 - g) * 0.5 * p
    dp_dt = alpha * (Q_in - Q_out) + gamma * math.sin(s)
    
    # 2. 지진 발생률 변화율
    p_rupture = 2.0
    forcing = (p - p_rupture) if p > p_rupture else 0.0
    ds_dt = beta * forcing - delta * s
    
    # 3. 가스 폐쇄도 변화율
    dg_dt = (p * (1.0 - g)) * math.exp(-k * p) - 0.2 * s * g
    
    return dp_dt, ds_dt, dg_dt

def calculate_lyapunov_containment(p, s, g):
    """
    보완된 리야푸노프 포함 함수 W(y)
    """
    W = 0.5 * (p**2) + 0.3 * (s**2) + 0.8 * (g**2) * math.exp(p)
    return W

def run_forecast_simulation():
    # 모델 파라미터 
    alpha, beta, gamma, delta, k = 0.6, 1.2, 0.3, 0.5, 0.4
    Q_in = 1.5  
    
    # 초기 상태 값 [압력, 지진동, 가스폐쇄도]
    p, s, g = 1.0, 0.1, 0.2
    
    # 수치해석 타임스텝 설정 (Euler Method)
    t = 0.0
    t_end = 50.0
    dt = 0.01  # 정밀도를 높이기 위해 0.01초 단위로 분할 연산
    
    print("="*60)
    print(" [Termux 전용 화산 분화 예측 수치 해석 엔진] ")
    print("="*60)
    
    c_safe = 3.5
    c_rupture = 12.0
    eruption_triggered = False
    
    while t <= t_end:
        W = calculate_lyapunov_containment(p, s, g)
        
        # 푸앵카레 포함 영역 상태 추적 및 실시간 판정
        if W > c_safe and W <= c_rupture and not eruption_triggered:
            print(f"[경보] Time {t:.2f}: 상태 궤적이 안전 지대(B_safe)를 탈출하여 임계 분화 영역(B_crit)에 진입했습니다.")
            print(f"       -> 현재 상태 - 압력: {p:.2f}, 지진: {s:.2f}, 가스폐쇄도: {g:.2f} (W = {W:.2f})")
            eruption_triggered = True
        
        if W > c_rupture:
            print(f"[폭발] Time {t:.2f}: 에너지 한계치(c_rupture)를 돌파하여 분화 궤적 구속이 해제되었습니다!")
            print(f"       -> 최종 마그마방 압력 임계치 돌파 시점 예보 완결.")
            break
            
        # 오일러 방법을 이용한 미분 가속도 업데이트
        dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in)
        p += dp_dt * dt
        s += ds_dt * dt
        g += dg_dt * dt
        t += dt
    else:
        print("[안전] 시뮬레이션 기간 동안 상태 궤적이 임계 포함 영역 내부에서 안정적으로 구속되었습니다.")
    print("="*60)

if __name__ == "__main__":
    run_forecast_simulation()
