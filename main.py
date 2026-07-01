import math

def get_earthquake_seismicity_rate(t, state_type, t_mainshock=20.0):
    """
    [지진 고도화] 실제 지진 데이터 법칙 주입
    - 전진(Preshock): 구텐베르크-리히터 법칙에 따라 분출 에너지가 지수적으로 증가
    - 여진(Aftershock): 오모리 법칙(Omori's Law)에 따라 1/(t-t_m)^p 비율로 감쇄
    """
    if state_type == "preshock":
        # 전진 단계: 시간이 갈수록 미소 지진 발생 빈도가 지수적으로 급증
        return 0.2 * math.exp(0.15 * t)
    elif state_type == "aftershock":
        # 여진 단계 (오모리 법칙): 주지진 발생 이후 시간 분모에 비례해 감쇄
        dt = t - t_mainshock
        if dt <= 0:
            dt = 0.01
        p_constant = 1.1 # 실제 관측치 평균 p-value
        return 5.0 / (dt ** p_constant)
    return 0.1

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in):
    """
    [화산 고도화] 가스 폐쇄 메커니즘이 주입된 동역학계
    """
    Q_out = (1.0 - g) * 0.5 * p
    dp_dt = alpha * (Q_in - Q_out) + gamma * math.sin(s)
    
    p_rupture = 2.0
    forcing = (p - p_rupture) if p > p_rupture else 0.0
    ds_dt = beta * forcing - delta * s
    
    dg_dt = (p * (1.0 - g)) * math.exp(-k * p) - 0.2 * s * g
    return dp_dt, ds_dt, dg_dt

def calculate_lyapunov_containment(p, s, g):
    return 0.5 * (p**2) + 0.3 * (s**2) + 0.8 * (g**2) * math.exp(p)

def run_combined_forecast_system():
    # 파라미터 및 초기화
    alpha, beta, gamma, delta, k = 0.6, 1.2, 0.3, 0.5, 0.4
    Q_in = 1.5  
    p, s, g = 1.0, 0.1, 0.2
    
    t = 0.0
    t_end = 40.0
    dt = 0.05
    t_mainshock = 20.0
    
    print("="*60)
    print(" [고도화 완료] 실제 데이터 법칙 통합 지진/화산 예보 시스템 ")
    print("="*60)
    
    c_safe, c_rupture = 3.5, 12.0
    volcano_alert = False
    
    while t <= t_end:
        # 1. 지진 실제 데이터 모델 상태 추적
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock)
        
        # 지진 동역학 피드백을 화산 지진동(s) 변수에 실시간 동기화하여 결합
        s_combined = s + eq_rate 
        W = calculate_lyapunov_containment(p, s_combined, g)
        
        # 실시간 모니터링 출력 (주요 전환점 스냅샷)
        if int(t * 20) % 40 == 0:
            print(f"[계측] Time {t:4.1f}s | 지진위험도(Omori): {eq_rate:5.2f} | 마그마압력: {p:4.2f} | 에너지지표(W): {W:5.2f}")
            
        if t == t_mainshock:
            print(f"\n🚨 [🚨주지진 발생] Time {t:.1f}s: 단층 파쇄 임계점 돌파! 여진 체제로 전환됩니다.\n")
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f"\n🌋 [화산 경보] Time {t:.1f}s: 지진 충격 격동으로 화산 궤적이 임계구역(B_crit)에 진입!")
            volcano_alert = True
            
        if W > c_rupture:
            print(f"💥 [화산 분화] Time {t:.1f}s: 복합 에너지 임계치 돌파! 폭발적 분화 발생.\n")
            break
            
        # 연산 업데이트
        dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, alpha, beta, gamma, delta, k, Q_in)
        p += dp_dt * dt
        s += ds_dt * dt
        g += dg_dt * dt
        t += dt
    print("="*60)

if __name__ == "__main__":
    run_combined_forecast_system()
