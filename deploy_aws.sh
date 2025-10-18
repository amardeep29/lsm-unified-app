#!/bin/bash

################################################################################
# LSM Unified App - AWS EC2 Deployment Script
# This script sets up the complete application on a single EC2 instance
################################################################################

set -e  # Exit on error

echo "=========================================="
echo "LSM Unified App - AWS Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Update system
echo -e "\n${GREEN}[1/8] Updating system packages...${NC}"
apt-get update
apt-get upgrade -y

# Install Python 3.11 and pip
echo -e "\n${GREEN}[2/8] Installing Python 3.11...${NC}"
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install Git
echo -e "\n${GREEN}[3/8] Installing Git...${NC}"
apt-get install -y git

# Install Nginx
echo -e "\n${GREEN}[4/8] Installing Nginx...${NC}"
apt-get install -y nginx

# Create application user
echo -e "\n${GREEN}[5/8] Creating application user...${NC}"
if ! id "lsmapp" &>/dev/null; then
    useradd -m -s /bin/bash lsmapp
    echo "User 'lsmapp' created"
else
    echo "User 'lsmapp' already exists"
fi

# Clone repository
echo -e "\n${GREEN}[6/8] Cloning repository...${NC}"
APP_DIR="/home/lsmapp/lsm-unified-app"

if [ -d "$APP_DIR" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd "$APP_DIR"
    sudo -u lsmapp git pull
else
    sudo -u lsmapp git clone https://github.com/amardeep29/lsm-unified-app.git "$APP_DIR"
fi

cd "$APP_DIR"

# Use the AWS version of unified app
sudo -u lsmapp cp unified_app_aws.py unified_app.py

# Create virtual environment
echo -e "\n${GREEN}[7/8] Setting up Python virtual environment...${NC}"
sudo -u lsmapp python3.11 -m venv venv
sudo -u lsmapp ./venv/bin/pip install --upgrade pip
sudo -u lsmapp ./venv/bin/pip install -r requirements.txt

# Create .env file
echo -e "\n${GREEN}[8/8] Creating environment configuration...${NC}"

if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Google AI API Key
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_UPLOAD_PRESET=client_onboarding_unsigned

# Client Configuration
CLIENT_FOLDER_NAME=XV1

# Server Configuration
PORT=5001
STUDIO_PORT=8501
ONBOARDING_PORT=8502

# Public URL (set this to your domain or EC2 public IP)
# Examples:
#   PUBLIC_URL=http://your-domain.com
#   PUBLIC_URL=http://3.12.34.56
PUBLIC_URL=

# Nginx reverse proxy (set to true if using nginx config below)
USE_NGINX=false
EOF

    chown lsmapp:lsmapp .env
    chmod 600 .env

    echo -e "${YELLOW}⚠️  IMPORTANT: Edit /home/lsmapp/lsm-unified-app/.env with your credentials${NC}"
    echo -e "${YELLOW}    Run: sudo nano /home/lsmapp/lsm-unified-app/.env${NC}"
fi

echo -e "\n${GREEN}=========================================="
echo -e "Deployment Complete!${NC}"
echo -e "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your credentials:"
echo "   sudo nano /home/lsmapp/lsm-unified-app/.env"
echo ""
echo "2. Set up systemd services (see setup_services.sh)"
echo ""
echo "3. Configure nginx (see nginx.conf)"
echo ""
echo "4. Open security group ports:"
echo "   - Port 80 (HTTP) or 443 (HTTPS)"
echo "   - Port 5001, 8501, 8502 (if not using nginx)"
