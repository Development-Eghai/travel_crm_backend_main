from datetime import datetime, timedelta
from models.api_key import APIKey
from models.user import User
from core.database import get_db
from schemas.user import LoginRequest, LoginResponse, UserStatus
from fastapi import FastAPI, Depends,File, UploadFile, HTTPException,Request,status
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
from fastapi.responses import JSONResponse
from typing import List

from jose import jwt, JWTError
from passlib.context import CryptContext

import os
from sqlalchemy.orm import Session

from api import trip_management
from api import invoice
from api.view_enquireform import enquire_router
from api.booking_request import booking_router
from api.trip_inquiries import trip_inquiry_router
from core.security import verify_api_key
from api.user import user_router
from api import (
    trip, destination, activity, trip_type, lead, lead_comments, quotation,
    bookings, category, trip_day, fixed_departure, lead_assignment, task,
    role, site_setting, activity_type, blog_post, tag, blog_category,
    quotation_item, user,booking_request
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

secure_app.include_router(trip_inquiry_router, prefix="/api/trip_enquires", tags=["Trip Enquires"])
secure_app.include_router(booking_router, prefix="/api/booking_request", tags=["Booking Requests"])
secure_app.include_router(enquire_router,prefix="/api/enquires", tags=["Enquires"])


# secure_app.include_router(trip_inquiry_router, prefix="/api/trip_enquires", tags=["Trip Enquires"])



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
# public_app.include_router(booking_router, prefix="/api/booking_request", tags=["Booking Requests"])
# public_app.include_router(trip_inquiry_router, prefix="/api/trip_enquires", tags=["Trip Enquires"])


try:
    # 🧬 Mount both apps
    app = FastAPI(title="Travel CRM Gateway")
    app.mount("/secure", secure_app)
    app.mount("/public", public_app)
except Exception as e:
    import sys
    print(f"Startup error: {e}", file=sys.stderr)
    raise


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin like "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login", response_model=LoginResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    normalized_email = request.email.lower()
    domain_name = request.domain_name
    user = db.query(User).filter(User.email == normalized_email, User.website == domain_name).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if user.status != UserStatus.Active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not active")

    # Get active API key if exists
    api_key_obj = db.query(APIKey).filter(
        APIKey.user_id == user.id,
        APIKey.is_active == True
    ).order_by(APIKey.created_at.desc()).first()

    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "tenant_id": str(user.tenant_id),
        "role": user.role.name
    }
    access_token = create_access_token(data=token_data)
    

    return LoginResponse(
        access_token=access_token,
        api_key=api_key_obj.key_value if api_key_obj else None
    )


@app.post("/admin_login", response_model=LoginResponse)
def admin_login(request: LoginRequest):
    email = request.email
    password = request.password
    if email == "sales@indianmountainrovers.com" and password == "IndianMountainRovers2511@":
        token_data = {
        "sub": str(1001),
        "email": email,
        "tenant_id": str(1234),
        "role": "admin"   
        }

        access_token = create_access_token(data=token_data)
        return LoginResponse(        access_token=access_token   )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")