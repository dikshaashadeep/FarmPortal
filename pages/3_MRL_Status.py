import streamlit as st
from database import get_all_records
from datetime import date

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

st.title("✅ MRL Compliance Status")
st.write("Check if animal products meet Maximum Residue Limits")
st.markdown("---")

records = get_all_records()

if not records:
    st.info("📭 No records found. Add medicine entries first!")
else:
    today = date.today()
    safe_count = sum(1 for r in records if date.fromisoformat(r[9]) <= today)
    unsafe_count = len(records) - safe_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total Records", len(records))
    with col2:
        st.metric("✅ MRL Compliant", safe_count)
    with col3:
        st.metric("❌ Non-Compliant", unsafe_count)

    st.markdown("---")
    st.subheader("📋 All Animal MRL Status")
    for r in records:
        safe_date = date.fromisoformat(r[9])
        days_left = (safe_date - today).days
        is_safe = today >= safe_date
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"🐄 **{r[2]}** ({r[1]})")
            st.caption(f"Species: {r[3]} | Medicine: {r[4]} | Dose: {r[5]}")
        with col2:
            st.write(f"📅 Given: {r[7]} | Withdrawal: {r[8]} days")
            st.caption(f"Safe Date: {r[9]} | Reason: {r[6]}")
        with col3:
            if is_safe:
                st.success("✅ SAFE")
            else:
                st.error(f"❌ {days_left}d left")
        st.markdown("---")