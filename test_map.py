import pydeck as pdk
import pandas as pd
import streamlit as st

# Load Sample Data
df = pd.DataFrame({
    "state": ["CA", "NY", "TX"],
    "city": ["Los Angeles", "New York", "Houston"],
    "latitude": [34.0522, 40.7128, 29.7604],
    "longitude": [-118.2437, -74.0060, -95.3698],
    "aqi": [85, 60, 120]
})

# Define Pydeck Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["longitude", "latitude"],  # Ensure correct order
    get_color=["aqi * 2", "255 - (aqi * 2)", "0", "180"],  # Example color mapping
    get_radius=100000,
    pickable=True
)

# Define View
view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=5,
    pitch=0
)

# Render Pydeck Map
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "City: {city}\nAQI: {aqi}"}
))
