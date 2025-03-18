import streamlit as st
from backend import aqi_and_components
import pydeck as pdk

st.title("🌍 Real-Time Air Quality Map with Pydeck")

# Input for location
lat = st.number_input("Enter Latitude", value=3.1390)
lng = st.number_input("Enter Longitude", value=101.6869)

if st.button("Get AQI Data"):
    aqi_data, components_data = aqi_and_components(lat, lng)

    if "error" in aqi_data:
        st.error(aqi_data["error"])
    else:
        st.success(f"Air Quality Index (AQI): {aqi_data['aqi']}")
        st.write(f"📍 Location: {aqi_data['city']}, {aqi_data['state']}")
        st.write(f"💨 Main Pollutant: {aqi_data['main_pollutant']}")
        st.write("🧪 Pollutant Components:")
        st.json(components_data)

        # AQI Color Mapping
        aqi = aqi_data['aqi']
        if aqi <= 50:
            color = [0, 255, 0]  # Green
        elif aqi <= 100:
            color = [255, 255, 0]  # Yellow
        elif aqi <= 150:
            color = [255, 165, 0]  # Orange
        elif aqi <= 200:
            color = [255, 0, 0]  # Red
        elif aqi <= 300:
            color = [128, 0, 128]  # Purple
        else:
            color = [139, 0, 0]  # Maroon

        # Define Pydeck layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": lat, "lon": lng, "color": color, "size": 100}],
            get_position=["lon", "lat"],
            get_color="color",
            get_radius="size",
            pickable=True,
        )

        # Define Pydeck view
        view_state = pdk.ViewState(
            latitude=lat,
            longitude=lng,
            zoom=10,
            pitch=0
        )

        # Render the map
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer]
        ))