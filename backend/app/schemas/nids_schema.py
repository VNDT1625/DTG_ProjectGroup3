"""
Đặc tả Hợp đồng Dữ liệu Pydantic (Data Contracts).
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool
    model_type: str
    timestamp: str

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    total_rows: int
    total_features: int
    has_ground_truth: bool
    validation_status: str
    preview_data: List[Dict[str, Any]]

class PredictRequest(BaseModel):
    file_id: str
    threshold: float = Field(default=0.50, ge=0.0, le=1.0)

class PredictionItem(BaseModel):
    row_id: int
    predicted_label: int # 0: Normal, 1: Attack
    prediction: str # Normal / Attack
    risk_score: float # 0.0 - 1.0
    risk_level: str # Low, Medium, High
    ground_truth_label: Optional[int] = None

class PredictionSummary(BaseModel):
    total_flows: int
    normal_count: int
    attack_count: int
    attack_percentage: float

class PredictResponse(BaseModel):
    file_id: str
    pure_inference_time_ms: float
    total_execution_time_ms: float
    summary: PredictionSummary
    predictions: List[PredictionItem]
