"""
Pipeline Tiền xử lý Dữ liệu (Preprocessing Module).
Phụ trách: Trần Thị Thu Hiền, Trần Ngọc Hải
"""
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

CATEGORICAL_COLS = ["proto", "service", "state"]
DROP_COLS = ["id", "attack_cat", "label"]

def build_preprocessor(numerical_cols: list[str]) -> ColumnTransformer:
    """Xây dựng bộ tiền xử lý kết hợp OneHotEncoder và StandardScaler."""
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="-")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ("num", num_pipeline, numerical_cols),
        ("cat", cat_pipeline, CATEGORICAL_COLS)
    ])
    
    return preprocessor
