import requests
from API.api_key import openWeather_key
from geopy.geocoders import Nominatim

def get_coordinates_from_zip(zip_code, country_code):
    """Converts ZIP + country code to latitude & longitude using OpenStreetMap's Nominatim."""
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(f"{zip_code}, {country_code}",timeout=5)

    if location:
        return location.latitude, location.longitude
    return None, None



def get_air_quality(lat,lon):
    aqi_url_complete = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={openWeather_key}"

    try:
        response = requests.get(aqi_url_complete)
        if response.status_code != 200:
            return {"error":f"❌ API Error {response.status_code}:{response.json().get('message', 'Unknown Error')}"}
        
        data = response.json()
        if not data['list']:
            return "⚠️ No air quality data available for this location."
         
        aqi = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']
        dt = data['list'][0]['dt']

        return {
            'aqi':aqi,
            "components":components,
            "time":dt
        }
    except requests.exceptions.RequestException as e:
        return {"error":f"🚨 Network Error: {str(e)}"}
    
    except requests.exceptions.Timeout:
        return {"error":"⏳ Request timed out. Please try again."}
    

    

values = get_air_quality(3.0396684249564596,101.4351033472648)

print(values['aqi'])
print(values['components'])
print(values['time'])
