import math

def get_earthquake_seismicity_rate(t, state_type, t_mainshock=20.0):
    """[지진 실제 물리 법칙] 순수 지수/역함수 모델"""
    if state_type == "preshock":
        return 0.2 * math.exp(0.15 * t)
    elif state_type == "aftershock":
        dt = t - t_mainshock
        if dt <= 0: dt = 0.01
        return 5.0 / (dt ** 1.1)
    return 0.1

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in):
    """[화산 동역학] 물리적 포화 함수(Tanh)가 전 변수에 반영된 안심 구조"""
    p_effect = math.tanh(p)
    # 지진동(s) 변수도 단층 마찰 포화 한계를 반영하도록 tanh 적용
    s_effect = math.tanh(s)
    
    Q_out = (1.0 - g) * 0.5 * p_effect
    dp_dt = alpha * (Q_in - Q_out) + gamma * math.sin(s_effect)
    
    p_rupture = 0.5
    forcing = (p_effect - p_rupture) if p_effect > p_rupture else 0.0
    ds_dt = beta * forcing - delta * s_effect
    
    dg_dt = (p_effect * (1.0 - g)) * math.exp(-k * p_effect) - 0.2 * s_effect * g
    return dp_dt, ds_dt, dg_dt

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth=10.0):
    """[쓰나미 실제 그린의 법칙] 천수 효과 증폭 연산"""
    dt = t - t_trigger
    if dt < 0: return 0.0
    
    damping = math.exp(-0.08 * dt)
    base_amplitude = initial_energy * damping * math.sin(1.5 * dt)
    
    h_deep = 4000.0
    if current_depth <= 0.5: current_depth = 0.5
    shoaling_factor = (h_deep / current_depth) ** 0.25
    
    return abs(base_amplitude) * shoaling_factor

def calculate_lyapunov_containment(p, s, g):
    """모든 물리량의 상한 포화를 적용하여 오버플로우를 원천 봉쇄한 에너지 함수 W"""
    p_safe = math.tanh(p)
    # 지진동 폭발로 인한 제곱(s**2) 오버플로우를 방지하기 위해 단층 마찰 감쇄(tanh) 적용
    s_safe = math.tanh(s)
    return 0.5 * (p_safe**2) + 0.3 * (s_safe**2) + 0.8 * (g**2) * math.exp(p_safe)

def run_combined_forecast_system():
    alpha, beta, gamma, delta, k = 0.2, 0.5, 0.1, 0.4, 0.3
    Q_in = 1.0  
    p, s, g = 0.5, 0.1, 0.2
    
    t = 0.0
    t_end = 40.0
    dt = 0.1  
    steps = 20 
    sub_dt = dt / steps
    
    t_mainshock = 20.0
    tsunami_triggered = False
    t_tsunami_start = 0.0
    tsunami_energy = 0.0
    
    print("="*65)
    print(" [완전 성공 완결판] 오버플로우 에러가 제거된 3대 자연재해 예보 ")
    print("="*65)
    
    c_safe, c_rupture = 0.3, 0.9
    volcano_alert = False
    
    while t <= t_end:
        current_depth = 4000.0 if t < 32.0 else max(10.0, 4000.0 - (3990.0 * (t - 32.0) / 8.0))
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock)
        
        # 내부 시간 분할 정밀 연산
        for _ in range(steps):
            s_combined = s + eq_rate
            dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, alpha, beta, gamma, delta, k, Q_in)
            p += dp_dt * sub_dt
            s += ds_dt * sub_dt
            g += dg_dt * sub_dt
            
        s_combined = s + eq_rate
        W = calculate_lyapunov_containment(p, s_combined, g)
        
        if t >= t_mainshock and not tsunami_triggered:
            print(f"\n🚨 [주지진 발생] Time {t:.1f}s: 해저 단층 대규모 변위! 쓰나미 에너지 충전.")
            tsunami_triggered = True
            t_tsunami_start = t
            tsunami_energy += 2.5
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f"🌋 [화산 경보] Time {t:.1f}s: 복합 마그마 에너지(W) 임계 구역 진입.")
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            print(f"💥 [화산 분화] Time {t:.1f}s: 마그마방 압력 폭발! 대분화로 추가 파동 형성.")
            tsunami_energy += 4.0
            volcano_alert = False
            
        tsunami_height = 0.0
        if tsunami_triggered:
            tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth)
            
        if int(t * 10) % 5 == 0:
            print(f"[계측] Time:{t:4.1f}s | 지진율:{eq_rate:4.1f} | 에너지(W):{W:6.2f} | 수심:{current_depth:6.1f}m | 🌊쓰나미파고:{tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0:
            print(f"\n🌊🌊 [대형 쓰나미 해안습격] Time {t:.1f}s: 최종 수심 {current_depth:.1f}m 도달!")
            print(f"     -> 그린의 천수 법칙(Green's Law)에 따라 파고가 {tsunami_height:.2f}m로 압축 증폭되었습니다.")
            break
            
        t += dt
    print("="*65)

if __name__ == "__main__":
    run_combined_forecast_system()
