import cv2
import threading
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from torchvision import models
from queue import Queue
import time

# Global variables
video_capture = None
frame = None
model = None
is_running = True
frame_queue = Queue(maxsize=1)  # Only keep latest frame
latest_detection = None
detection_thread = None

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

def detect_fire(frame):
    """Detect fire in the given frame."""
    if model is None:
        return False
    
    try:
        with torch.no_grad():
            input_batch = preprocess_frame(frame)
            output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            
            # Get probability for fire class (assuming class 1 is fire)
            fire_prob = probabilities[1].item()  # Index 1 for fire class
            
            # Only print and return True if fire probability is high enough
            if fire_prob > 0.5:
                print(f"Fire detected with confidence: {fire_prob:.2f}")
                return True
            else:
                print(f"No fire detected with confidence: {fire_prob:.2f}")
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
            if time.time() - last_detection_time < min_detection_interval:
                time.sleep(0.01)  # Short sleep to prevent CPU overload
                continue

            # Get the latest frame, skip if queue is empty
            if frame_queue.empty():
                continue
                
            frame_to_process = frame_queue.get_nowait()
            latest_detection = detect_fire(frame_to_process)
            last_detection_time = time.time()
            
        except Exception:
            continue

def initialize_droidcam(video_url):
    """Initialize DroidCam feed."""
    global video_capture, detection_thread
    try:
        video_capture = cv2.VideoCapture(video_url)
        if not video_capture.isOpened():
            raise RuntimeError(f"Could not open DroidCam feed at {video_url}")
        
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
        print(f"Error initializing DroidCam: {e}")
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