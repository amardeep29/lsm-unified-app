#!/bin/bash
# One-liner setup and run script for Nano Banana
# Usage: ./run.sh [script_name]

cd "$(dirname "$0")"
source venv/bin/activate
export GOOGLE_AI_API_KEY='AIzaSyDxRXDddcuFCIa_3JhbgTCBr4ffCs0hFaY'

if [ $# -eq 0 ]; then
    echo "🍌 Nano Banana Quick Commands:"
    echo "================================"
    echo ""
    echo "Easy Image Editing (one-liner):"
    echo "  ./run.sh easy 'image.jpg' 'edit instruction'"
    echo ""
    echo "Interactive Mode:"
    echo "  ./run.sh test"
    echo ""
    echo "Generate Image:"
    echo "  ./run.sh demo"
    echo ""
    echo "Examples:"
    echo "  ./run.sh easy 'demo_robot.png' 'make it purple'"
    echo "  ./run.sh easy 'demo_robot.png' 'add sunglasses'"
    echo ""
elif [ "$1" = "easy" ] && [ $# -eq 3 ]; then
    python easy_edit.py "$2" "$3"
elif [ "$1" = "test" ]; then
    python quick_test.py
elif [ "$1" = "demo" ]; then
    python quick_demo.py
else
    echo "❌ Invalid usage. Run './run.sh' for help."
fi