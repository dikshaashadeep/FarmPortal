import streamlit as st
from database import init_db, add_animal, get_all_animals

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

init_db()

st.title("🐄 Animal Registration")
st.write("Register new animals on the farm")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    animal_id = st.text_input("🏷️ Animal ID (e.g. COW-001)")
    name = st.text_input("📛 Animal Name")
    species = st.selectbox("🐾 Species", ["Cow", "Buffalo", "Goat", "Sheep", "Chicken", "Pig", "Duck", "Horse"])
    breed = st.text_input("🧬 Breed (e.g. Murrah, Holstein)")

with col2:
    age = st.text_input("📅 Age (e.g. 3 years)")
    gender = st.selectbox("⚧ Gender", ["Female", "Male"])
    owner = st.text_input("👨‍🌾 Owner Name")
    village = st.text_input("🏘️ Village / Location")

health_status = st.selectbox("🏥 Health Status", ["Healthy", "Under Observation", "Critical", "Under Treatment"])

st.markdown("---")

if st.button("💾 Register Animal", type="primary"):
    if animal_id and name and owner:
        success = add_animal(animal_id, name, species, breed, age, gender, owner, village, health_status)
        if success:
            st.success(f"✅ {name} registered successfully!")
            st.balloons()
        else:
            st.error(f"❌ Animal ID '{animal_id}' already exists!")
    else:
        st.error("❌ Please fill Animal ID, Name and Owner!")

st.markdown("---")
st.subheader("📋 Registered Animals")
animals = get_all_animals()
if not animals:
    st.info("📭 No animals registered yet!")
else:
    st.markdown(f"**Total: {len(animals)} animals**")
    for a in animals:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"🐄 **{a[2]}** ({a[1]})")
            st.caption(f"Species: {a[3]} | Breed: {a[4]} | Age: {a[5]}")
        with col2:
            st.write(f"👨‍🌾 Owner: {a[7]}")
            st.caption(f"Gender: {a[6]} | Village: {a[8]}")
        with col3:
            if a[9] == "Healthy":
                st.success("✅ Healthy")
            elif a[9] == "Critical":
                st.error("🚨 Critical")
            else:
                st.warning("👁️ Observation")
        st.markdown("---")