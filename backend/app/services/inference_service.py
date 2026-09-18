"""
Dịch vụ Suy luận Học máy (Inference Service) - Tầng điều phối mô hình.
"""
import os
import time
import pandas as pd
from backend.app.core.config import settings
from backend.app.services.mock_engine import MockEngine

class InferenceService:
    def __init__(self):
        self.model_path = os.path.join(settings.ARTIFACTS_DIR, "nids_pipeline.joblib")
        self.pipeline = None
        self._load_pipeline()
        
    def _load_pipeline(self):
        """Nạp pipeline .joblib nếu tồn tại, ngược lại sử dụng MockEngine."""
        if os.path.exists(self.model_path):
            try:
                import joblib
                self.pipeline = joblib.load(self.model_path)
                print(f"[InferenceService] Pipeline loaded successfully from {self.model_path}")
            except Exception as e:
                print(f"[InferenceService] Error loading pipeline: {e}. Fallback to MockEngine.")
                self.pipeline = None
        else:
            print("[InferenceService] Model artifact not found. Operating in MockEngine mode for Sprint 1.")
            self.pipeline = None

    def is_model_loaded(self) -> bool:
        return self.pipeline is not None

    def predict(self, df: pd.DataFrame, threshold: float = 0.5) -> dict:
        """Thực thi suy luận học máy trên ma trận dữ liệu DataFrame."""
        if self.pipeline is None:
            return MockEngine.generate_predictions(len(df))
            
        t_start = time.time()
        # Tách Ground Truth nếu có
        drop_cols = [c for c in ["id", "label", "attack_cat"] if c in df.columns]
        X = df.drop(columns=drop_cols)
        
        # Dự đoán xác suất
        proba = self.pipeline.predict_proba(X)[:, 1]
        inference_time = round((time.time() - t_start) * 1000, 2)
        
        predictions = []
        attack_count = 0
        for idx, p in enumerate(proba):
            is_attack = p >= threshold
            if is_attack:
                attack_count += 1
            predictions.append({
                "row_id": idx + 1,
                "predicted_label": 1 if is_attack else 0,
                "prediction": "Attack" if is_attack else "Normal",
                "risk_score": round(float(p), 4),
                "risk_level": "High" if p >= 0.7 else ("Medium" if p >= 0.3 else "Low"),
                "ground_truth_label": int(df["label"].iloc[idx]) if "label" in df.columns else None
            })
            
        return {
            "pure_inference_time_ms": inference_time,
            "total_execution_time_ms": inference_time,
            "summary": {
                "total_flows": len(df),
                "normal_count": len(df) - attack_count,
                "attack_count": attack_count,
                "attack_percentage": round((attack_count / len(df)) * 100, 2) if len(df) > 0 else 0.0
            },
            "predictions": predictions
        }

inference_service = InferenceService()
