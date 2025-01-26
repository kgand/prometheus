from fastapi import WebSocket
import logging
from connect import app
from ws_manager import manager, get_initial_camera_status

logger = logging.getLogger(__name__)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("New WebSocket connection attempt")
    try:
        await manager.connect(websocket)
        logger.info("WebSocket connection established")
        
        # Send initial camera status
        initial_status = await get_initial_camera_status()
        for camera in initial_status:
            await websocket.send_json({
                "type": "fire_update",
                "data": camera
            })
            
        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                logger.debug(f"Received message: {data}")
                # Handle any incoming messages if needed
            except Exception as e:
                logger.error(f"Error receiving message: {str(e)}")
                break
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        manager.disconnect(websocket)
        logger.info("WebSocket connection closed") 