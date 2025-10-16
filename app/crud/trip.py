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
    trip_fields = payload.dict(exclude={"media", "pricing", "policies", "itinerary"})
    trip_fields["category_id"] = payload.category_id or None
    trip_fields["themes"] = ",".join(payload.themes or [])

    # Create Trip model instance
    trip_model = Trip(**trip_fields)
    db.add(trip_model)
    db.commit()
    db.refresh(trip_model)

    # Add Media
    if payload.media:
        media_data = payload.media.dict() if hasattr(payload.media, "dict") else payload.media
        media_data["hero_image_url"] = generate_image(media_data["hero_image_url"])
        media_data["thumbnail_url"] = generate_image(media_data["thumbnail_url"])
        gallery_url = media_data["gallery_urls"]
        urls = []
        for url in gallery_url:
            urls.append(generate_image(url))
        media_data["gallery_urls"] = urls
        media_model = TripMedia(trip_id=trip_model.id, **media_data)
        db.add(media_model)

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
    trips = db.query(Trip).offset(skip).limit(limit).all()
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
            raise HTTPException(status_code=400, detail="Slug already exists. Please use a unique slug.")

    # Fetch existing trip
    trip_model = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip_model:
        raise HTTPException(status_code=404, detail="Trip not found.")

    # Update base fields
    trip_fields = payload.dict(exclude={"media", "pricing", "policies", "itinerary"})
    for key, value in trip_fields.items():
        setattr(trip_model, key, value)

    trip_model.category_id = payload.category_id or None
    trip_model.themes = ",".join(payload.themes or [])
    trip_model.slug = payload.slug

    # Update Media
    if payload.media:
        media_data = payload.media.dict() if hasattr(payload.media, "dict") else payload.media
        media_data["gallery_urls"] = ",".join(media_data.get("gallery_urls", []))
        if trip_model.media:
            for key, value in media_data.items():
                setattr(trip_model.media, key, value)
        else:
            media_model = TripMedia(trip_id=trip_model.id, **media_data)
            db.add(media_model)

    # Update Pricing
    if payload.pricing:
        pricing_data = jsonable_encoder(payload.pricing) if hasattr(payload.pricing, "dict") else payload.pricing
        pricing_json = json.dumps(pricing_data)
        if trip_model.pricing:
            trip_model.pricing.pricing_model = pricing_data.get("pricing_model")
            trip_model.pricing.data = pricing_json
        else:
            pricing_model = TripPricing(
                trip_id=trip_model.id,
                pricing_model=pricing_data.get("pricing_model"),
                data=pricing_json
            )
            db.add(pricing_model)

    # Replace Policies
    if payload.policies is not None:
        db.query(TripPolicy).filter(TripPolicy.trip_id == trip_model.id).delete()
        for policy in payload.policies:
            policy_data = policy.dict() if hasattr(policy, "dict") else policy
            policy_model = TripPolicy(trip_id=trip_model.id, **policy_data)
            db.add(policy_model)

    # Replace Itinerary
    if payload.itinerary is not None:
        db.query(Itinerary).filter(Itinerary.trip_id == trip_model.id).delete()
        for day in payload.itinerary:
            day_data = day.dict() if hasattr(day, "dict") else day
            day_data["image_urls"] = ",".join(day_data.get("image_urls", []))
            day_data["activities"] = ",".join(day_data.get("activities", []))
            day_data["meal_plan"] = ",".join(day_data.get("meal_plan", []))
            itinerary_model = Itinerary(trip_id=trip_model.id, **day_data)
            db.add(itinerary_model)

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
        customized_list = parsed.get("customized")

        if isinstance(customized_list, list) and customized_list:
            parsed["customized"] = customized_list[0]  # Take first item
        elif isinstance(customized_list, list):
            parsed["customized"] = {
                "pricing_type": "string",
                "base_price": 0,
                "discount": 0,
                "final_price": 0
            }

        return parsed
    except Exception:
        return {
            "customized": {
                "pricing_type": "string",
                "base_price": 0,
                "discount": 0,
                "final_price": 0
            }
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
        "faqs": trip.faqs,
        "terms": trip.terms,
        "privacy_policy": trip.privacy_policy,
        "payment_terms": trip.payment_terms,
        "created_at": trip.created_at,
        "updated_at": trip.updated_at,

        "media": {
            "hero_image_url": trip.media.hero_image_url if trip.media else None,
            "thumbnail_url": trip.media.thumbnail_url if trip.media else None,
            "gallery_urls": trip.media.gallery_urls.split(",") if trip.media and trip.media.gallery_urls else []
        } if trip.media else None,

        "pricing": {
            "pricing_model": trip.pricing.pricing_model,
            "fixed_departure": normalize_fixed_departure(trip.pricing.data)
        } if trip.pricing else None,


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