"""
Cloudinary utility functions for Nano Banana web app
"""

import os
import io
import time
import requests
from typing import Optional, Union
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CloudinaryManager:
    """Manages Cloudinary operations for the image studio"""
    
    def __init__(self):
        """Initialize Cloudinary configuration"""
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            secure=True
        )

        # CLIENT_FOLDER_NAME is now optional - can be provided per-request
        self.client_folder = os.getenv('CLIENT_FOLDER_NAME', None)

        # Validate configuration
        if not all([
            os.getenv('CLOUDINARY_CLOUD_NAME'),
            os.getenv('CLOUDINARY_API_KEY'),
            os.getenv('CLOUDINARY_API_SECRET')
        ]):
            raise ValueError("Missing Cloudinary configuration. Please set environment variables.")
    
    def upload_image(self, image_data: Union[bytes, Image.Image, str],
                    folder_type: str = "generated",
                    filename: Optional[str] = None,
                    client_folder: Optional[str] = None) -> dict:
        """
        Upload image to Cloudinary

        Args:
            image_data: Image bytes, PIL Image, or file path
            folder_type: 'input', 'generated', or 'edited'
            filename: Optional custom filename
            client_folder: Optional client folder name (overrides default from env)

        Returns:
            dict: Upload result with URL and public_id
        """
        try:
            timestamp = int(time.time())

            if filename is None:
                filename = f"image_{timestamp}"
            else:
                # Remove extension from filename
                filename = os.path.splitext(filename)[0]

            # Use provided client_folder or fall back to instance default
            folder_name = client_folder if client_folder is not None else self.client_folder

            # Validate that we have a client folder
            if folder_name is None:
                return {
                    'success': False,
                    'error': 'client_folder must be provided either in the request or via CLIENT_FOLDER_NAME environment variable'
                }

            # Create folder structure: client_name/folder_type/
            folder_path = f"{folder_name}/{folder_type}"
            
            # Handle different input types
            if isinstance(image_data, str) and os.path.exists(image_data):
                # File path
                upload_result = cloudinary.uploader.upload(
                    image_data,
                    folder=folder_path,
                    public_id=f"{filename}_{timestamp}",
                    resource_type="image",
                    overwrite=True
                )
            elif isinstance(image_data, Image.Image):
                # PIL Image
                img_bytes = io.BytesIO()
                image_data.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                upload_result = cloudinary.uploader.upload(
                    img_bytes,
                    folder=folder_path,
                    public_id=f"{filename}_{timestamp}",
                    resource_type="image",
                    overwrite=True
                )
            else:
                # Bytes
                upload_result = cloudinary.uploader.upload(
                    image_data,
                    folder=folder_path,
                    public_id=f"{filename}_{timestamp}",
                    resource_type="image",
                    overwrite=True
                )
            
            return {
                'success': True,
                'url': upload_result.get('secure_url'),
                'public_id': upload_result.get('public_id'),
                'width': upload_result.get('width'),
                'height': upload_result.get('height'),
                'bytes': upload_result.get('bytes'),
                'format': upload_result.get('format')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_image_from_url(self, cloudinary_url: str) -> Optional[Image.Image]:
        """
        Download image from Cloudinary URL
        
        Args:
            cloudinary_url: Cloudinary image URL
            
        Returns:
            PIL Image or None if failed
        """
        try:
            response = requests.get(cloudinary_url, timeout=30)
            response.raise_for_status()
            
            image = Image.open(io.BytesIO(response.content))
            return image
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
    
    def validate_cloudinary_url(self, url: str) -> bool:
        """
        Validate if URL is a proper Cloudinary URL
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if valid Cloudinary URL
        """
        if not url:
            return False
        
        # Basic Cloudinary URL validation
        cloudinary_domains = [
            'res.cloudinary.com',
            'cloudinary.com'
        ]
        
        return any(domain in url for domain in cloudinary_domains)
    
    def get_image_info(self, public_id: str) -> dict:
        """
        Get information about an image in Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            dict: Image information or error
        """
        try:
            result = cloudinary.api.resource(public_id)
            return {
                'success': True,
                'width': result.get('width'),
                'height': result.get('height'),
                'format': result.get('format'),
                'bytes': result.get('bytes'),
                'created_at': result.get('created_at'),
                'url': result.get('secure_url')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_image(self, public_id: str) -> dict:
        """
        Delete image from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            dict: Deletion result
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            return {
                'success': result.get('result') == 'ok',
                'result': result.get('result')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_images(self, folder_type: str = "generated", max_results: int = 50, client_folder: Optional[str] = None) -> dict:
        """
        List images in a specific folder

        Args:
            folder_type: Folder to search in
            max_results: Maximum number of results
            client_folder: Optional client folder (overrides default)

        Returns:
            dict: List of images or error
        """
        try:
            folder_name = client_folder if client_folder is not None else self.client_folder

            if folder_name is None:
                return {
                    'success': False,
                    'error': 'client_folder must be provided'
                }

            folder_path = f"{folder_name}/{folder_type}"

            result = cloudinary.api.resources(
                type="upload",
                prefix=folder_path,
                max_results=max_results,
                resource_type="image"
            )

            return {
                'success': True,
                'images': result.get('resources', []),
                'total_count': result.get('total_count', 0)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def list_client_folders(self) -> dict:
        """
        List all client folders in Cloudinary

        Returns:
            dict: List of client folder names or error
        """
        try:
            # Get all folders at root level
            result = cloudinary.api.root_folders()

            folders = [folder['name'] for folder in result.get('folders', [])]

            return {
                'success': True,
                'folders': folders
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def list_images_paginated(self, client_folder: str, folder_type: str = "all",
                             max_results: int = 30, next_cursor: Optional[str] = None,
                             start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
        """
        List images with pagination and optional date filtering

        Args:
            client_folder: Client folder name
            folder_type: 'all', 'generated', or 'edited'
            max_results: Number of results per page
            next_cursor: Pagination cursor from previous request
            start_date: Filter by start date (ISO format: YYYY-MM-DD)
            end_date: Filter by end date (ISO format: YYYY-MM-DD)

        Returns:
            dict: Paginated list of images with metadata
        """
        try:
            # Build folder path
            if folder_type == "all":
                folder_path = client_folder
            else:
                folder_path = f"{client_folder}/{folder_type}"

            # Build request parameters
            params = {
                'type': 'upload',
                'prefix': folder_path,
                'max_results': max_results,
                'resource_type': 'image',
                'context': True,
                'tags': True
            }

            if next_cursor:
                params['next_cursor'] = next_cursor

            # Execute request
            result = cloudinary.api.resources(**params)

            # Get images
            images = result.get('resources', [])

            # Filter by date if provided
            if start_date or end_date:
                from datetime import datetime
                filtered_images = []

                for img in images:
                    created_at = img.get('created_at', '')
                    if created_at:
                        # Parse date (format: 2024-10-07T12:34:56Z)
                        img_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).date()

                        # Check date range
                        if start_date:
                            start = datetime.fromisoformat(start_date).date()
                            if img_date < start:
                                continue

                        if end_date:
                            end = datetime.fromisoformat(end_date).date()
                            if img_date > end:
                                continue

                        filtered_images.append(img)

                images = filtered_images

            return {
                'success': True,
                'images': images,
                'total_count': result.get('total_count', 0),
                'next_cursor': result.get('next_cursor'),
                'has_more': 'next_cursor' in result
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def check_client_exists(self, client_name: str) -> dict:
        """
        Check if a client folder exists in Cloudinary

        Args:
            client_name: Client folder name to check

        Returns:
            dict: Existence status and folder path
        """
        try:
            # Try to get folder info
            result = cloudinary.api.subfolders(client_name)

            return {
                'success': True,
                'exists': True,
                'folder_path': client_name,
                'subfolders': [f['name'] for f in result.get('folders', [])]
            }

        except cloudinary.api.NotFound:
            return {
                'success': True,
                'exists': False,
                'folder_path': client_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def create_client_folders(self, client_name: str) -> dict:
        """
        Prepare client folder structure (folders will be created automatically on first upload)

        Note: Cloudinary doesn't have a direct folder creation API. Folders are created
        automatically when files are uploaded to them. This method just validates the
        client name and returns success so the UI can proceed.

        Args:
            client_name: Client folder name

        Returns:
            dict: Validation result
        """
        try:
            # Just validate the client name format
            import re
            if not re.match(r'^[a-zA-Z0-9-]+$', client_name):
                return {
                    'success': False,
                    'error': 'Invalid client name format'
                }

            # Folders will be created automatically when images are uploaded
            subfolders = ['input', 'generated', 'edited']

            return {
                'success': True,
                'folders_created': subfolders,
                'folder_path': client_name,
                'message': f'Client "{client_name}" is ready. Folders will be created automatically when you upload images.'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'folders_created': []
            }

    def get_upload_config(self, client_name: str) -> dict:
        """
        Get Cloudinary upload widget configuration for a client

        Args:
            client_name: Client folder name

        Returns:
            dict: Upload configuration parameters
        """
        try:
            return {
                'success': True,
                'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
                'api_key': os.getenv('CLOUDINARY_API_KEY'),
                'folder': f"{client_name}/input",
                'upload_preset': os.getenv('CLOUDINARY_UPLOAD_PRESET', 'ml_default')
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }