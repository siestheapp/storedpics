# Screenshot Upload API

A FastAPI backend for uploading and managing screenshot images with metadata.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### POST /upload

Upload a screenshot image with metadata.

**Required fields:**
- `file`: The image file (multipart/form-data)
- `uploader`: String identifier for the uploader

**Optional metadata fields:**
- `brand_name`: String
- `gender`: String (e.g., "men", "women", "unisex")
- `size_guide_header`: String
- `unit`: String
- `source_url`: String
- `category`: String
- `scope`: String
- `notes`: String
- `fit`: String (e.g., "slim", "regular", "relaxed")

**Response:**
```json
{
    "status": "success",
    "filename": "uploader__notes__20240220_123456.png",
    "file_path": "backend/ingests/2024-02-20/uploader__notes__20240220_123456.png",
    "metadata": {
        "original_filename": "original.png",
        "new_filename": "uploader__notes__20240220_123456.png",
        "uploader": "user123",
        "upload_date": "2024-02-20T12:34:56.789Z",
        "file_path": "backend/ingests/2024-02-20/uploader__notes__20240220_123456.png",
        "brand_name": "Example Brand",
        "gender": "men",
        "size_guide_header": "Size Guide",
        "unit": "cm",
        "source_url": "https://example.com",
        "category": "clothing",
        "scope": "global",
        "notes": "example notes",
        "fit": "regular"
    }
}
```

## File Structure

- Uploaded files are stored in `backend/ingests/YYYY-MM-DD/`
- Metadata is logged in `backend/metadata_log.json`
- Files are renamed to: `{uploader}__{notes}__{timestamp}.png` 