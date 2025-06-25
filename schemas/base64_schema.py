"""
Pydantic models for Base64 image conversion API.
"""
from pydantic import BaseModel, Field
from typing import Optional


class Base64DecodeRequest(BaseModel):
    """Request model for decoding Base64 string to image."""
    base64_string: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = Field(None, description="Optional filename for the decoded image")


class Base64EncodeResponse(BaseModel):
    """Response model for image to Base64 encoding."""
    base64_string: str = Field(..., description="Base64 encoded image string")
    original_filename: str = Field(..., description="Original filename of the uploaded image")
    file_size: int = Field(..., description="Size of the original image in bytes")


class Base64DecodeResponse(BaseModel):
    """Response model for Base64 to image decoding."""
    message: str = Field(..., description="Success message")
    file_path: str = Field(..., description="Path where the decoded image was saved")
    filename: str = Field(..., description="Name of the saved image file")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details") 