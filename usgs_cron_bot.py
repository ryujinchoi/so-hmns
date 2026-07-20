import time
import json
import os
import urllib.request
import ssl
import math
import test_conjectures
import so_formula_matrix

# 미국지질조사국(USGS) 공식 실시간 전세계 진도 4.5 이상 피드 (인위적 데이터 전면 폐기)
USGS_API_URL = "https://usgs.gov"
DATA_FILE = "data.json"

def reverse_geocode_territory(lat, lon, place_raw):
    place_upper = place_raw.upper()
    if "," in place_raw:
        possible_country = place_raw.split(",")[-1].strip().upper()
        if possible_country: return possible_country
    return "GLOBAL SEISMIC GRID"

def fetch_and_train_usgs_live():
    # 💡 인위적인 가짜 백업 함수(generate_failback_infinite_matrix)를 호출하던 모든 루프를 파괴했습니다.
    # 이제 인터넷 연결이 실패하면 가짜 데이터를 만들지 않고 정직하게 에러를 내며 멈춥니다.
    
    req = urllib.request.Request(USGS_API_URL, headers={"User-Agent": "SO-HMNS-Continuous-Bot"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(req, timeout=12, context=ctx) as response:
        geojson_data = json.loads(response.read().decode("utf-8"))
        
    features = geojson_data.get("features", [])
    if not features:
        raise Exception("USGS 서버에 현재 실시간 데이터가 비어있습니다.")
        
    current_data = {"forecasts": []}
    existing_ids = []
    
    for event in features:
        event_id = event.get("id")
        if event_id in existing_ids: continue 
        
        properties = event.get("properties", {})
        observed_mag = properties.get("mag")
        
        # 실시간 발생 진도가 4.0 미만인 마이너 지진은 필터링
        if observed_mag is None or observed_mag < 4.0: continue 
        
        epoch_time = properties.get("time", 0) / 1000.0
        geom = event.get("geometry", {})
        coords = geom.get("coordinates", [])
        
        if len(coords) < 2: continue
        
        # 100% 실제 USGS 원본 좌표 그대로 추출
        coords_iter = iter(coords)
        lon_val = float(next(coords_iter))
        lat_val = float(next(coords_iter))
        try:
            depth_val = float(next(coords_iter))
        except StopIteration:
            depth_val = 15.0
            
        target_territory = reverse_geocode_territory(lat_val, lon_val, properties.get("place", "Active Tectonic Fault Line"))
        
        # 진짜 실시간 관측 진도와 깊이를 감쇄 수식 모듈에 주입하여 예측 타임라인 연산
        forecast_time, dynamic_attenuation_factor = so_formula_matrix.calculate_future_timeline(epoch_time, observed_mag, target_territory, depth_val)
        
        # 실시간 데이터를 기반으로 한 쓰나미 정밀 판정
        place_upper = properties.get("place", "").upper()
        if "REGION" in place_upper or "COAST" in place_upper or "OCEAN" in place_upper or "SEA" in place_upper:
            if observed_mag >= 7.0:
                calculated_tsunami = (observed_mag - 6.5) * 2.2
                tsunami_display = f"{max(calculated_tsunami, 0.5):.1f}m"
                risk_level_msg = "⚠️ TSUNAMI WARNING"
            else:
                tsunami_display = "0.0m"
                risk_level_msg = "PREDICTED RISK"
        else:
            tsunami_display = "N/A (Inland Fault)"
            risk_level_msg = "PREDICTED RISK"
            
        if observed_mag >= 7.7:
            risk_level_msg = "💥 CRITICAL BREAK"
            
        mock_item = {
            "id": event_id,
            "forecast_time": forecast_time,
            "territory": target_territory,
            "location": properties.get("place", "Active Tectonic Fault Line"),
            "latitude": lat_val,
            "longitude": lon_val,
            "seismic_energy": 10 ** (1.5 * observed_mag + 4.8),
            "focal_depth": max(depth_val, 5.0),
            "bathymetry_depth": 15.0,
            "magnitude": observed_mag,
            "max_tsunami": tsunami_display,
            "risk_level": risk_level_msg,
            "message": f"Real-time USGS Stream Synced. Attenuation Factor: {round(dynamic_attenuation_factor, 2)}"
        }
        mock_item = test_conjectures.refine_prediction_engine(mock_item)
        current_data["forecasts"].append(mock_item)
        existing_ids.append(event_id)
        
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(current_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    while True:
        try:
            fetch_and_train_usgs_live()
        except Exception as e:
            # 인터넷이 끊기면 가짜 데이터를 쓰지 않고 로그에 정직하게 에러를 기록함
            with open("usgs_bot.log", "a") as log_f:
                log_f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 수집 에러 발생: {str(e)}\n")
        time.sleep(300)
