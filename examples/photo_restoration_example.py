#!/usr/bin/env python3
"""
Photo Restoration Example for Nano Banana (Gemini 2.5 Flash Image)

This script demonstrates how to restore and colorize old photographs using Nano Banana.
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from nano_banana_client import NanoBananaClient


def create_sample_old_photo(client):
    """Create a sample 'old' photo for demonstration purposes."""
    
    print("📸 Creating a sample vintage photo for restoration...")
    
    # Generate a vintage-style photo
    vintage_prompt = """
    Create a black and white vintage photograph from the 1940s showing a family portrait. 
    The image should have the characteristic grain, fading, and slight damage typical of old photographs. 
    Include some scratches, spots, and aging effects. Show a family of four (parents and two children) 
    posed formally in front of a house.
    """
    
    sample_path = client.generate_image(
        prompt=vintage_prompt,
        output_filename="sample_old_photo.png"
    )
    
    print(f"✅ Sample vintage photo created: {sample_path}")
    return sample_path


def main():
    """Demonstrate photo restoration capabilities."""
    
    print("🍌 Nano Banana Photo Restoration Example")
    print("=" * 50)
    
    try:
        # Initialize the client
        client = NanoBananaClient()
        
        # Show pricing information
        pricing = client.get_pricing_info()
        print(f"💰 Cost per image: ${pricing['cost_per_image_usd']}")
        print()
        
        # Check for existing old photos in the input directory
        input_dir = "images/input"
        old_photos = []
        
        if os.path.exists(input_dir):
            for filename in os.listdir(input_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    old_photos.append(os.path.join(input_dir, filename))
        
        if not old_photos:
            print("📁 No old photos found in images/input directory.")
            print("🎨 Creating a sample vintage photo for demonstration...")
            print()
            
            # Create a sample old photo
            sample_photo = create_sample_old_photo(client)
            old_photos = [sample_photo]
        else:
            print(f"📁 Found {len(old_photos)} photo(s) in input directory:")
            for photo in old_photos:
                print(f"  • {photo}")
            print()
        
        # Restoration examples with different approaches
        restoration_approaches = [
            {
                "prompt": "Restore and colorize this old photograph. Enhance the image quality, remove any damage or artifacts, and add realistic colors while preserving the original composition and subjects.",
                "suffix": "_restored_standard",
                "description": "Standard restoration and colorization"
            },
            {
                "prompt": "Restore this vintage photograph with enhanced details. Remove scratches, spots, and aging effects. Colorize it with warm, natural tones appropriate for the era. Sharpen the details and improve contrast while maintaining the authentic vintage feel.",
                "suffix": "_restored_enhanced",
                "description": "Enhanced restoration with period-appropriate colors"
            },
            {
                "prompt": "Restore and modernize this old photograph. Clean up all damage, colorize with vibrant modern colors, and enhance it to look like it was taken with today's high-quality cameras while keeping the original scene composition.",
                "suffix": "_restored_modern",
                "description": "Modern-style restoration"
            }
        ]
        
        restored_images = []
        total_cost = 0
        
        # Process each old photo
        for photo_idx, old_photo in enumerate(old_photos, 1):
            print(f"🔧 Processing photo {photo_idx}/{len(old_photos)}: {os.path.basename(old_photo)}")
            print()
            
            # Try each restoration approach
            for approach_idx, approach in enumerate(restoration_approaches, 1):
                print(f"  [{approach_idx}/{len(restoration_approaches)}] {approach['description']}...")
                
                try:
                    # Create output filename
                    base_name = os.path.splitext(os.path.basename(old_photo))[0]
                    output_filename = f"{base_name}{approach['suffix']}.png"
                    
                    # Restore the photo
                    restored_path = client.restore_photo(
                        image_path=old_photo,
                        custom_prompt=approach["prompt"],
                        output_filename=output_filename
                    )
                    
                    restored_images.append({
                        'original': old_photo,
                        'restored': restored_path,
                        'approach': approach['description']
                    })
                    
                    print(f"  ✅ Restored: {restored_path}")
                    
                    # Update cost tracking
                    if photo_idx == 1 and approach_idx == 1:
                        # Add cost for the sample photo creation if we created one
                        total_images = len(restored_images) + (1 if old_photos[0].endswith('sample_old_photo.png') else 0)
                    else:
                        total_images = len(restored_images)
                    
                    cost = client.estimate_cost(total_images)
                    print(f"  💵 Cumulative estimated cost: ${cost:.3f}")
                    print()
                    
                except Exception as e:
                    print(f"  ❌ Failed to restore photo: {e}")
                    print()
                    continue
        
        # Summary
        print("=" * 60)
        print("🎉 Photo Restoration Complete!")
        print(f"📸 Processed {len(old_photos)} original photo(s)")
        print(f"🔧 Created {len(restored_images)} restored version(s)")
        
        # Calculate final cost (include sample photo if created)
        final_total = len(restored_images)
        if old_photos and old_photos[0].endswith('sample_old_photo.png'):
            final_total += 1  # Add cost for sample photo creation
        
        print(f"💰 Total estimated cost: ${client.estimate_cost(final_total):.3f}")
        print()
        
        # Display results
        print("Restoration Results:")
        for result in restored_images:
            print(f"  📁 Original: {result['original']}")
            print(f"  🔧 Method: {result['approach']}")
            print(f"  ✨ Restored: {result['restored']}")
            print()
        
        print("💡 Tips for better photo restoration:")
        print("• Higher resolution input photos work better")
        print("• Describe the era/time period for better colorization")
        print("• Mention specific damage types you want fixed")
        print("• Be specific about the desired color style")
        print("• Consider the lighting conditions of the original photo")
        
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