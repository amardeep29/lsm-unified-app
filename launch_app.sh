#!/bin/bash
# Launch AI Image Studio without prompts

cd "$(dirname "$0")"
source venv/bin/activate

# Set environment variables
export GOOGLE_AI_API_KEY='AIzaSyDxRXDddcuFCIa_3JhbgTCBr4ffCs0hFaY'
export CLOUDINARY_CLOUD_NAME='dbutevqjq'
export CLOUDINARY_API_KEY='112259512859171'
export CLOUDINARY_API_SECRET='E3NzPkFDx_derDoPbTd2dcsZpZ0'
export CLIENT_FOLDER_NAME='XV1'

echo "🍉 Starting AI Image Studio..."
echo "🌐 Access your app at: http://localhost:8501"
echo "🎯 UI improvements: Fixed duplicate images, better layout!"
echo ""

# Skip email prompt and run headless
echo "" | streamlit run app.py --server.port 8501 --server.headless true --server.fileWatcherType none

echo ""
echo "App stopped."