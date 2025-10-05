from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.api_key import APIKey
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_api_key(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    key = db.query(APIKey).filter(APIKey.key_value == x_api_key, APIKey.is_active == True).first()
    if not key:
        raise HTTPException(status_code=403, detail="Invalid or inactive API key")
    return key

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)