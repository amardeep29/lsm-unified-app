#!/bin/bash

# Loudspeaker Marketing - Unified Application Starter
# This script starts all services in one place

set -e

echo "=========================================="
echo "Loudspeaker Marketing Image Playground"
echo "Starting Unified Application..."
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create a .env file with required environment variables"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Kill any existing processes on the ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:8501 | xargs kill -9 2>/dev/null || true
lsof -ti:8502 | xargs kill -9 2>/dev/null || true

echo "✓ Ports cleared"
echo ""

# Activate virtual environment
source venv/bin/activate

# Start the unified application
echo "🚀 Starting unified application..."
echo ""

python unified_app.py
