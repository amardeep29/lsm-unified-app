"""
Create an unsigned upload preset in Cloudinary
This script creates the upload preset needed for the client onboarding widget
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get credentials from .env
cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')
preset_name = os.getenv('CLOUDINARY_UPLOAD_PRESET', 'client_onboarding_unsigned')

print(f"Creating unsigned upload preset: {preset_name}")
print(f"Cloud name: {cloud_name}")

# Cloudinary API endpoint
url = f"https://api.cloudinary.com/v1_1/{cloud_name}/upload_presets"

# Preset configuration
preset_data = {
    "name": preset_name,
    "unsigned": True,  # This is the key setting!
    "folder": "",  # Allow dynamic folder specification
    "use_filename": True,
    "unique_filename": True,
    "overwrite": False,
    "tags": "client_onboarding"
}

# Make API request
response = requests.post(
    url,
    json=preset_data,
    auth=(api_key, api_secret)
)

if response.status_code == 200:
    print(f"\n✅ SUCCESS! Upload preset '{preset_name}' created successfully!")
    print(f"\nPreset details:")
    print(response.json())
    print(f"\nYou can now use the upload widget in your application.")
elif response.status_code == 409:
    print(f"\n⚠️  Preset '{preset_name}' already exists.")
    print(f"Checking if it's unsigned...")

    # Get existing preset
    get_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/upload_presets/{preset_name}"
    get_response = requests.get(get_url, auth=(api_key, api_secret))

    if get_response.status_code == 200:
        preset_info = get_response.json()
        if preset_info.get('unsigned'):
            print(f"✅ Preset is already configured as unsigned. You're good to go!")
        else:
            print(f"❌ ERROR: Preset exists but is NOT unsigned.")
            print(f"Please delete it from Cloudinary dashboard and run this script again.")
else:
    print(f"\n❌ ERROR: Failed to create preset")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
