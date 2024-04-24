from flask import Flask, jsonify, request
from flask_cors import CORS
import news
import weather

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes

@app.route('/news')
def get_news():
    country = request.args.get('country', default='us')
    source = request.args.get('source')
    category = request.args.get('category')
    query = request.args.get('query')
    return jsonify(news.fetch_news(country, source, category, query))

@app.route('/weather', methods=['GET'])
def handle_weather_request():
    action = request.args.get('action', type=int)
    city = request.args.get('city')
    country_code = request.args.get('country_code')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if action == 0:  # Get Geo Data
        if city and country_code:
            return jsonify(weather.get_geo_data(city, country_code))
        else:
            return jsonify({"error": "City and country code are required for geo data."})

    elif action == 1:  # Get Current Weather
        if lat and lon:
            return jsonify(weather.get_current_weather(lat, lon))
        else:
            return jsonify({"error": "Latitude and longitude are required for current weather."})

    elif action == 2:  # Get Weather Forecast
        if lat and lon:
            return jsonify(weather.get_weather_forecast(lat, lon))
        else:
            return jsonify({"error": "Latitude and longitude are required for weather forecast."})

    return jsonify({"error": "Invalid action specified."})

if __name__ == '__main__':
    app.run(debug=True)
