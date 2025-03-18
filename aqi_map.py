import streamlit as st
import pydeck as pdk
import pandas as pd
def display_aqi_map(location, aqi_data):
    lat, lng = location
    aqi_value = aqi_data['aqi']
    
    color = [0, 255, 0] if aqi_value <= 50 else [255, 255, 0] if aqi_value <= 100 else [255, 165, 0] if aqi_value <= 150 else [255, 0, 0] if aqi_value <= 200 else [153, 0, 76]
    
    map_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"lat": [lat], "lon": [lng], "aqi": [aqi_value]}),
        get_position=["lon", "lat"],
        get_radius=2,
        get_fill_color=color,
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lng,
        zoom=10,
        pitch=0,
    )
    
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[map_layer],
        tooltip={
            "html": "<b>AQI:</b> {aqi}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    ))