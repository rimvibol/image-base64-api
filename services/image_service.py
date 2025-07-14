"""
Image processing service for Base64 conversion operations.
"""
import base64
import os
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
import io

from utils.file_utils import (
    create_directories,
    validate_image_file,
    validate_base64_string,
    generate_unique_filename,
    sanitize_filename
)


class ImageService:
    """Service class for image to Base64 conversion operations."""
    
    def __init__(self):
        """Initialize the service and create necessary directories."""
        create_directories()
        self.uploads_dir = Path("uploads")
        # Output directory within the project
        self.outputs_dir = Path("outputs")
        
        # Ensure the output directory exists
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def encode_image_to_base64(self, file_content: bytes, filename: str) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Encode an image file to Base64 string.
        
        Args:
            file_content: Raw file content
            filename: Original filename
            
        Returns:
            Tuple of (success, error_message, result_data)
        """
        try:
            # Validate the uploaded file
            is_valid, error_message = validate_image_file(file_content, filename)
            if not is_valid:
                return False, error_message, None
            
            # Encode to Base64
            base64_string = base64.b64encode(file_content).decode('utf-8')
            
            # Prepare response data
            result_data = {
                "base64_string": base64_string,
                "original_filename": filename,
                "file_size": len(file_content)
            }
            
            return True, None, result_data
            
        except Exception as e:
            return False, f"Error encoding image to Base64: {str(e)}", None
    
    def decode_base64_to_image(self, base64_string: str, filename: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Decode a Base64 string to an image file.
        
        Args:
            base64_string: Base64 encoded image string
            filename: Optional filename for the decoded image
            
        Returns:
            Tuple of (success, error_message, result_data)
        """
        try:
            # Validate the Base64 string
            is_valid, error_message = validate_base64_string(base64_string)
            if not is_valid:
                return False, error_message, None
            
            # Decode Base64 to bytes
            image_data = base64.b64decode(base64_string)
            
            # Determine file extension from image data
            image = Image.open(io.BytesIO(image_data))
            format_extension = self._get_extension_from_format(image.format or 'PNG')
            
            # Generate filename if not provided
            if not filename:
                filename = f"decoded_image{format_extension}"
            else:
                # Ensure filename has proper extension
                if not Path(filename).suffix:
                    filename = f"{filename}{format_extension}"
            
            # Sanitize filename
            filename = sanitize_filename(filename)
            
            # Generate unique filename to avoid conflicts
            unique_filename = generate_unique_filename(filename, format_extension)
            
            # Save the image to the specified output directory
            file_path = self.outputs_dir / unique_filename
            
            # Save with proper format
            image.save(file_path, format=image.format)
            
            # Prepare response data
            result_data = {
                "message": "Image successfully decoded and saved",
                "file_path": str(file_path),
                "filename": unique_filename
            }
            
            return True, None, result_data
            
        except Exception as e:
            return False, f"Error decoding Base64 to image: {str(e)}", None
    
    def _get_extension_from_format(self, format_name: str) -> str:
        """
        Get file extension from PIL image format.
        
        Args:
            format_name: PIL image format name
            
        Returns:
            File extension with dot
        """
        format_to_extension = {
            'JPEG': '.jpg',
            'PNG': '.png',
            'GIF': '.gif',
            'BMP': '.bmp',
            'TIFF': '.tiff',
            'WEBP': '.webp'
        }
        
        return format_to_extension.get(format_name.upper(), '.png')
    
    def cleanup_old_files(self, max_age_hours: int = 24) -> None:
        """
        Clean up old files from uploads and outputs directories.
        This is a utility method that could be called periodically.
        
        Args:
            max_age_hours: Maximum age of files in hours before deletion
        """
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for directory in [self.uploads_dir, self.outputs_dir]:
            if directory.exists():
                for file_path in directory.iterdir():
                    if file_path.is_file():
                        file_age = current_time - file_path.stat().st_mtime
                        if file_age > max_age_seconds:
                            try:
                                file_path.unlink()
                            except Exception:
                                pass  # Ignore errors during cleanup 