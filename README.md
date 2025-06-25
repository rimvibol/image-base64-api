# Image Base64 API

A FastAPI-based REST API for converting images to Base64 strings and vice versa. This project follows Python best practices and provides a clean, production-ready solution for image encoding and decoding operations.

## Features

- **Image to Base64**: Upload image files (JPG, PNG, GIF, BMP, TIFF) and convert them to Base64 strings
- **Base64 to Image**: Convert Base64 strings back to image files with automatic format detection
- **File Validation**: Comprehensive validation for uploaded files and Base64 strings
- **Error Handling**: Clear error messages with proper HTTP status codes
- **API Documentation**: Auto-generated OpenAPI documentation
- **Production Ready**: Clean code structure following Python best practices

## Project Structure

```
image_base64_api/
├── main.py                   # Entrypoint to start FastAPI app
├── routers/
│   └── image_routes.py       # Route definitions
├── services/
│   └── image_service.py      # Image processing logic (encode/decode)
├── schemas/
│   └── base64_schema.py      # Pydantic models for requests
├── utils/
│   └── file_utils.py         # Helper functions for file operations
├── requirements.txt          # Dependencies
├── .gitignore                # Python .gitignore standard
└── README.md                 # API documentation & usage instructions
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd image_base64_api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Health Check
- **GET** `/api/v1/health`
- **Description**: Check if the API is running and healthy
- **Response**: API status information

### 2. Encode Image to Base64
- **POST** `/api/v1/encode-image`
- **Description**: Upload an image file and convert it to a Base64 string
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: Image file (JPG, PNG, GIF, BMP, TIFF) - max 10MB

**Response Example**:
```json
{
  "base64_string": "iVBORw0KGgoAAAANSUhEUgAA...",
  "original_filename": "example.jpg",
  "file_size": 12345
}
```

### 3. Decode Base64 to Image
- **POST** `/api/v1/decode-base64`
- **Description**: Convert a Base64 string back to an image file
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "base64_string": "iVBORw0KGgoAAAANSUhEUgAA...",
  "filename": "optional_filename.jpg"
}
```

**Response Example**:
```json
{
  "message": "Image successfully decoded and saved",
  "file_path": "outputs/decoded_image_abc123.jpg",
  "filename": "decoded_image_abc123.jpg"
}
```

## Usage Examples

### Using cURL

#### Encode Image to Base64
```bash
curl -X POST "http://localhost:8000/api/v1/encode-image" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/image.jpg"
```

#### Decode Base64 to Image
```bash
curl -X POST "http://localhost:8000/api/v1/decode-base64" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "base64_string": "iVBORw0KGgoAAAANSUhEUgAA...",
       "filename": "my_image.jpg"
     }'
```

### Using Python Requests

```python
import requests

# Encode image to Base64
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/encode-image', files=files)
    result = response.json()
    print(f"Base64 string: {result['base64_string'][:50]}...")

# Decode Base64 to image
base64_data = {
    'base64_string': result['base64_string'],
    'filename': 'decoded_image.jpg'
}
response = requests.post('http://localhost:8000/api/v1/decode-base64', json=base64_data)
result = response.json()
print(f"Image saved to: {result['file_path']}")
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid file format, corrupted image, or invalid Base64 string
- **413 Request Entity Too Large**: File size exceeds 10MB limit
- **500 Internal Server Error**: Unexpected server errors

**Error Response Format**:
```json
{
  "error": "Error message",
  "detail": "Additional error details"
}
```

## File Management

- **Uploads**: Temporary storage for uploaded files (auto-created)
- **Outputs**: Storage for decoded images (auto-created)
- **Cleanup**: Files are not automatically deleted; implement cleanup as needed

## Configuration

### Environment Variables
Create a `.env` file for environment-specific configuration:
```env
# API Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# File Upload Limits
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

### CORS Configuration
The API includes CORS middleware configured for development. For production, update the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Development

### Code Style
This project follows PEP 8 naming conventions and includes comprehensive docstrings.

### Testing
To add tests, create a `tests/` directory and use pytest:

```bash
pip install pytest
pytest tests/
```

### Linting
Use flake8 for code linting:

```bash
pip install flake8
flake8 .
```

## Production Deployment

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Security Considerations

- **File Upload Validation**: All uploaded files are validated for format and content
- **Filename Sanitization**: Filenames are sanitized to prevent path traversal attacks
- **Size Limits**: File uploads are limited to 10MB
- **Error Handling**: Sensitive information is not exposed in error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the error messages for troubleshooting
3. Open an issue on the repository

---

**Note**: This API is designed for development and testing purposes. For production use, consider implementing authentication, rate limiting, and additional security measures. 