import time
import schedule
from connect import db
from video_processing import process_base64_image
from nps import get_base64_of_webcam_image
from datetime import datetime
import logging
import threading
import asyncio
from ws_manager import manager
from twilio_manager import make_emergency_call
import os
from dotenv import load_dotenv
import base64
import cv2
from droidcam import cameras  # Import the cameras dict from droidcam

# Load environment variables
load_dotenv()
EMERGENCY_PHONE = os.getenv("EMERGENCY_PHONE_NUMBER")  # Fix environment variable name
logger = logging.getLogger(__name__)

# Log Twilio configuration
logger.info("Twilio Configuration:")
logger.info(f"Emergency Phone Number configured: {'Yes' if EMERGENCY_PHONE else 'No'}")
logger.info(f"Emergency Phone Number: {EMERGENCY_PHONE if EMERGENCY_PHONE else 'Not Set'}")

if not EMERGENCY_PHONE:
    logger.error("EMERGENCY_PHONE_NUMBER not found in .env file!")

parkcams = db.parkcams
fire_detections = db.fire_detections
user_cctv = db.user_cctv

# Dictionary to track last fire alerts for each camera
last_fire_alerts = {}
RECHECK_INTERVAL = 60  # 60 seconds

def update_camera_image(camera_id, image_data):
    """Update the image in fire_detections collection."""
    try:
        result = fire_detections.replace_one(
            {"camera_id": camera_id},
            {
                "camera_id": camera_id,
                "timestamp": image_data['timestamp'],
                "image": image_data['image']
            },
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    except Exception as e:
        logger.error(f"Error updating image for camera {camera_id}: {str(e)}")
        return False

def should_make_emergency_call(camera_id):
    """Determine if we should make an emergency call based on last alert time."""
    current_time = datetime.utcnow()
    last_alert = last_fire_alerts.get(camera_id)
    
    if last_alert is None:
        return True
        
    time_since_last_alert = (current_time - last_alert).total_seconds()
    return time_since_last_alert >= RECHECK_INTERVAL

def get_droidcam_frame(camera_id):
    """Get frame from DroidCam camera."""
    try:
        camera = cameras.get(str(camera_id))
        if camera:
            frame = camera.get_frame()
            if frame is not None:
                # Convert frame to base64
                _, buffer = cv2.imencode('.jpg', frame)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                return {'image': base64_image}
    except Exception as e:
        logger.error(f"Error getting DroidCam frame: {e}")
    return None

async def update_camera_status(camera_id, detection_data):
    """Update the fire detection status in parkcams collection."""
    try:
        # Determine which collection to update based on camera type
        collection = user_cctv if isinstance(camera_id, str) and str(camera_id).startswith("user_") else parkcams
        
        result = collection.update_one(
            {"_id": camera_id} if isinstance(camera_id, str) and str(camera_id).startswith("user_") else {"id": camera_id},
            {
                "$set": {
                    "last_checked": detection_data['timestamp'],
                    "fire_detected": detection_data['fire_detected'],
                    "confidence": detection_data['confidence'],
                    "error": detection_data.get('error', None)
                }
            }
        )
        
        # Get updated camera data for WebSocket broadcast
        camera_data = collection.find_one(
            {"_id": camera_id} if isinstance(camera_id, str) and str(camera_id).startswith("user_") else {"id": camera_id}
        )
        
        if camera_data and manager.active_connections:
            await manager.broadcast_fire_status(camera_data)
            
            # Handle emergency call if fire is detected
            if detection_data['fire_detected'] and should_make_emergency_call(camera_id):
                try:
                    logger.info(f"Attempting emergency call for camera {camera_id}")
                    if EMERGENCY_PHONE:
                        logger.info(f"Making emergency call to {EMERGENCY_PHONE}")
                        camera_name = camera_data.get("name", "Unknown Camera")
                        latitude = camera_data.get("latitude", 0)
                        longitude = camera_data.get("longitude", 0)
                        
                        # Log the TTS message that will be sent
                        tts_message = f"Alert! Fire detected at {camera_name}. "
                        if latitude != 0 and longitude != 0:
                            tts_message += f"Location coordinates: {latitude}, {longitude}. "
                        tts_message += "Please take immediate action."
                        logger.info(f"TTS Message to be sent: {tts_message}")
                        
                        # Make the call
                        call_result = make_emergency_call(
                            EMERGENCY_PHONE,
                            "CCTV",  # Generic camera name
                            latitude,
                            longitude
                        )
                        
                        if call_result:
                            last_fire_alerts[camera_id] = datetime.utcnow()
                            logger.info(f"✅ Emergency call completed successfully for camera {camera_id}")
                        else:
                            logger.error(f"❌ Emergency call failed for camera {camera_id}")
                    else:
                        logger.error("❌ Emergency call failed: EMERGENCY_PHONE_NUMBER not found in .env")
                except Exception as e:
                    logger.error(f"Failed to make emergency call for camera {camera_id}")
                    logger.error(f"Error details: {str(e)}")
                    logger.error(f"Camera data: {camera_data}")
                    # Log Twilio environment variables (without tokens)
                    logger.error(f"Twilio phone number configured: {'Yes' if os.getenv('TWILIO_PHONE_NUMBER') else 'No'}")
                    logger.error(f"Twilio account SID configured: {'Yes' if os.getenv('TWILIO_ACCOUNT_SID') else 'No'}")
                    logger.error(f"Twilio auth token configured: {'Yes' if os.getenv('TWILIO_AUTH_TOKEN') else 'No'}")
            
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating status for camera {camera_id}: {str(e)}")
        return False

async def process_camera(camera):
    """Process a single camera for fire detection."""
    try:
        camera_title = camera.get('title', 'Unknown')
        camera_id = camera.get('id') or camera.get('_id')  # Support both parkcams and user_cctv
        
        if not camera_id:
            logger.warning(f"Skipping camera {camera_title} - no ID found")
            return
            
        logger.info(f"Processing camera: {camera_title} (ID: {camera_id})")  # Changed to info for better visibility
        current_time = datetime.utcnow().isoformat()
        
        try:
            # Check if this is a DroidCam camera
            is_droidcam = isinstance(camera_id, str) and str(camera_id).startswith("user_")
            
            # Get image data based on camera type
            if is_droidcam:
                webcam_data = get_droidcam_frame(camera_id)
                logger.info(f"Got DroidCam frame for camera {camera_id}")  # Changed to info
            else:
                webcam_data = get_base64_of_webcam_image(camera.get('url'))
                logger.info(f"Got webcam image for camera {camera_id}")  # Changed to info
            
            if webcam_data and 'image' in webcam_data:
                # Store the image first
                image_data = {
                    'timestamp': current_time,
                    'image': webcam_data['image']
                }
                update_camera_image(camera_id, image_data)
                
                # Process the image for fire detection
                detection_result = process_base64_image(webcam_data['image'])
                logger.info(f"Detection result for camera {camera_id}: {detection_result}")  # Changed to info
                
                if detection_result:
                    is_fire = detection_result['class'] == 'Fire'
                    confidence = float(detection_result['confidence'])
                    
                    # Update the camera status
                    status_data = {
                        'timestamp': current_time,
                        'fire_detected': is_fire,
                        'confidence': confidence,
                        'error': None
                    }
                    
                    await update_camera_status(camera_id, status_data)
                    
                    if is_fire:
                        logger.info(
                            f"🔥 FIRE DETECTED for camera {camera_title} (ID: {camera_id}) "
                            f"with confidence: {confidence:.2%}"
                        )
                        
                        # Directly make emergency call here for immediate response
                        if should_make_emergency_call(camera_id):
                            try:
                                if EMERGENCY_PHONE:
                                    logger.info(f"Making immediate emergency call to {EMERGENCY_PHONE}")
                                    camera_name = camera.get("name", "Unknown Camera")
                                    latitude = camera.get("latitude", 0)
                                    longitude = camera.get("longitude", 0)
                                    
                                    # Make the call
                                    call_result = make_emergency_call(
                                        EMERGENCY_PHONE,
                                        "CCTV",  # Generic camera name
                                        latitude,
                                        longitude
                                    )
                                    
                                    if call_result:
                                        last_fire_alerts[camera_id] = datetime.utcnow()
                                        logger.info(f"✅ Emergency call completed successfully for camera {camera_id}")
                                    else:
                                        logger.error(f"❌ Emergency call failed for camera {camera_id}")
                                else:
                                    logger.error("❌ Emergency call failed: EMERGENCY_PHONE_NUMBER not found in .env")
                            except Exception as e:
                                logger.error(f"❌ Failed to make emergency call for camera {camera_id}")
                                logger.error(f"Error details: {str(e)}")
                                logger.error(f"Camera data: {camera}")
                                # Log Twilio environment variables (without tokens)
                                logger.error(f"Twilio phone number configured: {'Yes' if os.getenv('TWILIO_PHONE_NUMBER') else 'No'}")
                                logger.error(f"Twilio account SID configured: {'Yes' if os.getenv('TWILIO_ACCOUNT_SID') else 'No'}")
                                logger.error(f"Twilio auth token configured: {'Yes' if os.getenv('TWILIO_AUTH_TOKEN') else 'No'}")
                    else:
                        logger.info(
                            f"No fire detected for camera {camera_title} "
                            f"(Confidence: {confidence:.2%})"
                        )
                else:
                    # Update with processing error
                    error_status = {
                        'timestamp': current_time,
                        'fire_detected': False,
                        'confidence': 0.0,
                        'error': 'Failed to process image'
                    }
                    await update_camera_status(camera_id, error_status)
                    logger.warning(f"No detection result for camera {camera_title}")
            else:
                # Update with image retrieval error
                error_status = {
                    'timestamp': current_time,
                    'fire_detected': False,
                    'confidence': 0.0,
                    'error': 'No image data available'
                }
                await update_camera_status(camera_id, error_status)
                logger.warning(f"No image data for camera {camera_title}")
                
        except Exception as e:
            # Update with general error
            error_status = {
                'timestamp': current_time,
                'fire_detected': False,
                'confidence': 0.0,
                'error': str(e)
            }
            await update_camera_status(camera_id, error_status)
            logger.error(f"Error processing camera {camera_title}: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error in process_camera: {str(e)}")

async def process_all_cameras():
    """Process all cameras and update fire detection results in database."""
    try:
        logger.info("Starting camera processing cycle")
        
        # Get all cameras from both collections
        park_cameras = list(parkcams.find({}))
        user_cameras = list(user_cctv.find({}))
        all_cameras = park_cameras + user_cameras
        
        logger.info(f"Found {len(all_cameras)} cameras ({len(park_cameras)} park cameras, {len(user_cameras)} user cameras)")
        
        if not all_cameras:
            logger.warning("No cameras found in database")
            return
            
        # Process all cameras concurrently
        await asyncio.gather(*[process_camera(camera) for camera in all_cameras])
            
    except Exception as e:
        logger.error(f"Error in process_all_cameras: {str(e)}")

def start_fire_monitoring():
    """Start the fire monitoring background task."""
    async def run_monitoring():
        logger.info("Starting fire monitoring service...")
        while True:
            try:
                logger.info("Running fire detection cycle...")
                await process_all_cameras()
                logger.info("Completed fire detection cycle, waiting for next interval...")
            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
            finally:
                await asyncio.sleep(RECHECK_INTERVAL)

    # Get the event loop from the current context
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.info("Creating fire monitoring task in existing loop")
            asyncio.create_task(run_monitoring())
        else:
            logger.info("Starting new event loop for fire monitoring")
            loop.create_task(run_monitoring())
            loop.run_forever()
    except RuntimeError:
        logger.warning("No event loop found, creating new one")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(run_monitoring())
        loop.run_forever()
    except Exception as e:
        logger.error(f"Error in start_fire_monitoring: {e}")