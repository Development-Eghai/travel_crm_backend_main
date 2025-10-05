from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.bookings import BookingCreate, BookingOut
from models.bookings import Booking
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db)):
    try:
        booking = Booking(**booking_in.model_dump())
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return api_json_response_format(True, "Booking created successfully.", 201, BookingOut.model_validate(booking).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating booking: {e}", 500, {})

@router.get("/{booking_id}")
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return api_json_response_format(False, "Booking not found", 404, {})
        return api_json_response_format(True, "Booking retrieved successfully.", 200, BookingOut.model_validate(booking).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving booking: {e}", 500, {})

@router.get("/")
def get_all_bookings(db: Session = Depends(get_db)):
    try:
        bookings = db.query(Booking).all()
        data = [BookingOut.model_validate(b).model_dump() for b in bookings]
        return api_json_response_format(True, "Bookings retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving bookings: {e}", 500, {})

@router.put("/{booking_id}")
def update_booking(booking_id: int, booking_in: BookingCreate, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return api_json_response_format(False, "Booking not found", 404, {})
        for key, value in booking_in.model_dump().items():
            setattr(booking, key, value)
        db.commit()
        db.refresh(booking)
        return api_json_response_format(True, "Booking updated successfully.", 200, BookingOut.model_validate(booking).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating booking: {e}", 500, {})

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return api_json_response_format(False, "Booking not found", 404, {})
        db.delete(booking)
        db.commit()
        return api_json_response_format(True, "Booking deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting booking: {e}", 500, {})