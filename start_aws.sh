#!/bin/bash

################################################################################
# Quick Start Script for LSM Unified App (AWS Version)
# Use this for local testing before deploying to AWS
################################################################################

set -e

echo "=========================================="
echo "LSM Unified App - AWS Version"
echo "=========================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Copy .env.template to .env and configure it first."
    exit 1
fi

# Source environment variables
export $(cat .env | grep -v '^#' | xargs)

# Use AWS version of unified app
if [ ! -f "unified_app.py" ] || [ "unified_app_aws.py" -nt "unified_app.py" ]; then
    echo "Copying AWS version of unified_app.py..."
    cp unified_app_aws.py unified_app.py
fi

# Check Python version
PYTHON_CMD=""
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "Error: Python 3 not found!"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Clean up any existing processes on the ports
echo "Cleaning up ports..."
lsof -ti:5001,8501,8502 | xargs kill -9 2>/dev/null || true

sleep 1

# Set default values if not in .env
export PORT=${PORT:-5001}
export STUDIO_PORT=${STUDIO_PORT:-8502}
export ONBOARDING_PORT=${ONBOARDING_PORT:-8501}

echo ""
echo "=========================================="
echo "Starting Services..."
echo "=========================================="

# Start the unified app
$PYTHON_CMD unified_app.py

# Note: unified_app.py manages the Streamlit subprocesses
