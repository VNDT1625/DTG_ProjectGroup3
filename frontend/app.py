"""
Dashboard Giám sát An ninh Mạng Thời gian thực (AI-NIDS) - Streamlit Main App.
Phụ trách: Dương Hoàng Bảo Long
"""
import streamlit as st
import pandas as pd
import requests
from frontend.components.upload_view import render_upload_section
from frontend.components.metric_cards import render_metric_cards
from frontend.components.charts import render_donut_chart

st.set_page_config(
    page_title="AI-NIDS Dashboard | DTG Group 03",
    page_icon="🛡️",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🛡️ AI-NIDS: Bảng Điều Khiển Giám Sát An Ninh Mạng")
st.markdown("**Dự án Thực tập Doanh nghiệp DTG 2026 – Nhóm 03** | Chuẩn IEEE 1016 & C4 Model | UNSW-NB15 Dataset")

# Sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình Hệ thống")
    st.write(f"**Backend Gateway:** `{BACKEND_URL}`")
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=2)
        if r.status_code == 200:
            st.success("🟢 Backend Gateway: Online")
            data = r.json()
            st.caption(f"Model Engine: {data.get('model_type')}")
        else:
            st.warning("🟠 Backend Gateway: Degraded")
    except Exception:
        st.error("🔴 Backend Gateway: Offline (Vui lòng khởi chạy backend/main.py)")
        
    threshold = st.slider("Ngưỡng cảnh báo Rủi ro (Threshold)", min_value=0.1, max_value=0.9, value=0.5, step=0.05)
    st.info("Ngưỡng mặc định 0.50. Tăng ngưỡng để giảm thiểu báo động giả (False Positive).")

uploaded_file = render_upload_section()

if uploaded_file is not None:
    st.success(f"Đã nạp tệp: `{uploaded_file.name}` ({round(uploaded_file.size / 1024, 1)} KB)")
    
    # Đọc preview
    df_preview = pd.read_csv(uploaded_file, nrows=5)
    st.write("📋 **Bảng xem trước dữ liệu (5 dòng đầu tiên):**")
    st.dataframe(df_preview, use_container_width=True)
    
    if st.button("🚀 Bắt đầu Phân tích Xâm nhập Mạng", type="primary"):
        with st.spinner("Đang gửi dữ liệu tới Backend và chạy suy luận Machine Learning..."):
            try:
                # Gửi upload
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                res_upload = requests.post(f"{BACKEND_URL}/api/v1/upload", files=files, timeout=30)
                
                if res_upload.status_code == 200:
                    up_data = res_upload.json()
                    file_id = up_data["file_id"]
                    
                    # Gửi predict
                    payload = {"file_id": file_id, "threshold": threshold}
                    res_pred = requests.post(f"{BACKEND_URL}/api/v1/predict", json=payload, timeout=60)
                    
                    if res_pred.status_code == 200:
                        pred_data = res_pred.json()
                        st.success(f"✅ Phân tích hoàn tất! Độ trễ suy luận: {pred_data.get('pure_inference_time_ms')} ms")
                        
                        # Hiển thị KPI & Biểu đồ
                        render_metric_cards(pred_data["summary"])
                        c1, c2 = st.columns([1.2, 1.8])
                        with c1:
                            render_donut_chart(pred_data["summary"])
                        with c2:
                            st.subheader("⚠️ Danh sách Cảnh báo Nguy cơ Cao")
                            df_pred = pd.DataFrame(pred_data["predictions"])
                            st.dataframe(df_pred.head(20), use_container_width=True)
                    else:
                        st.error(f"Lỗi suy luận: {res_pred.text}")
                else:
                    st.error(f"Lỗi tải file: {res_upload.text}")
            except Exception as e:
                st.error(f"Lỗi kết nối tới Backend Gateway: {str(e)}")
