"""
Kiểm thử Chuỗi Tiền xử lý (Pipeline Tests).
"""
import pandas as pd
from ml_pipeline.src.preprocessing import build_preprocessor

def test_preprocessor_creation():
    num_cols = ["dur", "sbytes", "dbytes", "sttl", "dttl"]
    preprocessor = build_preprocessor(num_cols)
    assert preprocessor is not None
