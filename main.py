import math

def get_earthquake_seismicity_rate(t, state_type, t_mainshock=20.0):
    """[지진] 오모리 및 구텐베르크 법칙 (최대 포화값 제한으로 발산 방지)"""
    if state_type == "preshock":
        # 전진 단계 발산 제어
        val = 0.2 * math.exp(0.15 * t)
        return min(val, 5.0)
    elif state_type == "aftershock":
        dt = t - t_mainshock
        if dt <= 0: dt = 0.01
        val = 5.0 / (dt ** 1.1)
        return min(val, 10.0)
    return 0.1

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in):
    """[화산] 고압 환경 오버플로우 방지 장치가 추가된 동역학"""
    # 안전 장치: 압력이 너무 크면 가스 방출 통로(Q_out)가 강제로 열리거나 포화되도록 제어
    p_safe = min(p, 50.0) 
    
    Q_out = (1.0 - g) * 0.5 * p_safe
    dp_dt = alpha * (Q_in - Q_out) + gamma * math.sin(s)
    
    p_rupture = 2.0
    forcing = (p_safe - p_rupture) if p_safe > p_rupture else 0.0
    ds_dt = beta * forcing - delta * s
    
    # math.exp 내부 지수 폭발 방지 (-k * p가 너무 작아지면 0으로 수렴하게 처리)
    exp_arg = -k * p_safe
    exp_val = math.exp(exp_arg) if exp_arg > -50 else 0.0
    
    dg_dt = (p_safe * (1.0 - g)) * exp_val - 0.2 * s * g
    return dp_dt, ds_dt, dg_dt

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth=10.0):
    """[쓰나미] Green's Law 천수 효과"""
    dt = t - t_trigger
    if dt < 0: return 0.0
    
    damping = math.exp(-0.08 * dt)
    base_amplitude = initial_energy * damping * math.sin(1.5 * dt)
    
    h_deep = 4000.0
    if current_depth <= 0.5: current_depth = 0.5
    shoaling_factor = (h_deep / current_depth) ** 0.25
    
    actual_wave_height = abs(base_amplitude) * shoaling_factor
    return actual_wave_height

def calculate_lyapunov_containment(p, s, g):
    # 리야푸노프 함수 지수 폭발 방지 (math.exp(p) 포화 처리)
    p_safe = min(p, 20.0)
    return 0.5 * (p**2) + 0.3 * (s**2) + 0.8 * (g**2) * math.exp(p_safe)

def run_combined_forecast_system():
    alpha, beta, gamma, delta, k = 0.6, 1.2, 0.3, 0.5, 0.4
    Q_in = 1.5  
    p, s, g = 1.0, 0.1, 0.2
    
    t = 0.0
    t_end = 40.0
    dt = 0.05
    t_mainshock = 20.0
    
    tsunami_triggered = False
    t_tsunami_start = 0.0
    tsunami_energy = 0.0
    
    print("="*65)
    print(" [안정화 완료] 실제 데이터 법칙 통합 시스템 (지진·화산·쓰나미) ")
    print("="*65)
    
    c_safe, c_rupture = 3.5, 12.0
    volcano_alert = False
    
    while t <= t_end:
        current_depth = 4000.0 if t < 30.0 else 4000.0 - (3990.0 * (t - 30.0) / 10.0)
        
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock)
        
        s_combined = s + eq_rate 
        W = calculate_lyapunov_containment(p, s_combined, g)
        
        if t == t_mainshock:
            print(f"\n🚨 [주지진 발생] Time {t:.1f}s: 단층 파쇄! 해저 지각 변위로 쓰나미 파동 생성.")
            tsunami_triggered = True
            t_tsunami_start = t
            tsunami_energy += 1.5
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f"🌋 [화산 경보] Time {t:.1f}s: 지진 피드백으로 화산 궤적이 임계구역 진입.")
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            print(f"💥 [화산 분화] Time {t:.1f}s: 화산 대폭발 발생! 추가 쓰나미 충격파 방출.")
            tsunami_energy += 2.5
            volcano_alert = False
            
        tsunami_height = 0.0
        if tsunami_triggered:
            tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth)
            
        if int(t * 20) % 40 == 0:
            print(f"[계측] Time:{t:4.1f}s | 지진율:{eq_rate:4.1f} | 에너지(W):{W:5.1f} | 수심:{current_depth:6.1f}m | 🌊쓰나미파고:{tsunami_height:5.2f}m")
            
        if tsunami_height > 10.0:
            print(f"\n🌊🌊 [대형 쓰나미 해안습격] Time {t:.1f}s: 천수 효과로 인해 파고가 {tsunami_height:.2f}m를 돌파했습니다! 즉시 대피하십시오.")
            print(f"     -> 수심이 {current_depth:.1f}m로 얕아지며 그린의 법칙(Green's Law)에 의한 파고 압축 완료.\n")
            break
            
        dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, alpha, beta, gamma, delta, k, Q_in)
        p += dp_dt * dt
        s += ds_dt * dt
        g += dg_dt * dt
        t += dt
    print("="*65)

if __name__ == "__main__":
    run_combined_forecast_system()
