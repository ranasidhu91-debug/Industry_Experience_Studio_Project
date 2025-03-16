import streamlit as st
from frontend import get_geolocation
from backend import get_coordinates_from_zip, get_air_quality
st.title("Real-Time Air Quality Checker")

get_geolocation()

lat = st.experimental_get_query_params().get("lat", [None])[0]
lon = st.experimental_get_query_params().get("lon", [None])[0]

if lat == "manual":  # If user manually entered ZIP & country
    zip_code, country_code = lon.split(",")  # lon stores "zip_code,country_code"
    lat, lon = get_coordinates_from_zip(zip_code, country_code)

    if lat is None or lon is None:
        st.error("❌ Invalid ZIP or country code. Please enter a valid location.")
        st.stop()

if lat and lon:
    lat, lon = float(lat), float(lon)
    st.success(f"🌍 Location Detected: {lat}, {lon}")

    # Get AQI & Air Components
    air_quality = get_air_quality(lat, lon)

    # Handle API errors
    if "error" in air_quality:
        st.error(air_quality["error"])
    else:
        aqi = air_quality["aqi"]
        components = air_quality["components"]

        # Display AQI
        st.write(f"🌿 **Air Quality Index (AQI):** {aqi}")

        # Display air pollutants
        st.subheader("🛑 Air Pollutants (μg/m³)")
        st.write(f"- **CO (Carbon Monoxide):** {components['co']}")
        st.write(f"- **NO (Nitric Oxide):** {components['no']}")
        st.write(f"- **NO₂ (Nitrogen Dioxide):** {components['no2']}")
        st.write(f"- **O₃ (Ozone):** {components['o3']}")
        st.write(f"- **SO₂ (Sulfur Dioxide):** {components['so2']}")
        st.write(f"- **PM2.5 (Fine Particulate Matter):** {components['pm2_5']}")
        st.write(f"- **PM10 (Coarse Particulate Matter):** {components['pm10']}")
        st.write(f"- **NH₃ (Ammonia):** {components['nh3']}")
else:
    st.warning("🌍 Waiting for location... Please enable location services or enter manually.")