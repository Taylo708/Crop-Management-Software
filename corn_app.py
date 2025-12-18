import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="Taylor Farms AI - Weather & GDD", layout="wide")

# --- GDD CALCULATION LOGIC ---
def calculate_gdd(tmax, tmin):
    # Standard Corn GDD: Base 50°F, Ceiling 86°F
    tmax = 86 if tmax > 86 else (50 if tmax < 50 else tmax)
    tmin = 86 if tmin > 86 else (50 if tmin < 50 else tmin)
    gdd = ((tmax + tmin) / 2) - 50
    return max(0, gdd)

# --- APP FRONTEND ---
st.title("🌽 B&B Taylor Farms: GDD & Weather Forecast")

col_metrics, col_map = st.columns([1, 2])

with col_metrics:
    st.subheader("Field Vitals: Big")
    current_gdd = 1185 # From your July 23 Status
    st.metric("Accumulated GDD", f"{current_gdd}", "+24 Today")
    st.metric("Current Stage", "VT (Tassel)")
    
    # Milestone Tracking
    silk_target = 1300
    gdds_needed = silk_target - current_gdd
    st.write(f"**GDDs to Silking (R1):** {int(gdds_needed)}")
    st.progress(current_gdd / 2700, text="Progress to Black Layer")

with col_map:
    # Field Map centered on Stockbridge, MI
    m = folium.Map(location=[42.4590, -84.1950], zoom_start=15, tiles="CartoDB satellite")
    st_folium(m, width=700, height=350)

st.divider()

# --- WEATHER FORECAST & GDD PROJECTION ---
st.header("📅 7-Day GDD Projection")
st.write("Calculated using the 86/50 method for Pioneer Hybrid.")

# Mock Forecast Data (This would connect to a Weather API in a full build)
dates = [(datetime.now() + timedelta(days=i)).strftime('%b %d') for i in range(7)]
highs = [88, 90, 92, 85, 84, 87, 89]
lows = [65, 68, 70, 64, 62, 65, 67]

gdd_forecast = []
running_total = current_gdd

for h, l in zip(highs, lows):
    gain = calculate_gdd(h, l)
    running_total += gain
    gdd_forecast.append({
        "Daily Gain": gain,
        "Running Total": int(running_total)
    })

forecast_df = pd.DataFrame({
    "Date": dates,
    "High (°F)": highs,
    "Low (°F)": lows,
    "GDD Gain": [d["Daily Gain"] for d in gdd_forecast],
    "Proj. Total": [d["Running Total"] for d in gdd_forecast]
})

st.table(forecast_df)

# --- SMART ALERT ---
projected_r1 = dates[next(i for i, d in enumerate(gdd_forecast) if d["Running Total"] >= silk_target)]
st.success(f"### 🤖 AI Forecast: **Silking (R1)** is projected to begin on **{projected_r1}**.")
st.info("Based on your Pioneer variety at the 'Big' field, ensure all VT nutrient passes are completed before this date.")
