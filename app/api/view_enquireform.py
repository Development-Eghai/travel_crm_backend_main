from utils.email_utility import send_enquiry_email
from fastapi import APIRouter, Depends,Header,HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.model_enquireform import EnquireForm
from schemas.schema_enquireform import EnquireFormCreate, EnquireFormOut
from core.database import get_db
from utils.response import api_json_response_format
from models.user import User

from models.api_key import APIKey

router = APIRouter()

@router.get("/")
async def get_enquiries(db: Session = Depends(get_db),x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")
        
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")
        user_id = int(api_key_entry.user_id)
        enquiries = db.query(EnquireForm).filter(EnquireForm.user_id == user_id).order_by(EnquireForm.created_at.desc()).all()
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
        user = db.query(User).filter(User.website == data.domain_name).first()
        if not user:
            return api_json_response_format(False, "Invalid domain name — user not found.", 404, {})
        
        user_id = user.id 
        data = data.dict(exclude={"domain_name"})        
        new_enquiry = EnquireForm(user_id=user_id,**data)
        db.add(new_enquiry)
        db.commit()
        db.refresh(new_enquiry)
        response_data = EnquireFormOut.model_validate(new_enquiry).model_dump()        
        send_enquiry_email(response_data)

        return api_json_response_format(True, "Enquiry created successfully.", 201, response_data)
    except Exception as e:
        return api_json_response_format(False, f"Error creating enquiry: {e}", 500, {})

enquire_router = router