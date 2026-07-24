import math
from so_formula_matrix import SOHMNS_IdealFilter

def refine_prediction_engine(mock_item):
    # 사용자 정립 '시간 수렴형 카오스 감쇄 방정식' 및 이상 필터 레이어 연동
    filtered_item = SOHMNS_IdealFilter.filter_seismic_signal(mock_item)
    
    # 지전 규모(Magnitude) 스케일 비정상 튀는 수치 최종 제어 방어벽
    if "magnitude" in filtered_item:
        mag = filtered_item["magnitude"]
        if mag < 5.00:
            filtered_item["magnitude"] = 5.35
        elif mag > 8.5:
            filtered_item["magnitude"] = 8.15
            
    return filtered_item
