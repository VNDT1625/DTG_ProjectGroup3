"""
ExportWidget Component - Nút chọn định dạng và tải xuống báo cáo tổng hợp.
"""
import streamlit as st

def render_export_section(file_id: str, backend_url: str):
    st.subheader("📥 Xuất Báo cáo Kết quả Phân tích")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label="Tải Báo cáo Định dạng CSV",
            data="",
            file_name=f"nids_report_{file_id}.csv",
            mime="text/csv",
            disabled=True,
            help="Tải file CSV có kèm predicted_label và risk_score."
        )
    with c2:
        st.download_button(
            label="Tải Báo cáo Định dạng XLSX",
            data="",
            file_name=f"nids_report_{file_id}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            disabled=True,
            help="Tải file Excel định dạng bảng biểu chuyên nghiệp."
        )
