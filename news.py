import requests
import os
from dotenv import load_dotenv

# Load .env and get api key from file
load_dotenv()
api_key = os.getenv("NEWS_KEY")

def fetch_news(country, source=None, category=None, query=None):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": api_key, "country": country}

    if source:
        params["sources"] = source
    if category:
        params["category"] = category
    if query:
        params["q"] = query

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch news", "message": response.json()}

