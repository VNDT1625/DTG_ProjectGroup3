"""
UploadView Component - Kéo thả tệp CSV và gửi yêu cầu xác thực tới Backend.
"""
import streamlit as st

def render_upload_section():
    st.subheader("📤 1. Tải lên Dữ liệu Lưu lượng Mạng (CSV)")
    uploaded_file = st.file_uploader(
        "Kéo thả tệp log mạng (.csv) theo chuẩn UNSW-NB15 (Dung lượng tối đa 50MB)",
        type=["csv"],
        help="Hệ thống hỗ trợ tập dữ liệu chuẩn hóa UNSW-NB15 gồm 47 đặc trưng đầu vào."
    )
    return uploaded_file
