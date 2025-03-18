import requests
from API.api_key import iqair_key,open_weather
from geopy.geocoders import Nominatim




# Get Air Qualit Index First






#def get_coordinates_from_zip(zip_code, country_code):
#    """Converts ZIP + country code to latitude & longitude using OpenStreetMap's Nominatim."""
#    geolocator = Nominatim(user_agent="geoapi")
#    location = geolocator.geocode(f"{zip_code}, {country_code}",timeout=5)

#    if location:
#        return location.latitude, location.longitude
#    return None, None

# def get_coordiantes_from_city_state(city,state):
#     geolocator = Nominatim(user_agent="geoapi")
#     location = geolocator.geocode(city,timeout=5)

#     if location:
#         return location.latitude, location.longitude
#     return None, None




def aqi_and_components(lat,lng):
    aqi = getting_aqi(lat,lng)
    components = getting_components(lat,lng)
    return aqi,components

def getting_aqi(lat,lng):
    iqair_url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lng}&key={iqair_key}"
    try:

        response = requests.get(iqair_url)
        if response.status_code != 200:
            return {"error":f"❌ API Error {response.status_code}:{response.json().get('message', 'Unknown Error')}"}
        data = response.json()

        if not data['data']:
            return "⚠️ No air quality data available for this location."
        data = data['data']
        city = data['city']
        state = data['state']
        aqi = data['current']['pollution']['aqius']
        main_pollutant = data['current']['pollution']['mainus']
        weather = data['current']['weather']
        return {
            'city':city,
            'state':state,
            'aqi':aqi,
            'main_pollutant':main_pollutant,
            'weather':weather
        }
    except requests.exceptions.RequestException as e:
        return {"error":f"🚨 Network Error: {str(e)}"}
    
    except requests.exceptions.Timeout:
        return {"error":"⏳ Request timed out. Please try again."}

def getting_components(lat,lng):
    try:
        openweather_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lng}&appid={open_weather}"
        response = requests.get(openweather_url)
        if response.status_code != 200:
            return {"error":f"❌ API Error {response.status_code}:{response.json().get('message', 'Unknown Error')}"}
        data = response.json()

        if not data['list']:
            return "⚠️ No air quality data available for this location."
        components = data['list'][0]['components']
        return components       
    except requests.exceptions.RequestException as e:
        return {"error":f"🚨 Network Error: {str(e)}"}
    
    except requests.exceptions.Timeout:
        return {"error":"⏳ Request timed out. Please try again."}
