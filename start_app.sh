#!/bin/bash
# Startup script for AI Image Studio

echo "🍌 Starting AI Image Studio..."
echo "================================"

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Set environment variables (using existing API key)
export GOOGLE_AI_API_KEY='AIzaSyDxRXDddcuFCIa_3JhbgTCBr4ffCs0hFaY'
export CLOUDINARY_CLOUD_NAME='dbutevqjq'
export CLOUDINARY_API_KEY='112259512859171'
export CLOUDINARY_API_SECRET='E3NzPkFDx_derDoPbTd2dcsZpZ0'
export CLIENT_FOLDER_NAME='XV1'

# Note about Cloudinary setup
echo ""
echo "⚠️  CLOUDINARY SETUP - ALMOST COMPLETE!"
echo "✅ Cloud Name: dbutevqjq"
echo "✅ API Key: Set"
echo "⚠️  Still need: CLOUDINARY_API_SECRET (get from dashboard)"
echo ""
echo "Without Cloudinary, you can still:"
echo "• Generate images (saved locally)"
echo "• Test the interface"
echo "• See the UI design"
echo ""

# Start Streamlit
echo "🚀 Starting Streamlit app..."
echo "App will open in your browser at: http://localhost:8501"
echo ""

streamlit run app.py