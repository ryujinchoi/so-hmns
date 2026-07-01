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
            entry = f"실시간_{place}, {scale}, {alpha}, {beta}, 0.10, 0.40, 0.30, 1.2, 3000.0, {p_slope}, True, {mag}, 80.0, 25.0"
            live_entries.append(entry)
        return live_entries
    except:
        return []

def create_and_sync_observation_data():
    """고정 데이터셋에 폭우(Rain, mm) 및 태풍 풍속(Wind, m/s) 데이터 주입"""
    base_config = """# 관측소이름, 시간스케일, 알파, 베타, 감마, 델타, k, 유입량, 수심, 전조기울기, 쓰나미유무, 최대규모, 일일강수량(mm), 태풍풍속(m/s)
인도네시아_순다해구, 1.8, 0.25, 0.55, 0.12, 0.35, 0.28, 1.3, 6000.0, 0.18, True, 8.6, 350.0, 45.0
미국_산안드레아스, 4.0, 0.15, 0.45, 0.05, 0.50, 0.35, 1.1, 100.0, 0.12, False, 7.9, 20.0, 10.0
이탈리아_베수비오, 3.2, 0.30, 0.60, 0.15, 0.40, 0.25, 1.6, 2000.0, 0.05, True, 6.4, 180.0, 15.0
대한민국_양산단층, 15.0, 0.05, 0.30, 0.02, 0.70, 0.40, 0.8, 200.0, 0.08, False, 5.8, 250.0, 38.0
"""
    live_data = fetch_live_usgs_data()
    with open("stations.txt", "w", encoding="utf-8") as f:
        f.write(base_config)
        if live_data:
            f.write("# ---- 실시간 지진 및 기상 융합 데이터 ----\n")
            for entry in live_data:
                f.write(entry + "\n")

def load_dynamic_observation_stations():
    stations = {}
    create_and_sync_observation_data()
    with open("stations.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip(): continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 14: continue
            name = parts[0]
            # [수정 완결] 리스트에 인덱스 번호를 정확하게 매핑하여 float 변환 에러 해결
            stations[name] = {
                "scale_factor": float(parts[1]), 
                "alpha": float(parts[2]), 
                "beta": float(parts[3]),
                "gamma": float(parts[4]), 
                "delta": float(parts[5]), 
                "k": float(parts[6]),
                "Q_in": float(parts[7]), 
                "h_deep": float(parts[8]), 
                "p_slope": float(parts[9]),
                "tsunami_active": parts[10].lower() == "true", 
                "max_magnitude": float(parts[11]),
                "rain_mm": float(parts[12]), 
                "wind_ms": float(parts[13])
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
    rain_effect = 1.0 + (rain_mm / 500.0)
    p_eff, s_eff = math.tanh(p), math.tanh(s)
    dp_dt = alpha * (Q_in * rain_effect - (1.0 - g) * 0.5 * p_eff) + gamma * math.sin(s_eff)
    ds_dt = beta * ((p_eff - 0.5) if p_eff > 0.5 else 0.0) - delta * s_eff
    dg_dt = (p_eff * (1.0 - g)) * math.exp(-k * p_eff) - 0.2 * s_eff * g
    return dp_dt, ds_dt, dg_dt

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth, h_deep, wind_ms):
    dt = t - t_trigger
    if dt < 0: return 0.0
    shoaling_factor = (h_deep / (current_depth if current_depth > 0.5 else 0.5)) ** 0.25
    base_tsunami = abs(initial_energy * math.exp(-0.08 * dt) * math.sin(1.5 * dt)) * shoaling_factor
    storm_surge_effect = (wind_ms ** 2) / 400.0
    return base_tsunami + storm_surge_effect

def calculate_lyapunov_containment(p, s, g):
    return 0.5 * (math.tanh(p)**2) + 0.3 * (math.tanh(s)**2) + 0.8 * (g**2) * math.exp(math.tanh(p))

def log_to_target_file(log_text):
    with open("target_hmns.txt", "a", encoding="utf-8") as f:
        f.write(log_text + "\n")

def run_combined_forecast_system():
    base_date = datetime.now()
    stations = load_dynamic_observation_stations()
    
    print("="*75)
    print(" [지각-기상 대융합 완결] 지진·화산·쓰나미 및 태풍·폭우 연쇄 예보 플랫폼 ")
    print("="*75)
    print("종합 관측망 감시 구역 리스트:")
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
    
    start_log = f"\n=== [기상-지각 복합 연산 세션] ===\n▶ 대상 구역: {target_name}\n▶ 관측 기상: 일일 강수량 {cfg['rain_mm']}mm / 태풍 풍속 {cfg['wind_ms']}m/s"
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
            msg = f"🌋 [{current_timestamp_str} {window_str}] 폭우 지하수 유입 및 마그마 가압으로 포함 임계 영역 진입."
            print(msg); log_to_target_file(msg)
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            msg = f"💥 [{current_timestamp_str} {window_str}] 마그마방 압력 한계 초과 연쇄 분화 대폭발 발생!"
            print(msg); log_to_target_file(msg)
            tsunami_energy += 4.0; volcano_alert = False
            
        tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth, cfg["h_deep"], cfg["wind_ms"]) if tsunami_triggered and cfg["tsunami_active"] else 0.0
        
        if int(t * 5) % 4 == 0:
            print(f"[{current_timestamp_str}] 규모: M {current_magnitude:.1f} | 에너지(W): {W:4.2f} | 🌊기상복합해일파고: {tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0 and cfg["tsunami_active"]:
            msg = f"🌊🌊 [{current_timestamp_str} 대피요망] 태풍 서지 폭풍우 및 쓰나미 천수 중첩 해안 타격 시점 돌파!"
            print("\n" + msg); log_to_target_file(msg)
            break
        t += dt
    
    end_log = f"=== 연산 세션 완료 및 백업 완료 ===\n"
    log_to_target_file(end_log)
    print("="*75)
    print("💡 기상-지각 융합 결과가 'target_hmns.txt'에 성공적으로 누적 백업되었습니다.")
    print("="*75)

if __name__ == "__main__":
    run_combined_forecast_system()
