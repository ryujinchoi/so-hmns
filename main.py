import math
from datetime import datetime, timedelta

def get_real_timestamp_string(base_date, model_t, scale_factor):
    """모델 시간 t를 실제 날짜, 시, 분으로 정밀 변환"""
    total_days = model_t * scale_factor
    days = int(total_days)
    fractional_day = total_days - days
    total_seconds = int(fractional_day * 24 * 3600)
    
    forecast_time = base_date + timedelta(days=days, seconds=total_seconds)
    return forecast_time.strftime("%Y년 %m월 %d일 %H시 %M분")

def get_earthquake_seismicity_rate(t, state_type, t_mainshock, slope):
    if state_type == "preshock":
        return 0.2 * math.exp(slope * t)
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

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth, h_deep):
    dt = t - t_trigger
    if dt < 0: return 0.0
    damping = math.exp(-0.08 * dt)
    base_amplitude = initial_energy * damping * math.sin(1.5 * dt)
    
    if current_depth <= 0.5: current_depth = 0.5
    shoaling_factor = (h_deep / current_depth) ** 0.25
    return abs(base_amplitude) * shoaling_factor

def calculate_lyapunov_containment(p, s, g):
    p_safe = math.tanh(p)
    s_safe = math.tanh(s)
    return 0.5 * (p_safe**2) + 0.3 * (s_safe**2) + 0.8 * (g**2) * math.exp(p_safe)

def run_combined_forecast_system():
    base_date = datetime(2026, 7, 1, 0, 0) # 연산 기준 시점
    
    print("="*75)
    print(" [최종 고도화] 전 세계 위험 지역별 정밀 시각 및 발생 규모(M) 예보 엔진 ")
    print("="*75)
    print("분석할 글로벌 위험 영역을 선택하세요:")
    print("1: 인도네시아 순다 해구 (Sunda Trench)")
    print("2: 미국 산안드레아스 단층대 (San Andreas Fault)")
    print("3: 이탈리아 베수비오 화산대 (Mount Vesuvius)")
    print("4: 대한민국 양산 단층대 (Yangsan Fault)")
    
    try:
        choice = input("글로벌 타겟 선택 (1~4): ").strip()
    except:
        choice = "1"
        
    if choice == "1":
        target_name = "인도네시아 순다 해구"
        scale_factor = 1.8   
        alpha, beta, gamma, delta, k = 0.25, 0.55, 0.12, 0.35, 0.28
        Q_in = 1.3; h_deep = 6000.0; p_slope = 0.18; tsunami_active = True
        max_magnitude = 8.6 # 초강진 스케일 반영
    elif choice == "2":
        target_name = "미국 산안드레아스 단층대"
        scale_factor = 4.0   
        alpha, beta, gamma, delta, k = 0.15, 0.45, 0.05, 0.5, 0.35
        Q_in = 1.1; h_deep = 100.0; p_slope = 0.12; tsunami_active = False
        max_magnitude = 7.9 # 대형 직하형 지진
    elif choice == "3":
        target_name = "이탈리아 베수비오 화산대"
        scale_factor = 3.2   
        alpha, beta, gamma, delta, k = 0.3, 0.6, 0.15, 0.4, 0.25
        Q_in = 1.6; h_deep = 2000.0; p_slope = 0.05; tsunami_active = True
        max_magnitude = 6.4 # 화산성 지진 규모
    else:
        target_name = "대한민국 양산 단층대"
        scale_factor = 15.0  
        alpha, beta, gamma, delta, k = 0.05, 0.3, 0.02, 0.7, 0.4
        Q_in = 0.8; h_deep = 200.0; p_slope = 0.08; tsunami_active = False
        max_magnitude = 5.8 # 한반도 단층 파쇄 한계 규모

    p, s, g = 0.5, 0.1, 0.2
    t, t_end, dt = 0.0, 40.0, 0.2
    steps = 20; sub_dt = dt / steps
    
    t_mainshock = 20.0
    tsunami_triggered = False; t_tsunami_start = 0.0; tsunami_energy = 0.0
    volcano_alert = False; c_safe, c_rupture = 0.3, 0.9
    
    print(f"\n▶ 글로벌 타겟 매핑 완료: {target_name}")
    print(f"▶ 예측 연산 기준일: {base_date.strftime('%Y년 %m월 %d일 %H시 %M분')}")
    print("-"*75)
    
    while t <= t_end:
        if tsunami_active:
            current_depth = h_deep if t < 32.0 else max(10.0, h_deep - ((h_deep - 10.0) * (t - 32.0) / 8.0))
        else:
            current_depth = h_deep
            
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock, p_slope)
        current_timestamp_str = get_real_timestamp_string(base_date, t, scale_factor)
        
        for _ in range(steps):
            s_combined = s + eq_rate
            dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, alpha, beta, gamma, delta, k, Q_in)
            p += dp_dt * sub_dt
            s += ds_dt * sub_dt
            g += dg_dt * sub_dt
            
        s_combined = s + eq_rate
        W = calculate_lyapunov_containment(p, s_combined, g)
        
        # 실시간 규모(M) 연산: 지진동 지표에 비례하여 규모 스케일링 추정
        current_magnitude = min(max_magnitude, 3.0 + (math.log10(s_combined + 1.0) * (max_magnitude - 3.0) / 1.5))
        
        if t >= t_mainshock and not tsunami_triggered:
            print(f"\n🚨 [{current_timestamp_str} 예보] {target_name} 단층 최종 파쇄 돌파!")
            print(f"     💥 [본진 발생] 규모: M {max_magnitude:.1f} 대지진 격동 개시")
            tsunami_triggered = True
            t_tsunami_start = t; tsunami_energy += 2.5
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f" can🌋 [{current_timestamp_str} 예보] 지각 내부 에너지(W) 임계 탈출 시작.")
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            print(f"💥 [{current_timestamp_str} 예보] 마그마방 압력 포화 붕괴로 인한 연쇄 폭발 화산 분화 발생!")
            tsunami_energy += 4.0; volcano_alert = False
            
        tsunami_height = 0.0
        if tsunami_triggered and tsunami_active:
            tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth, h_deep)
            
        if int(t * 5) % 4 == 0:
            print(f"[{current_timestamp_str}] 추정규모: M {current_magnitude:.1f} | 포함에너지(W): {W:4.2f} | 🌊쓰나미파고: {tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0 and tsunami_active:
            print(f"\n🌊🌊 [{current_timestamp_str} 최종대피] 쓰나미 해안 타격 시점 도달!")
            print(f"     -> 그린의 법칙 압축 파고: {tsunami_height:.2f}m 도달 완결.")
            break
            
        t += dt
    print("="*75)

if __name__ == "__main__":
    run_combined_forecast_system()
