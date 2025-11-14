from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.api_key import APIKey
from utils.response import api_json_response_format

router = APIRouter()


def get_user_from_api_key(db: Session, x_api_key: str):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="x-api-key missing")

    api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
    if not api_key_entry:
        raise HTTPException(status_code=401, detail="Invalid API key")

    user = db.query(User).filter(User.id == api_key_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------------------------------------------------------
# GET SMTP SETTINGS
# -------------------------------------------------------
@router.get("/smtp")
def get_smtp_settings(
    db: Session = Depends(get_db),
    x_api_key: str = Header(None)
):
    try:
        user = get_user_from_api_key(db, x_api_key)

        data = {
            "smtp_host": user.smtp_host,
            "smtp_port": user.smtp_port,
            "smtp_username": user.smtp_username,
            "smtp_password": user.smtp_password,
            "admin_email": user.admin_email
        }

        return api_json_response_format(True, "SMTP settings loaded.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Failed loading SMTP settings: {e}", 500, {})


# -------------------------------------------------------
# UPDATE SMTP SETTINGS
# -------------------------------------------------------
@router.post("/smtp")
def update_smtp_settings(
    payload: dict,
    db: Session = Depends(get_db),
    x_api_key: str = Header(None)
):
    try:
        user = get_user_from_api_key(db, x_api_key)

        user.smtp_host = payload.get("smtp_host")
        user.smtp_port = payload.get("smtp_port")
        user.smtp_username = payload.get("smtp_username")
        user.smtp_password = payload.get("smtp_password")
        user.admin_email = payload.get("admin_email")

        db.commit()

        return api_json_response_format(True, "SMTP settings updated.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Failed updating SMTP settings: {e}", 500, {})


user_smtp_settings_router = router
