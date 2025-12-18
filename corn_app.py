import streamlit as st
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CornYield GDD Tracker", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR THE "PREVIEW" LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4255; }
    .status-card { background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #00ff00; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.title("🚜 Field Management")
field_name = st.sidebar.text_input("Field Name", "Big")
planting_date = st.sidebar.date_input("Planting Date", datetime(2025, 5, 1))
hybrid_rm = st.sidebar.number_input("Hybrid RM (Days)", value=112)
target_gdd = st.sidebar.number_input("Target GDD to Black Layer", value=2700)

# --- HEADER SECTION ---
st.title("🌽 CornYield GDD Tracker")
st.subheader(f"Current Status for Field: **{field_name}**")

# --- MAIN DASHBOARD METRICS ---
# Logic: These would be pulled from your Weather API in the final version
current_gdd = 1185
yesterday_gdd = 1162
daily_gain = current_gdd - yesterday_gdd

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accumulated GDD", f"{current_gdd}", f"+{daily_gain} Today")

with col2:
    progress = min(current_gdd / target_gdd, 1.0)
    st.metric("Season Progress", f"{int(progress * 100)}%", f"Target: {target_gdd}")

with col3:
    st.metric("Current Stage", "VT (Tassel)", "Critical Window")

with col4:
    st.metric("7-Day Forecast", "+145 GDD", "Hot/Dry")

# --- GROWTH STAGE TIMELINE ---
st.write("---")
st.header("📅 Growth Stage Projection")

# Define stages based on standard GDD triggers
stages = {
    "V6 Sidedress": 475,
    "VT Tasseling": 1150,
    "R1 Silking": 1300,
    "R6 Black Layer": 2700
}

# Create the visual timeline
cols = st.columns(len(stages))
for i, (stage, gdd_trigger) in enumerate(stages.items()):
    with cols[i]:
        if current_gdd >= gdd_trigger:
            st.markdown(f"**{stage}**")
            st.write("✅ Complete")
        elif current_gdd + 145 >= gdd_trigger:
             st.markdown(f"**{stage}**")
             st.write("⏳ **In 4 Days**")
        else:
            st.markdown(f"**{stage}**")
            st.write(f"Target: {gdd_trigger}")

# --- ACTIONABLE RECOMMENDATIONS ---
st.write("---")
st.header("🤖 Field Recommendations")

# Logic engine for alerts
if 1150 <= current_gdd <= 1300:
    st.markdown("""
        <div class="status-card">
            <h3>📍 Critical Stage: VT Tasseling</h3>
            <p>Your field is currently in the pollination window. Avoid heavy stress.</p>
            <ul>
                <li><b>Action:</b> Scout for Western Bean Cutworm and Corn Rootworm beetles.</li>
                <li><b>Logistics:</b> Ensure fungicide/micros are on hand if R1 timing stays on track for next week.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("System monitoring weather patterns. No critical nutrient alerts for current GDD window.")

st.write("---")
st.caption("Data synced with local weather station. Predicted maturity based on Pioneer GDD charts.")
