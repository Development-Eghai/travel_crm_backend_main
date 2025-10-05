from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.trip import Trip
from models.activity import Activity
from models.trip_type import TripType
from models.destination import Destination
from models.category import Category
from schemas.trip import TripOut
from schemas.trip_management import (
    ActivityOut, TripTypeOut, DestinationOut, CategoryOut
)
from utils.response import api_json_response_format

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def get_trip_management_dashboard(db: Session = Depends(get_db)):
    try:
        trips = db.query(Trip).all()
        trip_types = db.query(TripType).all()
        destinations = db.query(Destination).all()
        categories = db.query(Category).all()
        activities = db.query(Activity).all()

        data = {
            "trips": [TripOut.model_validate(t).model_dump() for t in trips],
            "trip_types": [TripTypeOut.model_validate(tt).model_dump() for tt in trip_types],
            "destinations": [DestinationOut.model_validate(d).model_dump() for d in destinations],
            "categories": [CategoryOut.model_validate(c).model_dump() for c in categories],
            "activities": [ActivityOut.model_validate(a).model_dump() for a in activities],
        }

        return api_json_response_format(True, "Trip Management dashboard loaded.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error loading dashboard: {e}", 500, {})