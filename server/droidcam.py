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