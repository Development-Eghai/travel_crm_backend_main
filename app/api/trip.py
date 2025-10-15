from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
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
import json

router = APIRouter()

def api_json_response_format(status: bool, message: str, error_code: int, data: any) -> dict:
    return {
        "success": status,
        "message": message,
        "error_code": error_code,
        "data": data
    }

@router.get("/", response_model=dict)
def list_trips(skip: int = Query(0), limit: int = Query(10), db: Session = Depends(get_db)):
    try:
        trips = get_trips(db, skip=skip, limit=limit)
        return api_json_response_format(True, "Trips fetched successfully", 0, trips)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

@router.get("/{trip_id}", response_model=dict)
def get_trip_by_id_endpoint(trip_id: int, db: Session = Depends(get_db)):
    try:
        trip = get_trip_by_id(db, trip_id)
        if not trip:
            return api_json_response_format(False, "Trip not found", 404, None)
        return api_json_response_format(True, "Trip fetched successfully", 0, trip)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

@router.post("/", response_model=dict)
def create_trip_endpoint(
    title: str = Form(...),
    overview: str = Form(...),
    destination_id: int = Form(...),
    destination_type: str = Form(...),
    category_id: int = Form(...),
    themes: str = Form(...),
    hotel_category: int = Form(...),
    pickup_location: str = Form(...),
    drop_location: str = Form(...),
    days: int = Form(...),
    nights: int = Form(...),
    meta_tags: str = Form(...),
    slug: str = Form(...),
    pricing_model: str = Form(...),
    highlights: str = Form(...),
    inclusions: str = Form(...),
    exclusions: str = Form(...),
    faqs: str = Form(...),
    terms: str = Form(...),
    privacy_policy: str = Form(...),
    payment_terms: str = Form(...),
    itinerary: str = Form(...),
    pricing: str = Form(...),
    policies: str = Form(...),
    hero_image: UploadFile = File(None),
    thumbnail_image: UploadFile = File(None),
    gallery_images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        payload = TripCreate(
            title=title,
            overview=overview,
            destination_id=destination_id,
            destination_type=destination_type,
            category_id=category_id,
            themes=themes.split(","),
            hotel_category=hotel_category,
            pickup_location=pickup_location,
            drop_location=drop_location,
            days=days,
            nights=nights,
            meta_tags=meta_tags,
            slug=slug,
            pricing_model=pricing_model,
            highlights=highlights,
            inclusions=inclusions,
            exclusions=exclusions,
            faqs=json.loads(faqs),
            terms=terms,
            privacy_policy=privacy_policy,
            payment_terms=payment_terms,
            itinerary=json.loads(itinerary),
            pricing=json.loads(pricing),
            policies=json.loads(policies)
        )
        new_trip = create_trip(db, payload, hero_image, thumbnail_image, gallery_images)
        return api_json_response_format(True, "Trip created successfully", 0, serialize_trip(new_trip))
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

@router.put("/{trip_id}", response_model=dict)
def update_trip_endpoint(trip_id: int, trip: TripCreate, db: Session = Depends(get_db)):
    try:
        updated = update_trip(db, trip_id, trip)
        if not updated:
            return api_json_response_format(False, "Trip not found", 404, None)
        return api_json_response_format(True, "Trip updated successfully", 0, serialize_trip(updated))
    except HTTPException as he:
        return api_json_response_format(False, he.detail, he.status_code, None)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)

@router.delete("/{trip_id}", response_model=dict)
def delete_trip_endpoint(trip_id: int, db: Session = Depends(get_db)):
    try:
        result = delete_trip(db, trip_id)
        return api_json_response_format(True, result["message"], 0, None)
    except HTTPException as he:
        return api_json_response_format(False, he.detail, he.status_code, None)
    except Exception as e:
        return api_json_response_format(False, str(e), 500, None)