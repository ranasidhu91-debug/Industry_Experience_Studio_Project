import requests
from API.api_key import iqair_key,open_weather
from geopy.geocoders import Nominatim
from pprint import pprint

lat = str(6.443589)
lng = str(101.435110)
lon = str(100.216599)

#aqi
#aqi_url_complete = f"http://api.waqi.info/feed/geo:{lat};{lng}/?token={waqi_key}" # aqi api

#aqi
#aqi_url_complete = f"https://api.waqi.info/feed/klang/?token=8437227b3dd6cba3e470d7a48fabb84f26c448ec"
#print(aqi_url_complete)
#openweather 
aqi_url_complete = f"http://api.airvisual.com/v2/city?city=Kuala Lumpuer&state=California&country=USA&key={{YOUR_API_KEY}}" #open weather api

#whatever = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start=1742132952&end=1742219352&appid={open_weather}"


#response = requests.get(aqi_url_complete)

#data = response.json()

#pprint(data)


states = f"http://api.airvisual.com/v2/states?country=Malaysia&key={iqair_key}"

response = requests.get(states)

