import time
import schedule
from connect import db
from video_processing import process_base64_image
from nps import get_base64_of_webcam_image
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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
                    "confidence": detection_data['confidence']
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
                
                current_time = datetime.utcnow().isoformat()
                
                try:
                    webcam_data = get_base64_of_webcam_image(camera['url'])
                    
                    if webcam_data and 'image' in webcam_data:
                        # Existing processing logic with extended error handling
                        pass
                    else:
                        error_status = {
                            'timestamp': current_time,
                            'fire_detected': False,
                            'confidence': 0.0,
                            'error': 'No image data available'
                        }
                        update_camera_status(camera_id, error_status)
                        logger.warning(f"No image data for camera {camera_title}")
                        
                except Exception as e:
                    error_status = {
                        'timestamp': current_time,
                        'fire_detected': False,
                        'confidence': 0.0,
                        'error': str(e)
                    }
                    update_camera_status(camera_id, error_status)
                    logger.error(f"Error processing camera {camera_title}: {str(e)}")
                    
            except Exception as e:
                logger.error(f"Unexpected error with camera {camera_title}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Critical error in process_all_cameras: {str(e)}")


def main():
    print("Starting fire monitoring service...")
    
    # Schedule the task to run every 5 minutes
    schedule.every(5).minutes.do(process_all_cameras)
    
    # Run immediately on startup
    process_all_cameras()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()