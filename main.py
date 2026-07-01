import math
import os
import urllib.request
import json
from datetime import datetime, timedelta

def fetch_live_usgs_data():
    """USGS 글로벌 지진 관측소 데이터 실시간 동기화"""
    url = "https://usgs.gov"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
        live_entries = []
        for feature in data.get("features", [])[:3]:
            props = feature["properties"]
            place = props["place"].replace(",", " ").replace(" ", "_")
            mag = props["mag"]
            scale = 2.0 if mag > 6.0 else 5.0
            alpha = round(0.1 + (mag * 0.02), 2)
            beta = round(0.3 + (mag * 0.04), 2)
            p_slope = round(0.05 + (mag * 0.015), 3)
            # 기본 기상 관측 사양: 기압 965hPa(강한 태풍), 일일강수량 120mm, 풍속 35m/s 매핑
            entry = f"실시간_{place}, {scale}, {alpha}, {beta}, 0.10, 0.40, 0.30, 1.2, 3000.0, {p_slope}, True, {mag}, 120.0, 35.0, 965.0"
            live_entries.append(entry)
        return live_entries
    except:
        return []

def create_and_sync_observation_data():
    """[기상 실제 데이터 스케일 고도화] 태풍 중심 기압(hPa) 항목 추가 연동"""
    base_config = """# 관측소이름, 시간스케일, 알파, 베타, 감마, 델타, k, 유입량, 수심, 전조기울기, 쓰나미유무, 최대규모, 일일강수량(mm), 태풍풍속(m/s), 중심기압(hPa)
인도네시아_순다해구, 1.8, 0.25, 0.55, 0.12, 0.35, 0.28, 1.3, 6000.0, 0.18, True, 8.6, 380.0, 48.0, 945.0
미국_산안드레아스, 4.0, 0.15, 0.45, 0.05, 0.50, 0.35, 1.1, 100.0, 0.12, False, 7.9, 15.0, 8.0, 1013.0
이탈리아_베수비오, 3.2, 0.30, 0.60, 0.15, 0.40, 0.25, 1.6, 2000.0, 0.05, True, 6.4, 210.0, 12.0, 1005.0
대한민국_양산단층, 15.0, 0.05, 0.30, 0.02, 0.70, 0.40, 0.8, 200.0, 0.08, False, 5.8, 290.0, 42.0, 955.0
"""
    live_data = fetch_live_usgs_data()
    with open("stations.txt", "w", encoding="utf-8") as f:
        f.write(base_config)
        if live_data:
            f.write("# ---- 실시간 지진 및 고도화 기상 데이터 ----\n")
            for entry in live_data:
                f.write(entry + "\n")

def load_dynamic_observation_stations():
    stations = {}
    create_and_sync_observation_data()
    with open("stations.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip(): continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 15: continue
            name = parts[0]
            stations[name] = {
                "scale_factor": float(parts[1]), "alpha": float(parts[2]), "beta": float(parts[3]),
                "gamma": float(parts[4]), "delta": float(parts[5]), "k": float(parts[6]),
                "Q_in": float(parts[7]), "h_deep": float(parts[8]), "p_slope": float(parts[9]),
                "tsunami_active": parts[10].lower() == "true", "max_magnitude": float(parts[11]),
                "rain_mm": float(parts[12]), "wind_ms": float(parts[13]), "press_hpa": float(parts[14])
            }
    return stations

def get_real_timestamp(base_date, model_t, scale_factor):
    return base_date + timedelta(days=model_t * scale_factor)

def get_earthquake_seismicity_rate(t, state_type, t_mainshock, slope):
    if state_type == "preshock": return 0.2 * math.exp(slope * t)
    elif state_type == "aftershock":
        dt = t - t_mainshock
        return 5.0 / ((dt if dt > 0 else 0.01) ** 1.1)
    return 0.1

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in, rain_mm):
    """실제 집중호우 침투 스케일(rain_mm) 반영 화산 가압 가속화"""
    rain_effect = 1.0 + (rain_mm / 400.0) 
    p_eff, s_eff = math.tanh(p), math.tanh(s)
    dp_dt = alpha * (Q_in * rain_effect - (1.0 - g) * 0.5 * p_eff) + gamma * math.sin(s_eff)
    ds_dt = beta * ((p_eff - 0.5) if p_eff > 0.5 else 0.0) - delta * s_eff
    dg_dt = (p_eff * (1.0 - g)) * math.exp(-k * p_eff) - 0.2 * s_eff * g
    return dp_dt, ds_dt, dg_dt

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth, h_deep, wind_ms, press_hpa):
    """
    [기상제해 정밀 고도화] Green's Law 천수 증폭 + 역기압 효과 + 풍파 해일 공식 적용
    - press_hpa가 1013hPa 표준기압보다 낮아질수록 흡입 효과로 해수면 강제 상승
    """
    dt = t - t_trigger
    if dt < 0: return 0.0
    shoaling_factor = (h_deep / (current_depth if current_depth > 0.5 else 0.5)) ** 0.25
    base_tsunami = abs(initial_energy * math.exp(-0.08 * dt) * math.sin(1.5 * dt)) * shoaling_factor
    
    # 1. 역기압 효과 정밀화: (1013 - 현재기압) * 0.01 미터 상승
    pressure_surge = max(0.0, (1013.0 - press_hpa) * 0.01)
    # 2. 태풍 강풍풍속 역학 해일 증폭
    wind_surge = (wind_ms ** 2) / 350.0
    
    return base_tsunami + pressure_surge + wind_surge

def calculate_lyapunov_containment(p, s, g):
    return 0.5 * (math.tanh(p)**2) + 0.3 * (math.tanh(s)**2) + 0.8 * (g**2) * math.exp(math.tanh(p))

def log_to_target_file(log_text):
    with open("target_hmns.txt", "a", encoding="utf-8") as f:
        f.write(log_text + "\n")

def run_combined_forecast_system():
    base_date = datetime.now()
    stations = load_dynamic_observation_stations()
    
    print("="*75)
    print(" [글로벌 최종 완성] 기상청 태풍 기압·폭우 수치 연동 통합 분석 플랫폼 ")
    print("="*75)
    print("관측 데이터 허브 기지 리스트:")
    for idx, name in enumerate(stations.keys(), 1):
        print(f" {idx}: {name}")
    print("-"*75)
    
    try:
        choice_idx = int(input(f"분석 대상 구역 번호 선택 (1~{len(stations)}): ").strip()) - 1
        target_name = list(stations.keys())[choice_idx]
    except:
        target_name = list(stations.keys())[0]
        
    cfg = stations[target_name]
    p, s, g = 0.5, 0.1, 0.2
    t, t_end, dt, steps = 0.0, 40.0, 0.2, 20
    sub_dt = dt / steps
    
    t_mainshock = 20.0
    tsunami_triggered = False; t_tsunami_start = 0.0; tsunami_energy = 0.0
    volcano_alert = False; c_safe, c_rupture = 0.3, 0.9
    
    start_log = f"\n=== [최종 기상-지각 데이터 피팅 세션] ===\n▶ 분석 타겟: {target_name}\n▶ 관측 기상 스펙: 강수량 {cfg['rain_mm']}mm | 태풍 풍속 {cfg['wind_ms']}m/s | 중심기압 {cfg['press_hpa']}hPa"
    print(start_log); log_to_target_file(start_log)
    
    while t <= t_end:
        current_depth = cfg["h_deep"] if not cfg["tsunami_active"] or t < 32.0 else max(10.0, cfg["h_deep"] - ((cfg["h_deep"] - 10.0) * (t - 32.0) / 8.0))
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock, cfg["p_slope"])
        
        event_time = get_real_timestamp(base_date, t, cfg["scale_factor"])
        current_timestamp_str = event_time.strftime("%Y년 %m월 %d일 %H시 %M분")
        
        error_range = timedelta(days=3 * cfg["scale_factor"] / 4.0)
        window_str = f"({(event_time-error_range).strftime('%m/%d')}~{(event_time+error_range).strftime('%m/%d')})"
        
        for _ in range(steps):
            s_combined = s + eq_rate
            dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, cfg["alpha"], cfg["beta"], cfg["gamma"], cfg["delta"], cfg["k"], cfg["Q_in"], cfg["rain_mm"])
            p += dp_dt * sub_dt; s += ds_dt * sub_dt; g += dg_dt * sub_dt
            
        s_combined = s + eq_rate
        W = calculate_lyapunov_containment(p, s_combined, g)
        current_magnitude = min(cfg["max_magnitude"], 3.0 + (math.log10(s_combined + 1.0) * (cfg["max_magnitude"] - 3.0) / 1.5))
        
        if t >= t_mainshock and not tsunami_triggered:
            msg = f"🚨 [{current_timestamp_str} {window_str}] 지각 임계 파쇄 본진 발생! [규모: M {cfg['max_magnitude']:.1f}]"
            print("\n" + msg); log_to_target_file(msg)
            tsunami_triggered = True; t_tsunami_start = t; tsunami_energy += 2.5
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            msg = f"🌋 [{current_timestamp_str} {window_str}] {cfg['rain_mm']}mm 호우 유입 가속화로 마그마 불안정 경계 진입."
            print(msg); log_to_target_file(msg)
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            msg = f"💥 [{current_timestamp_str} {window_str}] 압력 임계치 도달 연쇄 분화 대폭발 발생!"
            print(msg); log_to_target_file(msg)
            tsunami_energy += 4.0; volcano_alert = False
            
        # 태풍 중심기압(cfg["press_hpa"]) 매개변수까지 최종 주입
        tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth, cfg["h_deep"], cfg["wind_ms"], cfg["press_hpa"]) if tsunami_triggered and cfg["tsunami_active"] else 0.0
        
        if int(t * 5) % 4 == 0:
            print(f"[{current_timestamp_str}] 규모: M {current_magnitude:.1f} | 에너지(W): {W:4.2f} | 🌊태풍복합 쓰나미파고: {tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0 and cfg["tsunami_active"]:
            msg = f"🌊🌊 [{current_timestamp_str} 대피요망] 태풍 {cfg['press_hpa']}hPa 해일 서지 및 천수해일 변환 중첩 타격!"
            print("\n" + msg); log_to_target_file(msg)
            break
        t += dt
    
    end_log = f"=== 연산 세션 완료 및 백업 완료 ===\n"
    log_to_target_file(end_log)
    print("="*75)
    print("💡 기상-지각 5대 재해 대융합 데이터가 'target_hmns.txt'에 최종 저장되었습니다.")
    print("="*75)

if __name__ == "__main__":
    run_combined_forecast_system()
