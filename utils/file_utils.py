"""
Utility functions for file operations and validation.
"""
import os
import base64
import uuid
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
import io


def create_directories() -> None:
    """Create necessary directories if they don't exist."""
    directories = ["uploads", "outputs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def validate_image_file(file_content: bytes, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if the uploaded file is a valid image.
    
    Args:
        file_content: Raw file content
        filename: Name of the uploaded file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    file_extension = Path(filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        return False, f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
    
    # Check if file is actually an image
    try:
        image = Image.open(io.BytesIO(file_content))
        image.verify()  # Verify it's actually an image
        return True, None
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def validate_base64_string(base64_string: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if the provided string is a valid Base64 encoded image.
    
    Args:
        base64_string: Base64 encoded string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check if it's valid base64
        decoded_data = base64.b64decode(base64_string)
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_data))
        image.verify()
        
        return True, None
    except Exception as e:
        return False, f"Invalid Base64 string or not a valid image: {str(e)}"


def generate_unique_filename(original_filename: str, extension: str = None) -> str:
    """
    Generate a unique filename to avoid conflicts.
    
    Args:
        original_filename: Original filename
        extension: Optional file extension override
        
    Returns:
        Unique filename
    """
    if extension is None:
        extension = Path(original_filename).suffix
    
    # Remove extension from original filename
    name_without_ext = Path(original_filename).stem
    
    # Generate unique identifier
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{name_without_ext}_{unique_id}{extension}"


def get_file_size_mb(file_content: bytes) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_content: File content in bytes
        
    Returns:
        File size in MB
    """
    return len(file_content) / (1024 * 1024)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove potentially dangerous characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    sanitized = filename
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Limit length
    if len(sanitized) > 100:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:95] + ext
    
    return sanitized 