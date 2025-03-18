import streamlit as st
import requests
import pandas as pd
import json

st.markdown("""
<style>
    /* Card styling with theme-compatible colors */
    .card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    /* Strong contrast for metric values */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: var(--text-color, inherit) !important;
    }
    /* Semi-strong contrast for labels */
    .metric-label {
        font-size: 1rem;
        text-align: center;
        color: var(--text-color, inherit) !important;
        opacity: 0.8;
    }
    /* Header with border that respects theme colors */
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary-color, #0D47A1);
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-color, #E3F2FD);
    }
    /* Info box that maintains contrast in dark and light themes */
    .info-box {
        background-color: rgba(30, 136, 229, 0.1);
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid var(--primary-color, #1E88E5);
        margin-bottom: 1rem;
        color: var(--text-color, inherit) !important;
    }
    /* Ensure all text has appropriate contrast */
    p, span, div {
        color: var(--text-color, inherit) !important;
    }
</style>
""", unsafe_allow_html=True)

IQAIR_API_KEY = '6f342030-31eb-471b-966d-5294dc20af55'
OPENWEATHER_API_KEY = '02e0050a1354c6262cc263e7883b132f'


def get_air_quality_data(city, state, country):
    """
    Get air quality data from IQAir API for a specified location
    """
    url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={IQAIR_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to get data from IQAir: {response.status_code} - {response.text}")
        return None


def get_openweather_pollution_data(lat, lon):
    """
    Get detailed pollution data from OpenWeather API
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to get data from OpenWeather: {response.status_code} - {response.text}")
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

    # Sidebar - User Input
    st.sidebar.header("Location Settings")

    country = st.sidebar.selectbox("Country", ["Malaysia"], index=0)

    # Major states in Malaysia
    states = ["Kuala Lumpur", "Selangor", "Johor", "Penang", "Sabah", "Sarawak", "Melaka", "Perak", "Pahang"]
    state = st.sidebar.selectbox("State/Region", states)

    # Provide city options based on state
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


    # When user clicks to get data
    if st.sidebar.button("Get Air Quality Data"):
        if city != "Select a city":
            with st.spinner("Getting data..."):
                iqair_data = get_air_quality_data(city, state, country)

                if iqair_data and iqair_data['status'] == 'success':
                    # Get coordinates from IQAir data for OpenWeather API
                    lat = iqair_data['data']['location']['coordinates'][1]
                    lon = iqair_data['data']['location']['coordinates'][0]

                    # Get OpenWeather pollution data
                    openweather_data = get_openweather_pollution_data(lat, lon)

                    if openweather_data:
                        # Store both datasets for use in other parts of the page
                        st.session_state.air_data = iqair_data
                        st.session_state.pollutants_data = openweather_data
                        st.success("Data retrieved successfully!")
                    else:
                        st.error("Couldn't retrieve pollution data from OpenWeather API.")
                else:
                    st.error("Couldn't retrieve data from IQAir. Please check location and API key.")
        else:
            st.error("Please ensure both API keys are provided and a city is selected.")

    # Main content area - Display educational insights
    if 'air_data' in st.session_state and 'pollutants_data' in st.session_state:
        display_educational_insights(st.session_state.air_data, st.session_state.pollutants_data)


def display_educational_insights(iqair_data, openweather_data):
    """
    Display educational insights about air quality and asthma
    """
    st.markdown('<div class="sub-header">Educational Insights on Air Quality and Asthma</div>', unsafe_allow_html=True)

    pollution_data = iqair_data['data']['current']['pollution']
    weather_data = iqair_data['data']['current']['weather']

    # Display location information - removed inline styling that affected text color
    st.markdown(f"""
        <style>
            .location-info {{
                font-size: 12px;  
                font-weight: bold;  
            }}
        </style>
        <p class="location-info">Location: {iqair_data['data']['city']}, {iqair_data['data']['state']}, {iqair_data['data']['country']}</p>
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

    # Create a better AQI visualization - fixed text contrasts
    aqi_percentage = min(aqi_us / 500, 1.0)

    # Custom AQI gauge visualization with high-contrast text
    st.markdown(f"""
    <div class="card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.2rem; font-weight: 500;">AQI Level: {aqi_us} - {aqi_category}</div>
        </div>
        <div style="height: 25px; width: 100%; background-color: rgba(240, 240, 240, 0.2); border-radius: 15px; overflow: hidden;">
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

    # Better weather display with theme-compatible colors
    weather_cols = st.columns(3)
    with weather_cols[0]:
        st.markdown(f"""
        <div class="card">
            <div style="text-align: center;">
                <div style="font-size: 1rem;">Temperature</div>
                <div style="font-size: 2rem; font-weight: 600;">{weather_data['tp']}°C</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with weather_cols[1]:
        st.markdown(f"""
        <div class="card">
            <div style="text-align: center;">
                <div style="font-size: 1rem;">Humidity</div>
                <div style="font-size: 2rem; font-weight: 600;">{weather_data['hu']}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with weather_cols[2]:
        st.markdown(f"""
        <div class="card">
            <div style="text-align: center;">
                <div style="font-size: 1rem;">Wind Speed</div>
                <div style="font-size: 2rem; font-weight: 600;">{weather_data['ws']} m/s</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Extract pollutant concentrations from OpenWeather API
    if 'list' in openweather_data and len(openweather_data['list']) > 0:
        components = openweather_data['list'][0]['components']

        # Display detailed pollutant information
        st.markdown('<div class="sub-header">Detailed Pollutant Information</div>', unsafe_allow_html=True)

        # Define pollutant units and safe levels
        pollutant_info = {
            "co": {"name": "Carbon Monoxide (CO)", "unit": "μg/m³", "safe_level": 10000},
            "no": {"name": "Nitric Oxide (NO)", "unit": "μg/m³", "safe_level": 30},
            "no2": {"name": "Nitrogen Dioxide (NO₂)", "unit": "μg/m³", "safe_level": 40},
            "o3": {"name": "Ozone (O₃)", "unit": "μg/m³", "safe_level": 100},
            "so2": {"name": "Sulfur Dioxide (SO₂)", "unit": "μg/m³", "safe_level": 20},
            "pm2_5": {"name": "PM2.5", "unit": "μg/m³", "safe_level": 10},
            "pm10": {"name": "PM10", "unit": "μg/m³", "safe_level": 20},
            "nh3": {"name": "Ammonia (NH₃)", "unit": "μg/m³", "safe_level": 100}
        }

        # Create pollutant data without progress bars
        pollutant_data = []

        for key, value in components.items():
            if key in pollutant_info:
                safe_level = pollutant_info[key]["safe_level"]
                pollutant_data.append({
                    "pollutant": key,
                    "name": pollutant_info[key]["name"],
                    "value": value,
                    "unit": pollutant_info[key]["unit"],
                    "safe_level": safe_level
                })

        # Display pollutants in a grid with theme-compatible cards
        cols = st.columns(2)
        for i, pollutant in enumerate(pollutant_data):
            col_index = i % 2
            with cols[col_index]:
                st.markdown(f"""
                <div class="card">
                    <div style="text-align: center;">
                        <div style="font-size: 1rem;">{pollutant["name"]}</div>
                        <div style="font-size: 1.5rem; font-weight: 600;">{pollutant["value"]} {pollutant["unit"]}</div>
                    </div>
                    <div style="margin-top: 0.5rem;">
                        <div style="font-size: 0.8rem;">Safe level: {pollutant["safe_level"]} {pollutant["unit"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Main pollutant information
        st.markdown('<div class="sub-header">Main Pollutant Information</div>', unsafe_allow_html=True)

        pollutant_code_map = {
            "p1": "pm10",
            "p2": "pm2_5",
            "o3": "o3",
            "n2": "no2",
            "s2": "so2",
            "co": "co"
        }

        main_pollutant_code = pollutant_code_map.get(main_pollutant_us, "pm2_5")

        effects = {
            "pm10": "PM10 particles can enter the lungs, irritate and damage lung tissue, and worsen asthma symptoms. These particles typically come from dust, pollen, and mold.",
            "pm2_5": "PM2.5 is one of the most dangerous air pollutants. These tiny particles can penetrate deep into lungs and bloodstream, causing severe asthma attacks and other respiratory problems.",
            "o3": "Ozone irritates lung tissues, decreases lung function, and increases the frequency and severity of asthma attacks. It can make asthma patients more sensitive to allergens.",
            "no2": "Nitrogen dioxide irritates airways, causing inflammation, reducing resistance to respiratory infections, and particularly affects children with asthma.",
            "so2": "Sulfur dioxide irritates the eyes, nose, and throat, potentially triggering asthma attacks and other respiratory problems, especially in people with existing asthma.",
            "co": "Carbon monoxide reduces the blood's ability to carry oxygen, potentially worsening symptoms in asthma patients, especially those with pre-existing cardiovascular conditions."
        }

        mitigation = {
            "pm10": "On days with high PM10 levels, minimize outdoor activities, keep indoor air fresh, and use air purifiers.",
            "pm2_5": "Use high-efficiency air purifiers, keep windows and doors closed, reduce outdoor activities, especially in areas with heavy traffic.",
            "o3": "Avoid outdoor activities during afternoons and evenings when ozone levels are highest, especially intense exercise.",
            "no2": "Avoid areas with heavy traffic, maintain indoor air circulation (unless outdoor pollution is severe), and reduce use of gas appliances.",
            "so2": "In areas with high sulfur dioxide, limit outdoor time, use air purifiers, and maintain adequate hydration.",
            "co": "Ensure gas appliances are working properly, install carbon monoxide detectors, and maintain good ventilation."
        }

        main_pollutant_full = get_pollutant_full_name(main_pollutant_us)
        main_pollutant_value = components.get(main_pollutant_code, "N/A")
        main_pollutant_unit = pollutant_info.get(main_pollutant_code, {}).get("unit", "μg/m³")

        st.markdown(f"""
            <div class="info-box">
                <h3 style="font-size: 16px;">Current Main Pollutant: {main_pollutant_full} - {main_pollutant_value} {main_pollutant_unit}</h3>
                <p>{effects.get(main_pollutant_code, "No information available for this pollutant")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sub-header">How to Reduce Risk</div>', unsafe_allow_html=True)
        st.write(mitigation.get(main_pollutant_code, "No mitigation information available for this pollutant"))

        # All pollutants and their impact on asthma
        with st.expander("Learn About All Pollutants and Their Impact on Asthma"):
            # Use Streamlit's table functionality instead of matplotlib
            pollutant_data = []
            for code, info in pollutant_info.items():
                if code in components:
                    pollutant_data.append({
                        "Pollutant": info["name"],
                        "Current Level": f"{components[code]} {info['unit']}",
                        "Safe Level": f"{info['safe_level']} {info['unit']}",
                        "Impact on Asthma": effects.get(code, "No information available"),
                        "Mitigation Measures": mitigation.get(code, "No information available")
                    })

            df = pd.DataFrame(pollutant_data)
            st.dataframe(df, use_container_width=True)

    else:
        st.error("No detailed pollutant data available from OpenWeather API.")

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


def get_level_color(value, safe_level):
    """
    Get color based on pollutant level compared to safe level
    """
    percentage = (value / safe_level) * 100

    if percentage <= 50:
        return "#00E400"  # Green
    elif percentage <= 100:
        return "#FFFF00"  # Yellow
    elif percentage <= 150:
        return "#FF7E00"  # Orange
    elif percentage <= 200:
        return "#FF0000"  # Red
    else:
        return "#8F3F97"  # Purple


if __name__ == "__main__":
    main()

main()