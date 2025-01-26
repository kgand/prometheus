from twilio.rest import Client
from dotenv import load_dotenv
import os
from resources import get_emergency_places, get_city_from_coordinates
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
EMERGENCY_PHONE_NUMBER = os.environ.get("EMERGENCY_PHONE_NUMBER")

# Initialize Twilio client
try:
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.info("Twilio client initialized successfully")
    else:
        logger.error("Twilio credentials not found in environment variables")
        client = None
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {e}")
    client = None

def format_emergency_resources(resources):
    """Format emergency resources into a speakable message"""
    message_parts = []
    
    # Add hospitals
    if resources.get("hospitals"):
        nearest_hospital = resources["hospitals"][0]
        message_parts.append(f"Nearest hospital: {nearest_hospital['name']}, {nearest_hospital['dist']} kilometers away")
    
    # Add fire stations
    if resources.get("fire_stations"):
        nearest_station = resources["fire_stations"][0]
        message_parts.append(f"Nearest fire station: {nearest_station['name']}, {nearest_station['dist']} kilometers away")
    
    # Add shelters
    if resources.get("shelters"):
        nearest_shelter = resources["shelters"][0]
        message_parts.append(f"Nearest shelter: {nearest_shelter['name']}, {nearest_shelter['dist']} kilometers away")
    
    return ". ".join(message_parts)

def make_emergency_call(to_number, camera_name, latitude=0, longitude=0):
    """Make an emergency call using Twilio."""
    try:
        if not client:
            print("Error: Twilio client not initialized")
            return False

        if not TWILIO_PHONE_NUMBER:
            print("Error: Twilio phone number not configured")
            return False

        # Get city name from coordinates
        city = "Unknown location"
        if latitude != 0 and longitude != 0:
            city = get_city_from_coordinates(latitude, longitude)

        # Get emergency resources within 10 mile radius
        resources = get_emergency_places(latitude, longitude, 10)
        resource_message = format_emergency_resources(resources)
        
        # Construct TTS message with faster rate
        tts_message = f"Alert! Fire detected on CCTV camera in {city}. {resource_message}. Immediate action required."

        print(f"Initiating call from {TWILIO_PHONE_NUMBER} to {to_number}")
        print(f"TTS Message: {tts_message}")

        # Make the call with status callback and faster rate
        call = client.calls.create(
            twiml=f'<Response><Say voice="alice" language="en-US" rate="1.2">{tts_message}</Say><Pause length="1"/><Gather numDigits="1" timeout="10"/></Response>',
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            status_callback='https://demo.twilio.com/welcome/voice/',
            status_callback_method='POST'
        )

        print(f"Call initiated successfully. Call SID: {call.sid}")
        return True

    except Exception as e:
        print(f"Failed to make emergency call: {str(e)}")
        print(f"To: {to_number}, From: {TWILIO_PHONE_NUMBER}")
        # Print Twilio configuration status
        print(f"Twilio Account SID configured: {'Yes' if TWILIO_ACCOUNT_SID else 'No'}")
        print(f"Twilio Auth Token configured: {'Yes' if TWILIO_AUTH_TOKEN else 'No'}")
        print(f"Twilio Phone Number configured: {'Yes' if TWILIO_PHONE_NUMBER else 'No'}")
        return False 