import time
import schedule
from connect import db
from video_processing import process_base64_image
from nps import get_base64_of_webcam_image
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

parkcams = db.parkcams
fire_detections = db.fire_detections

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

def update_camera_status(camera_id, detection_data):
    """Update the fire detection status in parkcams collection."""
    try:
        result = parkcams.update_one(
            {"id": camera_id},
            {
                "$set": {
                    "last_checked": detection_data['timestamp'],
                    "fire_detected": detection_data['fire_detected'],
                    "confidence": detection_data['confidence'],
                    "error": detection_data.get('error', None)
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating status for camera {camera_id}: {str(e)}")
        return False

def process_all_cameras():
    """Process all cameras and update fire detection results in database."""
    try:
        logger.info("Starting camera processing cycle")
        cursor = parkcams.find({})
        all_cameras = list(cursor)
        logger.info(f"Found {len(all_cameras)} cameras")
        
        if not all_cameras:
            logger.warning("No cameras found in database")
            return
            
        for camera in all_cameras:
            try:
                camera_title = camera.get('title', 'Unknown')
                camera_id = camera.get('id')
                
                if not camera_id:
                    logger.warning(f"Skipping camera {camera_title} - no ID found")
                    continue
                
                logger.debug(f"Processing camera: {camera_title} (ID: {camera_id})")
                current_time = datetime.utcnow().isoformat()
                
                try:
                    # Get the latest image from the camera
                    webcam_data = get_base64_of_webcam_image(camera['url'])
                    
                    if webcam_data and 'image' in webcam_data:
                        # Store the image first
                        image_data = {
                            'timestamp': current_time,
                            'image': webcam_data['image']
                        }
                        update_camera_image(camera_id, image_data)
                        
                        # Process the image for fire detection
                        detection_result = process_base64_image(webcam_data['image'])
                        
                        if detection_result:
                            # Update the camera status
                            status_data = {
                                'timestamp': current_time,
                                'fire_detected': detection_result['class'] == 'Fire',
                                'confidence': float(detection_result['confidence']),
                                'error': None
                            }
                            
                            if update_camera_status(camera_id, status_data):
                                logger.info(
                                    f"Updated camera {camera_title}: "
                                    f"Fire {'detected' if detection_result['class'] == 'Fire' else 'not detected'} "
                                    f"(Confidence: {detection_result['confidence']:.2%})"
                                )
                        else:
                            # Update with processing error
                            error_status = {
                                'timestamp': current_time,
                                'fire_detected': False,
                                'confidence': 0.0,
                                'error': 'Failed to process image'
                            }
                            update_camera_status(camera_id, error_status)
                            logger.warning(f"No detection result for camera {camera_title}")
                    else:
                        # Update with image retrieval error
                        error_status = {
                            'timestamp': current_time,
                            'fire_detected': False,
                            'confidence': 0.0,
                            'error': 'No image data available'
                        }
                        update_camera_status(camera_id, error_status)
                        logger.warning(f"No image data for camera {camera_title}")
                        
                except Exception as e:
                    # Update with general error
                    error_status = {
                        'timestamp': current_time,
                        'fire_detected': False,
                        'confidence': 0.0,
                        'error': str(e)
                    }
                    update_camera_status(camera_id, error_status)
                    logger.error(f"Error processing camera {camera_title}: {str(e)}")
                    continue
                    
            except Exception as e:
                logger.error(f"Error processing camera {camera_title}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error in process_all_cameras: {str(e)}") 