"""
Configuration file for Nano Banana (Gemini 2.5 Flash Image) project.
"""

import os
from typing import Optional


class Config:
    """Configuration class for Nano Banana project."""
    
    # Model configuration
    MODEL_NAME = "gemini-2.5-flash-image-preview"
    
    # API configuration
    API_KEY_ENV_VAR = "GOOGLE_AI_API_KEY"
    
    # Image settings
    DEFAULT_OUTPUT_DIR = "images/output"
    DEFAULT_INPUT_DIR = "images/input"
    DEFAULT_IMAGE_FORMAT = "PNG"
    
    # Pricing information (as of the tutorial)
    COST_PER_IMAGE = 0.039  # USD
    IMAGES_PER_DOLLAR = 25
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Get the API key from environment variable.
        
        Returns:
            str: The API key if found, None otherwise
        """
        return os.getenv(Config.API_KEY_ENV_VAR)
    
    @staticmethod
    def validate_api_key() -> bool:
        """
        Validate that API key is available.
        
        Returns:
            bool: True if API key is available, False otherwise
        """
        return Config.get_api_key() is not None
    
    @staticmethod
    def get_output_path(filename: str) -> str:
        """
        Get the full output path for a filename.
        
        Args:
            filename (str): The filename
            
        Returns:
            str: Full path to the output file
        """
        return os.path.join(Config.DEFAULT_OUTPUT_DIR, filename)
    
    @staticmethod
    def get_input_path(filename: str) -> str:
        """
        Get the full input path for a filename.
        
        Args:
            filename (str): The filename
            
        Returns:
            str: Full path to the input file
        """
        return os.path.join(Config.DEFAULT_INPUT_DIR, filename)