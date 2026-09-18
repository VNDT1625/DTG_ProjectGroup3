"""
MetricCards Component - Hiển thị các chỉ số giám sát KPI cốt lõi.
"""
import streamlit as st

def render_metric_cards(summary: dict):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng số Luồng (Flows)", f"{summary.get('total_flows', 0):,}")
    with col2:
        st.metric("Lưu lượng Bình thường", f"{summary.get('normal_count', 0):,}")
    with col3:
        st.metric("Lưu lượng Tấn công", f"{summary.get('attack_count', 0):,}")
    with col4:
        rate = summary.get('attack_percentage', 0.0)
        st.metric("Tỷ lệ Xâm nhập", f"{rate:.1f}%", delta=f"{rate:.1f}%" if rate > 10 else None, delta_color="inverse")
