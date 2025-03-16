import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from backend import get_coordinates_from_zip, get_air_quality

st.title("Real-Time Air Quality Checker")

# ✅ Initialize session state for storing location
if "lat" not in st.session_state:
    st.session_state.lat = None
    st.session_state.lon = None

# ✅ Always show manual input fields
st.subheader("🔴 Enter your location manually OR click the 'Get Location' button")
zip_code = st.text_input("ZIP Code", placeholder="Enter ZIP Code", key="zip")
country_code = st.text_input("Country Code", placeholder="Enter Country Code (e.g., US, MY)", key="country")

# ✅ Geolocation Button
st.subheader("📍 OR Use Current Location")
#location = st.button("Get My Location")

geo_data = streamlit_geolocation()

# ✅ If location button is clicked, fetch location
    #geo_data = streamlit_geolocation()
if geo_data:
    st.session_state.lat = geo_data["latitude"]
    st.session_state.lon = geo_data["longitude"]
    st.success(f"🌍 Location Detected: {st.session_state.lat}, {st.session_state.lon}")

# ✅ Search Button (for both manual & auto location input)
if st.button("Search Air Quality"):
    # ✅ If manual input is provided, convert ZIP & Country to coordinates
    if zip_code and country_code:
        lat, lon = get_coordinates_from_zip(zip_code, country_code)
        if lat and lon:
            st.session_state.lat, st.session_state.lon = lat, lon
            st.success(f"📍 Using Manual Location: {lat}, {lon}")
        else:
            st.error("❌ Invalid ZIP or Country. Please enter a valid location.")

    # ✅ If no valid location, show error
    if st.session_state.lat is None or st.session_state.lon is None:
        st.warning("⚠️ Please enter a valid ZIP code & country or allow geolocation.")
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