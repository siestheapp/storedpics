from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
import os
import json
from datetime import datetime
from typing import Optional
import uuid

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")

# Ensure required directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Metadata log file path
METADATA_LOG = "logs/upload_metadata.json"

# Initialize metadata log if it doesn't exist
if not os.path.exists(METADATA_LOG):
    with open(METADATA_LOG, "w") as f:
        json.dump([], f)

@app.get("/", response_class=HTMLResponse)
async def gallery(request: Request):
    # Read the metadata log
    with open(METADATA_LOG, "r") as f:
        images = json.load(f)
    
    # Sort images by upload date, newest first
    images.sort(key=lambda x: x.get("uploaded_at", ""), reverse=True)
    
    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})

# Mount the static directory for serving images
app.mount("/images", StaticFiles(directory="uploads"), name="images")

@app.get("/upload-form", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    uploader: str = Form('sd'),
    brand_name: Optional[str] = Form(None),
    size_guide_header: Optional[str] = Form(None),
    gender: Optional[str] = Form('Men'),
    fit: Optional[str] = Form(None),
    unit: Optional[str] = Form('in'),
    category: Optional[str] = Form(None),
    source_url: Optional[str] = Form(None)
):
    # Generate a human-readable filename: <uploader>__<YYYYMMDD_HHMMSS>.<ext>
    file_extension = os.path.splitext(file.filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_uploader = uploader.replace(" ", "_")
    unique_filename = f"{safe_uploader}__{timestamp}{file_extension}"

    # Save the file
    file_path = os.path.join("uploads", unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Prepare metadata
    metadata = {
        "filename": unique_filename,
        "original_filename": file.filename,
        "uploader": uploader,
        "brand_name": brand_name,
        "gender": gender,
        "size_guide_header": size_guide_header,
        "unit": unit,
        "category": category,
        "fit": fit,
        "uploaded_at": datetime.now().isoformat()
    }
    
    # Read existing metadata
    with open(METADATA_LOG, "r") as f:
        all_metadata = json.load(f)
    
    # Add new metadata
    all_metadata.append(metadata)
    
    # Write updated metadata
    with open(METADATA_LOG, "w") as f:
        json.dump(all_metadata, f, indent=2)
    
    return {"message": "File uploaded successfully", "metadata": metadata}

@app.get("/routes")
def list_routes():
    return [route.path for route in app.routes]

@app.get("/image/{filename}", response_class=HTMLResponse)
async def image_detail(request: Request, filename: str = Path(...)):
    # Read the metadata log
    with open(METADATA_LOG, "r") as f:
        images = json.load(f)
    # Find the image by filename
    image = next((img for img in images if img["filename"] == filename), None)
    if not image:
        return HTMLResponse(content="<h2>Image not found</h2>", status_code=404)
    return templates.TemplateResponse("image_detail.html", {"request": request, "image": image})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 