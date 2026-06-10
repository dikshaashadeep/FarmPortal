import streamlit as st
from database import init_db, check_login

init_db()

st.set_page_config(page_title="AgriMed Shield", page_icon="🐄", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.markdown("""
        <div style="text-align:center; padding:60px 0 20px 0;">
            <div style="font-size:72px;">🐄</div>
            <h1 style="color:#1D9E75; font-size:48px; margin:0;">AgriMed Shield</h1>
            <p style="color:#888; font-size:18px;">Digital Farm Management Portal</p>
            <p style="color:#aaa; font-size:14px;">Monitoring MRL & Antimicrobial Usage in Livestock</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login to Continue")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("🔐 Login", type="primary", use_container_width=True):
            role = check_login(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.rerun()
            else:
                st.error("❌ Wrong username or password!")
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.caption("👨‍🌾 Farmer: `farmer1` / `farm123`")
        st.caption("👨‍⚕️ Vet: `vet1` / `vet123`")
        st.caption("⚙️ Admin: `admin` / `admin123`")

else:
    st.sidebar.markdown(f"### 👋 Hello, {st.session_state.username}!")
    st.sidebar.markdown(f"**Role:** {st.session_state.role}")
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    st.title("🐄 AgriMed Shield")
    st.subheader("Digital Farm Management Portal")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("💊 Track Medicine Usage\n\nLog every antimicrobial given to animals")
    with col2:
        st.warning("⏰ Withdrawal Period Alerts\n\nKnow when products are safe to sell")
    with col3:
        st.success("✅ MRL Compliance\n\nEnsure food safety with real-time checks")
    st.markdown("---")
    st.markdown("### 👈 Use the sidebar to navigate")
    st.caption("Developed by Team AgriMed Shield | GL Bajaj Group of Institutions, Mathura")