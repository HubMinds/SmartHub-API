import requests
import os
from dotenv import load_dotenv

## load .env and get api key from file
load_dotenv()


api_key = os.getenv("NEWS_KEY")

# would be a button/text box in the actual app
country = input("Enter your country code (e.g., us, uk): ")
source = input("Enter the source (optional): ")
category = input("Enter the category (optional): ")
query = input("Enter a keyword to search for (optional): ")

# construct api url using user inputs
url = "https://newsapi.org/v2/top-headlines"
params = {"apiKey": api_key}

if source:
    params["sources"] = source
elif country:
    params["country"] = country
elif category:
    params["category"] = category
elif query:
    params["q"] = query

# api request and response
response = requests.get(url, params=params)

if response.status_code == 200:
    # parsing the json response so that you can iterate through it to search for specifics, title in this case
    data = response.json()

    if data["totalResults"] > 0:
        # print only the titles of the top articles
        for article in data["articles"]:
            print(article["title"])
    else:
        print("No articles found.")
else:
    print("Error:", response.json()["message"])