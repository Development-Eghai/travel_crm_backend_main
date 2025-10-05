from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.trip_day import TripDayCreate, TripDayOut
from models.trip_day import TripDay
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_trip_day(day_in: TripDayCreate, db: Session = Depends(get_db)):
    try:
        day = TripDay(**day_in.model_dump())
        db.add(day)
        db.commit()
        db.refresh(day)
        return api_json_response_format(True, "Trip day created successfully.", 201, TripDayOut.model_validate(day).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating trip day: {e}", 500, {})

@router.get("/")
def get_all_trip_days(db: Session = Depends(get_db)):
    try:
        days = db.query(TripDay).all()
        data = [TripDayOut.model_validate(d).model_dump() for d in days]
        return api_json_response_format(True, "Trip days retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip days: {e}", 500, {})

@router.get("/trip/{trip_id}")
def get_days_by_trip(trip_id: int, db: Session = Depends(get_db)):
    try:
        days = db.query(TripDay).filter(TripDay.trip_id == trip_id).all()
        data = [TripDayOut.model_validate(d).model_dump() for d in days]
        return api_json_response_format(True, "Trip days for trip retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip days for trip: {e}", 500, {})

@router.get("/{day_id}")
def get_day_by_id(day_id: int, db: Session = Depends(get_db)):
    try:
        day = db.query(TripDay).filter(TripDay.id == day_id).first()
        if not day:
            return api_json_response_format(False, "Trip day not found", 404, {})
        return api_json_response_format(True, "Trip day retrieved successfully.", 200, TripDayOut.model_validate(day).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip day: {e}", 500, {})

@router.put("/{day_id}")
def update_trip_day(day_id: int, day_in: TripDayCreate, db: Session = Depends(get_db)):
    try:
        day = db.query(TripDay).filter(TripDay.id == day_id).first()
        if not day:
            return api_json_response_format(False, "Trip day not found", 404, {})
        for key, value in day_in.model_dump().items():
            setattr(day, key, value)
        db.commit()
        db.refresh(day)
        return api_json_response_format(True, "Trip day updated successfully.", 200, TripDayOut.model_validate(day).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating trip day: {e}", 500, {})

@router.delete("/{day_id}")
def delete_trip_day(day_id: int, db: Session = Depends(get_db)):
    try:
        day = db.query(TripDay).filter(TripDay.id == day_id).first()
        if not day:
            return api_json_response_format(False, "Trip day not found", 404, {})
        db.delete(day)
        db.commit()
        return api_json_response_format(True, "Trip day deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting trip day: {e}", 500, {})