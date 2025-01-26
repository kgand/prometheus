import cv2
import threading
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from torchvision import models

# Global variables
video_capture = None
frame = None
model = None
is_running = True

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
    except Exception as e:
        print(f"Error in fire detection: {e}")
    
    return False