##pip install requests
## pip install python-dotenv

import requests
import json
from datetime import datetime

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use the API key from the environment
api_key = os.getenv("WEATHER_KEY")


# Define the API endpoint and parameters
def get_geo_data(city, country_code, api_key):
  url = "http://api.openweathermap.org/geo/1.0/direct"
  params = {"q": f"{city},{country_code}", "limit": "1", "appid": api_key}

  response = requests.get(url, params=params)

  if response.status_code == 200:
    global data
    data = response.json()
    if data:
      return data[0]
    else:
      print(f"No geo data found for '{city}, {country_code}'")
      return None
  else:
    print(
        f"Error fetching geo data for '{city}, {country_code}': HTTP {response.status_code}"
    )
    print(response.text)
    return None


def get_current_weather(lat, lon, api_key):
  url = "https://api.openweathermap.org/data/2.5/weather"
  params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}

  response = requests.get(url, params=params)

  if response.status_code == 200:
    city_name, latitude, longitude = get_geo_data(city_name, country_code,
                                                  api_key)
    if city_name and latitude and longitude:
      weather_data = get_current_weather(latitude, longitude, api_key)
      if weather_data:
        # Extracting key information from the weather_data
        print(f"City: {city_name}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Feels like: {weather_data['main']['feels_like']}°C")
        print(f"Max Temperature: {weather_data['main']['temp_max']}°C")
        print(f"Min Temperature: {weather_data['main']['temp_min']}°C")
        print(f"Pressure: {weather_data['main']['pressure']} hPa")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"Weather: {weather_data['weather'][0]['main']}")
      else:
        print("Weather data not available.")
    else:
      print("Location not found.")
  else:
    print(
        f"Error fetching current weather for ({lat}, {lon}): HTTP {response.status_code}"
    )
    print(response.text)
    return None


def get_weather_forecast(lat, lon, api_key):
  url = "http://api.openweathermap.org/data/2.5/forecast"
  params = {
      "lat": lat,
      "lon": lon,
      "limit": 1,
      "appid": api_key,
      #default is K so need this to get C
      "units": "metric"
  }

  response = requests.get(url, params=params)

  if response.status_code == 200:
    return response.json()
  else:
    print(
        f"Error fetching weather data for ({lat}, {lon}): HTTP {response.status_code}"
    )
    print(response.text)
    return None


city_name = input("Enter the name of the city: ")
country_code = input("Enter the country code: ")
geo_data = get_geo_data(city_name, country_code, api_key)

if geo_data:
  forecast_data = get_weather_forecast(geo_data['lat'], geo_data['lon'],
                                       api_key)
  if forecast_data:
    ##print(forecast_data) will print the entire json that the API returns so I've condensed it (kinda).
    print('Forecasts:')
    for forecast in forecast_data['list']:
      timestamp = datetime.fromtimestamp(
          forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
      max_temp = forecast['main']['temp_max']
      min_temp = forecast['main']['temp_min']
      feels_like = forecast['main']['feels_like']
      print(
          f"Forecast at {timestamp}: Max Temperature: {max_temp} C, Min Temperature: {min_temp} C, Feels Like: {feels_like} C"
      )
