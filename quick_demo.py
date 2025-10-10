#!/usr/bin/env python3
"""
Quick Demo Script for Nano Banana Project

Run this script to quickly test your setup and generate a sample image.
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def main():
    """Quick demo to test the Nano Banana setup."""
    
    print("🍌 Nano Banana Quick Demo")
    print("=" * 40)
    
    try:
        from nano_banana_client import NanoBananaClient
        
        # Initialize client
        print("🔧 Initializing Nano Banana client...")
        client = NanoBananaClient()
        
        # Show pricing info
        pricing = client.get_pricing_info()
        print(f"💰 Ready! Cost per image: ${pricing['cost_per_image_usd']}")
        print()
        
        # Generate a simple test image
        print("🎨 Generating a test image...")
        prompt = "A cute robot sitting in a field of colorful flowers, cartoon style"
        
        output_path = client.generate_image(
            prompt=prompt,
            output_filename="demo_robot.png"
        )
        
        print(f"✅ Success! Demo image saved to: {output_path}")
        print(f"💵 Estimated cost: ${client.estimate_cost(1):.3f}")
        print()
        print("🎉 Your Nano Banana setup is working correctly!")
        print("📚 Check out the examples/ directory for more advanced usage.")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print()
        print("🔧 Setup Required:")
        print("1. Get an API key: https://aistudio.google.com")
        print("2. Set environment variable:")
        print("   export GOOGLE_AI_API_KEY='your_api_key_here'")
        print("3. Make sure billing is enabled on your Google Cloud project")
        print()
        print("💡 Or copy .env.template to .env and add your API key there")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print()
        print("🔧 Install dependencies:")
        print("   pip install -r requirements.txt")
        print("   # OR")
        print("   pip install google-genai Pillow")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print()
        print("💡 Tips:")
        print("• Check your internet connection")
        print("• Verify your API key is valid")
        print("• Test your prompt in Google AI Studio first")
        print("• Make sure billing is enabled")


if __name__ == "__main__":
    main()