import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("WEATHER_ID")

def get_geo_data(city, country_code):
    print(f"Fetching geo data for city: {city}, country: {country_code}")
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city},{country_code}", "limit": "1", "appid": api_key}
    response = requests.get(url, params=params)
    data = response.json() if response.status_code == 200 else None
    print(f"Geo data received: {data}")
    return data

def get_current_weather(lat, lon):
    print(f"Fetching current weather for lat: {lat}, lon: {lon}")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()
    print(f"Weather data received: {data}")
    return data

def get_weather_forecast(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

