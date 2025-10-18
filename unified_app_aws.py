#!/usr/bin/env python3
"""
Unified Application Server - All Services in One Place
Combines Flask API + Streamlit Apps + HTML Pages
"""

import os
import sys
import subprocess
import time
import signal
import atexit
from flask import Flask, request, jsonify, send_from_directory, render_template_string, redirect
from threading import Thread
import requests

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from nano_banana_client import NanoBananaClient

# Optional: Cloudinary support
try:
    from cloudinary_utils import CloudinaryManager
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("Warning: Cloudinary not available.")

app = Flask(__name__)

# Global state for subprocess management
streamlit_processes = {}
nano_client = None
cloudinary_client = None

# ============================================================================
# SUBPROCESS MANAGEMENT
# ============================================================================

def start_streamlit_app(name, script, port):
    """Start a Streamlit app as a subprocess"""
    try:
        env = os.environ.copy()
        env['API_SERVER_URL'] = f'http://localhost:{os.getenv("PORT", 5001)}'

        process = subprocess.Popen(
            [
                sys.executable, '-m', 'streamlit', 'run',
                script,
                '--server.port', str(port),
                '--server.headless', 'true',
                '--server.address', 'localhost',
                '--browser.serverAddress', 'localhost'
            ],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        streamlit_processes[name] = process
        print(f"✅ Started {name} on port {port}")
        return True
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return False

def stop_all_streamlit_apps():
    """Stop all Streamlit subprocesses"""
    for name, process in streamlit_processes.items():
        try:
            process.terminate()
            process.wait(timeout=5)
            print(f"✅ Stopped {name}")
        except Exception as e:
            print(f"⚠️ Error stopping {name}: {e}")
            try:
                process.kill()
            except:
                pass

# Register cleanup on exit
atexit.register(stop_all_streamlit_apps)

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n🛑 Shutting down all services...")
    stop_all_streamlit_apps()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================================
# CLIENT INITIALIZATION
# ============================================================================

def initialize_clients():
    """Initialize Nano Banana and Cloudinary clients"""
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

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

MAIN_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loudspeaker Marketing - Image Playground</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #06070B;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            width: 100%;
            background: #06070B;
            border-radius: 0;
            overflow: hidden;
        }

        header {
            background: #06070B;
            color: #E6E6E6;
            padding: 60px 40px;
            text-align: center;
            border-bottom: 1px solid rgba(231, 254, 58, 0.1);
        }

        h1 {
            font-size: 3rem;
            margin-bottom: 15px;
            font-weight: bold;
            color: #E6E6E6;
        }

        .subtitle {
            font-size: 1.2rem;
            color: #E6E6E6;
            opacity: 0.8;
        }

        .services {
            padding: 60px 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }

        .service-card {
            background: #272F35;
            border-radius: 12px;
            padding: 35px;
            transition: all 0.3s;
            border: 1px solid rgba(231, 254, 58, 0.15);
        }

        .service-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(231, 254, 58, 0.15);
            border-color: #E7FE3A;
        }

        .service-icon {
            font-size: 3rem;
            margin-bottom: 20px;
        }

        .service-title {
            font-size: 1.6rem;
            color: #E6E6E6;
            margin-bottom: 15px;
            font-weight: bold;
        }

        .service-description {
            color: #B0B0B0;
            margin-bottom: 25px;
            line-height: 1.6;
        }

        .service-button {
            display: inline-block;
            background: #E7FE3A;
            color: #06070B;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }

        .service-button::after {
            content: " →";
        }

        .service-button:hover {
            background: #d4eb25;
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(231, 254, 58, 0.4);
        }

        .api-section {
            background: #272F35;
            padding: 40px;
            border-top: 1px solid rgba(231, 254, 58, 0.1);
            margin: 0 40px 40px 40px;
            border-radius: 12px;
        }

        .api-title {
            font-size: 1.4rem;
            color: #E6E6E6;
            margin-bottom: 20px;
            font-weight: bold;
        }

        .api-links {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .api-link {
            background: #06070B;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            color: #E7FE3A;
            font-weight: 600;
            border: 1px solid rgba(231, 254, 58, 0.3);
            transition: all 0.3s;
        }

        .api-link:hover {
            background: #E7FE3A;
            color: #06070B;
            transform: translateY(-2px);
        }

        footer {
            background: #06070B;
            color: #E6E6E6;
            padding: 30px;
            text-align: center;
            border-top: 1px solid rgba(231, 254, 58, 0.1);
        }

        footer p {
            opacity: 0.7;
        }

        footer p:first-child {
            opacity: 1;
            margin-bottom: 10px;
        }

        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #E7FE3A;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            .services { padding: 30px 20px; }
            .api-section { padding: 25px; margin: 0 20px 30px 20px; }
            header { padding: 40px 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📢 Loudspeaker Marketing</h1>
            <p class="subtitle">Image Playground - All Services in One Place</p>
        </header>

        <div class="services">
            <div class="service-card">
                <div class="service-icon">🎨</div>
                <h2 class="service-title">Image Studio</h2>
                <p class="service-description">
                    Generate and edit images using AI. Create stunning visuals with text prompts or modify existing images.
                </p>
                <a href="http://localhost:{{ studio_port }}" class="service-button" target="_blank">
                    Open Studio
                </a>
            </div>

            <div class="service-card">
                <div class="service-icon">📋</div>
                <h2 class="service-title">Client Onboarding</h2>
                <p class="service-description">
                    Onboard new clients with folder creation, image uploads, and labeling. Complete 5-step workflow.
                </p>
                <a href="http://localhost:{{ onboarding_port }}" class="service-button" target="_blank">
                    Start Onboarding
                </a>
            </div>

            <div class="service-card">
                <div class="service-icon">📤</div>
                <h2 class="service-title">Upload Images</h2>
                <p class="service-description">
                    Standalone image upload page. Drag and drop images directly to Cloudinary client folders.
                </p>
                <a href="/upload" class="service-button">
                    Upload Images
                </a>
            </div>

            <div class="service-card">
                <div class="service-icon">📝</div>
                <h2 class="service-title">Label Images</h2>
                <p class="service-description">
                    Label uploaded images with product names. Download organized label files for processing.
                </p>
                <a href="/label-images" class="service-button">
                    Label Images
                </a>
            </div>
        </div>

        <div class="api-section">
            <h3 class="api-title">
                <span class="status-indicator"></span>
                API Endpoints
            </h3>
            <div class="api-links">
                <a href="/api/docs" class="api-link">📚 API Docs</a>
                <a href="/health" class="api-link">🏥 Health Check</a>
                <a href="/api/generate" class="api-link">🎨 Generate</a>
                <a href="/api/edit" class="api-link">✏️ Edit</a>
            </div>
        </div>

        <footer>
            <p>Powered by Nano Banana (Gemini 2.5 Flash) + Cloudinary + Streamlit</p>
            <p style="font-size: 0.9rem; margin-top: 5px;">
                All services running on unified server
            </p>
        </footer>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard"""
    # Get the base URL - use PUBLIC_URL for AWS deployment, or localhost for local
    public_url = os.environ.get('PUBLIC_URL', '')
    studio_port = int(os.environ.get('STUDIO_PORT', 8502))
    onboarding_port = int(os.environ.get('ONBOARDING_PORT', 8501))

    if public_url:
        # AWS/Production: Use public URL with ports or nginx proxy paths
        use_nginx = os.environ.get('USE_NGINX', 'false').lower() == 'true'
        if use_nginx:
            # Nginx reverse proxy setup
            studio_url = f"{public_url}/studio"
            onboarding_url = f"{public_url}/onboarding"
        else:
            # Direct port access
            studio_url = f"{public_url}:{studio_port}"
            onboarding_url = f"{public_url}:{onboarding_port}"
    else:
        # Local development
        studio_url = f"http://localhost:{studio_port}"
        onboarding_url = f"http://localhost:{onboarding_port}"

    # Update the HTML template to use these URLs
    html = MAIN_DASHBOARD_HTML.replace(
        'href="http://localhost:{{ studio_port }}"',
        f'href="{studio_url}"'
    ).replace(
        'href="http://localhost:{{ onboarding_port }}"',
        f'href="{onboarding_url}"'
    )

    return render_template_string(html)

# ============================================================================
# API ENDPOINTS (from api_server.py)
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'nano_banana': 'ready' if nano_client else 'not initialized',
        'cloudinary': 'ready' if cloudinary_client else 'not available',
        'services': {
            'image_studio': f"http://localhost:{os.environ.get('STUDIO_PORT', 8502)}",
            'onboarding': f"http://localhost:{os.environ.get('ONBOARDING_PORT', 8501)}"
        }
    })

@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API documentation"""
    return jsonify({
        'name': 'Loudspeaker Marketing - Unified API',
        'version': '3.0.0',
        'description': 'Unified API server with all services in one place',
        'endpoints': {
            '/': 'Main dashboard with navigation to all services',
            '/health': 'Health check endpoint',
            '/api/generate': 'Generate images from text prompts',
            '/api/edit': 'Edit images with text instructions',
            '/api/check-client': 'Check if client folder exists',
            '/api/create-client-folders': 'Create client folder structure',
            '/api/get-client-images': 'Get list of images for a client',
            '/api/get-upload-config': 'Get Cloudinary upload configuration',
            '/upload': 'Image upload page',
            '/label-images': 'Image labeling page'
        }
    })

# Import all API routes from api_server.py logic
# (We'll copy the relevant endpoints)

from PIL import Image
from io import BytesIO
import tempfile

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """Generate an image from a text prompt"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: prompt'}), 400

        prompt = data['prompt']
        client_folder = data.get('client_folder')

        if cloudinary_client and client_folder is None:
            return jsonify({'success': False, 'error': 'Missing required field: client_folder'}), 400

        generated_image = nano_client.generate_image(prompt=prompt, save_to_disk=False)

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
                return jsonify({'success': False, 'error': f"Failed to upload: {upload_result.get('error')}"}), 500
        else:
            img_bytes = BytesIO()
            generated_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            import base64
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            return jsonify({'success': True, 'image_base64': img_base64, 'format': 'png', 'prompt': prompt})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/edit', methods=['POST'])
def edit_image():
    """Edit an image using a text prompt"""
    try:
        data = request.get_json()
        if not data or 'image_url' not in data or 'prompt' not in data:
            return jsonify({'success': False, 'error': 'Missing required fields: image_url and prompt'}), 400

        image_url = data['image_url']
        prompt = data['prompt']
        client_folder = data.get('client_folder')

        if cloudinary_client and client_folder is None:
            return jsonify({'success': False, 'error': 'Missing required field: client_folder'}), 400

        edited_image = nano_client.edit_image(
            image_path="",
            prompt=prompt,
            save_to_disk=False,
            image_url=image_url
        )

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
                return jsonify({'success': False, 'error': f"Failed to upload: {upload_result.get('error')}"}), 500
        else:
            img_bytes = BytesIO()
            edited_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            import base64
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            return jsonify({'success': True, 'image_base64': img_base64, 'format': 'png', 'prompt': prompt, 'original_url': image_url})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/check-client', methods=['POST'])
def check_client():
    """Check if a client folder exists"""
    try:
        data = request.get_json()
        if not data or 'client_name' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: client_name'}), 400

        client_name = data['client_name'].strip()
        import re
        if not re.match(r'^[a-zA-Z0-9-]+$', client_name):
            return jsonify({'success': False, 'error': 'Client name can only contain letters, numbers, and hyphens'}), 400

        if len(client_name) < 3 or len(client_name) > 50:
            return jsonify({'success': False, 'error': 'Client name must be between 3 and 50 characters'}), 400

        if cloudinary_client:
            result = cloudinary_client.check_client_exists(client_name)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Cloudinary not configured'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create-client-folders', methods=['POST'])
def create_client_folders():
    """Create folder structure for a new client"""
    try:
        data = request.get_json()
        if not data or 'client_name' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: client_name'}), 400

        client_name = data['client_name'].strip()
        import re
        if not re.match(r'^[a-zA-Z0-9-]+$', client_name):
            return jsonify({'success': False, 'error': 'Client name can only contain letters, numbers, and hyphens'}), 400

        if cloudinary_client:
            result = cloudinary_client.create_client_folders(client_name)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Cloudinary not configured'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-upload-config', methods=['POST'])
def get_upload_config():
    """Get Cloudinary upload configuration"""
    try:
        data = request.get_json()
        if not data or 'client_name' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: client_name'}), 400

        client_name = data['client_name'].strip()

        if cloudinary_client:
            result = cloudinary_client.get_upload_config(client_name)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Cloudinary not configured'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-client-images', methods=['GET'])
def get_client_images():
    """Get list of images for a client"""
    try:
        client_name = request.args.get('client')
        if not client_name:
            return jsonify({'success': False, 'error': 'Missing required parameter: client'}), 400

        if cloudinary_client:
            result = cloudinary_client.list_images(
                folder_type="input",
                max_results=100,
                client_folder=client_name
            )

            if result.get('success'):
                images = [img.get('secure_url') for img in result.get('images', [])]
                return jsonify({'success': True, 'client': client_name, 'images': images, 'total_count': len(images)})
            else:
                return jsonify({'success': False, 'error': result.get('error', 'Failed to list images')}), 500
        else:
            return jsonify({'success': False, 'error': 'Cloudinary not configured'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-all-folders', methods=['GET'])
def get_all_folders():
    """Get all client folders from Cloudinary"""
    try:
        if cloudinary_client:
            result = cloudinary_client.list_client_folders()

            if result.get('success'):
                folders = result.get('folders', [])
                return jsonify({'success': True, 'folders': folders})
            else:
                return jsonify({'success': False, 'error': result.get('error', 'Failed to list folders')}), 500
        else:
            return jsonify({'success': False, 'error': 'Cloudinary not configured'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-signature', methods=['POST'])
def generate_signature():
    """Generate Cloudinary upload signature"""
    try:
        import cloudinary.utils
        data = request.get_json()
        folder = data.get('folder', '')
        params_to_sign = data.get('params_to_sign', {})

        if 'folder' not in params_to_sign:
            params_to_sign['folder'] = folder
        if 'timestamp' not in params_to_sign:
            params_to_sign['timestamp'] = int(time.time())

        signature = cloudinary.utils.api_sign_request(
            params_to_sign,
            os.getenv('CLOUDINARY_API_SECRET')
        )

        return jsonify({
            'signature': signature,
            'timestamp': params_to_sign['timestamp'],
            'api_key': os.getenv('CLOUDINARY_API_KEY')
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# HTML PAGES
# ============================================================================

@app.route('/upload', methods=['GET'])
def upload_page():
    """Serve upload page"""
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'upload_simple.html')
        with open(template_path, 'r') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to load upload page: {str(e)}'}), 500

@app.route('/label-images', methods=['GET'])
def label_images_page():
    """Serve label images page"""
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'label_images.html')
        with open(template_path, 'r') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to load label images page: {str(e)}'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize clients
    try:
        initialize_clients()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)

    # Get ports from environment
    port = int(os.environ.get('PORT', 5001))
    studio_port = int(os.environ.get('STUDIO_PORT', 8502))
    onboarding_port = int(os.environ.get('ONBOARDING_PORT', 8501))

    # Start Streamlit apps in background
    print("\n🚀 Starting Streamlit Services...")
    start_streamlit_app('Image Studio', 'app.py', studio_port)
    start_streamlit_app('Client Onboarding', 'client_onboarding.py', onboarding_port)

    # Wait for Streamlit apps to start
    time.sleep(3)

    print(f"\n{'='*60}")
    print(f"🎉 UNIFIED APPLICATION RUNNING")
    print(f"{'='*60}")
    print(f"\n📊 Main Dashboard: http://localhost:{port}/")
    print(f"🎨 Image Studio: http://localhost:{studio_port}/")
    print(f"📋 Client Onboarding: http://localhost:{onboarding_port}/")
    print(f"📚 API Docs: http://localhost:{port}/api/docs")
    print(f"🏥 Health Check: http://localhost:{port}/health")
    print(f"\n{'='*60}\n")

    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
