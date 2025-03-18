import streamlit as st
import pydeck as pdk
import pandas as pd
from accessory_functions import get_aqi_color,hex_to_rgb
def display_aqi_map(location, aqi_data):
    lat, lng = location
    aqi_value = aqi_data['aqi']
    color = get_aqi_color(aqi_value)
    color = hex_to_rgb(color)
    
    map_layer = pdk.Layer(
        "IconLayer",
        data=pd.DataFrame({
            "lat": [lat],
            "lon": [lng],
            "aqi": [aqi_value],
            "icon_data": [
                {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/e/ec/RedDot.svg", 
                    "width": 128,
                    "height": 128,
                    "anchorY": 128
                }
            ]
        }),
        get_position=["lon", "lat"],
        get_icon="icon_data",
        get_size=20,
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

def display_heatmap(location, components):
    lat, lng = location
    
    data = pd.DataFrame([
        {"lat": lat, "lon": lng, "value": components[comp], "component": comp} for comp in components
    ])
    
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=data,
        get_position=["lon", "lat"],
        get_weight="value",
        radius_pixels=60,
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lng,
        zoom=10,
        pitch=0,
        min_zoom=5,
        max_zoom=15,
    )
    
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[heatmap_layer],
        tooltip={
            "html": "<b>Component:</b> {component}<br><b>Value:</b> {value}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    ))