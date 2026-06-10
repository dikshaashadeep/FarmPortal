import streamlit as st
import sqlite3
from database import get_all_records, get_all_animals

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

if st.session_state.role != "Admin":
    st.error("❌ Admin access only!")
    st.stop()

st.title("⚙️ Admin Panel")
st.markdown("---")
st.warning("⚠️ Admin access only! Be careful.")

col1, col2 = st.columns(2)
with col1:
    st.metric("💊 Medicine Records", len(get_all_records()))
with col2:
    st.metric("🐄 Animals Registered", len(get_all_animals()))

st.markdown("---")
st.subheader("🗑️ Delete All Medicine Records")
if st.checkbox("I understand this deletes all medicine records permanently"):
    if st.button("🗑️ Delete Medicine Records", type="primary"):
        conn = sqlite3.connect("farmportal.db")
        conn.execute("DELETE FROM medicines")
        conn.commit()
        conn.close()
        st.success("✅ Done!")
        st.balloons()

st.markdown("---")
st.subheader("🗑️ Delete All Animal Registrations")
if st.checkbox("I understand this deletes all animal records permanently"):
    if st.button("🗑️ Delete Animal Records", type="primary"):
        conn = sqlite3.connect("farmportal.db")
        conn.execute("DELETE FROM animals")
        conn.commit()
        conn.close()
        st.success("✅ Done!")