from connect import db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import schedule
import threading
import time
from datetime import datetime
import logging
from fire_monitor import process_all_cameras

app = FastAPI()
parkcams = db.parkcams

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
    # Start the fire monitoring service
    start_fire_monitoring()

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


@app.post("/api/monitor/trigger")
async def trigger_monitoring():
    """Manually trigger the fire monitoring process."""
    try:
        process_all_cameras()
        return {"status": "success", "message": "Fire monitoring cycle triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monitor/status")
async def get_monitor_status():
    """Get the status of the last monitoring run for all cameras."""
    try:
        cursor = db.parkcams.find({}, {
            "id": 1,
            "title": 1,
            "last_checked": 1,
            "fire_detected": 1,
            "confidence": 1,
            "error": 1
        })
        status = list(cursor)
        return {"status": "success", "cameras": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
