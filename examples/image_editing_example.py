#!/usr/bin/env python3
"""
Image Editing Example for Nano Banana (Gemini 2.5 Flash Image)

This script demonstrates how to edit existing images using text prompts with Nano Banana.
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from nano_banana_client import NanoBananaClient


def main():
    """Demonstrate image editing with text prompts."""
    
    print("🍌 Nano Banana Image Editing Example")
    print("=" * 50)
    
    try:
        # Initialize the client
        client = NanoBananaClient()
        
        # Show pricing information
        pricing = client.get_pricing_info()
        print(f"💰 Cost per image: ${pricing['cost_per_image_usd']}")
        print()
        
        # Step 1: Generate a base image to edit
        print("🎨 Step 1: Generating a base image to edit...")
        base_prompt = "Create a photorealistic image of an orange cat with green eyes, sitting on a couch."
        
        base_image_path = client.generate_image(
            prompt=base_prompt,
            output_filename="base_cat.png"
        )
        print(f"✅ Base image created: {base_image_path}")
        print()
        
        # Step 2: Define editing examples
        editing_examples = [
            {
                "prompt": "Using the image of the cat, create a photorealistic, street-level view of the cat walking along a sidewalk in a New York City neighborhood, with the blurred legs of pedestrians and yellow cabs passing by in the background.",
                "filename": "cat_in_nyc.png",
                "description": "Moving cat to NYC street scene"
            },
            {
                "prompt": "Transform the cat into a superhero cat wearing a red cape and mask, maintaining the same orange fur and green eyes, sitting heroically on the couch with dramatic lighting.",
                "filename": "superhero_cat.png",
                "description": "Making the cat a superhero"
            },
            {
                "prompt": "Change the scene to show the same cat sitting on a tree branch in a beautiful autumn forest, with colorful falling leaves around it.",
                "filename": "forest_cat.png",
                "description": "Moving cat to autumn forest"
            },
            {
                "prompt": "Transform the couch into a luxurious golden throne and add a royal crown on the cat's head, making it look like a majestic cat king.",
                "filename": "royal_cat.png",
                "description": "Making the cat royalty"
            },
            {
                "prompt": "Add a wizard hat and magical sparkles around the cat, transform the background into a magical library with floating books and mystical lighting.",
                "filename": "wizard_cat.png",
                "description": "Making the cat a wizard"
            }
        ]
        
        print("✏️ Step 2: Performing various image edits...")
        print()
        
        edited_images = []
        
        for i, example in enumerate(editing_examples, 1):
            print(f"[{i}/{len(editing_examples)}] {example['description']}...")
            
            try:
                # Edit the base image
                edited_path = client.edit_image(
                    image_path=base_image_path,
                    prompt=example["prompt"],
                    output_filename=example["filename"]
                )
                
                edited_images.append(edited_path)
                print(f"✅ Created: {edited_path}")
                
                # Show cumulative cost
                total_images = i + 1  # +1 for the base image
                cost = client.estimate_cost(total_images)
                print(f"💵 Cumulative estimated cost: ${cost:.3f}")
                print()
                
            except Exception as e:
                print(f"❌ Failed to edit image: {e}")
                print()
                continue
        
        # Summary
        print("=" * 50)
        print("🎉 Image Editing Complete!")
        print(f"📸 Base image: {base_image_path}")
        print(f"✏️ Successfully created {len(edited_images)} edited versions")
        
        total_images = len(edited_images) + 1  # +1 for base image
        print(f"💰 Total estimated cost: ${client.estimate_cost(total_images):.3f}")
        print()
        print("Edited images:")
        for image_path in edited_images:
            print(f"  • {image_path}")
        
        print()
        print("💡 Tips for better editing:")
        print("• Be specific about what you want to change")
        print("• Describe the desired style and mood")
        print("• Mention if you want to preserve certain elements")
        print("• Use descriptive adjectives for better results")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print()
        print("To fix this:")
        print("1. Get an API key from https://aistudio.google.com")
        print("2. Set the GOOGLE_AI_API_KEY environment variable:")
        print("   export GOOGLE_AI_API_KEY='your_api_key_here'")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()