import time
import json
import os
import urllib.request
import test_conjectures

USGS_API_URL = "https://usgs.gov"
DATA_FILE = "data.json"

def reverse_geocode_territory(lat, lon, place_raw):
    lat, lon = float(lat), float(lon)
    place_upper = place_raw.upper()
    if (-11.0 <= lat <= 6.0) and (95.0 <= lon <= 141.0): return "INDONESIA"
    if (24.0 <= lat <= 46.0) and (122.0 <= lon <= 146.0): return "JAPAN REGION"
    if (-48.0 <= lat <= -34.0) and (166.0 <= lon <= 179.0): return "NEW ZEALAND"
    if "INDONESIA" in place_upper or "SUNDA" in place_upper or "JAVA" in place_upper: return "INDONESIA"
    if "JAPAN" in place_upper or "TOKYO" in place_upper or "IZU" in place_upper: return "JAPAN REGION"
    if "NEW ZEALAND" in place_upper or "WELLINGTON" in place_upper or "KERMADEC" in place_upper: return "NEW ZEALAND"
    return "GLOBAL SEISMIC GRID"

def fetch_and_train_usgs_live():
    print(f"\n📡 [{time.strftime('%Y-%m-%d %H:%M:%S')}] SO-HMNS 실시간 역추적 및 뉴질랜드 가중치 보완 가동...")
    try:
        req = urllib.request.Request(USGS_API_URL, headers={"User-Agent": "SO-HMNS-Continuous-Bot"})
        with urllib.request.urlopen(req, timeout=15) as response:
            geojson_data = json.loads(response.read().decode("utf-8"))
        features = geojson_data.get("features", [])
        if not features: return
        
        current_data = {"forecasts": []}
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict) and "forecasts" in loaded: current_data = loaded
            except: pass

        # 효율적인 비교 검산을 위해 기존 데이터 매핑 족보 확보
        existing_forecasts = {item.get("id"): item for item in current_data.get("forecasts", []) if item.get("id")}
        updated = False
        
        for event in features:
            event_id = event.get("id")
            properties = event.get("properties", {})
            observed_mag = properties.get("mag")
            
            if observed_mag is None or observed_mag < 4.5: continue 
            
            # ⚠️ [핵심 완치 1] USGS 서버 내부의 정정 업데이트 타임스탬프 스캔 비교
            remote_updated_time = properties.get("updated", 0)
            
            # 이미 우리 파일에 있는 지진 노드인 경우, 진도 수정 사항이 없다면 건너뛰기 처리
            if event_id in existing_forecasts:
                local_item = existing_forecasts[event_id]
                # 이미 반영된 업데이트 타임스탬프이거나 진도 값이 정확히 같다면 보완 생략
                if local_item.get("remote_updated") == remote_updated_time and local_item.get("magnitude") == observed_mag:
                    continue

            epoch_time = properties.get("time", 0) / 1000.0
            geom = event.get("geometry", {})
            coords = geom.get("coordinates", [0.0, 0.0, 0.0])
            if len(coords) < 2: continue
            
            lon_val = float(coords[0])
            lat_val = float(coords[1])
            depth_val = float(coords[2]) if len(coords) > 2 else 15.0
            
            target_territory = reverse_geocode_territory(lat_val, lon_val, properties.get("place", ""))
            
            # ⚠️ [핵심 완치 2] 뉴질랜드 수직 섭입대 해역 좌표 범위 진입 시 국지적 변위 가중치 1.2배 상향 적용
            attenuation_factor = 15
            if target_territory == "NEW ZEALAND":
                attenuation_factor = 18  # 파동 가중치 및 도달 시각 매트릭스 장기 감쇄 비율 정밀화 상향
            
            future_epoch = epoch_time + (86400 * (observed_mag - 3.5) * attenuation_factor)
            forecast_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(future_epoch))
            
            mock_item = {
                "id": event_id,
                "remote_updated": remote_updated_time,
                "forecast_time": forecast_time,
                "territory": target_territory,
                "location": properties.get("place", "Active Tectonic Fault Line"),
                "latitude": lat_val,
                "longitude": lon_val,
                "seismic_energy": 10 ** (1.5 * observed_mag + 4.8),
                "focal_depth": max(depth_val, 5.0),
                "bathymetry_depth": 15.0,
                "magnitude": observed_mag,
                "max_tsunami": "0.0m",
                "risk_level": "PREDICTED RISK",
                "message": f"Long-Term Grid Attenuation Signal Synchronized. Target: {target_territory}"
            }
            
            mock_item = test_conjectures.refine_prediction_engine(mock_item)
            
            # 기존 노드가 존재했던 경우 최신 정정 데이터로 완전 오버라이트 보완 치환
            if event_id in existing_forecasts:
                # 리스트 내부 해당 항목 찾아서 교체
                for idx, old_item in enumerate(current_data["forecasts"]):
                    if old_item.get("id") == event_id:
                        current_data["forecasts"][idx] = mock_item
                        break
                print(f"✨ [진도/시간 실시간 정정 보완] {mock_item['location']} -> M {observed_mag} (시각: {forecast_time})")
            else:
                current_data["forecasts"].append(mock_item)
                print(f"✨ [장기 예측 신규 적재 완료] {mock_item['location']} -> M {observed_mag}")
                
            existing_forecasts[event_id] = mock_item
            updated = True

        if updated:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(current_data, f, ensure_ascii=False, indent=4)
            print(f"✨ [정밀화 가동 완료] 총 {len(current_data['forecasts'])}개의 뉴질랜드 가중치 보완 셋 최종 적재 마감.")
    except Exception as e:
        print(f"❌ API 미래 파이프라인 연산 오류: {e}")

if __name__ == "__main__":
    print("🤖 SO-HMNS 뉴질랜드 단층 고도화 검산 시뮬레이션 데몬 기동 완료.")
    while True:
        fetch_and_train_usgs_live()
        time.sleep(300)
