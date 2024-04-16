import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use the API key from the environment
appId = os.getenv("TRANSPORT_ID")
appKey = os.getenv("TRANSPORT_KEY")

# Services: FHAM & SCSO

import requests
from datetime import datetime

import requests
from datetime import datetime

outbound = "outbound"
today_date = datetime.today().strftime('%Y-%m-%d')

def fetch_bus_timetables(appId, appKey, operator, service, outbound, today_date):
    try:
        
        
        
        # Construct the URL with parameters
        url = "http://www.transportapi.com/v3/uk/bus/service_timetables.json"
        params = {
            "app_id": appId,
            "app_key": appKey,
            "date": today_date,
            "direction": outbound,
            "operator": operator,
            "service": service
            
        }
        
        # Make the GET request
        response = requests.get(url, params=params)
        print(url, params)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_bus_timetable(data):
    try:
        destination_times = []
        for stop in data['stops']:
            destination_times.append((stop['name'], stop['aimed_departure_time']))
        return destination_times
    except KeyError:
        print("Error: Unable to parse data.")
        return None

# Example usage
appId = "your_app_id"
appKey = "your_app_key"
operator = input("Enter operator (SCSO or FHAM): ").upper()
service = input("Enter service number: ")

data = fetch_bus_timetables(appId, appKey, operator, service, outbound, today_date)
if data:
    print("Data fetched successfully!")
    destination_times = parse_bus_timetable(data)
    if destination_times:
        print("Destination times and names of bus stops:")
        for stop_name, departure_time in destination_times:
            print(f"{stop_name}: {departure_time}")
    else:
        print("Failed to parse destination times.")
else:
    print("Failed to fetch data.")
    
    
