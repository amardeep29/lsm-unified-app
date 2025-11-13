#!/bin/bash

################################################################################
# Production Update Script
# Pulls latest code, installs dependencies, and restarts services
################################################################################

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

APP_DIR="/home/lsmapp/lsm-unified-app"

echo -e "${GREEN}=========================================="
echo -e "LSM Unified App - Production Update"
echo -e "==========================================${NC}\n"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run with sudo${NC}"
    exit 1
fi

# Navigate to app directory
echo -e "${YELLOW}[1/5] Navigating to app directory...${NC}"
cd "$APP_DIR"

# Stash any local changes (shouldn't be any, but just in case)
echo -e "${YELLOW}[2/5] Pulling latest code...${NC}"
sudo -u lsmapp git fetch origin
sudo -u lsmapp git pull origin main

# Install/update dependencies
echo -e "${YELLOW}[3/5] Installing dependencies...${NC}"
sudo -u lsmapp ./venv/bin/pip install --upgrade pip
sudo -u lsmapp ./venv/bin/pip install -r requirements.txt

# Restart services
echo -e "${YELLOW}[4/5] Restarting services...${NC}"
systemctl restart lsm-flask
systemctl restart lsm-studio
systemctl restart lsm-onboarding

# Wait a moment for services to start
sleep 2

# Check service status
echo -e "${YELLOW}[5/5] Checking service status...${NC}"
FLASK_STATUS=$(systemctl is-active lsm-flask)
STUDIO_STATUS=$(systemctl is-active lsm-studio)
ONBOARDING_STATUS=$(systemctl is-active lsm-onboarding)

echo ""
echo -e "Flask API: ${FLASK_STATUS}" | sed "s/active/${GREEN}active${NC}/g" | sed "s/failed/${RED}failed${NC}/g"
echo -e "Image Studio: ${STUDIO_STATUS}" | sed "s/active/${GREEN}active${NC}/g" | sed "s/failed/${RED}failed${NC}/g"
echo -e "Client Onboarding: ${ONBOARDING_STATUS}" | sed "s/active/${GREEN}active${NC}/g" | sed "s/failed/${RED}failed${NC}/g"

# Check if all services are active
if [ "$FLASK_STATUS" = "active" ] && [ "$STUDIO_STATUS" = "active" ] && [ "$ONBOARDING_STATUS" = "active" ]; then
    echo -e "\n${GREEN}=========================================="
    echo -e "✅ Update Complete - All Services Running"
    echo -e "==========================================${NC}\n"
else
    echo -e "\n${RED}=========================================="
    echo -e "⚠️  Warning: Some services may not be running"
    echo -e "==========================================${NC}"
    echo -e "\nCheck logs with:"
    echo -e "  sudo journalctl -u lsm-flask -n 50"
    echo -e "  sudo journalctl -u lsm-studio -n 50"
    echo -e "  sudo journalctl -u lsm-onboarding -n 50\n"
    exit 1
fi
