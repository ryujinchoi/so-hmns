import time
import math

def calculate_future_timeline(epoch_time, observed_mag, target_territory, depth_val):
    base_factor = 14.2
    depth_compensation = min(float(depth_val) / 55.0, 4.2)
    bathymetry_factor = 0.0
    if target_territory == "NEW ZEALAND": bathymetry_factor = 0.55
    elif target_territory == "JAPAN REGION": bathymetry_factor = 0.25
    elif target_territory in ["MEXICO REGION", "PERU REGION"]: bathymetry_factor = 0.45
    magnitude_scale = float(observed_mag)
    nonlinear_curve = math.log10(1.0 + (magnitude_scale - 3.5) * 2.5) * 1.15
    dynamic_attenuation_factor = base_factor + depth_compensation + bathymetry_factor + nonlinear_curve
    
    # 💡 [🔥 시간 증폭 버그 완전 파쇄] 내부에서 날짜를 임의로 늘리지 않고 넘겨받은 에포크 타임을 그대로 유지하도록 교정
    forecast_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_time))
    return forecast_time, dynamic_attenuation_factor
