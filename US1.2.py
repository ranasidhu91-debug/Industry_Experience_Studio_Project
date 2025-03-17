import streamlit as st
import requests
import pandas as pd
import json


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


def get_air_quality_data(api_key, city, state, country):
    """
    Get air quality data from IQAir API for a specified location
    """
    url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to get data: {response.status_code} - {response.text}")
        return None


def calculate_asthma_risk_score(aqi):
    """
    Calculate asthma risk score based on AQI
    """
    if aqi <= 50:
        return 1, "Low Risk"
    elif aqi <= 100:
        return 2, "Low-Moderate Risk"
    elif aqi <= 150:
        return 3, "Moderate Risk"
    elif aqi <= 200:
        return 4, "High-Moderate Risk"
    else:
        return 5, "High Risk"


def get_aqi_category(aqi):
    """
    Get air quality category based on AQI value
    """
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def get_aqi_color(aqi):
    """
    Get color for AQI visualization
    """
    if aqi <= 50:
        return "#00E400"  # Green
    elif aqi <= 100:
        return "#FFFF00"  # Yellow
    elif aqi <= 150:
        return "#FF7E00"  # Orange
    elif aqi <= 200:
        return "#FF0000"  # Red
    elif aqi <= 300:
        return "#8F3F97"  # Purple
    else:
        return "#7E0023"  # Maroon


def main():
    st.title("Air Quality and Asthma Educational Insights")

    default_api_key = '6f342030-31eb-471b-966d-5294dc20af55'
    # Sidebar - User Input
    st.sidebar.header("Location Settings")

    country = st.sidebar.selectbox("Country", ["Malaysia"], index=0)

    # Major states in Malaysia - Adding the missing states
    states = ["Kuala Lumpur", "Selangor", "Johor", "Penang", "Sabah", "Sarawak", "Melaka", "Perak", "Pahang"]
    state = st.sidebar.selectbox("State/Region", states)

    # Provide city options based on state - ensure all states from the dropdown are included here
    city_options = {
        "Kuala Lumpur": ["Kuala Lumpur"],
        "Selangor": ["Shah Alam", "Petaling Jaya"],
        "Johor": ["Johor Bahru"],
        "Penang": ["George Town"],
        "Sabah": ["Kota Kinabalu", "Sandakan"],
        "Sarawak": ["Kuching", "Sibu"],
        "Melaka": ["Melaka"],
        "Perak": ["Ipoh"],
        "Pahang": ["Kuantan"]
    }

    # Ensure default city options for all states, even if not explicitly defined
    default_city_options = ["Select a city"]
    city = st.sidebar.selectbox("City", city_options.get(state, default_city_options))

    api_key = default_api_key

    # When user clicks to get data
    if st.sidebar.button("Get Air Quality Data"):
        if api_key and city != "Select a city":
            with st.spinner("Getting data..."):
                data = get_air_quality_data(api_key, city, state, country)

                if data and data['status'] == 'success':
                    # Store data for use in other parts of the page
                    st.session_state.air_data = data
                    st.success("Data retrieved successfully!")
                else:
                    st.error("Couldn't retrieve data. Please check location and API key.")

    # Main content area - Display educational insights
    if 'air_data' in st.session_state:
        display_educational_insights(st.session_state.air_data)


def display_educational_insights(data):
    """
    Display educational insights about air quality and asthma
    """
    st.markdown('<div class="sub-header">Educational Insights on Air Quality and Asthma</div>', unsafe_allow_html=True)

    pollution_data = data['data']['current']['pollution']
    weather_data = data['data']['current']['weather']

    # Display location information
    st.markdown(f"""
        <style>
            .location-info {{
                font-size: 12px;  
                font-weight: bold;  
            }}
        </style>
        <p class="location-info">Location: {data['data']['city']}, {data['data']['state']}, {data['data']['country']}</p>
        """, unsafe_allow_html=True)

    # AQI scores and explanation
    aqi_us = pollution_data['aqius']
    aqi_cn = pollution_data['aqicn']
    main_pollutant_us = pollution_data['mainus']
    main_pollutant_cn = pollution_data['maincn']

    risk_score, risk_level = calculate_asthma_risk_score(aqi_us)
    aqi_color = get_aqi_color(aqi_us)
    aqi_category = get_aqi_category(aqi_us)


    # Use a wider layout to prevent text truncation
    col1, col2 = st.columns([1, 1])

    with col1:
        st.metric("US AQI", aqi_us)
        st.write(f"**Main Pollutant (US):** {get_pollutant_full_name(main_pollutant_us)}")

    with col2:
        st.metric("Asthma Risk Score", f"{risk_score}/5")
        st.write(f"**Risk Level:** {risk_level}")

    # Air Quality Visualization
    st.markdown('<div class="sub-header">Air Quality Visualization</div>', unsafe_allow_html=True)

    # Create a better AQI visualization
    aqi_percentage = min(aqi_us / 500, 1.0)

    # Custom AQI gauge visualization
    st.markdown(f"""
    <div class="card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.2rem; font-weight: 500;">AQI Level: {aqi_us} - {aqi_category}</div>
        </div>
        <div style="height: 25px; width: 100%; background-color: #f0f0f0; border-radius: 15px; overflow: hidden;">
            <div style="height: 100%; width: {aqi_percentage * 100}%; background-color: {aqi_color}; border-radius: 15px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
            <span style="font-size: 0.8rem;">0 - Good</span>
            <span style="font-size: 0.8rem;">100 - Moderate</span>
            <span style="font-size: 0.8rem;">200 - Unhealthy</span>
            <span style="font-size: 0.8rem;">300+ - Hazardous</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Weather information
    st.markdown('<div class="sub-header">Current Weather Conditions</div>', unsafe_allow_html=True)

    # Better weather display
    weather_cols = st.columns(3)
    with weather_cols[0]:
        st.markdown(f"""
        <div class="card">
            <div style="text-align: center;">
                <div style="font-size: 1rem; color: #616161;">Temperature</div>
                <div style="font-size: 2rem; font-weight: 600;">{weather_data['tp']}°C</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with weather_cols[1]:
        st.markdown(f"""
        <div class="card">
            <div style="text-align: center;">
                <div style="font-size: 1rem; color: #616161;">Humidity</div>
                <div style="font-size: 2rem; font-weight: 600;">{weather_data['hu']}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with weather_cols[2]:
        st.markdown(f"""
        <div class="card">
            <div style="text-align: center;">
                <div style="font-size: 1rem; color: #616161;">Wind Speed</div>
                <div style="font-size: 2rem; font-weight: 600;">{weather_data['ws']} m/s</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main pollutant information
    st.markdown('<div class="sub-header">Main Pollutant Information</div>', unsafe_allow_html=True)

    pollutants = {
        "p1": "PM10",
        "p2": "PM2.5",
        "o3": "Ozone (O₃)",
        "n2": "Nitrogen Dioxide (NO₂)",
        "s2": "Sulfur Dioxide (SO₂)",
        "co": "Carbon Monoxide (CO)"
    }

    effects = {
        "p1": "PM10 particles can enter the lungs, irritate and damage lung tissue, and worsen asthma symptoms. These particles typically come from dust, pollen, and mold.",
        "p2": "PM2.5 is one of the most dangerous air pollutants. These tiny particles can penetrate deep into lungs and bloodstream, causing severe asthma attacks and other respiratory problems.",
        "o3": "Ozone irritates lung tissues, decreases lung function, and increases the frequency and severity of asthma attacks. It can make asthma patients more sensitive to allergens.",
        "n2": "Nitrogen dioxide irritates airways, causing inflammation, reducing resistance to respiratory infections, and particularly affects children with asthma.",
        "s2": "Sulfur dioxide irritates the eyes, nose, and throat, potentially triggering asthma attacks and other respiratory problems, especially in people with existing asthma.",
        "co": "Carbon monoxide reduces the blood's ability to carry oxygen, potentially worsening symptoms in asthma patients, especially those with pre-existing cardiovascular conditions."
    }

    mitigation = {
        "p1": "On days with high PM10 levels, minimize outdoor activities, keep indoor air fresh, and use air purifiers.",
        "p2": "Use high-efficiency air purifiers, keep windows and doors closed, reduce outdoor activities, especially in areas with heavy traffic.",
        "o3": "Avoid outdoor activities during afternoons and evenings when ozone levels are highest, especially intense exercise.",
        "n2": "Avoid areas with heavy traffic, maintain indoor air circulation (unless outdoor pollution is severe), and reduce use of gas appliances.",
        "s2": "In areas with high sulfur dioxide, limit outdoor time, use air purifiers, and maintain adequate hydration.",
        "co": "Ensure gas appliances are working properly, install carbon monoxide detectors, and maintain good ventilation."
    }

    main_pollutant_full = get_pollutant_full_name(main_pollutant_us)

    st.markdown(f"""
        <style>
            .info-box h3 {{
                font-size: 16px;  /* 调整 h3 字体大小 */
            }}
        </style>
        <div class="info-box">
            <h3>Current Main Pollutant: {main_pollutant_full}</h3>
            <p>{effects.get(main_pollutant_us, "No information available for this pollutant")}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sub-header">How to Reduce Risk</div>', unsafe_allow_html=True)
    st.write(mitigation.get(main_pollutant_us, "No mitigation information available for this pollutant"))

    # All pollutants and their impact on asthma
    with st.expander("Learn About All Pollutants and Their Impact on Asthma"):
        # Use Streamlit's table functionality instead of matplotlib
        pollutant_data = []
        for code, name in pollutants.items():
            pollutant_data.append({
                "Pollutant": name,
                "Impact on Asthma": effects.get(code, "No information available"),
                "Mitigation Measures": mitigation.get(code, "No information available")
            })

        df = pd.DataFrame(pollutant_data)
        st.dataframe(df, use_container_width=True)

    # Explanation of how AQI scores are calculated
    with st.expander("Learn How AQI Scores Are Calculated"):
        st.write("""
            **Air Quality Index (AQI) Calculation Method:**

            The Air Quality Index is calculated based on the concentration of different pollutants, typically including:
            - PM2.5 (Fine Particulate Matter)
            - PM10 (Inhalable Particulate Matter)
            - O₃ (Ozone)
            - NO₂ (Nitrogen Dioxide)
            - SO₂ (Sulfur Dioxide)
            - CO (Carbon Monoxide)

            Each pollutant has a sub-index, and the final AQI is the maximum of these sub-indices. The US AQI and China AQI use different calculation standards, which is why they differ.
            """)

        # Use Streamlit table to display AQI levels
        aqi_levels = [
            {"AQI Range": "0-50", "Level": "Good",
             "Health Impact": "Air quality is satisfactory, and air pollution poses little or no risk",
             "Asthma Risk": "Low"},
            {"AQI Range": "51-100", "Level": "Moderate",
             "Health Impact": "Acceptable air quality, but some pollutants may be a concern for a very small number of sensitive individuals",
             "Asthma Risk": "Low-Moderate"},
            {"AQI Range": "101-150", "Level": "Unhealthy for Sensitive Groups",
             "Health Impact": "May affect the health of sensitive groups", "Asthma Risk": "Moderate"},
            {"AQI Range": "151-200", "Level": "Unhealthy",
             "Health Impact": "Everyone may begin to experience health effects", "Asthma Risk": "High-Moderate"},
            {"AQI Range": "201-300", "Level": "Very Unhealthy",
             "Health Impact": "Health warnings, everyone may experience more serious health effects",
             "Asthma Risk": "High"},
            {"AQI Range": "301+", "Level": "Hazardous",
             "Health Impact": "Health alert, everyone may experience serious health effects",
             "Asthma Risk": "Very High"}
        ]

        st.table(pd.DataFrame(aqi_levels))

    # Asthma coping recommendations
    st.markdown('<div class="sub-header">Recommendations for Asthma Patients</div>', unsafe_allow_html=True)

    if risk_score <= 2:
        st.success("""
            **Recommendations for Low Risk Days:**
            - Carry on with normal daily activities
            - Carry rescue medication with you
            - Use controller medications as prescribed
            - Maintain fresh indoor air quality
            """)
    elif risk_score == 3:
        st.warning("""
            **Recommendations for Moderate Risk Days:**
            - Reduce prolonged outdoor activities
            - Avoid intense outdoor exercise
            - Monitor for changes in symptoms
            - Ensure rescue medications are readily available
            - Use air purifiers to improve indoor air quality
            """)
    else:
        st.error("""
            **Recommendations for High Risk Days:**
            - Stay indoors whenever possible
            - Keep windows and doors closed, use air purifiers
            - Avoid outdoor activities
            - Closely monitor symptoms
            - Follow medical advice to adjust medication if symptoms worsen
            - Consider wearing an N95 mask when outdoors
            """)



def get_pollutant_full_name(code):
    """
    Get the full name of a pollutant
    """
    pollutants = {
        "p1": "PM10 (Inhalable Particulate Matter)",
        "p2": "PM2.5 (Fine Particulate Matter)",
        "o3": "Ozone (O₃)",
        "n2": "Nitrogen Dioxide (NO₂)",
        "s2": "Sulfur Dioxide (SO₂)",
        "co": "Carbon Monoxide (CO)"
    }
    return pollutants.get(code, code)


if __name__ == "__main__":
    main()
