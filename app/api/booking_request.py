from utils.email_utility import send_booking_email
from fastapi import APIRouter, Depends,Header,HTTPException
from sqlalchemy.orm import Session
from models.booking_request import BookingRequest
from schemas.booking_request import BookingRequestCreate, BookingRequestOut
from core.database import get_db
from utils.response import api_json_response_format
from models.user import User

from models.api_key import APIKey

router = APIRouter()

@router.post("/")
def create_booking(data: BookingRequestCreate, db: Session = Depends(get_db)):
    try:
        print(data.domain_name)
        user = db.query(User).filter(User.website == data.domain_name).first()
        if not user:
            return api_json_response_format(False, "Invalid domain name — user not found.", 404, {})
        print(user.id)
        user_id = user.id 
        booking_data = data.dict(exclude={"domain_name"})
        booking = BookingRequest(user_id=user_id,**booking_data)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        response_data = BookingRequestOut.model_validate(booking).model_dump()        
        send_booking_email(response_data)

        return api_json_response_format(True, "Booking request submitted successfully.", 201, response_data)
    except Exception as e:
        return api_json_response_format(False, f"Error submitting booking request: {e}", 500, {})


@router.get("/")
def get_all_bookings(db: Session = Depends(get_db),x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")
        
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")
        user_id = int(api_key_entry.user_id) 

        bookings = db.query(BookingRequest).filter(BookingRequest.user_id == user_id).order_by(BookingRequest.created_at.desc()).all()
        data = [BookingRequestOut.model_validate(b).model_dump() for b in bookings]
        return api_json_response_format(True, "Bookings retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving bookings: {e}", 500, {})

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(BookingRequest).filter(BookingRequest.id == booking_id).first()
        if not booking:
            return api_json_response_format(False, "Booking not found", 404, {})
        data = BookingRequestOut.model_validate(booking).model_dump()
        return api_json_response_format(True, "Booking retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving booking: {e}", 500, {})
    
booking_router = router