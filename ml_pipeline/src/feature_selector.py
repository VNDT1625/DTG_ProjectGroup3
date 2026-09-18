"""
Trích chọn Đặc trưng Tối ưu (Feature Selection Module).
Phụ trách: Trần Thị Thu Hiền
"""
from sklearn.feature_selection import SelectKBest, mutual_info_classif

def build_feature_selector(k: int = 20):
    """Lựa chọn Top K đặc trưng có Mutual Information cao nhất."""
    return SelectKBest(score_func=mutual_info_classif, k=k)
