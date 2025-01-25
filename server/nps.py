import httpx
import json
import os
import base64
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import Any
from rich import print

load_dotenv()

NPS_API_KEY = os.environ.get("NPS_API_KEY")


class NpsClient:
    NPS_BASE_URL = "https://developer.nps.gov/api/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, url: str) -> httpx.Response:
        get_url = f"{self.NPS_BASE_URL}{url}?api_key={self.api_key}"
        headers = {"accept": "application/json"}

        return httpx.get(get_url, headers=headers)


def filter_webcams(data: Any) -> Any:
    return list(
        filter(
            lambda w: w["url"].startswith("https://www.nps.gov/media/webcam/view.htm")
            and w["latitude"]
            and w["longitude"],
            data,
        )
    )


def image_bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def get_base64_of_webcam_image(url: str):
    response = httpx.get(url)

    if response.status_code != 200:
        raise Exception(f"couldn't get page: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    img_tag = soup.find("img", id="webcamRefreshImage")
    if not img_tag:
        raise Exception("no image with id 'webcamRefreshImage' not found.")

    img_url = img_tag.get("src")

    if img_url.startswith("http"):
        img_src = img_url
    else:
        img_src = url + img_url

    img_response = httpx.get(img_src)

    if img_response.status_code != 200:
        raise Exception(f"couldn't retrieve the image: {img_response.status_code}")

    img_base64 = image_bytes_to_base64(img_response.content)

    return img_base64


nps = NpsClient(api_key=NPS_API_KEY)

webcams_response = nps.get("/webcams")
webcams_data = None

if webcams_response.status_code != 200:
    raise Exception("failed to get the webcams")
else:
    webcams_data = webcams_response.json()


def get_filtered_webcams_list():
    print("Recieved and filtered webcams")
    return filter_webcams(webcams_data["data"])
