from fastapi import FastAPI, Depends,File, UploadFile, HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
from fastapi.responses import JSONResponse
from typing import List



import os

from api import trip_management
from api import invoice
from api.view_enquireform import enquire_router
from core.security import verify_api_key
from api.user import user_router
from api import (
    trip, destination, activity, trip_type, lead, lead_comments, quotation,
    bookings, category, trip_day, fixed_departure, lead_assignment, task,
    role, site_setting, activity_type, blog_post, tag, blog_category,
    quotation_item, user
)

# 🔐 Secure app with global dependency
secure_app = FastAPI(
    title="Travel CRM",
    dependencies=[Depends(verify_api_key)]
)


# origins = [
#     "http://localhost:5173",
# ]



# ✅ Add CORS to secure app
secure_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (localhost etc.)
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@secure_app.get("/")
def root():
    return {"msg": "Secure app is live"}

# 🔗 Secure endpoints
secure_app.include_router(invoice.router, prefix="/api/invoice", tags=["invoice"])
secure_app.include_router(quotation_item.router, prefix="/api/quotation-items", tags=["Quotation Items"])
secure_app.include_router(blog_category.router, prefix="/api/blog-categories", tags=["Blog Categories"])
secure_app.include_router(tag.router, prefix="/api/tags", tags=["Tags"])
secure_app.include_router(blog_post.router, prefix="/api/blog-posts", tags=["Blog Posts"])
secure_app.include_router(activity_type.router, prefix="/api/activity-types", tags=["Activity Types"])
secure_app.include_router(site_setting.router, prefix="/api/site-settings", tags=["Site Settings"])
secure_app.include_router(role.router, prefix="/api/roles", tags=["Roles"])
secure_app.include_router(task.router, prefix="/api/task", tags=["Tasks"])
secure_app.include_router(lead_assignment.router, prefix="/api/lead-assignments", tags=["Lead Assignments"])
secure_app.include_router(fixed_departure.router, prefix="/api/fixed-departures", tags=["Fixed Departures"])
secure_app.include_router(trip_day.router, prefix="/api/trip-days", tags=["Trip Days"])
secure_app.include_router(category.router, prefix="/api/categories", tags=["Categories"])
secure_app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
secure_app.include_router(lead_comments.router, prefix="/api/lead-comments", tags=["Lead Comments"])
secure_app.include_router(quotation.router, prefix="/api/quotation", tags=["Quotation"])
secure_app.include_router(trip_type.router, prefix="/api/trip-types", tags=["Trip Types"])
secure_app.include_router(lead.router, prefix="/api/leads", tags=["Leads"])
secure_app.include_router(activity.router, prefix="/api/activities", tags=["Activities"])
secure_app.include_router(trip.router, prefix="/api/trips", tags=["Trips"])
secure_app.include_router(destination.router, prefix="/api/destinations", tags=["Destinations"])
secure_app.include_router(trip_management.router, prefix="/api/trip-management", tags=["Trip Management"])



# 🧑‍💼 Public app for user registration/login
public_app = FastAPI(
    title="User Access",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ✅ Add CORS to public app as well
public_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

public_app.include_router(user_router, prefix="/api/users", tags=["Users"])
public_app.include_router(enquire_router,prefix="/api/enquires", tags=["Enquires"])

try:
    # 🧬 Mount both apps
    app = FastAPI(title="Travel CRM Gateway")
    app.mount("/secure", secure_app)
    app.mount("/public", public_app)
except Exception as e:
    import sys
    print(f"Startup error: {e}", file=sys.stderr)
    raise

@app.get("/")
def gateway_root():
    return {"msg": "Travel CRM Gateway is live with the UPDATED GIT version in hostinger"}

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount the uploads folder for public access
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# Helper to check allowed file extensions
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



IMG_URL = "https://api.yaadigo.com/uploads"

@app.post("/upload")
def upload_image(image: UploadFile = File(...)):
    if image.filename == "":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No selected file")

    if not allowed_file(image.filename):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="File type not allowed")

    file_path = Path(UPLOAD_FOLDER) / image.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"{IMG_URL}/{image.filename}"
    print(image_url)
    # return trip.api_json_response_format(True, "Trips fetched successfully", 0, {})
    return JSONResponse(status_code=200, content={"message": "Upload successful", "url": image_url})

@app.post("/multiple")
def upload_gallery_images(gallery_images: List[UploadFile] = File(...), request: Request = None):
    if not gallery_images:
        return JSONResponse(content={'error': 'No files part'}, status_code=400)

    saved_files = []

    for file in gallery_images:
        if file.filename:
            filename = Path(file.filename).name  # Secure the filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_url = f"{IMG_URL}/{filename}"
            # file_url = request.url_for('static', path=f"uploads/{filename}")
            saved_files.append(str(image_url))

    return {'message': 'Files uploaded', 'files': saved_files}

