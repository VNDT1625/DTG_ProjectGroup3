"""
Các hàm tiện ích bảo mật và khử khuẩn dữ liệu.
"""
import re
import uuid

def generate_file_id() -> str:
    """Sinh định danh ngẫu nhiên chuẩn UUID v4 cho phiên tệp."""
    return f"fl_{uuid.uuid4().hex[:12]}_2026"

def sanitize_formula_injection(value: str) -> str:
    """Ngăn chặn CSV/Formula Injection bằng cách thêm dấu nháy đơn nếu bắt đầu bằng =, +, -, @."""
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return f"'{value}"
    return value
