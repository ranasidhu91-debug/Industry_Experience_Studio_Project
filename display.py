import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from backend import get_coordinates_from_zip, get_air_quality

st.title("Real-Time Air Quality Checker")

# ✅ Initialize session state variables
if "lat" not in st.session_state:
    st.session_state.lat = None
    st.session_state.lon = None

if "use_manual" not in st.session_state:
    st.session_state.use_manual = False  # Tracks if manual input mode is active

# ✅ Toggle Between Manual & Automatic Location
use_manual = st.checkbox("🔄 Switch to Manual Location Entry", value=st.session_state.use_manual)

# ✅ If switching modes, reset lat/lon to prevent stale values
if use_manual != st.session_state.use_manual:
    st.session_state.lat = None
    st.session_state.lon = None

# ✅ Store toggle state
st.session_state.use_manual = use_manual

# ✅ Manual Input Section (Only visible if manual mode is active)
if st.session_state.use_manual:
    st.subheader("🔴 Enter Your Location Manually")
    zip_code = st.text_input("ZIP Code", placeholder="Enter ZIP Code")

    if st.button("Submit Location"):
        if zip_code:
            lat, lon = get_coordinates_from_zip(zip_code, "MY")  # Hardcoded to Malaysia
            if lat and lon:
                st.session_state.lat, st.session_state.lon = lat, lon
                st.success(f"📍 Using Manual Location: {lat}, {lon}")
            else:
                st.error("❌ Invalid ZIP Code. Please enter a valid Malaysian ZIP Code.")
else:
    # ✅ Automatic Geolocation Mode
    st.subheader("📍 Use Automatic Location")
    geo_data = streamlit_geolocation()

    if geo_data:
        st.session_state.lat = geo_data["latitude"]
        st.session_state.lon = geo_data["longitude"]
        if st.session_state.lat and st.session_state.lon:
            st.success(f"🌍 Location Detected: {st.session_state.lat}, {st.session_state.lon}")

# ✅ Search Button (works for both manual & automatic input)
if st.button("Search Air Quality"):
    if st.session_state.lat is None or st.session_state.lon is None:
        st.warning("⚠️ Please enter a valid ZIP code or enable geolocation.")
    else:
        # ✅ Fetch & Display Air Quality Data
        air_quality = get_air_quality(st.session_state.lat, st.session_state.lon)

        if "error" in air_quality:
            st.error(air_quality["error"])
        else:
            aqi = air_quality["aqi"]
            components = air_quality["components"]

            # Display AQI
            st.write(f"🌿 **Air Quality Index (AQI):** {aqi}")

            # Display air pollutants
            st.subheader("🛑 Air Pollutants (μg/m³)")
            for key, value in components.items():
                st.write(f"- **{key.upper()}:** {value}")

