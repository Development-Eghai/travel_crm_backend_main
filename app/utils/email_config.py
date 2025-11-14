# app/utils/email_config.py
from core.database import SessionLocal
from models.api_key import APIKey
from models.user import User
from typing import Optional, Dict

def get_tenant_email_settings_by_api_key(api_key_value: str) -> Optional[Dict]:
    """
    Return tenant SMTP settings for the given API key.
    Uses a local Session and closes it.
    """
    if not api_key_value:
        return None

    db = SessionLocal()
    try:
        api = db.query(APIKey).filter(APIKey.key_value == api_key_value).first()
        if not api:
            return None
        user = db.query(User).filter(User.id == api.user_id).first()
        if not user:
            return None

        return {
            "smtp_host": user.smtp_host,
            "smtp_port": int(user.smtp_port) if user.smtp_port else 587,
            "smtp_username": user.smtp_username,
            "smtp_password": user.smtp_password,
            "admin_email": user.admin_email or user.smtp_username
        }
    finally:
        db.close()
