#!/usr/bin/env python3
"""
Quick Test Script - Super easy interface for testing Nano Banana

Just run this script and follow the prompts, or use the helper functions directly:

Quick functions you can use:
- generate("your prompt") -> generates image
- edit("image.jpg", "edit instruction") -> edits image  
- restore("old_photo.jpg") -> restores photo
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from nano_banana_client import NanoBananaClient

# Global client instance
client = None

def init_client():
    """Initialize the client once"""
    global client
    if client is None:
        try:
            client = NanoBananaClient()
            print(f"🍌 Nano Banana ready! Cost per image: ${client.get_pricing_info()['cost_per_image_usd']}")
        except Exception as e:
            print(f"❌ Setup error: {e}")
            print("💡 Make sure GOOGLE_AI_API_KEY is set!")
            return False
    return True

def generate(prompt, filename=None):
    """Generate image with one line: generate('a cat on a beach')"""
    if not init_client():
        return None
    
    try:
        print(f"🎨 Generating: {prompt[:50]}...")
        result = client.generate_image(prompt, filename)
        print(f"✅ Generated: {result}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def edit(image_path, prompt, filename=None):
    """Edit image with one line: edit('my_photo.jpg', 'add sunglasses')"""
    if not init_client():
        return None
    
    # Smart path finding
    if not os.path.exists(image_path):
        # Try in images/input/
        input_path = f"images/input/{image_path}"
        if os.path.exists(input_path):
            image_path = input_path
        # Try in images/output/
        elif os.path.exists(f"images/output/{image_path}"):
            image_path = f"images/output/{image_path}"
        else:
            print(f"❌ Image not found: {image_path}")
            print("💡 Try putting it in images/input/ directory")
            return None
    
    try:
        print(f"✏️ Editing {image_path}: {prompt[:50]}...")
        result = client.edit_image(image_path, prompt, filename)
        print(f"✅ Edited: {result}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def restore(image_path, filename=None):
    """Restore photo with one line: restore('old_photo.jpg')"""
    if not init_client():
        return None
    
    # Smart path finding
    if not os.path.exists(image_path):
        input_path = f"images/input/{image_path}"
        if os.path.exists(input_path):
            image_path = input_path
        elif os.path.exists(f"images/output/{image_path}"):
            image_path = f"images/output/{image_path}"
        else:
            print(f"❌ Image not found: {image_path}")
            return None
    
    try:
        print(f"🔧 Restoring: {image_path}")
        result = client.restore_photo(image_path, filename)
        print(f"✅ Restored: {result}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def list_images():
    """List available images in input and output directories"""
    print("\n📁 Available Images:")
    
    input_dir = "images/input"
    output_dir = "images/output"
    
    if os.path.exists(input_dir):
        input_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        if input_files:
            print(f"\n📥 Input images ({input_dir}):")
            for f in input_files:
                print(f"  • {f}")
    
    if os.path.exists(output_dir):
        output_files = [f for f in os.listdir(output_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        if output_files:
            print(f"\n📤 Generated images ({output_dir}):")
            for f in output_files:
                print(f"  • {f}")
    
    if not (input_files or output_files):
        print("  No images found. Add some images to images/input/ to get started!")

def interactive_mode():
    """Run interactive mode"""
    print("🍌 Nano Banana Quick Test")
    print("=" * 30)
    
    if not init_client():
        return
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Generate image from text")
        print("2. Edit existing image") 
        print("3. Restore old photo")
        print("4. List available images")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            prompt = input("Enter image description: ").strip()
            if prompt:
                generate(prompt)
        
        elif choice == "2":
            list_images()
            image = input("\nEnter image filename: ").strip()
            edit_prompt = input("Enter edit instruction: ").strip()
            if image and edit_prompt:
                edit(image, edit_prompt)
        
        elif choice == "3":
            list_images()
            image = input("\nEnter image filename: ").strip()
            if image:
                restore(image)
        
        elif choice == "4":
            list_images()
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        interactive_mode()
    else:
        # Command line usage
        print("🍌 Quick Test Functions:")
        print("=" * 25)
        print("Run in Python:")
        print('  generate("a sunset over mountains")')
        print('  edit("photo.jpg", "make it more colorful")')
        print('  restore("old_photo.jpg")')
        print()
        print("Or run interactively:")
        print("  python quick_test.py")