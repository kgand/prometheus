from connect import db
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from owm import get_weather
import uvicorn
import schedule
import threading
import time
from datetime import datetime
import logging
import os
import socket
from wildfires import get_wildfire_incidents
from dotenv import load_dotenv
from fire_monitor import process_all_cameras
from droidcam import initialize_droidcam, cleanup, generate_frames
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List

# Load environment variables
load_dotenv()

app = FastAPI()
parkcams = db.parkcams
user_cctv = db.user_cctv


# Pydantic models
class CameraBase(BaseModel):
    name: str
    ip_address: str
    location: Optional[str] = None


class CameraCreate(CameraBase):
    user_id: str


class CameraUpdate(CameraBase):
    pass


class Camera(CameraBase):
    id: str
    user_id: str
    fire_detected: bool = False
    last_checked: Optional[datetime] = None
    last_alert: Optional[datetime] = None

    class Config:
        from_attributes = True


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add a background task worker
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the fire monitoring schedule
def start_fire_monitoring():
    # Schedule fire monitoring every 5 minutes
    schedule.every(5).minutes.do(process_all_cameras)

    # Run immediately on startup
    process_all_cameras()

    # Start the background scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
    scheduler_thread.start()


# Add startup event handler
@app.on_event("startup")
async def startup_event():
    # Initialize DroidCam using IP from .env
    droidcam_ip = os.getenv("DROIDCAM_IP")
    if not droidcam_ip:
        logging.warning("DROIDCAM_IP not found in .env")
        return

    # Check if a default camera already exists for this IP
    default_camera = user_cctv.find_one({"ip_address": droidcam_ip})

    if default_camera:
        camera_id = default_camera["_id"]
    else:
        # Create a default camera entry
        result = user_cctv.insert_one(
            {
                "name": "Default DroidCam",
                "ip_address": droidcam_ip,
                "user_id": "system",  # Use a system identifier for the default camera
                "fire_detected": False,
                "created_at": datetime.utcnow(),
            }
        )
        camera_id = result.inserted_id

    droidcam_url = f"http://{droidcam_ip}:4747/video"
    if not initialize_droidcam(droidcam_url, camera_id):
        logging.error("Failed to initialize DroidCam")
    # Start the fire monitoring service
    # start_fire_monitoring()


@app.on_event("shutdown")
async def shutdown_event():
    cleanup()


def parse_document(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


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
        print("found wildfires for")

        return wildfires
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve wildfires")


@app.get("/droidcam", response_class=HTMLResponse)
async def droidcam_page():
    """Serve the DroidCam video feed page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DroidCam Fire Detection</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; text-align: center; }
            h1 { color: #333; }
            .video-container { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>DroidCam Fire Detection Feed</h1>
        <div class="video-container">
            <img src="/droidcam/feed" alt="DroidCam Feed" style="max-width: 100%; height: auto;">
        </div>
    </body>
    </html>
    """


@app.get("/droidcam/feed")
async def video_feed():
    """Stream the DroidCam video feed."""
    return StreamingResponse(
        generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("0.0.0.0", port))
                return port
        except OSError:
            continue
    raise RuntimeError(
        f"No available ports found between {start_port} and {start_port + max_attempts - 1}"
    )


# Camera management endpoints
@app.post("/api/cameras", response_model=Camera)
async def create_camera(camera: CameraCreate):
    """Add a new camera for a user."""
    try:
        # Create camera document
        camera_dict = camera.dict()
        camera_dict["fire_detected"] = False
        camera_dict["created_at"] = datetime.utcnow()

        result = user_cctv.insert_one(camera_dict)
        camera_dict["id"] = str(result.inserted_id)

        # Initialize camera feed
        camera_url = f"http://{camera.ip_address}:4747/video"
        if not initialize_droidcam(camera_url, result.inserted_id):
            # If initialization fails, delete the camera document
            user_cctv.delete_one({"_id": result.inserted_id})
            raise HTTPException(
                status_code=400, detail="Failed to initialize camera feed"
            )

        return Camera(**camera_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cameras/{user_id}", response_model=List[Camera])
async def get_user_cameras(user_id: str):
    """Get all cameras for a user."""
    try:
        cameras = []
        cursor = user_cctv.find({"user_id": user_id})
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            cameras.append(Camera(**doc))
        return cameras
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/cameras/{camera_id}", response_model=Camera)
async def update_camera(camera_id: str, camera: CameraUpdate):
    """Update camera details."""
    try:
        update_result = user_cctv.update_one(
            {"_id": ObjectId(camera_id)}, {"$set": camera.dict(exclude_unset=True)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Camera not found")

        # Get updated camera
        doc = user_cctv.find_one({"_id": ObjectId(camera_id)})
        doc["id"] = str(doc.pop("_id"))
        return Camera(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/cameras/{camera_id}")
async def delete_camera(camera_id: str):
    """Delete a camera."""
    try:
        result = user_cctv.delete_one({"_id": ObjectId(camera_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Camera not found")
        return {"status": "success", "message": "Camera deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cameras/{camera_id}/status")
async def get_camera_status(camera_id: str):
    """Get the current status of a camera."""
    try:
        doc = user_cctv.find_one({"_id": ObjectId(camera_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Camera not found")

        return {
            "id": str(doc["_id"]),
            "fire_detected": doc.get("fire_detected", False),
            "last_checked": doc.get("last_checked"),
            "last_alert": doc.get("last_alert"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    try:
        port = find_available_port(8000)
        print(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Failed to start server: {e}")
