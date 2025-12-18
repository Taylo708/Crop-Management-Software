import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- SETTINGS ---
st.set_page_config(page_title="B&B Taylor Farms AI", layout="wide")

# --- DATA PARSING LOGIC (Based on New Age Labs July 22 SDG) ---
def analyze_sap(new_leaf, old_leaf, ear_leaf, nutrient):
    # Rule from New Age Guide: -20% or more is a deficiency (Red) [cite: 35]
    diff = ((new_leaf - old_leaf) / old_leaf) * 100
    
    status = "✅ Balanced"
    if diff <= -20:
        status = "🚨 ACTIONABLE DEFICIENCY (RED)"
    elif diff >= 20:
        status = "💎 LUXURY UPTAKE (BLUE)"
    
    return round(diff, 2), status

# --- SIDEBAR & AUTH ---
st.sidebar.title("🌽 Field Logistics")
field = st.sidebar.selectbox("Field", ["Big", "North 40"])
variety = st.sidebar.text_input("Variety", "Pioneer") # [cite: 74]
planting_date = st.sidebar.date_input("Planting Date", datetime(2025, 5, 1))

# --- MAIN DASHBOARD ---
st.title(f"B&B Taylor Farms - Field: {field}")
st.info(f"Report Date: July 23, 2025 | Growth Stage: VT (Tassel)") # [cite: 3, 75]

# --- NUTRIENT METRICS ---
# Data points directly from New Age Labs July 22 SDG report [cite: 78]
col1, col2, col3 = st.columns(3)

# Potassium Analysis [cite: 78, 81]
k_diff, k_status = analyze_sap(1490, 2620, 2690, "Potassium")
with col1:
    st.metric("Potassium (K) Gradient", f"{k_diff}%", delta_color="inverse")
    st.write(f"Status: {k_status}")

# Phosphorus Analysis [cite: 78, 83]
p_diff, p_status = analyze_sap(144, 82.3, 173, "Phosphorus")
with col2:
    st.metric("Phosphorus (P) Gradient", f"{p_diff}%")
    st.write(f"Status: {p_status}")

# Nitrogen Efficiency [cite: 78, 237]
with col3:
    st.metric("Nitrogen Efficiency (NCE%)", "93.6%", "New Leaf Target >80%") # [cite: 40]
    st.write("Status: ✅ Optimized Conversion")

# --- MICRONUTRIENT ALERT ---
st.divider()
st.subheader("🤖 AI Predictive Recommendation")

# Boron Analysis [cite: 78]
boron_ear = 0.89 
if boron_ear < 3.0: # New Age OLS Low range for Corn Boron is 3 [cite: 78]
    st.error(f"**POLLINATION WARNING:** Ear Leaf Boron is critically low at **{boron_ear} ppm**. "
             f"This is below the optimal threshold of 3.0 ppm. "
             f"Apply foliar Boron within 48 hours for successful silking.")

# Energy Check [cite: 78]
sugar_ear = 0.825
if 0.5 <= sugar_ear <= 1.5: # New Age target for Metabolic Sugars [cite: 47]
    st.success(f"**Photosynthesis Check:** Ear Leaf Sugars are healthy at {sugar_ear}%. "
               "The plant has energy; it just needs mineral balance.")

# --- DATA TABLE ---
st.write("### Raw Sap Data Snapshot")
raw_data = {
    "Nutrient": ["Potassium (K)", "Phosphorus (P)", "Boron (B)", "NCE%"],
    "New Leaf (ppm)": [1490, 144, 2.64, "93.6%"], # [cite: 78]
    "Old Leaf (ppm)": [2620, 82.3, 0.49, "90.1%"], # [cite: 78]
    "Ear Leaf (ppm)": [2690, 173, 0.89, "95.5%"]  # [cite: 78, 237]
}
st.dataframe(pd.DataFrame(raw_data))