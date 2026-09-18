"""
Charts Component - Trực quan hóa tỷ lệ xâm nhập và mức độ rủi ro bằng Plotly.
"""
import plotly.graph_objects as go
import streamlit as st

def render_donut_chart(summary: dict):
    labels = ["Bình thường (Normal)", "Tấn công (Attack)"]
    values = [summary.get("normal_count", 0), summary.get("attack_count", 0)]
    colors = ["#10B981", "#EF4444"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.55,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hoverinfo='label+value+percent'
    )])
    fig.update_layout(
        title_text="Phân bố Tỷ lệ Xâm nhập Mạng",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)
