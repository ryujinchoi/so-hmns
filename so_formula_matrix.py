import time
import math

class SOHMNS_IdealFilter:
    @staticmethod
    def filter_seismic_signal(item):
        if "magnitude" in item:
            item["magnitude"] = round(item["magnitude"], 2)
        return item

def calculate_future_timeline(epoch_time, observed_mag, target_territory, depth_val):
    base_factor = 14.12
    depth_compensation = min(float(depth_val) / 58.5, 3.92)
    bathymetry_factor = 0.0
    t_upper = target_territory.upper()
    
    if "NEW ZEALAND" in t_upper: bathymetry_factor = 0.52
    elif "JAPAN" in t_upper: bathymetry_factor = 0.22
    elif "MEXICO" in t_upper or "PERU" in t_upper or "CHILE" in t_upper: bathymetry_factor = 0.42
    elif "ICELAND" in t_upper or "ATLANTIC" in t_upper: bathymetry_factor = 0.62
    elif "PHILIPPINES" in t_upper or "INDONESIA" in t_upper: bathymetry_factor = 0.32
    
    dynamic_tensor =  + (math.log10(1.0 + (float(observed_mag) - 3.5) * 2.2) * 1.15) + (math.sin(float(observed_mag) * 1.57) * 0.18)
    viscous_dissipation =  - (min(float(depth_val) / 24.5, 6.15) * 1.75) - 0.15
    
    dynamic_attenuation_factor = base_factor + depth_compensation + bathymetry_factor + dynamic_tensor + viscous_dissipation
    
    forecast_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_time))
    return forecast_time, dynamic_attenuation_factor
