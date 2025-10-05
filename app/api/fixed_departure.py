from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.fixed_departure import FixedDepartureCreate, FixedDepartureOut
from models.fixed_departure import FixedDeparture
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_fixed_departure(fd_in: FixedDepartureCreate, db: Session = Depends(get_db)):
    try:
        fd = FixedDeparture(**fd_in.model_dump())
        db.add(fd)
        db.commit()
        db.refresh(fd)
        return api_json_response_format(True, "Fixed departure created successfully.", 201, FixedDepartureOut.model_validate(fd).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating fixed departure: {e}", 500, {})

@router.get("/")
def get_all_fixed_departures(db: Session = Depends(get_db)):
    try:
        departures = db.query(FixedDeparture).all()
        data = [FixedDepartureOut.model_validate(d).model_dump() for d in departures]
        return api_json_response_format(True, "Fixed departures retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving fixed departures: {e}", 500, {})

@router.get("/trip/{trip_id}")
def get_departures_by_trip(trip_id: int, db: Session = Depends(get_db)):
    try:
        departures = db.query(FixedDeparture).filter(FixedDeparture.trip_id == trip_id).all()
        data = [FixedDepartureOut.model_validate(d).model_dump() for d in departures]
        return api_json_response_format(True, "Departures for trip retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving departures for trip: {e}", 500, {})

@router.get("/{fd_id}")
def get_departure_by_id(fd_id: int, db: Session = Depends(get_db)):
    try:
        fd = db.query(FixedDeparture).filter(FixedDeparture.id == fd_id).first()
        if not fd:
            return api_json_response_format(False, "Fixed departure not found", 404, {})
        return api_json_response_format(True, "Fixed departure retrieved successfully.", 200, FixedDepartureOut.model_validate(fd).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving fixed departure: {e}", 500, {})

@router.put("/{fd_id}")
def update_fixed_departure(fd_id: int, fd_in: FixedDepartureCreate, db: Session = Depends(get_db)):
    try:
        fd = db.query(FixedDeparture).filter(FixedDeparture.id == fd_id).first()
        if not fd:
            return api_json_response_format(False, "Fixed departure not found", 404, {})
        for key, value in fd_in.model_dump().items():
            setattr(fd, key, value)
        db.commit()
        db.refresh(fd)
        return api_json_response_format(True, "Fixed departure updated successfully.", 200, FixedDepartureOut.model_validate(fd).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating fixed departure: {e}", 500, {})

@router.delete("/{fd_id}")
def delete_fixed_departure(fd_id: int, db: Session = Depends(get_db)):
    try:
        fd = db.query(FixedDeparture).filter(FixedDeparture.id == fd_id).first()
        if not fd:
            return api_json_response_format(False, "Fixed departure not found", 404, {})
        db.delete(fd)
        db.commit()
        return api_json_response_format(True, "Fixed departure deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting fixed departure: {e}", 500, {})