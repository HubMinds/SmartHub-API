import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use the API key from the environment
api_key = os.getenv("WEATHER_KEY")
appId = os.getenv("TRANSPORT_ID")
appKey = os.getenv("TRANSPORT_KEY")

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

# Function to get journey from lonlat to lonlat
def get_journey_data(lonlat_from, lonlat_to):
    url = f"http://transportapi.com/v3/uk/public/journey/from/{lonlat_from}/to/{lonlat_to}.json"
    params = {
        "service": "silverrail",
        "app_id": appId,
        "app_key": appKey
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Error fetching journey data for lonlat_from:{lonlat_from} to lonlat_to:{lonlat_to}: HTTP {response.status_code}"
        )
        print(response.text)
        return None

# Function to convert geo data to lonlat format
def get_lonlat(geo_data):
    return f"{geo_data['lon']},{geo_data['lat']}"

city_name_origin = input("Enter the name of the origin city: ")
country_code_origin = input("Enter the origin country code: ")

# Get geo data for origin city
geo_data_origin = get_geo_data(city_name_origin, country_code_origin, api_key)

if geo_data_origin:
    lonlat_origin = get_lonlat(geo_data_origin)
    print(f"Origin: {lonlat_origin}")

    city_name_dest = input("Enter the name of the destination city: ")
    country_code_dest = input("Enter the destination country code: ")

    # Get geo data for destination city
    geo_data_dest = get_geo_data(city_name_dest, country_code_dest, api_key)

    if geo_data_dest:
        lonlat_dest = get_lonlat(geo_data_dest)
        print(f"Destination: {lonlat_dest}")

        journey_data = get_journey_data(lonlat_origin, lonlat_dest)

        if journey_data:
            print(journey_data)
        else:
            print("Journey data not available for the given origin and destination.")
    else:
        print("Geo data for the destination city not found.")
else:
    print("Geo data for the origin city not found.")
