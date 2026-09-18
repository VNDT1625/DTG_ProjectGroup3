"""
Cấu hình cốt lõi hệ thống AI-NIDS Backend.
"""
import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "AI-NIDS Backend Gateway"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:8501", "http://127.0.0.1:8501", "*"]
    MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024 # 50 MB
    MAX_ROWS_LIMIT: int = 100_000
    ARTIFACTS_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml_pipeline/artifacts"))
    DATA_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))

settings = Settings()
