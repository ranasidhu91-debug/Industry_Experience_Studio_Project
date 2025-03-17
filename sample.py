import requests
from API.api_key import iqair_key,open_weather
from geopy.geocoders import Nominatim
from pprint import pprint

lat = str(1.5646)
lng = str(101.435110)
lon = str(104.2451)

#aqi
#aqi_url_complete = f"http://api.waqi.info/feed/geo:{lat};{lng}/?token={waqi_key}" # aqi api

#aqi
#aqi_url_complete = f"https://api.waqi.info/feed/klang/?token=8437227b3dd6cba3e470d7a48fabb84f26c448ec"
#print(aqi_url_complete)
#openweather 
whatever = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={open_weather}"


response = requests.get(whatever)

data = response.json()

pprint(data)




#city_data = f'http://api.airvisual.com/v2/city?city=Bandar Penawar&state=Johor&country=Malaysia&key={iqair_key}'

#response = requests.get(city_data)

#data = response.json()

#pprint(data)