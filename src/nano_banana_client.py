"""
NanoBanana client wrapper for Gemini 2.5 Flash Image (Nano Banana) API.
"""

import os
import sys
from typing import List, Optional, Union
from PIL import Image
from io import BytesIO
import time
import requests

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from config import Config

try:
    from google import genai
except ImportError:
    print("Error: google-genai package not installed. Please run: pip install google-genai")
    sys.exit(1)


class NanoBananaClient:
    """
    A wrapper class for the Gemini 2.5 Flash Image (Nano Banana) API.
    
    This class provides easy-to-use methods for:
    - Generating images from text prompts
    - Editing images with text instructions
    - Restoring and colorizing old photos
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NanoBanana client.
        
        Args:
            api_key (Optional[str]): The Google AI API key. If not provided,
                                   will try to get from environment variable.
        """
        self.api_key = api_key or Config.get_api_key()
        
        if not self.api_key:
            raise ValueError(
                f"API key not provided. Please set the {Config.API_KEY_ENV_VAR} "
                "environment variable or pass the api_key parameter."
            )
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = Config.MODEL_NAME
        
        # Ensure output directories exist
        os.makedirs(Config.DEFAULT_OUTPUT_DIR, exist_ok=True)
        os.makedirs(Config.DEFAULT_INPUT_DIR, exist_ok=True)
    
    def generate_image(self, 
                      prompt: str, 
                      output_filename: Optional[str] = None,
                      save_to_disk: bool = True) -> Union[Image.Image, str]:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt (str): The text description of the image to generate
            output_filename (Optional[str]): Filename to save the image. 
                                           If None, will generate a timestamp-based name.
            save_to_disk (bool): Whether to save the image to disk
            
        Returns:
            Union[Image.Image, str]: PIL Image object if save_to_disk=False, 
                                   file path if save_to_disk=True
        """
        print(f"🎨 Generating image: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            
            # Extract image from response
            image = self._extract_image_from_response(response)
            
            if save_to_disk:
                if not output_filename:
                    timestamp = int(time.time())
                    output_filename = f"generated_{timestamp}.png"
                
                output_path = Config.get_output_path(output_filename)
                image.save(output_path)
                print(f"✅ Image saved to: {output_path}")
                return output_path
            
            return image
            
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")
            raise
    
    def edit_image(self,
                  image_path: str,
                  prompt: str,
                  output_filename: Optional[str] = None,
                  save_to_disk: bool = True,
                  image_url: Optional[str] = None) -> Union[Image.Image, str]:
        """
        Edit an existing image using a text prompt.

        Args:
            image_path (str): Path to the input image (ignored if image_url is provided)
            prompt (str): Text description of the desired edits
            output_filename (Optional[str]): Filename to save the edited image.
                                           If None, will generate a timestamp-based name.
            save_to_disk (bool): Whether to save the image to disk
            image_url (Optional[str]): URL to download the image from (takes precedence over image_path)

        Returns:
            Union[Image.Image, str]: PIL Image object if save_to_disk=False,
                                   file path if save_to_disk=True
        """
        print(f"✏️  Editing image: {image_url if image_url else image_path}")
        print(f"📝 Edit instruction: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")

        try:
            # Load the input image
            if image_url:
                # Download image from URL
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                input_image = Image.open(BytesIO(response.content))
            else:
                input_image = Image.open(image_path)
            
            # Send both prompt and image to the API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, input_image],
            )
            
            # Extract edited image from response
            edited_image = self._extract_image_from_response(response)
            
            if save_to_disk:
                if not output_filename:
                    timestamp = int(time.time())
                    base_name = os.path.splitext(os.path.basename(image_path))[0]
                    output_filename = f"{base_name}_edited_{timestamp}.png"
                
                output_path = Config.get_output_path(output_filename)
                edited_image.save(output_path)
                print(f"✅ Edited image saved to: {output_path}")
                return output_path
            
            return edited_image
            
        except Exception as e:
            print(f"❌ Error editing image: {str(e)}")
            raise
    
    def restore_photo(self, 
                     image_path: str, 
                     output_filename: Optional[str] = None,
                     custom_prompt: Optional[str] = None,
                     save_to_disk: bool = True) -> Union[Image.Image, str]:
        """
        Restore and colorize an old photograph.
        
        Args:
            image_path (str): Path to the old photo
            output_filename (Optional[str]): Filename to save the restored image.
                                           If None, will generate a timestamp-based name.
            custom_prompt (Optional[str]): Custom restoration prompt. If None, uses default.
            save_to_disk (bool): Whether to save the image to disk
            
        Returns:
            Union[Image.Image, str]: PIL Image object if save_to_disk=False, 
                                   file path if save_to_disk=True
        """
        print(f"🔧 Restoring photo: {image_path}")
        
        # Default restoration prompt
        if not custom_prompt:
            custom_prompt = "Restore and colorize this old photograph. Enhance the image quality, remove any damage or artifacts, and add realistic colors while preserving the original composition and subjects."
        
        try:
            # Load the old photo
            old_photo = Image.open(image_path)
            
            # Send restoration prompt and image to the API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[custom_prompt, old_photo],
            )
            
            # Extract restored image from response
            restored_image = self._extract_image_from_response(response)
            
            if save_to_disk:
                if not output_filename:
                    timestamp = int(time.time())
                    base_name = os.path.splitext(os.path.basename(image_path))[0]
                    output_filename = f"{base_name}_restored_{timestamp}.png"
                
                output_path = Config.get_output_path(output_filename)
                restored_image.save(output_path)
                print(f"✅ Restored photo saved to: {output_path}")
                return output_path
            
            return restored_image
            
        except Exception as e:
            print(f"❌ Error restoring photo: {str(e)}")
            raise
    
    def _extract_image_from_response(self, response) -> Image.Image:
        """
        Extract the image from the API response.
        
        Args:
            response: The API response object
            
        Returns:
            Image.Image: The extracted PIL Image
            
        Raises:
            ValueError: If no image is found in the response
        """
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(f"📄 Response text: {part.text}")
            elif part.inline_data is not None:
                return Image.open(BytesIO(part.inline_data.data))
        
        raise ValueError("No image found in the API response")
    
    def estimate_cost(self, num_images: int) -> float:
        """
        Estimate the cost for generating a number of images.
        
        Args:
            num_images (int): Number of images to estimate cost for
            
        Returns:
            float: Estimated cost in USD
        """
        return num_images * Config.COST_PER_IMAGE
    
    def get_pricing_info(self) -> dict:
        """
        Get pricing information for the Nano Banana model.
        
        Returns:
            dict: Pricing information
        """
        return {
            "cost_per_image_usd": Config.COST_PER_IMAGE,
            "images_per_dollar": Config.IMAGES_PER_DOLLAR,
            "model_name": self.model_name
        }