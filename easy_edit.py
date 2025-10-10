#!/usr/bin/env python3
"""
Easy Image Editor - Simple one-liner interface for Nano Banana

Usage:
    python easy_edit.py "path/to/image.jpg" "your edit instruction"

Examples:
    python easy_edit.py "my_photo.jpg" "make it more colorful"
    python easy_edit.py "portrait.png" "add sunglasses"
    python easy_edit.py "landscape.jpg" "change to winter scene"
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from nano_banana_client import NanoBananaClient


def easy_edit(image_path, prompt):
    """Edit an image with a simple prompt - one function call!"""
    
    # Initialize client
    client = NanoBananaClient()
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        print("💡 Tip: Place your image in the 'images/input/' directory")
        return None
    
    print(f"🖼️  Input: {image_path}")
    print(f"✏️  Edit: {prompt}")
    print()
    
    # Generate output filename
    input_name = Path(image_path).stem
    output_filename = f"{input_name}_edited.png"
    
    try:
        # Edit the image
        result_path = client.edit_image(
            image_path=image_path,
            prompt=prompt,
            output_filename=output_filename
        )
        
        print(f"🎉 Success! Edited image saved as: {result_path}")
        print(f"💰 Cost: ${client.estimate_cost(1):.3f}")
        return result_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Command line interface for easy editing"""
    
    if len(sys.argv) != 3:
        print("🍌 Easy Nano Banana Image Editor")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python easy_edit.py <image_path> <edit_instruction>")
        print()
        print("Examples:")
        print('  python easy_edit.py "my_photo.jpg" "make it more colorful"')
        print('  python easy_edit.py "portrait.png" "add sunglasses"')
        print('  python easy_edit.py "images/input/photo.jpg" "change to winter scene"')
        print()
        print("💡 Tips:")
        print("• Put your images in 'images/input/' directory")
        print("• Use quotes around your edit instruction")
        print("• Be specific about what you want to change")
        print("• Results are saved in 'images/output/'")
        return
    
    image_path = sys.argv[1]
    prompt = sys.argv[2]
    
    easy_edit(image_path, prompt)


if __name__ == "__main__":
    main()