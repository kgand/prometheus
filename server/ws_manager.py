from fastapi import WebSocket
from typing import Dict, Set
import logging
import json
from datetime import datetime
from connect import db

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info("New WebSocket client connected")
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("WebSocket client disconnected")
        
    async def broadcast_fire_status(self, camera_data: Dict):
        """Broadcast fire status to all connected clients."""
        if not self.active_connections:
            return
            
        try:
            # Format message for clients
            message = {
                "type": "fire_update",
                "data": {
                    "camera_id": str(camera_data["_id"]),
                    "fire_detected": camera_data.get("fire_detected", False),
                    "confidence": camera_data.get("confidence", 0.0),
                    "location": {
                        "lat": camera_data.get("latitude", 0),
                        "lng": camera_data.get("longitude", 0)
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            # Broadcast to all connected clients
            for connection in self.active_connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to client: {e}")
                    # Remove dead connections
                    try:
                        self.active_connections.remove(connection)
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Error broadcasting fire status: {e}")

# Global connection manager
manager = ConnectionManager()

async def get_initial_camera_status():
    """Get initial status of all cameras."""
    try:
        cameras = []
        cursor = db.user_cctv.find(
            {"fire_detected": True},
            {"_id": 1, "fire_detected": 1, "confidence": 1, "latitude": 1, "longitude": 1}
        )
        
        for doc in cursor:
            cameras.append({
                "camera_id": str(doc["_id"]),
                "fire_detected": doc.get("fire_detected", False),
                "confidence": doc.get("confidence", 0.0),
                "location": {
                    "lat": doc.get("latitude", 0),
                    "lng": doc.get("longitude", 0)
                }
            })
            
        return cameras
    except Exception as e:
        logger.error(f"Error getting initial camera status: {e}")
        return [] 