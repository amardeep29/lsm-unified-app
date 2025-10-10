"""
Create a SIGNED upload preset that allows folder parameter
This is simpler and more reliable than dynamic signature generation
"""

import os
import requests

# Load credentials
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
api_key = os.environ.get('CLOUDINARY_API_KEY')
api_secret = os.environ.get('CLOUDINARY_API_SECRET')

preset_name = 'client_onboarding_signed'

print(f"Creating SIGNED upload preset: {preset_name}")
print("This preset will be SIGNED (not unsigned) which allows folder parameter")

# Create new SIGNED preset
url = f"https://api.cloudinary.com/v1_1/{cloud_name}/upload_presets"

preset_data = {
    "name": preset_name,
    "unsigned": False,  # SIGNED preset
    "folder": "",  # Empty = allows dynamic folder
    "use_filename": True,
    "unique_filename": True,
    "overwrite": False
}

response = requests.post(
    url,
    json=preset_data,
    auth=(api_key, api_secret)
)

if response.status_code == 200:
    print(f"\n✅ SUCCESS! Created SIGNED preset: {preset_name}")
    print(f"\nNow update .env to use this preset:")
    print(f"CLOUDINARY_UPLOAD_PRESET={preset_name}")
elif response.status_code == 409:
    print(f"\n⚠️  Preset already exists. That's OK!")
    print(f"CLOUDINARY_UPLOAD_PRESET={preset_name}")
else:
    print(f"\n❌ Failed: {response.status_code}")
    print(response.text)
