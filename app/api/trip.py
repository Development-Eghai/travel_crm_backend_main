from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.trip import TripCreate
from crud.trip import (
    create_trip,
    get_trips,
    get_trip_by_id,
    delete_trip,
    serialize_trip,
    update_trip
)

router = APIRouter()

# ✅ Unified response format
def api_json_response_format(status: bool, message: str, error_code: int, data: any) -> dict:
    return {
        "success": status,
        "message": message,
        "error_code": error_code,
        "data": data
    }

# ✅ List all trips with optional pagination
@router.get("/", response_model=dict)
def list_trips(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db)) -> dict:
    try:
        trips = get_trips(db, skip=skip, limit=limit)
        return api_json_response_format(True, "Trips fetched successfully", 0, trips)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

# ✅ Get single trip by ID
@router.get("/{trip_id}", response_model=dict)
def get_trip_by_id_endpoint(trip_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        trip = get_trip_by_id(db, trip_id)
        if not trip:
            return api_json_response_format(False, "Trip not found", 404, None)
        return api_json_response_format(True, "Trip fetched successfully", 0, trip)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

# ✅ Create new trip
@router.post("/", response_model=dict)
def create_trip_endpoint(trip: TripCreate, db: Session = Depends(get_db)) -> dict:
    try:
        new_trip = create_trip(db, trip)
        return api_json_response_format(True, "Trip created successfully", 0, serialize_trip(new_trip))
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

# ✅ Update existing trip
@router.put("/{trip_id}", response_model=dict)
def update_trip_endpoint(trip_id: int, trip: TripCreate, db: Session = Depends(get_db)) -> dict:
    try:
        updated = update_trip(db, trip_id, trip)
        if not updated:
            return api_json_response_format(False, "Trip not found", 404, None)
        return api_json_response_format(True, "Trip updated successfully", 0, serialize_trip(updated))
    except HTTPException as he:
        return api_json_response_format(False, he.detail, he.status_code, None)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

# ✅ Delete trip
@router.delete("/{trip_id}", response_model=dict)
def delete_trip_endpoint(trip_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        result = delete_trip(db, trip_id)
        return api_json_response_format(True, result["message"], 0, None)
    except HTTPException as he:
        return api_json_response_format(False, he.detail, he.status_code, None)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)