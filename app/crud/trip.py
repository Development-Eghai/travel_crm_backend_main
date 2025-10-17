import base64
import os
from datetime import datetime
import io
import json
from PIL import Image
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models.trip import Itinerary, Trip, TripMedia, TripPolicy, TripPricing
from schemas.trip import TripCreate
from fastapi import HTTPException
import uuid

# -------------------- Slug Generator --------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def generate_unique_slug(db: Session, base_slug: str) -> str:
    existing = db.query(Trip).filter(Trip.slug == base_slug).first()
    if not existing:
        return base_slug
    return f"{base_slug}-{uuid.uuid4().hex[:6]}"

def generate_image(image_input):
    """
    Accepts either Base64 string or bytes.
    Saves the image as .webp and returns the file path.
    """
    if isinstance(image_input, str):
        if image_input.startswith("data:image"):
            image_input = image_input.split(",")[1]
        image_data = base64.b64decode(image_input)
    elif isinstance(image_input, (bytes, bytearray)):
        image_data = image_input
    else:
        raise ValueError("Invalid image input type. Must be base64 string or bytes.")

    image = Image.open(io.BytesIO(image_data))

    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    image.save(file_path, format="WEBP", quality=85)

    return file_path
# -------------------- Create --------------------


def create_trip(db: Session, payload: TripCreate):
    # Check for duplicate slug
    if payload.slug:
        existing = db.query(Trip).filter(Trip.slug == payload.slug).first()
        if existing:
            payload.slug = generate_unique_slug(db, payload.slug)

    

    # Prepare base trip data
    trip_fields = payload.dict(exclude={"pricing", "policies", "itinerary"})
    trip_fields["category_id"] = payload.category_id or None
    trip_fields["themes"] = ",".join(payload.themes or [])
    trip_fields["faqs"] = json.dumps(payload.faqs or [])
    trip_fields["gallery_images"] = json.dumps(payload.gallery_images or [])
    trip_fields["hero_image"] = payload.hero_image

    # Create Trip model instance
    trip_model = Trip(**trip_fields)
    db.add(trip_model)
    db.commit()
    db.refresh(trip_model)

    # Add Pricing
    if payload.pricing:
        pricing_data = jsonable_encoder(payload.pricing) if hasattr(payload.pricing, "dict") else payload.pricing
        pricing_model = TripPricing(
            trip_id=trip_model.id,
            pricing_model=pricing_data.get("pricing_model"),
            data=json.dumps(pricing_data)
        )
        db.add(pricing_model)

    # Add Policies
    if payload.policies:
        for policy in payload.policies:
            policy_data = policy.dict() if hasattr(policy, "dict") else policy
            policy_model = TripPolicy(trip_id=trip_model.id, **policy_data)
            db.add(policy_model)

    # Add Itinerary
    if payload.itinerary:
        for day in payload.itinerary:
            day_data = day.dict() if hasattr(day, "dict") else day
            day_data["image_urls"] = ",".join(day_data.get("image_urls", []))
            day_data["activities"] = ",".join(day_data.get("activities", []))
            day_data["meal_plan"] = ",".join(day_data.get("meal_plan", []))
            itinerary_model = Itinerary(trip_id=trip_model.id, **day_data)
            db.add(itinerary_model)

    db.commit()

    return trip_model


# -------------------- Read --------------------

def get_trips(db: Session, skip: int = 0, limit: int = 10) -> list:
    trips = (
        db.query(Trip)
        .order_by(Trip.created_at.desc())  # ✅ newest first
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [serialize_trip(t) for t in trips]


def get_trip_by_id(db: Session, trip_id: int) -> dict:
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    return serialize_trip(trip) if trip else None



# -------------------- Update --------------------

def update_trip(db: Session, trip_id: int, payload: TripCreate):
    # Check for slug conflict
    if payload.slug:
        existing_slug = db.query(Trip).filter(Trip.slug == payload.slug, Trip.id != trip_id).first()
        if existing_slug:
            payload.slug = generate_unique_slug(db, payload.slug)

    # Fetch existing trip
    trip_model = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip_model:
        raise HTTPException(status_code=404, detail="Trip not found.")

    # Update base fields
    trip_fields = payload.dict(exclude={"pricing", "policies", "itinerary"})
    trip_fields["category_id"] = payload.category_id or None
    trip_fields["themes"] = ",".join(payload.themes or [])
    trip_fields["faqs"] = json.dumps(payload.faqs or [])
    trip_fields["gallery_images"] = json.dumps(payload.gallery_images or [])
    trip_fields["hero_image"] = payload.hero_image

    for key, value in trip_fields.items():
        setattr(trip_model, key, value)

    # Update Pricing
    if payload.pricing:
        pricing_data = jsonable_encoder(payload.pricing)
        pricing_json = json.dumps(pricing_data)
        if trip_model.pricing:
            trip_model.pricing.pricing_model = pricing_data.get("pricing_model")
            trip_model.pricing.data = pricing_json
        else:
            db.add(TripPricing(
                trip_id=trip_model.id,
                pricing_model=pricing_data.get("pricing_model"),
                data=pricing_json
            ))

    # Replace Policies
    if payload.policies is not None:
        db.query(TripPolicy).filter(TripPolicy.trip_id == trip_model.id).delete()
        for policy in payload.policies:
            policy_data = policy.dict() if hasattr(policy, "dict") else policy
            db.add(TripPolicy(trip_id=trip_model.id, **policy_data))

    # Replace Itinerary
    if payload.itinerary is not None:
        db.query(Itinerary).filter(Itinerary.trip_id == trip_model.id).delete()
        for day in payload.itinerary:
            day_data = day.dict() if hasattr(day, "dict") else day
            day_data["image_urls"] = ",".join(day_data.get("image_urls", []))
            day_data["activities"] = ",".join(day_data.get("activities", []))
            day_data["meal_plan"] = ",".join(day_data.get("meal_plan", []))
            db.add(Itinerary(trip_id=trip_model.id, **day_data))

    db.commit()
    db.refresh(trip_model)
    return trip_model


# -------------------- Delete --------------------

def delete_trip(db: Session, trip_id: int) -> dict:
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"message": f"Trip '{trip.title}' deleted successfully"}

# -------------------- Serializer --------------------

def normalize_fixed_departure(data: str) -> dict:
    try:
        parsed = json.loads(data)

        # Flatten fixed_departure list to single object
        fixed_list = parsed.get("fixed_departure")
        if isinstance(fixed_list, list) and fixed_list:
            parsed["fixed_departure"] = fixed_list[0]
        elif isinstance(fixed_list, list):
            parsed["fixed_departure"] = {
                "title": "",
                "description": "",
                "from_date": None,
                "to_date": None,
                "available_slots": 0,
                "base_price": 0,
                "discount": 0,
                "final_price": 0,
                "booking_amount": 0,
                "gst_percentage": 0
            }

        # Flatten customized list to single object
        customized_list = parsed.get("customized")
        if isinstance(customized_list, list) and customized_list:
            parsed["customized"] = customized_list[0]
        elif isinstance(customized_list, list):
            parsed["customized"] = None

        return parsed
    except Exception:
        return {
            "pricing_model": "fixed_departure",
            "fixed_departure": {
                "title": "",
                "description": "",
                "from_date": None,
                "to_date": None,
                "available_slots": 0,
                "base_price": 0,
                "discount": 0,
                "final_price": 0,
                "booking_amount": 0,
                "gst_percentage": 0
            },
            "customized": None
        }

def serialize_trip(trip: Trip) -> dict:
    return {
        "id": trip.id,
        "title": trip.title,
        "overview": trip.overview,
        "destination_id": trip.destination_id,
        "destination_type": trip.destination_type,
        "category_id": trip.category_id,
        "themes": trip.themes.split(",") if trip.themes else [],
        "hotel_category": trip.hotel_category,
        "pickup_location": trip.pickup_location,
        "drop_location": trip.drop_location,
        "days": trip.days,
        "nights": trip.nights,
        "meta_tags": trip.meta_tags,
        "slug": trip.slug,
        "pricing_model": trip.pricing_model,
        "highlights": trip.highlights,
        "inclusions": trip.inclusions,
        "exclusions": trip.exclusions,
        "faqs": json.loads(trip.faqs) if trip.faqs else [],
        "terms": trip.terms,
        "privacy_policy": trip.privacy_policy,
        "payment_terms": trip.payment_terms,
        "created_at": trip.created_at,
        "updated_at": trip.updated_at,
        "hero_image": trip.hero_image,
        "gallery_images": json.loads(trip.gallery_images) if trip.gallery_images else [],

        # "media": {
        #     "hero_image_url": trip.media.hero_image_url if trip.media else None,
        #     "thumbnail_url": trip.media.thumbnail_url if trip.media else None,
        #     "gallery_urls": trip.media.gallery_urls.split(",") if trip.media and trip.media.gallery_urls else []
        # } if trip.media else None,

        "pricing": normalize_fixed_departure(trip.pricing.data) if trip.pricing else None,


        "policies": [
            {
                "title": p.title,
                "content": p.content
            } for p in trip.policies
        ] if trip.policies else [],

        "itinerary": [
            {
                "day_number": i.day_number,
                "title": i.title,
                "description": i.description,
                "image_urls": i.image_urls.split(",") if i.image_urls else [],
                "activities": i.activities.split(",") if i.activities else [],
                "hotel_name": i.hotel_name,
                "meal_plan": i.meal_plan.split(",") if i.meal_plan else []
            } for i in trip.itinerary
        ] if trip.itinerary else []
    }