"""
FastAPI router for image to Base64 conversion endpoints.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from services.image_service import ImageService
from schemas.base64_schema import (
    Base64DecodeRequest,
    Base64EncodeResponse,
    Base64DecodeResponse,
    ErrorResponse
)

# Initialize router
router = APIRouter(prefix="/api/v1", tags=["image-conversion"])

# Initialize service
image_service = ImageService()


@router.post(
    "/encode-image",
    response_model=Base64EncodeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Encode image to Base64",
    description="Upload an image file and convert it to a Base64 encoded string."
)
async def encode_image_to_base64(
    file: UploadFile = File(..., description="Image file to encode (JPG, PNG, GIF, BMP, TIFF)")
) -> Base64EncodeResponse:
    """
    Encode an uploaded image file to Base64 string.
    
    Args:
        file: Image file uploaded via multipart/form-data
        
    Returns:
        Base64EncodeResponse with the encoded string and metadata
        
    Raises:
        HTTPException: If file is invalid, too large, or processing fails
    """
    try:
        # Check if file was uploaded
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file uploaded"
            )
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        file_content = await file.read()
        
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size is {max_size / (1024*1024)}MB"
            )
        
        # Process the image
        success, error_message, result_data = image_service.encode_image_to_base64(
            file_content, file.filename
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        return Base64EncodeResponse(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/decode-base64",
    response_model=Base64DecodeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Decode Base64 to image",
    description="Convert a Base64 encoded string back to an image file and save it."
)
async def decode_base64_to_image(
    request: Base64DecodeRequest
) -> Base64DecodeResponse:
    """
    Decode a Base64 string to an image file and save it.
    
    Args:
        request: Base64DecodeRequest containing the Base64 string and optional filename
        
    Returns:
        Base64DecodeResponse with file path and success message
        
    Raises:
        HTTPException: If Base64 string is invalid or processing fails
    """
    try:
        # Process the Base64 string
        success, error_message, result_data = image_service.decode_base64_to_image(
            request.base64_string, request.filename
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        return Base64DecodeResponse(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is running and healthy."
)
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        JSON response indicating API health
    """
    return {
        "status": "healthy",
        "message": "Image Base64 API is running",
        "version": "1.0.0"
    }


@router.get(
    "/hello",
    status_code=status.HTTP_200_OK,
    summary="Hello endpoint",
    description="Simple hello endpoint to test the API."
)
async def hello():
    """
    Hello endpoint for testing purposes.
    
    Returns:
        JSON response with a hello message
    """
    return {
        "message": "Hello! Welcome to the Image Base64 API",
        "endpoints": {
            "encode": "/api/v1/encode-image",
            "decode": "/api/v1/decode-base64",
            "health": "/api/v1/health"
        }
    } 