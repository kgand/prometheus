from nps import get_base64_of_webcam_image
from rich import print

def test_single_webcam():
    # Test URL - this is an example NPS webcam URL
    test_url = "https://www.nps.gov/media/webcam/view.htm?id=9B5FC6BA-9FE6-EC6B-61637825D562D367" 
    
    try:
        result = get_base64_of_webcam_image(test_url)

        print("\nDetection Results:")
        print("=================")
        print(f"Detected: {result['detection']['class']}")
        print(f"Confidence: {result['detection']['confidence']:.2%}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    print("Testing fire detection...")
    test_single_webcam()