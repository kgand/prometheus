from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

import httpx
import math
import json


# Haversine formula to calculate the distance between two lat/lon points


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # radius of earth in km
    return c * r


# NOTE: radius in miles
def get_emergency_places(lat, lon, radius):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    place_types = {
        "hospitals": "hospital",
        "food_banks": "food_bank",
        "fire_stations": "fire_station",
        "shelters": "shelter",
        "community_centers": "community_center",
    }

    places_data = {}

    for place_type_key, place_type_value in place_types.items():
        params = {
            "location": f"{lat},{lon}",
            "radius": radius * 1609.34,  # converts miles to meters
            "type": place_type_value,
            "key": GOOGLE_MAPS_API_KEY,
        }

        response = httpx.get(endpoint, params=params)
        if response.status_code == 200:
            places = response.json().get("results", [])
            places_data[place_type_key] = []

            for place in places:
                place_lat = place["geometry"]["location"]["lat"]
                place_lon = place["geometry"]["location"]["lng"]
                distance = haversine(lat, lon, place_lat, place_lon)

                place_info = {
                    "id": place.get("place_id"),
                    "name": place.get("name"),
                    "address": place.get("vicinity", ""),
                    "lat": place_lat,
                    "lon": place_lon,
                    "dist": round(distance, 2),  # NOTE: distance in miles
                }

                places_data[place_type_key].append(place_info)

    return places_data
