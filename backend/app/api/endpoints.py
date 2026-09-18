"""
API Endpoints Router của hệ thống AI-NIDS Backend.
"""
from datetime import datetime
import pandas as pd
import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from backend.app.schemas.nids_schema import HealthResponse, UploadResponse, PredictRequest, PredictResponse
from backend.app.core.security import generate_file_id
from backend.app.core.config import settings
from backend.app.services.inference_service import inference_service
from backend.app.services.report_generator import ReportGenerator

router = APIRouter()

# In-memory storage cho prototype
SESSION_CACHE = {}

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Kiểm tra tính khả dụng của Backend Gateway và Model Pipeline."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        model_loaded=inference_service.is_model_loaded(),
        model_type="XGBoost / Random Forest Classifier (nids_pipeline.joblib)" if inference_service.is_model_loaded() else "MockEngine (Sprint 1)",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@router.post("/api/v1/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Tiếp nhận file CSV, kiểm tra MIME type, kích thước <= 50MB và cấu trúc đặc trưng."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận tệp định dạng .csv")
        
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="Kích thước tệp vượt quá giới hạn 50MB")
        
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Không thể đọc file CSV: {str(e)}")
        
    if len(df) > settings.MAX_ROWS_LIMIT:
        raise HTTPException(status_code=400, detail=f"Số dòng vượt quá giới hạn {settings.MAX_ROWS_LIMIT}")
        
    file_id = generate_file_id()
    SESSION_CACHE[file_id] = df
    
    has_ground_truth = "label" in df.columns
    preview = df.head(5).fillna("").to_dict(orient="records")
    
    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        total_rows=len(df),
        total_features=len(df.columns),
        has_ground_truth=has_ground_truth,
        validation_status="PASSED",
        preview_data=preview
    )

@router.post("/api/v1/predict", response_model=PredictResponse)
def predict_network_traffic(req: PredictRequest):
    """Thực thi suy luận phát hiện xâm nhập mạng."""
    if req.file_id not in SESSION_CACHE:
        raise HTTPException(status_code=404, detail="Phiên làm việc (file_id) không tồn tại hoặc đã hết hạn.")
        
    df = SESSION_CACHE[req.file_id]
    result = inference_service.predict(df, threshold=req.threshold)
    
    # Lưu kết quả vào cache phục vụ export
    SESSION_CACHE[f"res_{req.file_id}"] = result["predictions"]
    
    return PredictResponse(
        file_id=req.file_id,
        pure_inference_time_ms=result["pure_inference_time_ms"],
        total_execution_time_ms=result["total_execution_time_ms"],
        summary=result["summary"],
        predictions=result["predictions"]
    )

@router.get("/api/v1/export/{format_type}")
def export_report(format_type: str, file_id: str):
    """Xuất báo cáo định dạng CSV hoặc XLSX kèm kiểm soát an toàn."""
    res_key = f"res_{file_id}"
    if res_key not in SESSION_CACHE:
        raise HTTPException(status_code=404, detail="Kết quả phân tích không tìm thấy.")
        
    results = SESSION_CACHE[res_key]
    if format_type.lower() == "csv":
        buf = ReportGenerator.generate_csv(results)
        return Response(content=buf.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=nids_report_{file_id}.csv"})
    elif format_type.lower() == "xlsx":
        buf = ReportGenerator.generate_excel(results)
        return Response(content=buf.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=nids_report_{file_id}.xlsx"})
    else:
        raise HTTPException(status_code=400, detail="Định dạng xuất không hợp lệ (hỗ trợ csv, xlsx)")
