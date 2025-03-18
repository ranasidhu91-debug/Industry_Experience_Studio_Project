import streamlit as st
from backend import aqi_and_components
from streamlit_js_eval import get_geolocation
from accessory_functions import *
from educational_insight import display_educational_insights
from aqi_map import display_aqi_map

@st.cache_data
def cached_get_locations():
    """Caches location retrieval to avoid recomputation."""
    return getting_locations()

@st.cache_data
def cached_get_air_quality_data(lat, lng):
    """Caches AQI data for a given location to minimize API calls."""
    return aqi_and_components(lat, lng)

# Apply custom CSS for the selected UI elements
st.markdown("""
<style>
    .card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
    }
    .metric-label {
        font-size: 1rem;
        color: #616161;
        text-align: center;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #0D47A1;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E3F2FD;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)



def main():
    st.title("Air Quality and Asthma Educational Insights")

    # Sidebar - User Input
    st.sidebar.header("Location Settings")

    # Toggle between auto-location and manual selection
    use_auto_location = st.sidebar.checkbox("Use My Location", value=False)

    coord, states, city_options = cached_get_locations()

    city = "Select a city"

    if use_auto_location:
    # if st.sidebar.button('Use My Location'):
        #location = streamlit_geolocation()
        location = get_geolocation()
        if location:
            lat,lng = location['coords']['latitude'],location['coords']['longitude']
            #lat, lng = location["latitude"], location["longitude"]
            st.session_state.auto_location = (lat, lng)
            #st.success(f"Detected Location: {lat}, {lng}")
    # else:
    #     st.warning("Unable to detect location. Please enable location services or select manually.")

    else:
        # Manual selection
        state = st.sidebar.selectbox("State/Region", states)
        default_city_options = ["Select a city"]
        city = st.sidebar.selectbox("City", city_options.get(state, default_city_options))

    # When user clicks to get data
    if st.sidebar.button("Get Air Quality Data"):
        with st.spinner("Getting data..."):
            if use_auto_location and "auto_location" in st.session_state:
            #if "auto_location" in st.session_state:
                lat, lng = st.session_state.auto_location
            elif 'city' in locals() and city != "Select a city":
                lat, lng = coord[state][city]['Latitude'], coord[state][city]['Longitude']
                st.session_state.manual_location = (lat,lng)
            else:
                st.error("Please Select a Location.")
                return

            aqi, components = cached_get_air_quality_data(lat,lng)
            if aqi and components:
                st.session_state.aqi_data = aqi
                st.session_state.components_data = components
                st.session_state.location = (lat,lng)
                st.session_state.map_updated = True
            else:
                st.error('No data available')

    # Main content area - Display educational insights
    if 'aqi_data' in st.session_state and 'components_data' in st.session_state and 'location' in st.session_state:
        display_educational_insights(st.session_state.aqi_data, st.session_state.components_data)
        display_aqi_map(st.session_state.location, st.session_state.aqi_data)


if __name__ == "__main__":
    main()

main()