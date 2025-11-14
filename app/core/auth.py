from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.api_key import APIKey

def get_current_user_id(
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="x-api-key header missing")

    api_key_row = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
    if not api_key_row:
        raise HTTPException(status_code=401, detail="Invalid x-api-key")

    return api_key_row.user_id
