# Unified Architecture Documentation

## Overview

The Loudspeaker Marketing Image Playground has been **refactored into a unified architecture** where all services run from a single entry point.

Previously, you needed to start:
- Flask API server (port 5001)
- Streamlit Onboarding app (port 8501)
- Streamlit Image Studio (port 8502)

**Now**, you start **ONE application** that manages everything!

---

## Architecture Design

```
unified_app.py (Main Process - Port 5001)
├── Flask API Server (HTTP Server)
│   ├── Main Dashboard (/)
│   ├── API Endpoints (/api/*)
│   ├── HTML Pages (/upload, /label-images)
│   └── Health Check (/health)
│
├── Streamlit Image Studio (Subprocess - Port 8502)
│   ├── Image Generation Dashboard
│   ├── Image Editing Interface
│   └── Cloudinary Integration
│
└── Streamlit Client Onboarding (Subprocess - Port 8501)
    ├── 5-Step Onboarding Workflow
    ├── Client Folder Management
    ├── Image Upload Interface
    └── Links to Label Images Page
```

---

## Quick Start

### **Option 1: Using the Start Script (Recommended)**

```bash
./start.sh
```

That's it! Everything starts automatically.

### **Option 2: Manual Start**

```bash
# Activate virtual environment
source venv/bin/activate

# Start unified application
python unified_app.py
```

---

## Accessing Services

Once started, you'll see:

```
============================================================
🎉 UNIFIED APPLICATION RUNNING
============================================================

📊 Main Dashboard: http://localhost:5001/
🎨 Image Studio: http://localhost:8502/
📋 Client Onboarding: http://localhost:8501/
📚 API Docs: http://localhost:5001/api/docs
🏥 Health Check: http://localhost:5001/health

============================================================
```

### **Main Dashboard** - http://localhost:5001/
Central navigation hub with quick access to all services. Beautiful UI with service cards and API endpoints.

### **Image Studio** - http://localhost:8502/
Generate and edit images using AI:
- Text-to-image generation
- Image editing with prompts
- Cloudinary integration
- Cost tracking

### **Client Onboarding** - http://localhost:8501/
Complete 5-step onboarding workflow:
1. Enter client information
2. Create folder structure
3. Upload images
4. Label images with product names
5. Complete and view summary

### **Upload Page** - http://localhost:5001/upload
Standalone image upload interface with drag-and-drop functionality.

### **Label Images** - http://localhost:5001/label-images?client=CLIENT_NAME
Label uploaded images with product names and download organized label files.

---

## API Endpoints

All API endpoints are available at `http://localhost:5001/api/*`

### Image Operations

**POST /api/generate**
```json
{
  "prompt": "A cute robot in a field of flowers",
  "client_folder": "client_name"
}
```

**POST /api/edit**
```json
{
  "image_url": "https://example.com/image.jpg",
  "prompt": "Add sunglasses and a hat",
  "client_folder": "client_name"
}
```

### Client Management

**POST /api/check-client**
```json
{
  "client_name": "client-abc"
}
```

**POST /api/create-client-folders**
```json
{
  "client_name": "client-abc"
}
```

**GET /api/get-client-images?client=CLIENT_NAME**

Returns list of images in client's input folder.

**POST /api/get-upload-config**
```json
{
  "client_name": "client-abc"
}
```

### Utility Endpoints

**GET /health** - Health check for all services

**GET /api/docs** - API documentation

**POST /api/generate-signature** - Generate Cloudinary upload signature

---

## Environment Variables

Required variables in `.env`:

```env
# Nano Banana (Google AI)
GOOGLE_AI_API_KEY=your_google_ai_api_key

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_UPLOAD_PRESET=your_upload_preset

# Optional: Client folder name (can be overridden per request)
CLIENT_FOLDER_NAME=default_client

# Port Configuration (optional)
PORT=5001                    # Main Flask app
STUDIO_PORT=8502            # Image Studio
ONBOARDING_PORT=8501        # Client Onboarding
```

---

## File Structure

```
nano_banana_project/
├── unified_app.py           # ⭐ MAIN APPLICATION
├── start.sh                 # Quick start script
├── app.py                   # Image Studio (Streamlit)
├── client_onboarding.py     # Onboarding (Streamlit)
├── api_server.py            # ❌ DEPRECATED (now in unified_app.py)
├── src/
│   ├── nano_banana_client.py
│   └── cloudinary_utils.py
├── templates/
│   ├── upload_simple.html
│   └── label_images.html
├── requirements.txt
└── .env
```

---

## Benefits of Unified Architecture

### ✅ **Single Entry Point**
- Start one command instead of 3 separate processes
- Easier to manage and monitor

### ✅ **Simplified Deployment**
- Deploy one application instead of coordinating multiple services
- Single port exposure option (5001)
- Internal services managed automatically

### ✅ **Better Resource Management**
- Parent process manages child Streamlit processes
- Automatic cleanup on shutdown
- Graceful termination of all services

### ✅ **Centralized Navigation**
- Beautiful main dashboard at root URL
- Easy access to all services
- Professional user experience

### ✅ **Easier Development**
- Single development server to run
- Integrated logging
- Simplified debugging

---

## Process Management

### **Starting the Application**

```bash
./start.sh
```

or

```bash
python unified_app.py
```

### **Stopping the Application**

Press `Ctrl+C` in the terminal where unified_app.py is running.

The application automatically:
1. Catches the interrupt signal
2. Terminates all Streamlit subprocesses
3. Performs graceful shutdown
4. Cleans up resources

### **Manual Cleanup** (if needed)

```bash
# Kill all processes on used ports
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9
lsof -ti:8502 | xargs kill -9
```

---

## Deployment Options

### **Local Development**

```bash
./start.sh
```

### **Production (Render, Heroku, etc.)**

The unified application can be deployed with a single `Procfile`:

**For Render:**
```yaml
# render.yaml
services:
  - type: web
    name: loudspeaker-marketing
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python unified_app.py
    envVars:
      - key: PORT
        value: 10000
      - key: STUDIO_PORT
        value: 10001
      - key: ONBOARDING_PORT
        value: 10002
```

**For Heroku:**
```
web: python unified_app.py
```

### **Docker**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001 8501 8502

CMD ["python", "unified_app.py"]
```

---

## Migration Guide

### **Old Way (3 separate commands):**

```bash
# Terminal 1
python api_server.py

# Terminal 2
streamlit run client_onboarding.py

# Terminal 3
streamlit run app.py
```

### **New Way (1 command):**

```bash
./start.sh
```

or

```bash
python unified_app.py
```

That's it! All services start automatically.

---

## Troubleshooting

### **Port Already in Use**

```bash
# Clean up ports
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9
lsof -ti:8502 | xargs kill -9

# Then restart
./start.sh
```

### **Streamlit Services Not Starting**

Check the logs:
```bash
tail -f /tmp/unified_app.log
```

Ensure Streamlit is installed:
```bash
pip install streamlit
```

### **Environment Variables Not Loaded**

Ensure `.env` file exists in the project root:
```bash
ls -la .env
```

### **Import Errors**

Activate virtual environment and reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## API Integration (for n8n or external services)

All API endpoints remain the same. Update your base URL to:

```
http://localhost:5001/api
```

Example n8n HTTP Request node configuration:
```
URL: http://localhost:5001/api/generate
Method: POST
Body:
{
  "prompt": "{{$json.prompt}}",
  "client_folder": "{{$json.client}}"
}
```

---

## Monitoring

### **Health Check**

```bash
curl http://localhost:5001/health
```

Response:
```json
{
  "status": "healthy",
  "nano_banana": "ready",
  "cloudinary": "ready",
  "services": {
    "image_studio": "http://localhost:8502",
    "onboarding": "http://localhost:8501"
  }
}
```

### **Service Status**

Visit the main dashboard at http://localhost:5001/ to see all services with live status indicators.

---

## What Changed?

### **Files Added:**
- ✅ `unified_app.py` - Main unified application
- ✅ `start.sh` - Quick start script
- ✅ `UNIFIED_ARCHITECTURE.md` - This documentation

### **Files Deprecated:**
- ⚠️ `api_server.py` - Functionality moved to `unified_app.py`
  - Still exists but no longer needed
  - Can be removed or kept as reference

### **Files Unchanged:**
- ✅ `app.py` - Image Studio (still used by unified_app.py)
- ✅ `client_onboarding.py` - Onboarding (still used by unified_app.py)
- ✅ `src/` - All utility modules unchanged
- ✅ `templates/` - All HTML templates unchanged

---

## Next Steps

1. **Test Locally**: Run `./start.sh` and test all features
2. **Review Main Dashboard**: Visit http://localhost:5001/
3. **Test API Endpoints**: Use the `/api/docs` endpoint
4. **Prepare for Deployment**: Review deployment options above
5. **Deploy to Cloud**: Use Render, Heroku, or Docker

---

## Support

If you encounter any issues:
1. Check logs: `tail -f /tmp/unified_app.log`
2. Verify environment variables in `.env`
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check port availability: `lsof -i :5001`

---

**🎉 Congratulations!** You now have a unified, production-ready application architecture!
