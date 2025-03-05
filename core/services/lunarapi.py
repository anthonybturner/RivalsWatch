# core/lunarapi.py
import requests
from django.conf import settings

def get_lunar_data(endpoint):
    url = f"https://api.lunarapi.org/{endpoint}"
    headers = {
        "Authorization": f"Bearer {settings.LUNAR_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # return the data as JSON if successful
    else:
        return None  # or handle the error accordingly

def get_all_heroes():
    url = "https://api.lunarapi.org/marvelrivals/heroes/"
    headers = {"Authorization": f"Bearer {settings.LUNAR_API_KEY}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON data of all heroes
    else:
        return []

