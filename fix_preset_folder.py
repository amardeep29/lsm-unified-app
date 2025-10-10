"""
Fix upload preset to properly support dynamic folder paths
The issue is that unsigned presets need special configuration to accept folder parameters
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
preset_name = os.environ.get('CLOUDINARY_UPLOAD_PRESET')

print(f"Fixing upload preset: {preset_name}")
print(f"Issue: Unsigned presets need 'use_asset_folder_as_public_id_prefix' to respect folder parameter\n")

# Update preset to allow dynamic folders
url = f"https://api.cloudinary.com/v1_1/{cloud_name}/upload_presets/{preset_name}"

preset_data = {
    "unsigned": True,
    "folder": "",  # Empty allows dynamic folder
    "use_filename": True,
    "unique_filename": True,
    "use_asset_folder_as_public_id_prefix": False,  # Don't use asset folder in public_id
    "disallow_public_id": False  # Allow custom paths
}

response = requests.put(
    url,
    json=preset_data,
    auth=(api_key, api_secret)
)

if response.status_code == 200:
    print(f"✅ Preset updated successfully!")
    print(f"\nNow test: Upload an image and check if it goes to client/input/ folder")
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)
