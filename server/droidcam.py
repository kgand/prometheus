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