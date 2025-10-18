#!/bin/bash

################################################################################
# Setup Systemd Services for LSM Unified App
# Run this script after deploy_aws.sh to create systemd services
################################################################################

set -e

echo "=========================================="
echo "Setting up Systemd Services"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

APP_DIR="/home/lsmapp/lsm-unified-app"

# Create systemd service for Flask API
echo "[1/3] Creating Flask API service..."
cat > /etc/systemd/system/lsm-flask.service << EOF
[Unit]
Description=LSM Unified App - Flask API
After=network.target

[Service]
Type=simple
User=lsmapp
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/python unified_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Image Studio
echo "[2/3] Creating Image Studio service..."
cat > /etc/systemd/system/lsm-studio.service << EOF
[Unit]
Description=LSM Image Studio - Streamlit
After=network.target

[Service]
Type=simple
User=lsmapp
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/streamlit run app.py --server.port=8502 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Client Onboarding
echo "[3/3] Creating Client Onboarding service..."
cat > /etc/systemd/system/lsm-onboarding.service << EOF
[Unit]
Description=LSM Client Onboarding - Streamlit
After=network.target

[Service]
Type=simple
User=lsmapp
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/streamlit run client_onboarding.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable services to start on boot
echo "Enabling services..."
systemctl enable lsm-flask.service
systemctl enable lsm-studio.service
systemctl enable lsm-onboarding.service

echo ""
echo "=========================================="
echo "Services Created Successfully!"
echo "=========================================="
echo ""
echo "Service Management Commands:"
echo ""
echo "Start all services:"
echo "  sudo systemctl start lsm-flask lsm-studio lsm-onboarding"
echo ""
echo "Stop all services:"
echo "  sudo systemctl stop lsm-flask lsm-studio lsm-onboarding"
echo ""
echo "Restart all services:"
echo "  sudo systemctl restart lsm-flask lsm-studio lsm-onboarding"
echo ""
echo "Check status:"
echo "  sudo systemctl status lsm-flask"
echo "  sudo systemctl status lsm-studio"
echo "  sudo systemctl status lsm-onboarding"
echo ""
echo "View logs:"
echo "  sudo journalctl -u lsm-flask -f"
echo "  sudo journalctl -u lsm-studio -f"
echo "  sudo journalctl -u lsm-onboarding -f"
echo ""
