#!/bin/bash
# Start AI Image Studio with Cloudinary API Secret

cd "$(dirname "$0")"
source venv/bin/activate

echo "🍌 AI Image Studio Setup"
echo "========================"
echo ""
echo "I can see your Cloudinary is working (XV1 Generated folder exists!)"
echo "We just need your API Secret to complete the setup."
echo ""
echo "Find it in your Cloudinary Dashboard > API Keys section"
echo ""

# Prompt for API secret
read -p "Enter your Cloudinary API Secret: " CLOUDINARY_SECRET

if [ -z "$CLOUDINARY_SECRET" ]; then
    echo "No secret provided. Starting with limited functionality..."
    CLOUDINARY_SECRET="dummy_secret"
fi

# Set all environment variables
export GOOGLE_AI_API_KEY='AIzaSyDxRXDddcuFCIa_3JhbgTCBr4ffCs0hFaY'
export CLOUDINARY_CLOUD_NAME='dbutevqjq'  
export CLOUDINARY_API_KEY='E3NzPkFDx_derDoPbTd2dcsZpZ0'
export CLOUDINARY_API_SECRET="$CLOUDINARY_SECRET"
export CLIENT_FOLDER_NAME='XV1'

echo ""
echo "🚀 Starting AI Image Studio..."
echo "🌐 Opening at: http://localhost:8501"
echo ""
echo "✅ All variables set!"
echo "✅ Google AI API Key: ****$(echo $GOOGLE_AI_API_KEY | tail -c 6)"
echo "✅ Cloudinary Cloud: $CLOUDINARY_CLOUD_NAME"
echo "✅ Cloudinary API Key: ****$(echo $CLOUDINARY_API_KEY | tail -c 6)"
echo "✅ Cloudinary API Secret: ****$(echo $CLOUDINARY_API_SECRET | tail -c 6)"
echo "✅ Client Folder: $CLIENT_FOLDER_NAME"
echo ""

# Start Streamlit
echo "" | streamlit run app.py --server.port 8501 --server.headless true --server.fileWatcherType none