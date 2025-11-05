# XLIFF Editor Backend

FastAPI-based backend for parsing and managing XLIFF 1.2 files.

## Setup

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn main:app --reload
```

### Production Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Health check endpoint

**Response:**
```json
{
  "message": "XLIFF Editor API",
  "version": "1.0"
}
```

### `POST /upload`
Upload and parse an XLIFF file

**Request:**
- Form-data with file field containing .xliff or .xlf file

**Response:**
```json
{
  "version": "1.2",
  "files": [...]
}
```

### `PUT /trans-unit`
Update a translation unit's target

**Request Body:**
```json
{
  "file_index": 0,
  "trans_unit_id": "1",
  "target_text": "New translation",
  "target_tags": []
}
```

### `GET /download`
Download the modified XLIFF file

**Response:**
- XLIFF file as attachment

### `DELETE /clear`
Clear the currently loaded file from memory

## File Structure

```
backend/
├── main.py           # FastAPI application and endpoints
├── models.py         # Pydantic data models
├── xliff_parser.py   # XLIFF parsing logic with lxml
└── requirements.txt  # Python dependencies
```

## Testing with cURL

### Upload a file
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.xliff"
```

### Download the file
```bash
curl -X GET "http://localhost:8000/download" \
  --output modified.xliff
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

- **FastAPI**: Modern, fast web framework
- **uvicorn**: ASGI server
- **lxml**: Powerful XML processing library
- **pydantic**: Data validation using Python type hints
- **python-multipart**: For file upload support

## Notes

- The current implementation stores files in memory
- For production, implement proper file storage (database, file system, S3, etc.)
- CORS is configured for local development on ports 3000 and 5173