import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database import get_all_records
from datetime import date

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

st.markdown("""<style>
.metric-card { background:linear-gradient(135deg,#0f4c35,#1D9E75); border-radius:15px; padding:20px; text-align:center; color:white; margin:5px; }
.metric-value { font-size:42px; font-weight:bold; }
.metric-label { font-size:14px; color:#a8f0d4; margin-top:5px; }
.dashboard-header { background:linear-gradient(135deg,#0a2e20,#1D9E75); padding:30px; border-radius:15px; margin-bottom:25px; text-align:center; }
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="dashboard-header">
<h1 style="color:white;margin:0;">📊 Farm Analytics Dashboard</h1>
<p style="color:#a8f0d4;margin:5px 0 0 0;">Real-time AMU Trends & MRL Compliance Overview</p>
</div>""", unsafe_allow_html=True)

records = get_all_records()

if not records:
    st.info("📭 No records yet! Add medicine entries first.")
else:
    df = pd.DataFrame(records, columns=["id","animal_id","animal_name","species","medicine","dose","reason","date_given","withdrawal_days","safe_date"])
    today = date.today()
    safe_count = sum(1 for r in records if date.fromisoformat(r[9]) <= today)
    unsafe_count = len(records) - safe_count

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">🐄 {len(df)}</div><div class="metric-label">Total Records</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="background:linear-gradient(135deg,#1a3a5c,#2196F3);"><div class="metric-value">💊 {df["medicine"].nunique()}</div><div class="metric-label">Medicines Used</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="background:linear-gradient(135deg,#1a3a1a,#4CAF50);"><div class="metric-value">✅ {safe_count}</div><div class="metric-label">Safe to Sell</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card" style="background:linear-gradient(135deg,#3a1a1a,#f44336);"><div class="metric-value">⚠️ {unsafe_count}</div><div class="metric-label">In Withdrawal</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🐄 Records by Species")
        sc = df["species"].value_counts().reset_index()
        sc.columns = ["Species","Count"]
        fig1 = px.pie(sc, names="Species", values="Count", hole=0.4,
            color_discrete_sequence=["#1D9E75","#2196F3","#FF9800","#9C27B0","#f44336"])
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### 💊 Top Medicines Used")
        mc = df["medicine"].value_counts().reset_index()
        mc.columns = ["Medicine","Count"]
        fig2 = px.bar(mc.head(10), x="Medicine", y="Count", color="Count",
            color_continuous_scale=["#0a2e20","#1D9E75","#a8f0d4"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white",
            xaxis=dict(gridcolor="#333"), yaxis=dict(gridcolor="#333"))
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📅 Usage Over Time")
        df["date_given"] = pd.to_datetime(df["date_given"])
        dc = df.groupby("date_given").size().reset_index(name="Count")
        fig3 = px.line(dc, x="date_given", y="Count", markers=True,
            color_discrete_sequence=["#1D9E75"])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white",
            xaxis=dict(gridcolor="#333"), yaxis=dict(gridcolor="#333"))
        fig3.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("### 🎯 MRL Compliance")
        fig4 = go.Figure(go.Pie(
            labels=["✅ Safe","⚠️ Withdrawal"],
            values=[safe_count or 0.1, unsafe_count or 0.1],
            marker_colors=["#1D9E75","#f44336"], hole=0.5))
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig4, use_container_width=True)