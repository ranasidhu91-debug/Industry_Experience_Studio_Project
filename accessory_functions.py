import pandas as pd
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
    

def getting_locations():
    locations = pd.read_csv("cities_with_lat_lon.csv").drop(columns=['Unnamed: 0'])
    state_cities_coord = locations.groupby('State').apply(lambda x: x.set_index('City').to_dict(orient='index'), include_groups=False).to_dict()
    states = locations['State'].unique().tolist()
    state_cities = locations.groupby('State')['City'].apply(list).to_dict()
    return state_cities_coord,states,state_cities
