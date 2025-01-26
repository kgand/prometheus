from connect import db, app
from fastapi import HTTPException
from utils import parse_document
from owm import get_weather
from resources import get_emergency_places
from wildfires import get_wildfire_incidents
from webcams import get_camera_by_camera_id

parkcams = db.parkcams

# non-ml endpoints


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/allcams")
def read_allcams():
    try:
        print("Finding all cameras...")
        all_documents = parkcams.find({})
        all_parkcams = [parse_document(doc) for doc in all_documents]
        print(f"found {len(all_parkcams)} cameras")

        return all_parkcams
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve park cams")


@app.get("/weather")
def read_weather(lat: float, lon: float):
    try:
        print(f"Finding weather for {lat}, {lon}...")
        weather = get_weather(lat, lon)
        print(f"found weather for {lat}, {lon}...")

        return weather
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve weather")


@app.get("/wildfires")
def read_wildfires():
    try:
        print("Finding wildfires")
        wildfires = get_wildfire_incidents()
        print("found wildfires")

        return wildfires
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve wildfires")


@app.get("/resources")
def read_resources(lat: float, lon: float, radius: int):
    try:
        print(f"Finding resources in {lat}, {lon} within {radius} mile radius...")
        resources = get_emergency_places(lat, lon, radius)
        print(f"found resources in {lat}, {lon} within {radius} mile radius...")

        return resources
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve resources")


@app.get("/camera")
def read_camera(id: str):
    try:
        print(f"Finding camera {id}")
        camera = get_camera_by_camera_id(id)
        print(f"found camera {id}")

        return camera
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve camera")
