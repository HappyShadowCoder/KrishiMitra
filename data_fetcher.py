import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather_by_town(town_name: str):
    """
    Fetches CURRENT weather data for a specific town using the free API.
    """
    if not OPENWEATHER_API_KEY:
        raise Exception("OpenWeatherMap API key is not set in the .env file.")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={town_name}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current_weather = {
            "location_name": f"{data['name']}, {data['sys']['country']}",
            "temperature_celsius": data["main"]["temp"],
            "humidity_percent": data["main"]["humidity"],
            "wind_speed_mps": data["wind"]["speed"],
            "description": data["weather"][0]["description"].title(),
            "rainfall_last_hour_mm": data.get("rain", {}).get("1h", 0.0)
        }
        return {"current_conditions": current_weather}

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise Exception("Invalid OpenWeatherMap API key.")
        if e.response.status_code == 404:
            raise Exception(f"The town '{town_name}' could not be found.")
        raise Exception(f"API request failed: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


def fetch_weather_forecast_by_town(town_name: str):
    """
    Fetches a 5-DAY, 3-HOUR forecast, including rain probability, for a specific town.
    """
    if not OPENWEATHER_API_KEY:
        raise Exception("OpenWeatherMap API key is not set in the .env file.")

    # Use the free 'forecast' endpoint
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={town_name}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast_list = []
        # The 'list' key contains 40 forecast entries (8 per day for 5 days)
        for entry in data.get("list", []):
            forecast_list.append({
                "datetime": entry["dt_txt"],
                "temperature_celsius": entry["main"]["temp"],
                # 'pop' is the Probability of Precipitation
                "rain_chance_percent": entry["pop"] * 100,
                "description": entry["weather"][0]["description"].title()
            })

        return {"forecast": forecast_list}

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise Exception("Invalid OpenWeatherMap API key.")
        if e.response.status_code == 404:
            raise Exception(f"The town '{town_name}' could not be found for forecast.")
        raise Exception(f"API request failed: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

