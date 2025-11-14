from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session
from models.booking_request import BookingRequest
from schemas.booking_request import BookingRequestCreate, BookingRequestOut
from core.database import get_db
from utils.response import api_json_response_format
from models.user import User
from models.api_key import APIKey
from utils.email_utility import send_booking_email

router = APIRouter()


# ----------------------------------------------------------
# CREATE BOOKING  (TENANT EMAIL ENABLED)
# ----------------------------------------------------------
@router.post("/")
def create_booking(
    data: BookingRequestCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Domain validation
        user = db.query(User).filter(User.website == data.domain_name).first()
        if not user:
            return api_json_response_format(False, "Invalid domain name – user not found.", 404, {})

        booking_data = data.model_dump()
        booking = BookingRequest(user_id=user.id, **booking_data)

        db.add(booking)
        db.commit()
        db.refresh(booking)

        response_data = BookingRequestOut.model_validate(booking).model_dump()

        # TENANT EMAIL — uses x-api-key
        x_api_key = request.headers.get("x-api-key")
        try:
            send_booking_email(response_data, x_api_key)
        except Exception as e:
            print("Booking created but email failed:", e)

        return api_json_response_format(True, "Booking request submitted successfully.", 201, response_data)

    except Exception as e:
        return api_json_response_format(False, f"Error submitting booking request: {e}", 500, {})


# ----------------------------------------------------------
# GET ALL BOOKINGS (not deleted)
# ----------------------------------------------------------
@router.get("/")
def get_all_bookings(db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key missing")

        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        user_id = api_entry.user_id

        records = (
            db.query(BookingRequest)
            .filter(BookingRequest.user_id == user_id, BookingRequest.is_deleted == False)
            .order_by(BookingRequest.created_at.desc())
            .all()
        )

        data = [BookingRequestOut.model_validate(b).model_dump() for b in records]
        return api_json_response_format(True, "Bookings retrieved.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving bookings: {e}", 500, {})


# ----------------------------------------------------------
# GET ONE BOOKING
# ----------------------------------------------------------
@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(BookingRequest).filter(BookingRequest.id == booking_id).first()
        if not booking or booking.is_deleted:
            return api_json_response_format(False, "Booking not found", 404, {})

        data = BookingRequestOut.model_validate(booking).model_dump()
        return api_json_response_format(True, "Booking retrieved.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving booking: {e}", 500, {})


# ----------------------------------------------------------
# SOFT DELETE
# ----------------------------------------------------------
@router.delete("/{booking_id}/soft")
def soft_delete_booking(booking_id: int, db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        record = db.query(BookingRequest).filter(
            BookingRequest.id == booking_id,
            BookingRequest.user_id == api_entry.user_id
        ).first()

        if not record:
            return api_json_response_format(False, "Booking not found", 404, {})

        record.is_deleted = True
        db.commit()

        return api_json_response_format(True, "Booking moved to trash.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Error deleting booking: {e}", 500, {})


# ----------------------------------------------------------
# TRASH LIST
# ----------------------------------------------------------
@router.get("/trash/list")
def get_booking_trash(db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        records = (
            db.query(BookingRequest)
            .filter(BookingRequest.user_id == api_entry.user_id, BookingRequest.is_deleted == True)
            .order_by(BookingRequest.created_at.desc())
            .all()
        )

        data = [BookingRequestOut.model_validate(b).model_dump() for b in records]
        return api_json_response_format(True, "Trash retrieved.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trash: {e}", 500, {})


# ----------------------------------------------------------
# HARD DELETE
# ----------------------------------------------------------
@router.delete("/{booking_id}/hard")
def hard_delete_booking(booking_id: int, db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:
        api_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_entry:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        record = db.query(BookingRequest).filter(
            BookingRequest.id == booking_id,
            BookingRequest.user_id == api_entry.user_id
        ).first()

        if not record:
            return api_json_response_format(False, "Booking not found", 404, {})

        db.delete(record)
        db.commit()

        return api_json_response_format(True, "Booking permanently deleted.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Error deleting booking: {e}", 500, {})


booking_router = router
