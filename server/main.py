from connect import db
from fastapi import FastAPI, HTTPException
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
from dotenv import load_dotenv
from fire_monitor import process_all_cameras
from droidcam import initialize_droidcam, cleanup, generate_frames

# Load environment variables
load_dotenv()

app = FastAPI()
parkcams = db.parkcams

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
    droidcam_ip = os.getenv('DROIDCAM_IP')
    if not droidcam_ip:
        logging.warning("DROIDCAM_IP not found in .env")
        return
        
    droidcam_url = f"http://{droidcam_ip}:4747/video"
    if not initialize_droidcam(droidcam_url):
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
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found between {start_port} and {start_port + max_attempts - 1}")

if __name__ == "__main__":
    try:
        port = find_available_port(8000)
        print(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Failed to start server: {e}")
