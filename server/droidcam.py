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
import asyncio
from ws_manager import manager

# Global variables
cameras = {}  # Store multiple camera instances
model = None

class DroidCamera:
    def __init__(self, camera_id, video_url):
        self.camera_id = camera_id
        self.video_url = video_url
        self.video_capture = None
        self.is_running = True
        self.frame = None
        self.frame_queue = Queue(maxsize=1)
        self.last_fire_detection = None
        self.recheck_interval = 60  # 1 minute between checks if fire detected
        self.detection_thread = None
        self.read_thread = None

    def start(self):
        """Start camera threads."""
        try:
            self.video_capture = cv2.VideoCapture(self.video_url)
            if not self.video_capture.isOpened():
                raise RuntimeError(f"Could not open camera feed at {self.video_url}")

            # Set camera properties
            self.video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            # Start threads
            self.detection_thread = threading.Thread(target=self._detection_worker, daemon=True)
            self.read_thread = threading.Thread(target=self._read_frames, daemon=True)
            
            self.detection_thread.start()
            self.read_thread.start()
            return True
        except Exception as e:
            print(f"Error starting camera {self.camera_id}: {e}")
            return False

    def stop(self):
        """Stop camera threads."""
        self.is_running = False
        if self.video_capture:
            self.video_capture.release()

    def _read_frames(self):
        """Continuously read frames."""
        frame_count = 0
        frame_skip = 2  # Process every nth frame

        while self.is_running:
            if self.video_capture and self.video_capture.isOpened():
                ret, current_frame = self.video_capture.read()
                if ret:
                    self.frame = current_frame
                    frame_count += 1
                    if frame_count % frame_skip == 0:
                        if not self.frame_queue.full():
                            self.frame_queue.put(current_frame)
                        else:
                            try:
                                self.frame_queue.get_nowait()
                                self.frame_queue.put(current_frame)
                            except:
                                pass
                else:
                    # Try to reconnect
                    time.sleep(5)
                    self.video_capture = cv2.VideoCapture(self.video_url)
            else:
                time.sleep(5)
                self.video_capture = cv2.VideoCapture(self.video_url)

    async def _update_fire_status(self, fire_detected: bool, confidence: float):
        """Update fire detection status in MongoDB and broadcast via WebSocket."""
        try:
            current_time = datetime.utcnow()
            
            # Update MongoDB
            update_result = db.user_cctv.update_one(
                {"_id": self.camera_id},
                {
                    "$set": {
                        "last_checked": current_time,
                        "fire_detected": fire_detected,
                        "confidence": confidence,
                        "last_alert": current_time if fire_detected else None
                    }
                }
            )
            
            # Get camera data for WebSocket broadcast
            camera_data = db.user_cctv.find_one({"_id": self.camera_id})
            if camera_data:
                # Broadcast update via WebSocket
                await manager.broadcast_fire_status(camera_data)
                
            if fire_detected:
                self.last_fire_detection = current_time
                print(f"Fire alert for camera {self.camera_id}! Will recheck in {self.recheck_interval} seconds")
            
        except Exception as e:
            print(f"Error updating fire status: {e}")

    def _should_check_fire(self):
        """Determine if we should check for fire based on the detection cycle."""
        if self.last_fire_detection is None:
            return True
            
        time_since_detection = (datetime.utcnow() - self.last_fire_detection).total_seconds()
        return time_since_detection >= self.recheck_interval

    def _detection_worker(self):
        """Worker thread for fire detection."""
        last_detection_time = 0
        min_detection_interval = 0.1  # Minimum time between detections

        while self.is_running:
            try:
                current_time = time.time()
                if current_time - last_detection_time < min_detection_interval:
                    time.sleep(0.01)
                    continue

                if not self._should_check_fire():
                    time.sleep(1)
                    continue

                if self.frame_queue.empty():
                    continue
                    
                frame_to_process = self.frame_queue.get_nowait()
                fire_detected, confidence = detect_fire(frame_to_process)
                
                # Use asyncio to run the coroutine
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._update_fire_status(fire_detected, confidence))
                loop.close()
                
                last_detection_time = current_time
                
            except Exception as e:
                print(f"Error in detection worker: {e}")
                time.sleep(1)

    def get_frame(self):
        """Get current frame for streaming."""
        return self.frame

def load_model():
    """Load the fire detection model."""
    global model
    try:
        # Initialize model with proper weights parameter
        model = models.inception_v3(weights=None, init_weights=True)
        model.fc = torch.nn.Linear(model.fc.in_features, 3)
        state_dict = torch.load('inception_final.pth', map_location=torch.device('cpu'), weights_only=True)
        model.load_state_dict(state_dict)
        model.eval()
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def detect_fire(frame):
    """Detect fire in the given frame."""
    if model is None:
        return False, 0.0
    
    try:
        with torch.no_grad():
            input_batch = preprocess_frame(frame)
            output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            
            # Get probability for fire class
            fire_prob = probabilities[0].item()
            
            return fire_prob > 0.5, fire_prob
            
    except Exception as e:
        print(f"Error in fire detection: {e}")
    
    return False, 0.0

def preprocess_frame(frame):
    """Preprocess frame for model inference."""
    transform = transforms.Compose([
        transforms.Resize((299, 299)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    input_tensor = transform(pil_image)
    input_batch = input_tensor.unsqueeze(0)
    
    return input_batch

def initialize_droidcam(video_url, camera_id):
    """Initialize DroidCam feed."""
    global cameras
    
    try:
        # Load model if not loaded
        if model is None and not load_model():
            raise RuntimeError("Failed to load fire detection model")
            
        # Create and start new camera instance
        camera = DroidCamera(camera_id, video_url)
        if camera.start():
            cameras[str(camera_id)] = camera
            return True
            
        return False
        
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return False

def cleanup():
    """Cleanup all camera resources."""
    for camera in cameras.values():
        camera.stop()
    cameras.clear()

def generate_frames(camera_id):
    """Generate frames for video streaming."""
    camera = cameras.get(str(camera_id))
    if not camera:
        return
        
    while camera.is_running:
        frame = camera.get_frame()
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')