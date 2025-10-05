from sqlalchemy.orm import Session
from models.user import User
from models.api_key import APIKey
from schemas.user import UserCreate
from passlib.context import CryptContext
from datetime import datetime
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password[:72])




def create_user(db: Session, user: UserCreate):
    normalized_email = user.email.lower()
    print("Password received:", user.password)
    print("Length:", len(user.password.encode("utf-8")))
    # Check for existing email
    if db.query(User).filter(User.email == normalized_email).first():
        raise ValueError("Email already registered")

    # Create user
    db_user = User(
        username=user.username,
        email=normalized_email,
        first_name=user.first_name,
        last_name=user.last_name,
        mobile_number=user.mobile_number,
        website=user.website,
        password_hash=get_password_hash(user.password),
        role=user.role,
        status="Active",
        send_user_email=user.send_user_email,
        tenant_id=user.tenant_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Generate API key
    key_value = secrets.token_urlsafe(32)
    api_key = APIKey(
        key_value=key_value,
        label=f"Auto-generated for {db_user.email}",
        tenant_id=db_user.tenant_id,
        user_id=db_user.id,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return db_user, key_value


def get_users(db: Session):
    return db.query(User).all()