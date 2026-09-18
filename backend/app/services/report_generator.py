"""
Dịch vụ Xuất Báo cáo Đa định dạng (CSV, XLSX, PDF).
"""
import io
import pandas as pd
from backend.app.core.security import sanitize_formula_injection

class ReportGenerator:
    @staticmethod
    def generate_csv(results: list) -> io.BytesIO:
        df = pd.DataFrame(results)
        # Khử khuẩn chống CSV injection
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].apply(sanitize_formula_injection)
        buf = io.BytesIO()
        df.to_csv(buf, index=False, encoding="utf-8-sig")
        buf.seek(0)
        return buf

    @staticmethod
    def generate_excel(results: list) -> io.BytesIO:
        df = pd.DataFrame(results)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="AI_NIDS_Report")
        buf.seek(0)
        return buf
