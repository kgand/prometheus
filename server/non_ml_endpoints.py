from connect import db, app
from fastapi import HTTPException, Body
from utils import parse_document
from owm import get_weather
from resources import get_emergency_places
from wildfires import get_wildfire_incidents
from webcams import get_camera_by_camera_id
from datetime import datetime
from pydantic import BaseModel

parkcams = db.parkcams
user_cctv = db.user_cctv  # Add user_cctv collection

class CameraAdd(BaseModel):
    ip_address: str
    latitude: float
    longitude: float
    email: str
    name: str

# non-ml endpoints


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/allcams")
def read_allcams():
    try:
        print("Finding all cameras...")
        # Get cameras from both collections
        park_cameras = [parse_document(doc) for doc in parkcams.find({})]
        user_cameras = [parse_document(doc) for doc in user_cctv.find({})]
        all_cameras = park_cameras + user_cameras
        print(f"found {len(all_cameras)} cameras")

        return all_cameras
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve cameras")


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


@app.post("/addcam")
def add_camera(camera: CameraAdd):
    try:
        print(f"Adding new camera for {camera.email}...")
        
        # Create new camera document
        new_camera = {
            "name": camera.name,
            "ip_address": camera.ip_address,
            "user_id": "user",  # You might want to add proper user ID management
            "fire_detected": False,
            "created_at": datetime.utcnow().isoformat(),
            "confidence": 0,
            "last_alert": None,
            "last_checked": datetime.utcnow().isoformat(),
            "latitude": camera.latitude,
            "longitude": camera.longitude,
            "last_connected": datetime.utcnow().isoformat(),
            "status": "offline",
            "email": camera.email
        }
        
        # Insert into user_cctv collection instead of parkcams
        result = user_cctv.insert_one(new_camera)
        
        if result.inserted_id:
            new_camera["_id"] = str(result.inserted_id)
            print(f"Successfully added camera {new_camera['name']}")
            return new_camera
        else:
            raise HTTPException(status_code=500, detail="Failed to add camera")
            
    except Exception as e:
        print(f"Error adding camera: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/usercams")
def read_usercams():
    try:
        print("Finding user cameras...")
        user_cameras = [parse_document(doc) for doc in user_cctv.find({})]
        print(f"found {len(user_cameras)} user cameras")
        return user_cameras
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve user cameras")
