import streamlit as st
from database import get_all_records
from datetime import date

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

st.title("⏰ Withdrawal Period Alerts")
st.write("Check which animals are safe to sell today")
st.markdown("---")

records = get_all_records()

if not records:
    st.info("📭 No records found. Add medicine entries first!")
else:
    today = date.today()
    safe, not_safe = [], []
    for r in records:
        if today >= date.fromisoformat(r[9]):
            safe.append(r)
        else:
            not_safe.append(r)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total Records", len(records))
    with col2:
        st.metric("✅ Safe to Sell", len(safe))
    with col3:
        st.metric("⚠️ In Withdrawal", len(not_safe))

    st.markdown("---")
    if not_safe:
        st.subheader("⚠️ Animals Still in Withdrawal Period")
        for r in not_safe:
            days_left = (date.fromisoformat(r[9]) - today).days
            st.error(f"🐄 **{r[2]}** ({r[1]}) | Medicine: {r[4]} | Safe after: **{r[9]}** | ⏳ **{days_left} days left**")

    if safe:
        st.subheader("✅ Safe to Sell Now")
        for r in safe:
            st.success(f"🐄 **{r[2]}** ({r[1]}) | Medicine: {r[4]} | Safe since: **{r[9]}**")

    if not not_safe:
        st.success("🎉 All animals are currently safe to sell!")