from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from core.database import SessionLocal
from schemas.user import UserCreate, UserLogin, UserWithKey, UserOut
from crud.user import create_user, get_users
from core.security import verify_password
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user, api_key = create_user(db, user)
        user_data = UserOut.model_validate(db_user).model_dump()
        return api_json_response_format(True, "User created successfully.", 201, {"user": user_data, "api_key": api_key})
    except ValueError as e:
        return api_json_response_format(False, str(e), 400, {})
    except Exception as e:
        return api_json_response_format(False, f"Unexpected error creating user: {e}", 500, {})

@router.get("/")
def read_all(db: Session = Depends(get_db)):
    try:
        users = get_users(db)
        data = [UserOut.model_validate(u).model_dump() for u in users]
        return api_json_response_format(True, "Users retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving users: {e}", 500, {})

@router.post("/signin")
def sign_in(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == credentials.email).first()

        # Validate user and password
        if not user or not verify_password(credentials.password, user.password_hash):
            return api_json_response_format(False, "Invalid email or password.", 401, {})

        # Check user status
        if user.status != "Active":
            return api_json_response_format(False, f"User account is {user.status}.", 403, {})

        # Get API key
        api_key = user.api_keys[0].key_value if user.api_keys else None
        # Prepare user data
        user_data = UserOut.model_validate(user).model_dump()

        return api_json_response_format(True, "Sign-in successful.", 200, {
            "user": user_data,
            "api_key": api_key
        })

    except Exception as e:
        return api_json_response_format(False, f"Error during sign-in: {e}", 500, {})
    
user_router = router