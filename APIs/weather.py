import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use the API key from the environment
api_key = os.getenv("WEATHER_KEY")


# Define the API endpoint and parameters to get geo data
def get_geo_data(city, country_code, api_key):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city},{country_code}", "limit": "1", "appid": api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
        else:
            print(f"No geo data found for '{city}, {country_code}'")
            return None
    else:
        print(f"Error fetching geo data for '{city}, {country_code}': HTTP {response.status_code}")
        print(response.text)
        return None


# Define the API endpoint and parameters to get current weather
def get_current_weather(lat, lon, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        if weather_data:
            return weather_data
        else:
            print("Weather data not available.")
            return None
    else:
        print(f"Error fetching current weather: HTTP {response.status_code}")
        print(response.text)
        return None


# Get weather forecast
def get_weather_forecast(lat, lon, api_key):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data: HTTP {response.status_code}")
        print(response.text)
        return None


# Main program
city_name = input("Enter the name of the city: ")
country_code = input("Enter the country code: ")

# Get geo data
geo_data = get_geo_data(city_name, country_code, api_key)

if geo_data:
    print(f"City: {geo_data['name']}")
    print(f"Latitude: {geo_data['lat']}")
    print(f"Longitude: {geo_data['lon']}")

    # Get current weather
    current_weather = get_current_weather(geo_data['lat'], geo_data['lon'], api_key)

    if current_weather:
        print("Current Weather:")
        print(f"Description: {current_weather['weather'][0]['description']}")
        print(f"Temperature: {current_weather['main']['temp']}°C")
        print(f"Humidity: {current_weather['main']['humidity']}%")
        print(f"Wind Speed: {current_weather['wind']['speed']} m/s")
        
        # Check if precipitation data is available
        if 'rain' in current_weather:
            print(f"Precipitation (1h): {current_weather['rain']['3h']} mm")
        elif 'snow' in current_weather:
            print(f"Precipitation (1h): {current_weather['snow']['3h']} mm")
        else:
            print("Precipitation: None")

    # Get weather forecast
    forecast_data = get_weather_forecast(geo_data['lat'], geo_data['lon'], api_key)

    if forecast_data:
        print('\nForecasts:')
        for forecast in forecast_data['list']:
            timestamp = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\nForecast at {timestamp}:")
            print(f"Description: {forecast['weather'][0]['description']}")
            print(f"Temperature: {forecast['main']['temp']}°C")
            print(f"Humidity: {forecast['main']['humidity']}%")
            print(f"Wind Speed: {forecast['wind']['speed']} m/s")
            if 'rain' in forecast:
                print(f"Precipitation (1h): {forecast['rain']['3h']} mm")
            elif 'snow' in forecast:
                print(f"Precipitation (1h): {forecast['snow']['3h']} mm")
            else:
                print("Precipitation: None")
            ##print(forecast_data) for json files
