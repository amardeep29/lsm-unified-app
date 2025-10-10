#!/usr/bin/env python3
"""
Flask API Server for n8n Integration with Nano Banana
Accepts image URLs and prompts, returns generated image URLs
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os
import sys
import tempfile
import time
from PIL import Image
from io import BytesIO

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from nano_banana_client import NanoBananaClient

# Optional: Cloudinary support for returning URLs
try:
    from cloudinary_utils import CloudinaryManager
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("Warning: Cloudinary not available. Images will be returned as base64 data.")

app = Flask(__name__)

# Initialize clients
nano_client = None
cloudinary_client = None

def initialize_clients():
    """Initialize Nano Banana and optionally Cloudinary clients"""
    global nano_client, cloudinary_client

    try:
        nano_client = NanoBananaClient()
        print("✅ Nano Banana client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Nano Banana client: {e}")
        raise

    if CLOUDINARY_AVAILABLE:
        try:
            cloudinary_client = CloudinaryManager()
            print("✅ Cloudinary client initialized")
        except Exception as e:
            print(f"⚠️ Cloudinary initialization failed: {e}")
            print("Will return base64 encoded images instead of URLs")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'nano_banana': 'ready' if nano_client else 'not initialized',
        'cloudinary': 'ready' if cloudinary_client else 'not available'
    })

@app.route('/generate', methods=['POST'])
def generate_image():
    """
    Generate an image from a text prompt

    Request JSON:
    {
        "prompt": "A cute robot in a field of flowers",
        "client_folder": "client_name"  // optional, defaults to env variable
    }

    Response JSON:
    {
        "success": true,
        "image_url": "https://res.cloudinary.com/...",
        "public_id": "...",
        "prompt": "...",
        "client_folder": "..."
    }
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: prompt'
            }), 400

        prompt = data['prompt']
        client_folder = data.get('client_folder')  # Optional parameter

        # Validate client_folder if using Cloudinary
        if cloudinary_client and client_folder is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: client_folder (required when using Cloudinary)'
            }), 400

        # Generate image
        print(f"🎨 Generating image for prompt: {prompt[:50]}...")
        if client_folder:
            print(f"📁 Client folder: {client_folder}")

        generated_image = nano_client.generate_image(
            prompt=prompt,
            save_to_disk=False
        )

        # Upload to Cloudinary or return base64
        if cloudinary_client:
            upload_result = cloudinary_client.upload_image(
                image_data=generated_image,
                folder_type="generated",
                filename=f"generated_{int(time.time())}",
                client_folder=client_folder
            )

            if upload_result['success']:
                return jsonify({
                    'success': True,
                    'image_url': upload_result['url'],
                    'public_id': upload_result['public_id'],
                    'prompt': prompt,
                    'client_folder': client_folder
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f"Failed to upload to Cloudinary: {upload_result.get('error')}"
                }), 500
        else:
            # Return base64 encoded image
            img_bytes = BytesIO()
            generated_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            import base64
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

            return jsonify({
                'success': True,
                'image_base64': img_base64,
                'format': 'png',
                'prompt': prompt
            })

    except Exception as e:
        print(f"❌ Error in /generate: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/edit', methods=['POST'])
def edit_image():
    """
    Edit an image using a text prompt

    Request JSON:
    {
        "image_url": "https://example.com/image.jpg",
        "prompt": "Add sunglasses and a hat",
        "client_folder": "client_name"  // optional, defaults to env variable
    }

    Response JSON:
    {
        "success": true,
        "image_url": "https://res.cloudinary.com/...",
        "public_id": "...",
        "prompt": "...",
        "original_url": "...",
        "client_folder": "..."
    }
    """
    try:
        data = request.get_json()

        if not data or 'image_url' not in data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: image_url and prompt'
            }), 400

        image_url = data['image_url']
        prompt = data['prompt']
        client_folder = data.get('client_folder')  # Optional parameter

        # Validate client_folder if using Cloudinary
        if cloudinary_client and client_folder is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: client_folder (required when using Cloudinary)'
            }), 400

        # Edit image
        print(f"✏️ Editing image from URL: {image_url[:50]}...")
        print(f"📝 Edit instruction: {prompt[:50]}...")
        if client_folder:
            print(f"📁 Client folder: {client_folder}")

        edited_image = nano_client.edit_image(
            image_path="",  # Not used when image_url is provided
            prompt=prompt,
            save_to_disk=False,
            image_url=image_url
        )

        # Upload to Cloudinary or return base64
        if cloudinary_client:
            upload_result = cloudinary_client.upload_image(
                image_data=edited_image,
                folder_type="edited",
                filename=f"edited_{int(time.time())}",
                client_folder=client_folder
            )

            if upload_result['success']:
                return jsonify({
                    'success': True,
                    'image_url': upload_result['url'],
                    'public_id': upload_result['public_id'],
                    'prompt': prompt,
                    'original_url': image_url,
                    'client_folder': client_folder
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f"Failed to upload to Cloudinary: {upload_result.get('error')}"
                }), 500
        else:
            # Return base64 encoded image
            img_bytes = BytesIO()
            edited_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            import base64
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

            return jsonify({
                'success': True,
                'image_base64': img_base64,
                'format': 'png',
                'prompt': prompt,
                'original_url': image_url
            })

    except Exception as e:
        print(f"❌ Error in /edit: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check-client', methods=['POST'])
def check_client():
    """
    Check if a client folder exists in Cloudinary

    Request JSON:
    {
        "client_name": "client-abc"
    }

    Response JSON:
    {
        "success": true,
        "exists": true,
        "folder_path": "client-abc",
        "subfolders": ["input", "generated", "edited"]
    }
    """
    try:
        data = request.get_json()

        if not data or 'client_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: client_name'
            }), 400

        client_name = data['client_name'].strip()

        # Validate client name
        import re
        if not re.match(r'^[a-zA-Z0-9-]+$', client_name):
            return jsonify({
                'success': False,
                'error': 'Client name can only contain letters, numbers, and hyphens'
            }), 400

        if len(client_name) < 3 or len(client_name) > 50:
            return jsonify({
                'success': False,
                'error': 'Client name must be between 3 and 50 characters'
            }), 400

        # Check if client exists
        if cloudinary_client:
            result = cloudinary_client.check_client_exists(client_name)
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': 'Cloudinary not configured'
            }), 500

    except Exception as e:
        print(f"❌ Error in /api/check-client: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/create-client-folders', methods=['POST'])
def create_client_folders():
    """
    Create folder structure for a new client

    Request JSON:
    {
        "client_name": "client-abc"
    }

    Response JSON:
    {
        "success": true,
        "folders_created": ["input", "generated", "edited"],
        "folder_path": "client-abc",
        "message": "Successfully created folder structure for client-abc"
    }
    """
    try:
        data = request.get_json()

        if not data or 'client_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: client_name'
            }), 400

        client_name = data['client_name'].strip()

        # Validate client name
        import re
        if not re.match(r'^[a-zA-Z0-9-]+$', client_name):
            return jsonify({
                'success': False,
                'error': 'Client name can only contain letters, numbers, and hyphens'
            }), 400

        if len(client_name) < 3 or len(client_name) > 50:
            return jsonify({
                'success': False,
                'error': 'Client name must be between 3 and 50 characters'
            }), 400

        # Create folders
        if cloudinary_client:
            print(f"📁 Creating folders for client: {client_name}")
            result = cloudinary_client.create_client_folders(client_name)
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': 'Cloudinary not configured'
            }), 500

    except Exception as e:
        print(f"❌ Error in /api/create-client-folders: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get-upload-config', methods=['POST'])
def get_upload_config():
    """
    Get Cloudinary upload configuration for a client

    Request JSON:
    {
        "client_name": "client-abc"
    }

    Response JSON:
    {
        "success": true,
        "cloud_name": "your-cloud",
        "api_key": "your-key",
        "folder": "client-abc/input",
        "upload_preset": "ml_default"
    }
    """
    try:
        data = request.get_json()

        if not data or 'client_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: client_name'
            }), 400

        client_name = data['client_name'].strip()

        # Get upload config
        if cloudinary_client:
            result = cloudinary_client.get_upload_config(client_name)
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': 'Cloudinary not configured'
            }), 500

    except Exception as e:
        print(f"❌ Error in /api/get-upload-config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'name': 'Nano Banana API Server',
        'version': '2.1.0',
        'description': 'API server for n8n integration with Nano Banana image generation and client onboarding',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            '/generate': {
                'method': 'POST',
                'description': 'Generate an image from a text prompt',
                'body': {
                    'prompt': 'Text description of the image to generate (required)',
                    'client_folder': 'Client folder name for Cloudinary organization (required when using Cloudinary)'
                }
            },
            '/edit': {
                'method': 'POST',
                'description': 'Edit an image using a text prompt',
                'body': {
                    'image_url': 'URL of the image to edit (required)',
                    'prompt': 'Text description of the desired edits (required)',
                    'client_folder': 'Client folder name for Cloudinary organization (required when using Cloudinary)'
                }
            },
            '/api/check-client': {
                'method': 'POST',
                'description': 'Check if a client folder exists in Cloudinary',
                'body': {
                    'client_name': 'Client folder name (required)'
                }
            },
            '/api/create-client-folders': {
                'method': 'POST',
                'description': 'Create folder structure for a new client',
                'body': {
                    'client_name': 'Client folder name (required)'
                }
            },
            '/api/get-upload-config': {
                'method': 'POST',
                'description': 'Get Cloudinary upload widget configuration',
                'body': {
                    'client_name': 'Client folder name (required)'
                }
            },
            '/api/get-client-images': {
                'method': 'GET',
                'description': 'Get list of images for a client from input folder',
                'query_params': {
                    'client': 'Client folder name (required)'
                }
            }
        },
        'notes': {
            'client_folder': 'The client_folder parameter determines the Cloudinary folder structure: {client_folder}/{generated|edited}/',
            'cloudinary_optional': 'If Cloudinary is not configured, images will be returned as base64 encoded data instead'
        }
    })

@app.route('/api/generate-signature', methods=['POST'])
def generate_signature():
    """
    Generate Cloudinary upload signature for secure uploads
    This allows the widget to upload to specific folders
    """
    try:
        import cloudinary.utils
        import time
        import hashlib

        data = request.get_json()
        folder = data.get('folder', '')

        # Get parameters to sign from the widget
        params_to_sign = data.get('params_to_sign', {})

        # Add folder to params if not already present
        if 'folder' not in params_to_sign:
            params_to_sign['folder'] = folder

        # Generate timestamp if not provided
        if 'timestamp' not in params_to_sign:
            params_to_sign['timestamp'] = int(time.time())

        print(f"Signing params: {params_to_sign}")

        # Generate signature using Cloudinary's method
        signature = cloudinary.utils.api_sign_request(
            params_to_sign,
            os.getenv('CLOUDINARY_API_SECRET')
        )

        print(f"Generated signature: {signature}")

        return jsonify({
            'signature': signature,
            'timestamp': params_to_sign['timestamp'],
            'api_key': os.getenv('CLOUDINARY_API_KEY')
        })

    except Exception as e:
        print(f"Signature generation error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get-client-images', methods=['GET'])
def get_client_images():
    """
    Get list of images for a specific client from the input folder

    Query Parameters:
        client: Client folder name (required)

    Response JSON:
    {
        "success": true,
        "client": "client-name",
        "images": ["url1", "url2", ...]
    }
    """
    try:
        client_name = request.args.get('client')

        if not client_name:
            return jsonify({
                'success': False,
                'error': 'Missing required parameter: client'
            }), 400

        # Get images from Cloudinary
        if cloudinary_client:
            result = cloudinary_client.list_images(
                folder_type="input",
                max_results=100,
                client_folder=client_name
            )

            if result.get('success'):
                # Extract URLs from resources
                images = [img.get('secure_url') for img in result.get('images', [])]

                return jsonify({
                    'success': True,
                    'client': client_name,
                    'images': images,
                    'total_count': len(images)
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to list images')
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Cloudinary not configured'
            }), 500

    except Exception as e:
        print(f"❌ Error in /api/get-client-images: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/upload', methods=['GET'])
def upload_page():
    """
    Serve the standalone upload HTML page (simple version with direct API upload)
    """
    try:
        # Read the simple HTML template (direct upload, no widget)
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'upload_simple.html')
        with open(template_path, 'r') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to load upload page: {str(e)}'
        }), 500

@app.route('/label-images', methods=['GET'])
def label_images_page():
    """
    Serve the image labeling HTML page
    """
    try:
        # Read the label images HTML template
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'label_images.html')
        with open(template_path, 'r') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to load label images page: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Initialize clients on startup
    try:
        initialize_clients()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("Make sure GOOGLE_AI_API_KEY environment variable is set")
        sys.exit(1)

    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))

    print(f"\n🚀 Nano Banana API Server starting on port {port}")
    print(f"📚 API Documentation: http://localhost:{port}/")
    print(f"🏥 Health Check: http://localhost:{port}/health")
    print(f"🎨 Generate Endpoint: http://localhost:{port}/generate")
    print(f"✏️ Edit Endpoint: http://localhost:{port}/edit")
    print(f"📤 Upload Page: http://localhost:{port}/upload\n")

    app.run(host='0.0.0.0', port=port, debug=False)
