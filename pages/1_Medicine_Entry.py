import streamlit as st
import pandas as pd
from database import init_db, add_record
from datetime import date, timedelta

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

init_db()

@st.cache_data
def load_medicines():
    try:
        df = pd.read_excel("Veterinary_Medicines_Master.xlsx")
        return df
    except:
        return None

med_df = load_medicines()

if med_df is not None:
    med_dict = dict(zip(med_df['Medicine_Name'], med_df['Withdrawal_Period_Days']))
    medicine_list = med_df['Medicine_Name'].tolist()
else:
    med_dict = {
        "Oxytetracycline": 21, "Ampicillin": 14,
        "Enrofloxacin": 14, "Penicillin": 7,
        "Amoxicillin": 10, "Streptomycin": 18
    }
    medicine_list = list(med_dict.keys())

st.title("💊 Medicine Entry Form")
st.write("Fill in the details of antimicrobial given to the animal")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    animal_id = st.text_input("🐄 Animal ID (e.g. COW-001)")
    animal_name = st.text_input("📛 Animal Name")
    species = st.selectbox("🐾 Species", ["Cow", "Buffalo", "Goat", "Sheep", "Chicken", "Pig", "Duck", "Horse"])

with col2:
    medicine_name = st.selectbox("💊 Medicine Name", medicine_list)
    dose = st.text_input("💉 Dose (e.g. 5ml, 2 tablets)")
    reason = st.selectbox("📋 Reason", ["Treatment", "Prevention", "Feed Additive"])

withdrawal_days = int(med_dict.get(medicine_name, 7))
date_given = st.date_input("📅 Date Given", value=date.today())
st.info(f"⏳ Auto Withdrawal Period for **{medicine_name}**: **{withdrawal_days} days**")
safe_date = date_given + timedelta(days=withdrawal_days)
st.success(f"✅ Safe to sell after: **{safe_date}**")
st.markdown("---")

if st.button("💾 Save Record", type="primary"):
    if animal_id and animal_name and dose:
        add_record(animal_id, animal_name, species, medicine_name, dose, reason,
                   str(date_given), withdrawal_days, str(safe_date))
        st.success("✅ Record saved successfully!")
        st.balloons()
    else:
        st.error("❌ Please fill Animal ID, Name and Dose!")