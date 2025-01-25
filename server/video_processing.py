import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import base64
import io
import numpy as np

# Initialize model and transforms (do this only once when module loads)
def load_model():
    # Create the base model first
    model = models.inception_v3(pretrained=False)
    # Modify the final layer for 3 classes to match saved weights
    model.fc = torch.nn.Linear(model.fc.in_features, 3)
    # Load the trained weights
    model.load_state_dict(torch.load('inception_final.pth', map_location=torch.device('cpu'), weights_only=True))
    model.eval()
    return model

def get_transforms():
    return transforms.Compose([
        transforms.Resize((299, 299)),  # InceptionV3 expects 299x299
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

# Global instances
MODEL = load_model()
TRANSFORMS = get_transforms()
CLASS_NAMES = ['Fire', 'Smoke', 'Neutral']  # Original classes

def process_base64_image(base64_string):
    """Process a base64 image and return prediction."""
    try:
        # Decode base64
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess image
        image_tensor = TRANSFORMS(image)
        image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension
        
        # Get prediction
        with torch.no_grad():
            outputs = MODEL(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Combine Smoke and Neutral probabilities
            fire_prob = float(probabilities[0][0])  # Fire probability
            other_prob = float(probabilities[0][1] + probabilities[0][2])  # Smoke + Neutral
            
            # Determine class and confidence
            if fire_prob > other_prob:
                return {
                    'class': 'Fire',
                    'confidence': fire_prob
                }
            else:
                return {
                    'class': 'Neutral',
                    'confidence': other_prob
                }
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None