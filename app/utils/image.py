import os, io
from datetime import datetime
from fastapi import UploadFile, HTTPException
from PIL import Image

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(file: UploadFile) -> str:
    try:
        image_data = file.file.read()
        image = Image.open(io.BytesIO(image_data))
        file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        image.save(file_path, format="WEBP", quality=85)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image upload failed: {str(e)}")