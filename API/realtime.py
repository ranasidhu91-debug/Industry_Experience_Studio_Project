import requests

from api_key import api_key
from base_url import root_url
import json
import pprint


city = "kuala-lumpur"

api_url = root_url + city + "/?token=" + api_key

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    pprint.pprint(data['data'])