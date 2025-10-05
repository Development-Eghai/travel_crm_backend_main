from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.trip_type import TripTypeCreate, TripTypeOut
from models.trip_type import TripType
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_trip_type(trip_type_in: TripTypeCreate, db: Session = Depends(get_db)):
    try:
        trip_type = TripType(**trip_type_in.model_dump())
        db.add(trip_type)
        db.commit()
        db.refresh(trip_type)
        return api_json_response_format(True, "Trip type created successfully.", 201, TripTypeOut.model_validate(trip_type).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating trip type: {e}", 500, {})

@router.get("/")
def get_all_trip_types(db: Session = Depends(get_db)):
    try:
        trip_types = db.query(TripType).all()
        data = [TripTypeOut.model_validate(t).model_dump() for t in trip_types]
        return api_json_response_format(True, "Trip types retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip types: {e}", 500, {})

@router.get("/{trip_type_id}")
def get_trip_type_by_id(trip_type_id: int, db: Session = Depends(get_db)):
    try:
        trip_type = db.query(TripType).filter(TripType.id == trip_type_id).first()
        if not trip_type:
            return api_json_response_format(False, "Trip type not found", 404, {})
        return api_json_response_format(True, "Trip type retrieved successfully.", 200, TripTypeOut.model_validate(trip_type).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving trip type: {e}", 500, {})

@router.put("/{trip_type_id}")
def update_trip_type(trip_type_id: int, trip_type_in: TripTypeCreate, db: Session = Depends(get_db)):
    try:
        trip_type = db.query(TripType).filter(TripType.id == trip_type_id).first()
        if not trip_type:
            return api_json_response_format(False, "Trip type not found", 404, {})
        for key, value in trip_type_in.model_dump().items():
            setattr(trip_type, key, value)
        db.commit()
        db.refresh(trip_type)
        return api_json_response_format(True, "Trip type updated successfully.", 200, TripTypeOut.model_validate(trip_type).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating trip type: {e}", 500, {})

@router.delete("/{trip_type_id}")
def delete_trip_type(trip_type_id: int, db: Session = Depends(get_db)):
    try:
        trip_type = db.query(TripType).filter(TripType.id == trip_type_id).first()
        if not trip_type:
            return api_json_response_format(False, "Trip type not found", 404, {})
        db.delete(trip_type)
        db.commit()
        return api_json_response_format(True, "Trip type deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting trip type: {e}", 500, {})