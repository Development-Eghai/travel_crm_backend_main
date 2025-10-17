from utils.email_utility import send_enquiry_email
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.model_enquireform import EnquireForm
from schemas.schema_enquireform import EnquireFormCreate, EnquireFormOut
from core.database import get_db
from utils.response import api_json_response_format

router = APIRouter()

@router.get("/")
async def get_enquiries(db: Session = Depends(get_db)):
    try:
        enquiries = db.query(EnquireForm).order_by(EnquireForm.created_at.desc()).all()
        data = [EnquireFormOut.model_validate(e).model_dump() for e in enquiries]
        return api_json_response_format(True, "Enquiries retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving enquiries: {e}", 500, {})

@router.get("/{enquire_id}")
async def get_enquiry(enquire_id: int, db: Session = Depends(get_db)):
    try:
        enquiry = db.query(EnquireForm).filter(EnquireForm.id == enquire_id).first()
        if not enquiry:
            return api_json_response_format(False, "Enquiry not found", 404, {})
        data = EnquireFormOut.model_validate(enquiry).model_dump()
        return api_json_response_format(True, "Enquiry retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving enquiry: {e}", 500, {})

@router.post("/")
async def create_enquiry(data: EnquireFormCreate, db: Session = Depends(get_db)):
    try:
        new_enquiry = EnquireForm(**data.dict())
        db.add(new_enquiry)
        db.commit()
        db.refresh(new_enquiry)
        response_data = EnquireFormOut.model_validate(new_enquiry).model_dump()

        # ✅ Send email notification
        send_enquiry_email(response_data)

        return api_json_response_format(True, "Enquiry created successfully.", 201, response_data)
    except Exception as e:
        return api_json_response_format(False, f"Error creating enquiry: {e}", 500, {})

enquire_router = router