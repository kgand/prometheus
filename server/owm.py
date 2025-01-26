import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OPENWEATHERMAP_API_KEY not found in environment variables")


class OwmClient:
    OWM_BASE_URL = "http://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, url: str, params: dict = None) -> httpx.Response:
        if params is None:
            params = {}
        params["appid"] = self.api_key
        params["units"] = "metric"
        
        get_url = f"{self.OWM_BASE_URL}{url}"
        headers = {"accept": "application/json"}

        print(f"Making request to OpenWeatherMap API: {get_url}")
        print(f"With params: {params}")
        response = httpx.get(get_url, params=params, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        return response


owm = OwmClient(api_key=OPENWEATHERMAP_API_KEY)


def get_weather(lat, lon):
    try:
        weather_response = owm.get("/weather", params={"lat": lat, "lon": lon})
        weather_response.raise_for_status()
        data = weather_response.json()
        
        # Format the response to match our interface
        if data and "main" in data and "weather" in data:
            return {
                "main": {
                    "temp": data["main"].get("temp"),
                    "humidity": data["main"].get("humidity"),
                    "feels_like": data["main"].get("feels_like")
                },
                "weather": data.get("weather", [{"main": "Unknown", "description": "No description", "icon": "01d"}]),
                "wind": {
                    "speed": data.get("wind", {}).get("speed", 0)
                }
            }
        return None
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
