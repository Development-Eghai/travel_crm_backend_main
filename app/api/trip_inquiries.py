from utils.email_utility import send_trip_inquiry_email
from fastapi import APIRouter, Depends,Header,HTTPException
from sqlalchemy.orm import Session
from models.trip_inquiries import TripInquiry
from models.user import User
from schemas.trip_inquiries import TripInquiryCreate, TripInquiryOut
from core.database import get_db
from utils.response import api_json_response_format

from models.api_key import APIKey

router = APIRouter()

@router.post("/")
def create_trip_inquiry(data: TripInquiryCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.website == data.domain_name).first()
        if not user:
            return api_json_response_format(False, "Invalid domain name — user not found.", 404, {})        

        user_id = user.id
        inquiry = TripInquiry(
            user_id=user_id, 
            departure_date=data.departure_date,
            adults=data.adults,
            children=data.children,
            children_ages=",".join(map(str, data.children_ages)) if data.children_ages else None,
            full_name=data.full_name,
            email=data.email,
            phone_number=data.phone_number
        )
        db.add(inquiry)
        db.commit()
        db.refresh(inquiry)
        response_data = TripInquiryOut.model_validate(inquiry).model_dump()
        send_trip_inquiry_email(response_data)
        return api_json_response_format(True, "Trip inquiry submitted successfully.", 201, response_data)
    except Exception as e:
        return api_json_response_format(False, f"Error submitting trip inquiry: {e}", 500, {})

@router.get("/")
def get_all_trip_inquiries(db: Session = Depends(get_db),x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")
        
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        user_id = int(api_key_entry.user_id) 
        
        inquiries = db.query(TripInquiry).filter(TripInquiry.user_id == user_id).order_by(TripInquiry.created_at.desc()).all()
        data = [TripInquiryOut.model_validate(i).model_dump() for i in inquiries]
        return api_json_response_format(True, "Trip inquiries retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip inquiries: {e}", 500, {})

@router.get("/{inquiry_id}")
def get_trip_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    try:
        inquiry = db.query(TripInquiry).filter(TripInquiry.id == inquiry_id).first()
        if not inquiry:
            return api_json_response_format(False, "Trip inquiry not found", 404, {})
        data = TripInquiryOut.model_validate(inquiry).model_dump()
        return api_json_response_format(True, "Trip inquiry retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip inquiry: {e}", 500, {})
    
@router.delete("/{inquiry_id}")
def delete_trip_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    try:
        inquiry = db.query(TripInquiry).filter(TripInquiry.id == inquiry_id).first()
        if not inquiry:
            return api_json_response_format(False, "Trip inquiry not found", 404, {})
        
        db.delete(inquiry)
        db.commit()
        return api_json_response_format(True, "Trip inquiry deleted successfully.", 200, {})
    except Exception as e:
        db.rollback()
        return api_json_response_format(False, f"Error deleting trip inquiry: {e}", 500, {})
    
trip_inquiry_router = router