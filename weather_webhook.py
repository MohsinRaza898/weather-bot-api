from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone
from datetime import datetime

app = Flask(__name__)

OPENWEATHER_API_KEY = '184245c1fbeb6b2d1923121721351de7'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("Request received:", req)
    
    # Extract city and date from webhook request
    city = req['queryResult']['parameters'].get('city')
    date = req['queryResult']['parameters'].get('date')
    
    if not city:
        return jsonify({"fulfillmentText": "Please specify a city."})

    # Default to current date if no date provided
    if not date:
        date = datetime.now(timezone.utc).date()
    else:
        date = datetime.fromisoformat(date).date()

    # Fetch weather data
    weather_data = get_weather(city, date)
    
    return jsonify({"fulfillmentText": weather_data})

def get_weather(city, date):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data['cod'] != "200":
        return f"Unable to fetch weather data for {city}. Please check the city name."
    
    # Find weather for the requested date
    weather_description = "No forecast available."
    for entry in data['list']:
        entry_date = datetime.fromtimestamp(entry['dt'], timezone.utc).date()
        if entry_date == date:
            weather_description = f"Weather in {city} on {date} is {entry['weather'][0]['description']} with a temperature of {entry['main']['temp']}°C."
            break

    return weather_description

if __name__ == '__main__':
    app.run(debug=True)
