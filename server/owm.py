import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")


class OwmClient:
    OWM_BASE_URL = "http://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, url: str) -> httpx.Response:
        get_url = f"{self.OWM_BASE_URL}{url}&appid={self.api_key}&units=metric"
        headers = {"accept": "application/json"}

        return httpx.get(get_url, headers=headers)


owm = OwmClient(api_key=OPENWEATHERMAP_API_KEY)


def get_weather(lat, lon):
    weather_response = owm.get(f"/weather?lat={lat}&lon={lon}")

    return weather_response.json()
