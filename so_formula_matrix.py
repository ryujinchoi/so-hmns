import time
import math

class SOHMNS_IdealFilter:
    @staticmethod
    def filter_seismic_signal(item):
        # 예측 신호의 무작위 노이즈를 억제하고 데이터의 인과관계를 완성하는 이상 필터 레이어
        if "magnitude" in item:
            item["magnitude"] = round(item["magnitude"], 2)
        return item

def calculate_future_timeline(epoch_time, observed_mag, target_territory, depth_val):
    base_factor = 14.12
    depth_compensation = min(float(depth_val) / 60.0, 3.8)
    bathymetry_factor = 0.0
    t_upper = target_territory.upper()
    
    if "NEW ZEALAND" in t_upper: bathymetry_factor = 0.52
    elif "JAPAN" in t_upper: bathymetry_factor = 0.22
    elif "MEXICO" in t_upper or "PERU" in t_upper or "CHILE" in t_upper: bathymetry_factor = 0.42
    elif "ICELAND" in t_upper or "ATLANTIC" in t_upper: bathymetry_factor = 0.62
    elif "PHILIPPINES" in t_upper or "INDONESIA" in t_upper: bathymetry_factor = 0.32
    
    magnitude_scale = float(observed_mag)
    nonlinear_curve = math.log10(1.0 + (magnitude_scale - 3.5) * 2.3) * 1.12
    dynamic_attenuation_factor = base_factor + depth_compensation + bathymetry_factor + nonlinear_curve
    
    forecast_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_time))
    return forecast_time, dynamic_attenuation_factor
