import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from backend import get_coordinates_from_zip, get_air_quality


def main():
    st.Title("Real Time Air Quality Checker")

    if "lat" not in st.session_state and "lon" not in st.session_state:
        st.session_state.lat = None
        st.session_state.lon = None

    