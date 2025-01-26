from twilio.rest import Client
from dotenv import load_dotenv
import os
from resources import get_emergency_places
import json
from datetime import datetime

load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
EMERGENCY_PHONE_NUMBER = os.environ.get("EMERGENCY_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def format_emergency_resources(resources):
    """Format emergency resources into a speakable message"""
    message_parts = []
    
    # Add hospitals
    if resources.get("hospitals"):
        nearest_hospital = resources["hospitals"][0]
        message_parts.append(f"The nearest hospital is {nearest_hospital['name']}, {nearest_hospital['dist']} kilometers away at {nearest_hospital['address']}")
    
    # Add fire stations
    if resources.get("fire_stations"):
        nearest_station = resources["fire_stations"][0]
        message_parts.append(f"The nearest fire station is {nearest_station['name']}, {nearest_station['dist']} kilometers away at {nearest_station['address']}")
    
    # Add shelters
    if resources.get("shelters"):
        nearest_shelter = resources["shelters"][0]
        message_parts.append(f"The nearest shelter is {nearest_shelter['name']}, {nearest_shelter['dist']} kilometers away at {nearest_shelter['address']}")
    
    return ". ".join(message_parts)

def make_emergency_call(phone_number=None, camera_name="Unknown Camera", lat=0, lon=0):
    """Make an emergency call to the specified phone number or default emergency number"""
    try:
        # Use provided phone number or fall back to emergency number from .env
        target_number = phone_number if phone_number else EMERGENCY_PHONE_NUMBER
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Get emergency resources within 10 mile radius
        resources = get_emergency_places(lat, lon, 10)
        
        # Format the message
        resource_message = format_emergency_resources(resources)
        alert_message = f"""This is a critical fire alert notification. Fire has been detected on camera {camera_name} at {current_time}. {resource_message}. Press any key to acknowledge this alert."""
        
        # Create TwiML with voice parameters and gather input
        twiml = f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <Response>
                <Say voice="alice" language="en-US">{alert_message}</Say>
                <Pause length="1"/>
                <Gather numDigits="1" timeout="10"/>
            </Response>
        """
        
        # Make the call with status callback
        call = client.calls.create(
            twiml=twiml,
            to=target_number,
            from_=TWILIO_PHONE_NUMBER,
            method='POST',
            status_callback='https://demo.twilio.com/welcome/voice/',
            status_callback_method='POST'
        )
        
        print(f"Emergency call initiated: {call.sid}")
        return True
        
    except Exception as e:
        print(f"Error making emergency call: {e}")
        return False 