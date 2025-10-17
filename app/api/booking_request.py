from utils.email_utility import send_booking_email
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.booking_request import BookingRequest
from schemas.booking_request import BookingRequestCreate, BookingRequestOut
from core.database import get_db
from utils.response import api_json_response_format

router = APIRouter()

@router.post("/")
def create_booking(data: BookingRequestCreate, db: Session = Depends(get_db)):
    try:
        booking = BookingRequest(**data.dict())
        db.add(booking)
        db.commit()
        db.refresh(booking)
        response_data = BookingRequestOut.model_validate(booking).model_dump()

        # ✅ Send confirmation email
        send_booking_email(response_data)

        return api_json_response_format(True, "Booking request submitted successfully.", 201, response_data)
    except Exception as e:
        return api_json_response_format(False, f"Error submitting booking request: {e}", 500, {})


@router.get("/")
def get_all_bookings(db: Session = Depends(get_db)):
    try:
        bookings = db.query(BookingRequest).order_by(BookingRequest.created_at.desc()).all()
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