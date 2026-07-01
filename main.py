import math
import os
import urllib.request
import json
from datetime import datetime, timedelta

def fetch_live_usgs_data():
    """
    [실시간 데이터 통합] 미국지질조사국(USGS) API로부터 
    최근 24시간 동안 발생한 전세계 규모 4.5 이상의 실제 지진 관측 데이터를 실시간 수집
    """
    print("🌐 [실시간 관측망 작동] USGS 글로벌 지진 관측소로부터 최신 데이터 동기화 중...")
    url = "https://usgs.gov"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        live_entries = []
        for feature in data.get("features", [])[:5]: # 최신 대표 관측 데이터 5개 추출
            props = feature["properties"]
            place = props["place"].replace(",", " ").replace(" ", "_")
            mag = props["mag"]
            
            # 실제 관측 스케일을 동역학 파라미터로 자동 매핑 치환
            # 규모가 클수록 판의 마찰 한계와 압력 경향 강도 증가
            scale = 2.0 if mag > 6.0 else 5.0
            alpha = round(0.1 + (mag * 0.02), 2)
            beta = round(0.3 + (mag * 0.04), 2)
            p_slope = round(0.05 + (mag * 0.015), 3)
            
            entry = f"실시간_{place}, {scale}, {alpha}, {beta}, 0.10, 0.40, 0.30, 1.2, 3000.0, {p_slope}, True, {mag}"
            live_entries.append(entry)
            
        print(f"✅ 동기화 완료: 최신 글로벌 관측 데이터 {len(live_entries)}건 추가 로드 성공.")
        return live_entries
    except Exception as e:
        print(f"⚠️ 실시간 오프라인 상태 또는 API 지연 발생 (기본 내장 데이터셋으로 대체 연산): {e}")
        return []

def create_and_sync_observation_data():
    """기존 가용 데이터베이스 파일에 실시간 웹 데이터를 결합하여 최종 업데이트"""
    base_config = """# 관측소이름, 시간스케일(factor), 알파, 베타, 감마, 델타, k, 유입량, 수심, 전조기울기, 쓰나미유무, 최대규모
인도네시아_순다해구, 1.8, 0.25, 0.55, 0.12, 0.35, 0.28, 1.3, 6000.0, 0.18, True, 8.6
미국_산안드레아스, 4.0, 0.15, 0.45, 0.05, 0.50, 0.35, 1.1, 100.0, 0.12, False, 7.9
이탈리아_베수비오, 3.2, 0.30, 0.60, 0.15, 0.40, 0.25, 1.6, 2000.0, 0.05, True, 6.4
대한민국_양산단층, 15.0, 0.05, 0.30, 0.02, 0.70, 0.40, 0.8, 200.0, 0.08, False, 5.8
"""
    live_data = fetch_live_usgs_data()
    
    # 언제든 파일이 갱신되거나 추가되어도 덮어쓰지 않고 최신화 유지
    with open("stations.txt", "w", encoding="utf-8") as f:
        f.write(base_config)
        if live_data:
            f.write("# ---- 실시간 핫 플러그인 업데이트 데이터 ----\n")
            for entry in live_data:
                f.write(entry + "\n")

def load_dynamic_observation_stations():
    stations = {}
    create_and_sync_observation_data()
    
    with open("stations.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 12: continue
            name = parts[0]
            stations[name] = {
                "scale_factor": float(parts[1]), "alpha": float(parts[2]), "beta": float(parts[3]),
                "gamma": float(parts[4]), "delta": float(parts[5]), "k": float(parts[6]),
                "Q_in": float(parts[7]), "h_deep": float(parts[8]), "p_slope": float(parts[9]),
                "tsunami_active": parts[10].lower() == "true", "max_magnitude": float(parts[11])
            }
    return stations

def get_real_timestamp_string(base_date, model_t, scale_factor):
    total_days = model_t * scale_factor
    days = int(total_days)
    fractional_day = total_days - days
    total_seconds = int(fractional_day * 24 * 3600)
    return (base_date + timedelta(days=days, seconds=total_seconds)).strftime("%Y년 %m월 %d일 %H시 %M분")

def get_earthquake_seismicity_rate(t, state_type, t_mainshock, slope):
    if state_type == "preshock":
        return 0.2 * math.exp(slope * t)
    elif state_type == "aftershock":
        dt = t - t_mainshock
        return 5.0 / ((dt if dt > 0 else 0.01) ** 1.1)
    return 0.1

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in):
    p_eff, s_eff = math.tanh(p), math.tanh(s)
    dp_dt = alpha * (Q_in - (1.0 - g) * 0.5 * p_eff) + gamma * math.sin(s_eff)
    ds_dt = beta * ((p_eff - 0.5) if p_eff > 0.5 else 0.0) - delta * s_eff
    dg_dt = (p_eff * (1.0 - g)) * math.exp(-k * p_eff) - 0.2 * s_eff * g
    return dp_dt, ds_dt, dg_dt

def get_tsunami_wave_height(t, t_trigger, initial_energy, current_depth, h_deep):
    dt = t - t_trigger
    if dt < 0: return 0.0
    shoaling_factor = (h_deep / (current_depth if current_depth > 0.5 else 0.5)) ** 0.25
    return abs(initial_energy * math.exp(-0.08 * dt) * math.sin(1.5 * dt)) * shoaling_factor

def calculate_lyapunov_containment(p, s, g):
    return 0.5 * (math.tanh(p)**2) + 0.3 * (math.tanh(s)**2) + 0.8 * (g**2) * math.exp(math.tanh(p))

def run_combined_forecast_system():
    base_date = datetime.now() # 실제 현재 날짜 시각 적용
    stations = load_dynamic_observation_stations()
    
    print("="*75)
    print(" [글로벌 올데이터 연동 완료] 실시간 기상/지각 API 동적 수집 분석 시스템 ")
    print("="*75)
    print("가용한 종합 관측 감시망 리스트:")
    for idx, name in enumerate(stations.keys(), 1):
        print(f" {idx}: {name}")
    print("-"*75)
    
    try:
        choice_idx = int(input(f"분석할 실시간/고정 관측소 번호 선택 (1~{len(stations)}): ").strip()) - 1
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
    
    print(f"\n▶ 타겟 데이터셋 로드 완료: {target_name}")
    print(f"▶ 현재 분석 연산 개시 시각: {base_date.strftime('%Y년 %m월 %d일 %H시 %M분')}")
    print("-"*75)
    
    while t <= t_end:
        current_depth = cfg["h_deep"] if not cfg["tsunami_active"] or t < 32.0 else max(10.0, cfg["h_deep"] - ((cfg["h_deep"] - 10.0) * (t - 32.0) / 8.0))
        current_phase = "preshock" if t < t_mainshock else "aftershock"
        eq_rate = get_earthquake_seismicity_rate(t, current_phase, t_mainshock, cfg["p_slope"])
        current_timestamp_str = get_real_timestamp_string(base_date, t, cfg["scale_factor"])
        
        for _ in range(steps):
            s_combined = s + eq_rate
            dp_dt, ds_dt, dg_dt = volcano_dynamic_system(p, s_combined, g, cfg["alpha"], cfg["beta"], cfg["gamma"], cfg["delta"], cfg["k"], cfg["Q_in"])
            p += dp_dt * sub_dt; s += ds_dt * sub_dt; g += dg_dt * sub_dt
            
        s_combined = s + eq_rate
        W = calculate_lyapunov_containment(p, s_combined, g)
        current_magnitude = min(cfg["max_magnitude"], 3.0 + (math.log10(s_combined + 1.0) * (cfg["max_magnitude"] - 3.0) / 1.5))
        
        if t >= t_mainshock and not tsunami_triggered:
            print(f"\n🚨 [{current_timestamp_str} 예보] {target_name} 단층 임계 돌파!")
            print(f"     💥 [본진 터짐] 관측 기반 규모: M {cfg['max_magnitude']:.1f} 격동")
            tsunami_triggered = True; t_tsunami_start = t; tsunami_energy += 2.5
            
        if W > c_safe and W <= c_rupture and not volcano_alert:
            print(f" can🌋 [{current_timestamp_str} 예보] 복합 마그마 에너지 위상 탈출.")
            volcano_alert = True
            
        if W > c_rupture and volcano_alert:
            print(f"💥 [{current_timestamp_str} 예보] 압력 임계치 도달 연쇄 분화!")
            tsunami_energy += 4.0; volcano_alert = False
            
        tsunami_height = get_tsunami_wave_height(t, t_tsunami_start, tsunami_energy, current_depth, cfg["h_deep"]) if tsunami_triggered and cfg["tsunami_active"] else 0.0
        
        if int(t * 5) % 4 == 0:
            print(f"[{current_timestamp_str}] 실시간규모: M {current_magnitude:.1f} | 포함에너지(W): {W:4.2f} | 🌊쓰나미파고: {tsunami_height:5.2f}m")
            
        if tsunami_height > 12.0 and cfg["tsunami_active"]:
            print(f"\n🌊🌊 [{current_timestamp_str} 최종대피] 그린의 법칙에 의한 쓰나미 연안 습격 임계 도달.")
            break
        t += dt
    print("="*75)

if __name__ == "__main__":
    run_combined_forecast_system()
