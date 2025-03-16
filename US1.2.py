import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Air Quality and Asthma Educational Insights", layout="wide")


def get_air_quality_data(city, api_key):
    """Get air quality data from AQICN API"""
    url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "ok":
            return data["data"]
        else:
            st.error(f"Failed to get data: {data['status']}")
            return None
    else:
        st.error(f"Failed to get data: {response.status_code}")
        return None


def get_air_quality_by_geo(lat, lon, api_key):
    """Get air quality data from AQICN API based on coordinates"""
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "ok":
            return data["data"]
        else:
            st.error(f"Failed to get data: {data['status']}")
            return None
    else:
        st.error(f"Failed to get data: {response.status_code}")
        return None


def calculate_air_quality_score(aqi):
    """Calculate air quality score based on AQI using AQICN standards"""
    if aqi <= 50:
        return "Good (0-50)", "Air quality is considered satisfactory, and air pollution poses little or no risk.", "#009966"
    elif aqi <= 100:
        return "Moderate (51-100)", "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.", "#FFDE33"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups (101-150)", "Members of sensitive groups may experience health effects. The general public is less likely to be affected.", "#FF9933"
    elif aqi <= 200:
        return "Unhealthy (151-200)", "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.", "#CC0033"
    elif aqi <= 300:
        return "Very Unhealthy (201-300)", "Health alert: The risk of health effects is increased for everyone.", "#660099"
    else:
        return "Hazardous (300+)", "Health warning of emergency conditions: everyone is more likely to be affected.", "#7E0023"


def get_pollutant_impact(pollutant, value):
    """Get information about how pollutants affect asthma"""
    impacts = {
        "co": {
            "name": "Carbon Monoxide (CO)",
            "impact": "Mild",
            "description": "Carbon monoxide reduces the blood's ability to carry oxygen, which may aggravate symptoms for asthma patients, especially at higher concentrations.",
            "unit": "mg/m³",
            "threshold": {
                "safe": 4.4,  # mg/m³
                "moderate": 9.4,
                "high": 12.4
            }
        },
        "no2": {
            "name": "Nitrogen Dioxide (NO₂)",
            "impact": "Severe",
            "description": "Nitrogen dioxide is a strong asthma trigger that can increase airway inflammation, reduce resistance to respiratory infections, and lead to asthma attacks.",
            "unit": "μg/m³",
            "threshold": {
                "safe": 40,  # μg/m³
                "moderate": 100,
                "high": 200
            }
        },
        "o3": {
            "name": "Ozone (O₃)",
            "impact": "Severe",
            "description": "Ozone is a major trigger for asthma patients, irritating the lungs and causing coughing, chest tightness, and breathing difficulties. Long-term exposure can worsen asthma symptoms.",
            "unit": "μg/m³",
            "threshold": {
                "safe": 100,  # μg/m³
                "moderate": 160,
                "high": 240
            }
        },
        "pm25": {
            "name": "Fine Particulate Matter (PM2.5)",
            "impact": "Severe",
            "description": "PM2.5 is a major asthma trigger. These tiny particles can penetrate deep into the lungs, causing inflammation that can worsen asthma symptoms and potentially trigger attacks.",
            "unit": "μg/m³",
            "threshold": {
                "safe": 12,  # μg/m³
                "moderate": 35,
                "high": 55
            }
        },
        "pm10": {
            "name": "Inhalable Particulate Matter (PM10)",
            "impact": "Moderate",
            "description": "PM10 can cause throat and eye irritation and may trigger asthma attacks, though typically with less impact than PM2.5.",
            "unit": "μg/m³",
            "threshold": {
                "safe": 20,  # μg/m³
                "moderate": 50,
                "high": 150
            }
        },
        "so2": {
            "name": "Sulfur Dioxide (SO₂)",
            "impact": "Moderate",
            "description": "Sulfur dioxide is a known asthma trigger that can cause airway constriction and bronchospasm, particularly affecting those who already have asthma.",
            "unit": "μg/m³",
            "threshold": {
                "safe": 40,  # μg/m³
                "moderate": 125,
                "high": 350
            }
        }
    }

    info = impacts.get(pollutant, {"name": pollutant, "impact": "Unknown", "description": "No information available",
                                   "unit": "μg/m³", "threshold": {"safe": 0, "moderate": 0, "high": 0}})

    # Evaluate severity level
    level = "Safe"
    if value > info["threshold"]["high"]:
        level = "High Risk"
    elif value > info["threshold"]["moderate"]:
        level = "Moderate Risk"
    elif value > info["threshold"]["safe"]:
        level = "Low Risk"

    return info["name"], info["impact"], info["description"], level, info["unit"]


def create_gauge_chart(aqi_value):
    """Create AQI gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Air Quality Index"},
        gauge={
            'axis': {'range': [None, 300], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#009966'},
                {'range': [50, 100], 'color': '#FFDE33'},
                {'range': [100, 150], 'color': '#FF9933'},
                {'range': [150, 200], 'color': '#CC0033'},
                {'range': [200, 300], 'color': '#660099'},
                {'range': [300, 500], 'color': '#7E0023'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': aqi_value
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def main():
    st.title("Air Quality and Asthma Educational Insights")

    st.sidebar.header("Settings")

    # API Key input
    api_key = st.sidebar.text_input("Enter AQICN API Key", type="password")

    # Select input method
    input_method = st.sidebar.radio("Select input method", ["City Name", "GPS Coordinates"])

    # Malaysia main cities
    malaysia_cities = {
        "Kuala Lumpur": "Kuala Lumpur",
        "Johor Bahru": "Johor",
        "Penang": "Perai",
        "Malacca": "Melaka",
        "Kota Kinabalu": "kota-kinabalu",
        "Kuching": "kuching",
        "Ipoh": "ipoh",
        "Shah Alam": "shah-alam"
    }

    if input_method == "City Name":
        selected_city = st.sidebar.selectbox("Select city", list(malaysia_cities.keys()))
        city_code = malaysia_cities[selected_city]
    else:
        lat = st.sidebar.number_input("Latitude", value=3.1390, format="%.4f")
        lon = st.sidebar.number_input("Longitude", value=101.6869, format="%.4f")

    # Get data button
    if st.sidebar.button("Get Air Quality Data") and api_key:
        with st.spinner("Getting data..."):
            if input_method == "City Name":
                air_data = get_air_quality_data(city_code, api_key)
                location_name = selected_city
            else:
                air_data = get_air_quality_by_geo(lat, lon, api_key)
                location_name = f"Coordinates ({lat}, {lon})"

            if air_data:
                # Successfully got data, display results
                st.success(f"Successfully retrieved air quality data for {location_name}")

                # Display station info
                st.subheader("Station Information")
                st.info(f"Data from: {air_data.get('city', {}).get('name', {})}")

                # Display current date time
                time_str = air_data.get('data', {}).get('time', {}).get('s',
                                                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                st.subheader(f"Data updated at: {time_str}")

                # Get AQI
                aqi = air_data.get('aqi', 0)

                # Display air quality score
                st.subheader("Overall Air Quality Score")
                score, description, color = calculate_air_quality_score(aqi)

                col1, col2 = st.columns([1, 2])

                with col1:
                    st.plotly_chart(create_gauge_chart(aqi), use_container_width=True)

                with col2:
                    st.markdown(f"### Score: {score}")
                    st.markdown(f"**{description}**")
                    st.markdown("---")
                    st.markdown("### How the Score is Calculated")
                    st.markdown("""
                    The Air Quality Index is calculated based on the concentration of these pollutants:
                    - PM2.5 (Fine Particulate Matter)
                    - PM10 (Inhalable Particulate Matter)
                    - O₃ (Ozone)
                    - NO₂ (Nitrogen Dioxide)
                    - SO₂ (Sulfur Dioxide)
                    - CO (Carbon Monoxide)

                    AQI Range from 0 to 500+:
                    - 0-50: Good - Air quality is satisfactory, poses little or no risk
                    - 51-100: Moderate - Air quality is acceptable, risk for some sensitive individuals
                    - 101-150: Unhealthy for Sensitive Groups - Members of sensitive groups may experience health effects
                    - 151-200: Unhealthy - General public may experience health effects, sensitive groups more serious effects
                    - 201-300: Very Unhealthy - Health alert, risk increased for everyone
                    - 300+: Hazardous - Health warnings of emergency conditions, entire population affected
                    """)

                # Display main pollutant - MODIFIED SECTION
                st.subheader("Main Pollutant")

                # Extract pollutant data
                pollutants = {}
                iaqi = air_data.get('iaqi', {})
                for key in ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']:
                    if key in iaqi:
                        pollutants[key] = iaqi[key].get('v', 0)

                if pollutants:
                    highest_pollutant = max(pollutants.items(), key=lambda x: x[1])
                    pollutant_name, value = highest_pollutant

                    name, impact, description, level, unit = get_pollutant_impact(pollutant_name, value)

                    level_color = {
                        "High Risk": "red",
                        "Moderate Risk": "orange",
                        "Low Risk": "blue",
                        "Safe": "green"
                    }.get(level, "gray")

                    st.markdown(f"### Main pollutant: {name}")
                    st.markdown(f"**Current concentration:** {value} {unit} - <span style='color:{level_color};'>**{level}**</span>",
                                unsafe_allow_html=True)
                    st.markdown(f"**Impact on Asthma::** {impact}")
                    st.markdown(f"**Detailed information:** {description}")
                else:
                    st.warning("No pollutant data available for this location")

                # Display pollutant effects on asthma
                st.subheader("Pollutant Effects on Asthma")

                pollutant_data = []
                for pollutant, value in pollutants.items():
                    name, impact, description, level, unit = get_pollutant_impact(pollutant, value)
                    pollutant_data.append({
                        "Name": name,
                        "Concentration": f"{value} {unit}",
                        "Impact on Asthma": impact,
                        "Current Level": level,
                        "Details": description
                    })

                # Sort pollutants by impact severity
                impact_levels = {"Severe": 3, "Moderate": 2, "Mild": 1, "Unknown": 0}
                pollutant_data.sort(key=lambda x: impact_levels.get(x["Impact on Asthma"], 0), reverse=True)

                # Use colors to represent different risk levels
                for item in pollutant_data:
                    col = st.columns([1, 4])[1]
                    with col:
                        if item["Impact on Asthma"] == "Severe":
                            color = "red"
                        elif item["Impact on Asthma"] == "Moderate":
                            color = "orange"
                        elif item["Impact on Asthma"] == "Mild":
                            color = "blue"
                        else:
                            color = "gray"

                        level_color = {
                            "High Risk": "red",
                            "Moderate Risk": "orange",
                            "Low Risk": "blue",
                            "Safe": "green"
                        }.get(item["Current Level"], "gray")

                        st.markdown(
                            f"### {item['Name']} - <span style='color:{color};'>**{item['Impact on Asthma']} Impact**</span>",
                            unsafe_allow_html=True)
                        st.markdown(
                            f"**Current concentration:** {item['Concentration']} - <span style='color:{level_color};'>**{item['Current Level']}**</span>",
                            unsafe_allow_html=True)
                        st.markdown(f"**Details:** {item['Details']}")
                        st.markdown("---")

                        # Provide recommendations based on air quality
                st.subheader("Asthma Management Recommendations")
                if aqi <= 100:
                    st.success("""
                                                ✅ Current air quality is suitable for most asthma patients:
                                                - Outdoor activities are generally safe
                                                - Continue using preventive medications as prescribed
                                                - Stay vigilant and carry rescue medication
                                                """)
                elif aqi <= 150:
                        st.warning("""
                                                ⚠️ Moderate air quality risk:
                                                - Sensitive individuals should consider reducing strenuous outdoor activities
                                                - Carry rescue medication when going outdoors
                                                - Monitor for any changes in symptoms
                                                - Consider keeping windows closed and using air purifiers
                                                """)
                else:
                        st.error("""
                                                🚨 High air quality risk:
                                                - Avoid outdoor activities
                                                - Keep windows closed and use air purifiers
                                                - Strictly follow your asthma management plan
                                                - Seek medical attention if symptoms worsen
                                                """)
            else:
                    st.error("Could not retrieve air quality data. Please check your API key and location information.")
    else:
                if not api_key and st.sidebar.button("Get Air Quality Data"):
                    st.warning("Please enter your AQICN API key")

                # Display app information
                st.info("""
                                    ### Malaysia Air Quality and Asthma Educational Insights

                                    This application provides real-time air quality data and shows its impact on asthma patients.

                                    **Features:**
                                    - View real-time Air Quality Index (AQI) and detailed scores
                                    - Understand how different pollutants affect asthma
                                    - Get asthma management recommendations based on current air quality

                                    **How to use:**
                                    1. Enter your AQICN API key in the left menu
                                    2. Select a Malaysian city or enter custom coordinates
                                    3. Click the "Get Air Quality Data" button
                                    """)

                # Display educational information about air quality and asthma
                st.subheader("Relationship Between Air Quality and Asthma")
                st.markdown("""
                                    Air pollution is one of the major triggers for asthma. The following pollutants significantly impact asthma patients:

                                    - **Fine Particulate Matter (PM2.5)**: These tiny particles can penetrate deep into the lungs, causing inflammatory responses and are one of the primary triggers for asthma.
                                    - **Ozone (O₃)**: Ground-level ozone is created by sunlight reacting with pollutants from vehicle exhaust and other sources. It irritates the airways and can worsen asthma symptoms.
                                    - **Nitrogen Dioxide (NO₂)**: Mainly from vehicle exhaust and industrial emissions, it increases airway inflammation and reduces resistance to respiratory infections.
                                    - **Sulfur Dioxide (SO₂)**: An industrial pollutant that can cause airway constriction and bronchospasm.

                                    Research shows that on days with poor air quality, there is a significant increase in asthma-related emergency room visits and hospitalizations.
                                    """)

if __name__ == "__main__":
    main()