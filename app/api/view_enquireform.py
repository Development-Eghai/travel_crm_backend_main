from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from models.model_enquireform import EnquireForm
from schemas.schema_enquireform import (
    EnquireFormCreate,
    EnquireFormUpdate,
    EnquireFormOut
)

from core.database import get_db
from utils.response import api_json_response_format
from models.user import User
from models.api_key import APIKey
from utils.email_utility import send_enquiry_email

router = APIRouter()


# ---------------------------------------------------------------
# GET ALL (non-deleted)
# ---------------------------------------------------------------
@router.get("/")
async def get_enquiries(db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        enquiries = (
            db.query(EnquireForm)
            .filter(EnquireForm.user_id == api_entry.user_id, EnquireForm.is_deleted == False)
            .order_by(EnquireForm.created_at.desc())
            .all()
        )

        data = [EnquireFormOut.model_validate(e).model_dump() for e in enquiries]
        return api_json_response_format(True, "Enquiries retrieved.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving enquiries: {e}", 500, {})


# ---------------------------------------------------------------
# GET ONE
# ---------------------------------------------------------------
@router.get("/{enquire_id}")
async def get_enquiry(enquire_id: int, db: Session = Depends(get_db)):
    try:
        enquiry = db.query(EnquireForm).filter(EnquireForm.id == enquire_id).first()
        if not enquiry or enquiry.is_deleted:
            return api_json_response_format(False, "Enquiry not found", 404, {})

        data = EnquireFormOut.model_validate(enquiry).model_dump()
        return api_json_response_format(True, "Enquiry retrieved.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving enquiry: {e}", 500, {})


# ---------------------------------------------------------------
# CREATE ENQUIRY
# ---------------------------------------------------------------
@router.post("/")
async def create_enquiry(
    data: EnquireFormCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.website == data.domain_name).first()
        if not user:
            return api_json_response_format(False, "Invalid domain name – user not found.", 404, {})

        payload = data.dict(exclude={"domain_name"})
        record = EnquireForm(user_id=user.id, **payload)

        db.add(record)
        db.flush()
        record.enquiry_id = record.id

        db.commit()
        db.refresh(record)

        response_data = EnquireFormOut.model_validate(record).model_dump()

        x_api_key = request.headers.get("x-api-key")
        try:
            send_enquiry_email(response_data, x_api_key)
        except Exception as e:
            print("Email failed:", e)

        return api_json_response_format(True, "Enquiry created successfully.", 201, response_data)

    except Exception as e:
        return api_json_response_format(False, f"Error creating enquiry: {e}", 500, {})


# ---------------------------------------------------------------
# UPDATE ENQUIRY (PUT)
# ---------------------------------------------------------------
@router.put("/{enquire_id}")
async def update_enquiry(
    enquire_id: int,
    data: EnquireFormUpdate,
    db: Session = Depends(get_db),
    x_api_key: str = Header(None)
):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        record = (
            db.query(EnquireForm)
            .filter(
                EnquireForm.id == enquire_id,
                EnquireForm.user_id == api_entry.user_id,
                EnquireForm.is_deleted == False
            )
            .first()
        )

        if not record:
            return api_json_response_format(False, "Enquiry not found", 404, {})

        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)

        response_data = EnquireFormOut.model_validate(record).model_dump()

        return api_json_response_format(True, "Enquiry updated successfully.", 200, response_data)

    except Exception as e:
        db.rollback()
        return api_json_response_format(False, f"Error updating enquiry: {e}", 500, {})


# ---------------------------------------------------------------
# SOFT DELETE
# ---------------------------------------------------------------
@router.delete("/{enquire_id}/soft")
async def soft_delete_enquiry(enquire_id: int, db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        record = db.query(EnquireForm).filter(
            EnquireForm.id == enquire_id,
            EnquireForm.user_id == api_entry.user_id
        ).first()

        if not record:
            return api_json_response_format(False, "Enquiry not found", 404, {})

        record.is_deleted = True
        db.commit()

        return api_json_response_format(True, "Enquiry moved to trash.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Error deleting enquiry: {e}", 500, {})


# ---------------------------------------------------------------
# TRASH LIST
# ---------------------------------------------------------------
@router.get("/trash/list")
async def get_enquiry_trash(db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        trashed = (
            db.query(EnquireForm)
            .filter(EnquireForm.user_id == api_entry.user_id, EnquireForm.is_deleted == True)
            .order_by(EnquireForm.created_at.desc())
            .all()
        )

        data = [EnquireFormOut.model_validate(e).model_dump() for e in trashed]
        return api_json_response_format(True, "Trash retrieved.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trash: {e}", 500, {})


# ---------------------------------------------------------------
# HARD DELETE
# ---------------------------------------------------------------
@router.delete("/{enquire_id}/hard")
async def hard_delete_enquiry(enquire_id: int, db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        record = db.query(EnquireForm).filter(
            EnquireForm.id == enquire_id,
            EnquireForm.user_id == api_entry.user_id
        ).first()

        if not record:
            return api_json_response_format(False, "Enquiry not found", 404, {})

        db.delete(record)
        db.commit()

        return api_json_response_format(True, "Enquiry permanently deleted.", 200, {})

    except Exception as e:
        db.rollback()
        return api_json_response_format(False, f"Error deleting enquiry: {e}", 500, {})


enquire_router = router
