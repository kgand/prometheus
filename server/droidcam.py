import cv2
import threading
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from torchvision import models
from queue import Queue
import time
from datetime import datetime, timedelta
from connect import db

# Global variables
video_capture = None
frame = None
model = None
is_running = True
frame_queue = Queue(maxsize=1)  # Only keep latest frame
latest_detection = None
detection_thread = None
current_camera_id = None  # Store current camera ID
last_fire_detection = None  # Track when fire was last detected
recheck_interval = 60  # Seconds to wait before rechecking after fire detection

def load_model():
    """Load the fire detection model."""
    global model
    try:
        # Initialize the model architecture with 3 classes to match saved weights
        model = models.inception_v3(pretrained=False)
        model.fc = torch.nn.Linear(model.fc.in_features, 3)  # Match the saved model's 3 classes
        # Load the trained weights
        state_dict = torch.load('inception_final.pth', map_location=torch.device('cpu'), weights_only=True)
        model.load_state_dict(state_dict)
        model.eval()
    except Exception as e:
        print(f"Error loading model: {e}")
        return False
    return True

def preprocess_frame(frame):
    """Preprocess frame for model inference."""
    transform = transforms.Compose([
        transforms.Resize((299, 299)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Convert BGR to RGB and to PIL Image
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    
    # Apply transformations
    input_tensor = transform(pil_image)
    input_batch = input_tensor.unsqueeze(0)
    
    return input_batch

def update_fire_status(camera_id, fire_detected):
    """Update fire detection status in MongoDB."""
    global last_fire_detection
    try:
        current_time = datetime.utcnow()
        
        # Update the document with just fire status
        db.user_cctv.update_one(
            {"_id": camera_id},
            {
                "$set": {
                    "last_checked": current_time,
                    "fire_detected": fire_detected,
                    "last_alert": current_time if fire_detected else None
                }
            }
        )
        
        # Update last fire detection time if fire is detected
        if fire_detected:
            last_fire_detection = current_time
            print(f"Fire alert set! Will recheck in {recheck_interval} seconds")
        else:
            print("No fire detected, status reset to false")
            
    except Exception as e:
        print(f"Error updating MongoDB: {e}")

def should_check_for_fire():
    """Determine if we should check for fire based on the detection cycle."""
    global last_fire_detection
    
    # If we haven't detected fire yet, or if it's been more than recheck_interval since last detection
    if last_fire_detection is None:
        return True
        
    time_since_detection = (datetime.utcnow() - last_fire_detection).total_seconds()
    return time_since_detection >= recheck_interval

def detect_fire(frame):
    """Detect fire in the given frame."""
    if model is None or current_camera_id is None:
        return False
    
    try:
        # Check if we should perform detection based on the cycle
        if not should_check_for_fire():
            return latest_detection  # Return last detection result
            
        with torch.no_grad():
            input_batch = preprocess_frame(frame)
            output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            
            # Get probability for fire class (assuming class 1 is fire)
            fire_prob = probabilities[1].item()  # Index 1 for fire class
            
            # Update MongoDB with detection results (just true/false)
            fire_detected = fire_prob > 0.5
            update_fire_status(current_camera_id, fire_detected)
            
            # Only print if fire is detected
            if fire_detected:
                print("Fire detected!")
            return fire_detected
            
    except Exception as e:
        print(f"Error in fire detection: {e}")
    
    return False

def detection_worker():
    """Worker thread for fire detection."""
    global latest_detection
    last_detection_time = 0
    min_detection_interval = 0.1  # Minimum time between detections in seconds

    while is_running:
        try:
            current_time = time.time()
            if current_time - last_detection_time < min_detection_interval:
                time.sleep(0.01)  # Short sleep to prevent CPU overload
                continue

            # Get the latest frame, skip if queue is empty
            if frame_queue.empty():
                continue
                
            frame_to_process = frame_queue.get_nowait()
            latest_detection = detect_fire(frame_to_process)
            last_detection_time = current_time
            
        except Exception:
            continue

def initialize_droidcam(video_url, camera_id):
    """Initialize DroidCam feed."""
    global video_capture, detection_thread, current_camera_id
    try:
        video_capture = cv2.VideoCapture(video_url)
        if not video_capture.isOpened():
            raise RuntimeError(f"Could not open camera feed at {video_url}")
        
        current_camera_id = camera_id
        
        # Set camera properties for better performance
        video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer size
        
        # Load the fire detection model
        if not load_model():
            raise RuntimeError("Failed to load fire detection model")
        
        # Start detection thread
        detection_thread = threading.Thread(target=detection_worker, daemon=True)
        detection_thread.start()
        
        # Start frame reading thread
        threading.Thread(target=read_frames, daemon=True).start()
        return True
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return False

def cleanup():
    """Cleanup resources."""
    global is_running, video_capture
    is_running = False
    if video_capture:
        video_capture.release()

def read_frames():
    """Continuously read and process frames from the DroidCam feed."""
    global frame, is_running
    frame_count = 0
    frame_skip = 2  # Process every nth frame

    while is_running:
        if video_capture and video_capture.isOpened():
            ret, current_frame = video_capture.read()
            if ret:
                frame = current_frame  # Update display frame immediately
                
                # Only process every nth frame for detection
                frame_count += 1
                if frame_count % frame_skip == 0:
                    # Update frame queue, dropping old frame if necessary
                    if not frame_queue.full():
                        frame_queue.put(current_frame)
                    else:
                        try:
                            frame_queue.get_nowait()  # Remove old frame
                            frame_queue.put(current_frame)  # Add new frame
                        except Exception:
                            pass
            else:
                break
        else:
            break

def get_frame():
    """Get the current frame."""
    return frame

def generate_frames():
    """Generate frames for video streaming."""
    while is_running:
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')