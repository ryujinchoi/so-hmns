import time
import math

def calculate_future_timeline(epoch_time, observed_mag, target_territory, depth_val):
    base_factor = 14.2
    depth_compensation = min(float(depth_val) / 55.0, 4.2)
    
    # 💡 [글ローバル 확장 장치]: 새로운 국가가 레이더망에 포획되었을 때의 지형적 감쇄 가중치 추가 설계
    bathymetry_factor = 0.0
    t_upper = target_territory.upper()
    
    if "NEW ZEALAND" in t_upper: bathymetry_factor = 0.55
    elif "JAPAN" in t_upper: bathymetry_factor = 0.25
    elif "MEXICO" in t_upper or "PERU" in t_upper or "CHILE" in t_upper: bathymetry_factor = 0.45
    elif "ICELAND" in t_upper or "ATLANTIC" in t_upper: bathymetry_factor = 0.65 # 신규 대서양권 가중치 저격
    elif "PHILIPPINES" in t_upper or "INDONESIA" in t_upper: bathymetry_factor = 0.35 # 동남아 불의 고리 가중치
    
    magnitude_scale = float(observed_mag)
    nonlinear_curve = math.log10(1.0 + (magnitude_scale - 3.5) * 2.5) * 1.15
    dynamic_attenuation_factor = base_factor + depth_compensation + bathymetry_factor + nonlinear_curve
    
    forecast_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_time))
    return forecast_time, dynamic_attenuation_factor
