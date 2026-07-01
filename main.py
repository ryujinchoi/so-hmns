import math
from datetime import datetime, timedelta

def get_real_date_string(base_date, model_t, scale_factor=2.5):
    """
    [날짜 매핑] 모델 시간 t를 실제 일수(Days)로 변환하여 구체적인 날짜 계산
    scale_factor = 2.5 (모델 시간 1단위 = 실제 시간 2.5일)
    """
    total_days = model_t * scale_factor
    forecast_date = base_date + timedelta(days=total_days)
    return forecast_date.strftime("%Y년 %m월 %d일")

def get_earthquake_seismicity_rate(t, state_type, t_mainshock=20.0):
    if state_type == "preshock":
        return 0.2 * math.exp(0.15 * t)
    elif state_type == "aftershock":
        dt = t - t_mainshock
        if dt <= 0: dt = 0.01
        return 5.0 / (dt ** 1.1)
    return 0.1

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in):
    p_effect = math.tanh(p)
    s_effect = math.tanh(s)
    
    Q_out = (1.0 - g) * 0.5 * p_effect
    dp_dt = alpha * (Q_in - Q_out) + gamma * math.sin(s_effect)
    
    p_rupture = 0.5
    forcing = (p_effect - p_rupture) if p_effect > p_rupture else 0.0
    ds_dt = beta * forcing - delta * s_effect
    
    dg_dt = (p_effect * (1.0 - g)) * math.exp(-k * p_effect) - 0.2 * s_effect * g
    return dp_dt, ds_dt, dg_dt

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth=10.0):
    dt = t - t_trigger
    if dt < 0: return 0.0
    damping = math.exp(-0.08 * dt)
    base_amplitude = initial_energy * damping * math.sin(1.5 * dt)
    
    h_deep = 4000.0
    if current_depth <= 0.5: current_depth = 0.5
    shoaling_factor = (h_deep / current_depth) ** 0.25
    return abs(base_amplitude) * shoaling_factor

def calculate_lyapunov_containment(p, s, g):
    p_safe = math.tanh(p)
    s_safe = math.tanh(s)
    return 0.5 * (p_safe**2) + 0.3 * (s_safe**2) + 0.8 * (g**2) * math.exp(p_safe)

def run_combined_forecast_system():
    # 현재 날짜 기준점 설정 (2026년 7월 1일 수요일)
    base_date = datetime(2026, 7, 1)
    scale_factor = 2.5 # 1 t = 2.5일
    
    alpha, beta, gamma, delta, k = 0.2, 0.5, 0.1, 0.4, 0.3
    Q_in = 1.0  
    p, s, g = 0.5, 0.1, 0.2
    
    t = 0.0
    t_end = 40.0
    dt = 0.2  
    steps = 20 
    sub_dt = dt / steps
    
    t_mainshock = 20.0
    tsunami_triggered = False
    t_tsunami_start = 0.0
    tsunami_energy = 0.0
    
    print("="*75)
    print(" [스케일 보완 완료] 실제 날짜 변환 및 지구물리 관측 매핑 예보 ")
    print(f" 연산 기준 날짜 (현재): {base_date.strftime('%Y년 %m월 %d일')}")
    print("="*75)
    
    c_safe, c_rupture = 0.3, 0.9
    volcano_alert = False
    
    while t <= t_end:
        current_depth = 4000.0 if t < 32.0 else max(10.0, 4000.0 - (3990.0 * (t - 32.0) / 8.0))
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock)
        
        # 실제 예측 날짜로 매핑 변환
        current_date_str = get_real_date_string(base_date, t, scale_factor)
        
        for _ in range(steps):
            s_combined = s + eq_rate
            dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, alpha, beta, gamma, delta, k, Q_in)
            p += dp_dt * sub_dt
            s += ds_dt * sub_dt
            g += dg_dt * sub_dt
            
        s_combined = s + eq_rate
        W = calculate_lyapunov_containment(p, s_combined, g)
        
        if t >= t_mainshock and not tsunami_triggered:
            print(f"\n🚨 [{current_date_str} 예보] 주지진 최종 도달! 해저 지각 붕괴로 해일 트리거.")
            tsunami_triggered = True
            t_tsunami_start = t
            tsunami_energy += 2.5
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f"🌋 [{current_date_str} 예보] 마그마 축적 에너지가 위상학적 임계 안전 구역을 탈출.")
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            print(f"💥 [{current_date_str} 예보] 화산 대폭발(분화) 최종 위험 시점 도달!")
            tsunami_energy += 4.0
            volcano_alert = False
            
        tsunami_height = 0.0
        if tsunami_triggered:
            tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth)
            
        if int(t * 5) % 2 == 0:
            print(f"[{current_date_str}] 지진율:{eq_rate:4.1f} | 에너지(W):{W:4.2f} | 🌊쓰나미파고:{tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0:
            print(f"\n🌊🌊 [{current_date_str} 최종대피] 쓰나미 대륙붕 천수 압축 완료! 해안 습격 예상일 확정.")
            break
            
        t += dt
    print("="*75)

if __name__ == "__main__":
    run_combined_forecast_system()
