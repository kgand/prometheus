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
        
        for camera in all_cameras:
            camera_id = camera.get('id')
            camera_title = camera.get('title', 'Unknown')
            
            try:
                current_time = datetime.utcnow().isoformat()
                webcam_data = get_base64_of_webcam_image(camera['url'])
                
                if webcam_data and 'image' in webcam_data:
                    # Store the image
                    image_data = {
                        'timestamp': current_time,
                        'image': webcam_data['image']
                    }
                    update_camera_image(camera_id, image_data)
                    
                    # Process for fire detection
                    detection_result = process_base64_image(webcam_data['image'])
                    
                    if detection_result:
                        status_data = {
                            'timestamp': current_time,
                            'fire_detected': detection_result['class'] == 'Fire',
                            'confidence': float(detection_result['confidence'])
                        }
                        update_camera_status(camera_id, status_data)
                        
            except Exception as e:
                logger.error(f"Error processing camera {camera_title}: {str(e)}")
    except Exception as e:
        logger.error(f"Error in process_all_cameras: {str(e)}")
        
def main():
    print("Starting fire monitoring service...")
    
    # Basic scheduling and startup mechanism
    schedule.every(5).minutes.do(process_all_cameras)
    process_all_cameras()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()