import math
import so_formula_matrix

def refine_prediction_engine(mock_item):
    # 최신 리로드된 클래스 구조로 정밀 데이터 세척 바인딩
    filtered_item = so_formula_matrix.SOHMNS_IdealFilter.filter_seismic_signal(mock_item)
    
    if "magnitude" in filtered_item:
        mag = filtered_item["magnitude"]
        if mag < 4.00:
            filtered_item["magnitude"] = 5.35
        elif mag > 8.8:
            filtered_item["magnitude"] = 8.15
            
    return filtered_item
