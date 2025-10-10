#!/usr/bin/env python3
"""
Image Generation Example for Nano Banana (Gemini 2.5 Flash Image)

This script demonstrates how to generate images from text prompts using Nano Banana.
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from nano_banana_client import NanoBananaClient


def main():
    """Demonstrate image generation from various text prompts."""
    
    print("🍌 Nano Banana Image Generation Example")
    print("=" * 50)
    
    try:
        # Initialize the client
        client = NanoBananaClient()
        
        # Show pricing information
        pricing = client.get_pricing_info()
        print(f"💰 Cost per image: ${pricing['cost_per_image_usd']}")
        print(f"📊 Images per dollar: ~{pricing['images_per_dollar']}")
        print()
        
        # Example prompts to try
        example_prompts = [
            {
                "prompt": "Create a photorealistic image of an orange cat with green eyes, sitting on a couch.",
                "filename": "orange_cat.png"
            },
            {
                "prompt": "A futuristic cityscape at sunset with flying cars and neon lights reflecting on glass buildings.",
                "filename": "futuristic_city.png"
            },
            {
                "prompt": "A serene mountain lake with crystal clear water, surrounded by pine trees and snow-capped peaks.",
                "filename": "mountain_lake.png"
            },
            {
                "prompt": "A steampunk-style robot playing a violin in a Victorian-era music hall.",
                "filename": "steampunk_robot.png"
            },
            {
                "prompt": "A cozy coffee shop interior with warm lighting, wooden furniture, and people reading books.",
                "filename": "coffee_shop.png"
            }
        ]
        
        print("🎨 Generating sample images...")
        print()
        
        generated_images = []
        
        for i, example in enumerate(example_prompts, 1):
            print(f"[{i}/{len(example_prompts)}] Generating: {example['prompt'][:60]}...")
            
            try:
                # Generate image
                output_path = client.generate_image(
                    prompt=example["prompt"],
                    output_filename=example["filename"]
                )
                
                generated_images.append(output_path)
                print(f"✅ Generated: {output_path}")
                
                # Estimate cost
                cost = client.estimate_cost(i)
                print(f"💵 Cumulative estimated cost: ${cost:.3f}")
                print()
                
            except Exception as e:
                print(f"❌ Failed to generate image: {e}")
                print()
                continue
        
        # Summary
        print("=" * 50)
        print("🎉 Generation Complete!")
        print(f"📸 Successfully generated {len(generated_images)} images")
        print(f"💰 Total estimated cost: ${client.estimate_cost(len(generated_images)):.3f}")
        print()
        print("Generated images:")
        for image_path in generated_images:
            print(f"  • {image_path}")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print()
        print("To fix this:")
        print("1. Get an API key from https://aistudio.google.com")
        print("2. Set the GOOGLE_AI_API_KEY environment variable:")
        print("   export GOOGLE_AI_API_KEY='your_api_key_here'")
        print("3. Or copy .env.template to .env and fill in your API key")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()