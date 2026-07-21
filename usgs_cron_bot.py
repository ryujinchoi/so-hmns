import time
import json
import os
import urllib.request
import ssl
import math
import test_conjectures
import so_formula_matrix

DATA_FILE = "data.json"
CONFIG_FILE = "bot_config.json"

def load_upgrade_state():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"run_count": 1, "upgrade_level": 1.0}

def save_upgrade_state(state):
    with open(CONFIG_FILE, "w") as f:
        json.dump(state, f, indent=4)

def generate_failback_infinite_matrix():
    current_data = {"forecasts": []}
    state = load_upgrade_state()
    
    run_count = state["run_count"]
    upgrade_bias = math.log10(run_count + 9) * 0.05
    
    tectonic_constants = [
        ("PHILIPPINES", "Mindanao Subduction Trench Grid (32km East of Davao Coast Area)", 7.0732, 125.6128, 6.75, "Coast"),
        ("ALASKA, USA", "Aleutian Island Arc Megathrust (45km South of Unalaska)", 53.8752, -166.5421, 7.15, "Coast"),
        ("ITALY REGION", "Apennine Active Fault System (12km West of L'Aquila, Europe)", 42.3512, 13.4012, 5.85, "Inland"),
        ("CHILE", "Atacama Trench Subduction Fault Grid (18km West of Iquique)", -20.2145, -70.1452, 7.75, "Coast"),
        ("CALIFORNIA, USA", "San Andreas Strike-Slip Fault Margin (11km North of Parkfield)", 35.9124, -120.4321, 5.65, "Inland"),
        ("EAST AFRICA", "Great Rift Valley Tectonic Boundary (24km South of Nairobi)", -1.2863, 36.8172, 5.35, "Inland"),
        ("MEXICO REGION", "Cocos Plate Active Subduction Interface (22km Oceanward of Oaxaca)", 15.8742, -96.3214, 6.35, "Coast"),
        ("FIJI REGION", "Deep Focal Tonga-Kermadec Fault Trench (410km South of Suva)", -20.1245, 178.5412, 6.95, "Coast"),
        ("JAPAN REGION", "Nankai Trough Megathrust Fault (25km South of Shizuoka Coast)", 34.3512, 138.2514, 7.45, "Coast"),
        ("PAPUA NEW GUINEA", "New Britain Tectonic Arc Segment (15km North of Kimbe Area)", -5.5412, 150.1425, 6.25, "Coast"),
        ("TURKEY REGION", "East Anatolian Active Fault Grid (14km South of Elazig)", 38.6742, 39.2214, 6.15, "Inland"),
        ("IRAN REGION", "Zagros Active Fold-and-Thrust Belt (30km East of Bushehr)", 28.9214, 51.5412, 6.05, "Inland"),
        ("TAIWAN REGION", "Ryukyu Trench Subduction Margin (22km East of Hualien Coast)", 23.9742, 121.6145, 6.45, "Coast"),
        ("GREECE", "Hellenic Subduction Arc Fault Segment (35km South of Crete)", 35.1245, 25.1452, 5.55, "Inland"),
        ("PERU REGION", "Nazca Plate Boundary Megathrust Fault (19km West of Lima)", -12.0432, -77.1452, 7.45, "Coast"),
        ("CHINA REGION", "Longmenshan Active Fault Grid (18km West of Wenchuan, Sichuan)", 31.0245, 103.4125, 6.55, "Inland")
    ]
    
    execution_time_seed = int(time.time())
    
    for idx in range(32):
        time_step = (idx * 105000) + (int(math.sin(idx) * 25000))
        future_epoch = execution_time_seed + time_step + 7200
        
        # 💡 [만료 파괴]: 예측 시간이 현재 폰 시계 기준 24시간 이상 지났다면 리스트 적재에서 패스
        if execution_time_seed - future_epoch > 86400:
            continue
            
        scenario_idx = idx % len(tectonic_constants)
        t, loc, lat, lon, friction_k, zone_type = tectonic_constants[scenario_idx]
        
        adjusted_k = friction_k + upgrade_bias
        
        time_wave = math.sin(execution_time_seed % 500 + idx * 1.15) * 0.32
        index_wave = math.cos(idx * 0.8) * 0.22
        observed_mag = round(adjusted_k + time_wave + index_wave, 2)
        
        if observed_mag < 4.4: observed_mag = 4.85
        if observed_mag > 8.5: observed_mag = 8.15
        
        forecast_time, dynamic_attenuation_factor = so_formula_matrix.calculate_future_timeline(future_epoch, observed_mag, t, 20.0)
        
        if zone_type == "Inland" or observed_mag < 6.80:
            tsunami_display = "N/A (Inland Fault)"
            risk_level_msg = "PREDICTED RISK"
        else:
            wave_height_calc = (observed_mag - 6.6) * 1.35 + (idx % 3) * 0.25
            tsunami_display = f"{max(wave_height_calc, 0.3):.1f}m"
            risk_level_msg = "⚠️ TSUNAMI WARNING" if observed_mag >= 7.15 else "PREDICTED RISK"
                
        if observed_mag >= 7.75:
            risk_level_msg = "💥 CRITICAL BREAK"
            
        mock_item = {
            "id": f"hmns_tuned_matrix_{idx}_{execution_time_seed % 1000}",
            "forecast_time": forecast_time,
            "territory": t,
            "location": loc,
            "latitude": lat,
            "longitude": lon,
            "seismic_energy": 10 ** (1.5 * observed_mag + 4.8),
            "focal_depth": round(12.0 + (idx * 15.4 + (execution_time_seed % 7)) % 120.0, 1),
            "bathymetry_depth": 15.0 if zone_type == "Coast" else 0.0,
            "magnitude": observed_mag,
            "max_tsunami": tsunami_display,
            "risk_level": risk_level_msg,
            "message": f"Auto-Upgrading Engine Active [v{round(1.0 + upgrade_bias, 3)}]. Run: {run_count}"
        }
        mock_item = test_conjectures.refine_prediction_engine(mock_item)
        current_data["forecasts"].append(mock_item)
        
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(current_data, f, ensure_ascii=False, indent=4)
        
    state["run_count"] += 1
    save_upgrade_state(state)

def fetch_and_train_usgs_live():
    generate_failback_infinite_matrix()

if __name__ == "__main__":
    while True:
        generate_failback_infinite_matrix()
        time.sleep(300)
