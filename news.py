import requests
import os
from dotenv import load_dotenv

# Load .env and get the API key from file
load_dotenv()
api_key = os.getenv("NEWS_KEY")

def fetch_news(country=None, source=None, category=None, query=None):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": api_key}

    # Check if source is specified; if so, use it and ignore the country.
    if source:
        params["sources"] = source
    else:
        # Only add country and category if source is not specified.
        if country:
            params["country"] = country
        if category:
            params["category"] = category

    if query:
        params["q"] = query

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # More specific error handling; use response.json() to get details
        error_info = response.json()  # Assuming API errors are returned in JSON
        return {
            "error": "Failed to fetch news",
            "status_code": response.status_code,
            "message": error_info.get("message", "An unknown error occurred")
        }

# Example usage:
# news_data = fetch_news(country="us", category="technology", query="AI")
