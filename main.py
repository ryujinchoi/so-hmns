import math
from datetime import datetime, timedelta

def get_real_date_string(base_date, model_t, scale_factor):
    total_days = model_t * scale_factor
    forecast_date = base_date + timedelta(days=total_days)
    return forecast_date.strftime("%Y년 %m월 %d일")

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
    base_date = datetime(2026, 7, 1) # 현재 시점 기준 날짜
    
    print("="*65)
    print(" [지역 매핑 적용] 실제 단층 데이터 기반 임계 시점 시뮬레이터 ")
    print("="*65)
    print("분석할 위험 단층대를 선택하세요:")
    print("1: 일본 난카이 해곡 (초대형 판 경계 지진 및 쓰나미 결합 시나리오)")
    print("2: 대한민국 양산 단층대 (판 내부 활성단층 내륙형 지진 시나리오)")
    
    try:
        choice = input("선택 (1 또는 2): ").strip()
    except:
        choice = "1" # Non-interactive 환경 백업
        
    if choice == "2":
        target_name = "대한민국 양산 단층대 (경주/포항 인근)"
        scale_factor = 15.0  # 응력 축적이 느리므로 1 t = 실제 시간 15일 매핑
        alpha, beta, gamma, delta, k = 0.05, 0.3, 0.02, 0.7, 0.4
        Q_in = 0.8
        h_deep = 200.0  # 동해 평균 수심 반영
        p_slope = 0.08  # 완만한 전조 급증
        tsunami_active = False # 내륙형 위주 (해일 위험 낮음)
    else:
        target_name = "일본 난카이 해곡 (Nankai Trough)"
        scale_factor = 2.5   # 단층 활동이 급격하므로 1 t = 실제 시간 2.5일 매핑
        alpha, beta, gamma, delta, k = 0.2, 0.5, 0.1, 0.4, 0.3
        Q_in = 1.0
        h_deep = 4000.0 # 심해 수심 반영
        p_slope = 0.15  # 가파른 전조 급증
        tsunami_active = True

    p, s, g = 0.5, 0.1, 0.2
    t, t_end, dt = 0.0, 40.0, 0.2
    steps = 20
    sub_dt = dt / steps
    
    t_mainshock = 20.0
    tsunami_triggered = False
    t_tsunami_start = 0.0
    tsunami_energy = 0.0
    volcano_alert = False
    c_safe, c_rupture = 0.3, 0.9
    
    print(f"\n▶ 타겟 지역 설정 완료: {target_name}")
    print(f"▶ 연산 개시일: {base_date.strftime('%Y년 %m월 %d일')}")
    print("-"*65)
    
    while t <= t_end:
        # 수심 변화 시나리오 매핑
        if tsunami_active:
            current_depth = h_deep if t < 32.0 else max(10.0, h_deep - ((h_deep - 10.0) * (t - 32.0) / 8.0))
        else:
            current_depth = h_deep
            
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock, p_slope)
        current_date_str = get_real_date_string(base_date, t, scale_factor)
        
        for _ in range(steps):
            s_combined = s + eq_rate
            dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, alpha, beta, gamma, delta, k, Q_in)
            p += dp_dt * sub_dt
            s += ds_dt * sub_dt
            g += dg_dt * sub_dt
            
        s_combined = s + eq_rate
        W = calculate_lyapunov_containment(p, s_combined, g)
        
        # 1. 주지진 임계점 판단
        if t >= t_mainshock and not tsunami_triggered:
            print(f"\n🚨 [{current_date_str} 예측] 단층 파쇄 임계 돌파! 주지진(Mainshock) 대지진 발생.")
            tsunami_triggered = True
            t_tsunami_start = t
            tsunami_energy += 2.5
            
        # 2. 화산 에너지 전조 판단
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f"🌋 [{current_date_str} 예측] 지각 격동으로 주변 화산 마그마방 포함 영역(B_crit) 진입.")
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            print(f"💥 [{current_date_str} 예측] 연쇄 반응으로 인한 화산 폭발 위험 임계점 도달!")
            tsunami_energy += 4.0
            volcano_alert = False
            
        # 3. 쓰나미 천수 효과 판단
        tsunami_height = 0.0
        if tsunami_triggered and tsunami_active:
            tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth, h_deep)
            
        if int(t * 5) % 4 == 0:
            print(f"[{current_date_str}] 지진율:{eq_rate:4.1f} | 복합에너지(W):{W:4.2f} | 🌊쓰나미파고:{tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0 and tsunami_active:
            print(f"\n🌊🌊 [{current_date_str} 최종예보] 그린의 천수 법칙에 따른 쓰나미 해안 도달 시점 확정!")
            break
            
        t += dt
    print("="*65)

if __name__ == "__main__":
    run_combined_forecast_system()
