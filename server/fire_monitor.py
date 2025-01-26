import time
import schedule
from connect import db
from video_processing import process_base64_image
from nps import get_base64_of_webcam_image
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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