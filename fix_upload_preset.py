"""
Update the upload preset to properly handle dynamic folders
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

print(f"Updating upload preset: {preset_name}")

# Update preset with proper folder handling
url = f"https://api.cloudinary.com/v1_1/{cloud_name}/upload_presets/{preset_name}"

# Configuration that allows dynamic folder specification
preset_data = {
    "unsigned": True,
    "folder": "",  # Empty = allows dynamic folder from widget
    "use_filename": True,
    "unique_filename": True,
    "overwrite": False,
    "disallow_public_id": False  # Allow custom folder paths
}

response = requests.put(
    url,
    json=preset_data,
    auth=(api_key, api_secret)
)

if response.status_code == 200:
    print(f"\n✅ Upload preset updated successfully!")
    result = response.json()
    print(f"\nPreset configuration:")
    print(f"  Name: {result.get('name')}")
    print(f"  Unsigned: {result.get('unsigned')}")
    print(f"  Folder: '{result.get('folder')}' (empty = dynamic)")
    print(f"  Use filename: {result.get('use_filename')}")
    print(f"  Disallow public_id: {result.get('disallow_public_id')}")
else:
    print(f"\n❌ Failed to update preset")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
