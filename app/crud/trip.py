import base64
import os
import io
import json
import uuid
from datetime import datetime
from PIL import Image
from typing import List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.trip import Itinerary, Trip, TripMedia, TripPolicy, TripPricing
from schemas.trip import TripCreate

# -------------------- Slug Generator --------------------

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_unique_slug(db: Session, base_slug: str) -> str:
    existing = db.query(Trip).filter(Trip.slug == base_slug).first()
    if not existing:
        return base_slug
    return f"{base_slug}-{uuid.uuid4().hex[:6]}"


# -------------------- Image Handling --------------------

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

def create_trip(db: Session, payload: TripCreate, user_id: int):
    # Ensure unique slug
    if payload.slug:
        existing = db.query(Trip).filter(Trip.slug == payload.slug).first()
        if existing:
            payload.slug = generate_unique_slug(db, payload.slug)

    # Prepare Trip Base Data
    trip_fields = payload.dict(exclude={"pricing", "policies", "itinerary"})
    trip_fields["category_id"] = ",".join(payload.category_id or [])
    trip_fields["themes"] = ",".join(payload.themes or [])
    trip_fields["faqs"] = json.dumps(payload.faqs or [])
    trip_fields["gallery_images"] = json.dumps(payload.gallery_images or [])
    trip_fields["hero_image"] = payload.hero_image
    trip_fields["user_id"] = user_id

    # Create Trip Entry
    trip_model = Trip(**trip_fields)
    db.add(trip_model)
    db.commit()
    db.refresh(trip_model)

    # ---- Add Pricing ----
    if payload.pricing:
        pricing_data = jsonable_encoder(payload.pricing)
        # ✅ Validate costingPackages not empty before saving
        if (
            pricing_data.get("pricing_model") == "fixed_departure"
            and isinstance(pricing_data.get("fixed_departure"), list)
        ):
            for fd in pricing_data["fixed_departure"]:
                if not fd.get("costingPackages"):
                    raise HTTPException(status_code=400, detail="costingPackages cannot be empty")

        pricing_model = TripPricing(
            trip_id=trip_model.id,
            pricing_model=pricing_data.get("pricing_model"),
            data=json.dumps(pricing_data)
        )
        db.add(pricing_model)

    # ---- Add Policies ----
    if payload.policies:
        for policy in payload.policies:
            policy_data = policy.dict() if hasattr(policy, "dict") else policy
            policy_model = TripPolicy(trip_id=trip_model.id, **policy_data)
            db.add(policy_model)

    # ---- Add Itinerary ----
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

def get_trips(db: Session, user_id: int, skip: int = 0, limit: int = 10, category_ids: List[int] = None) -> list:
    query = db.query(Trip).filter(Trip.user_id == user_id)

    # Filter by multiple category IDs (OR logic)
    if category_ids and len(category_ids) > 0:
        filter_conditions = []
        for cat_id in category_ids:
            cat_str = str(cat_id)
            filter_conditions.append(
                or_(
                    Trip.category_id == cat_str,
                    Trip.category_id.like(f"{cat_str},%"),
                    Trip.category_id.like(f"%,{cat_str}"),
                    Trip.category_id.like(f"%,{cat_str},%")
                )
            )
        query = query.filter(or_(*filter_conditions))

    trips = query.order_by(Trip.created_at.desc()).offset(skip).limit(limit).all()
    return [serialize_trip(t) for t in trips]


def get_trip_by_id(db: Session, trip_id: int) -> dict:
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    return serialize_trip(trip) if trip else None


# -------------------- Update --------------------

def update_trip(db: Session, trip_id: int, payload: TripCreate):
    # Unique slug check
    if payload.slug:
        existing_slug = db.query(Trip).filter(Trip.slug == payload.slug, Trip.id != trip_id).first()
        if existing_slug:
            payload.slug = generate_unique_slug(db, payload.slug)

    trip_model = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip_model:
        raise HTTPException(status_code=404, detail="Trip not found.")

    # Update core fields
    trip_fields = payload.dict(exclude={"pricing", "policies", "itinerary"})
    trip_fields["category_id"] = ",".join(payload.category_id or [])
    trip_fields["themes"] = ",".join(payload.themes or [])
    trip_fields["faqs"] = json.dumps(payload.faqs or [])
    trip_fields["gallery_images"] = json.dumps(payload.gallery_images or [])
    trip_fields["hero_image"] = payload.hero_image

    for key, value in trip_fields.items():
        setattr(trip_model, key, value)

    # Update Pricing
    if payload.pricing:
        pricing_data = jsonable_encoder(payload.pricing)
        if (
            pricing_data.get("pricing_model") == "fixed_departure"
            and isinstance(pricing_data.get("fixed_departure"), list)
        ):
            for fd in pricing_data["fixed_departure"]:
                if not fd.get("costingPackages"):
                    raise HTTPException(status_code=400, detail="costingPackages cannot be empty")

        pricing_json = json.dumps(pricing_data)
        if trip_model.pricing:
            trip_model.pricing.pricing_model = pricing_data.get("pricing_model")
            trip_model.pricing.data = pricing_json
        else:
            db.add(TripPricing(trip_id=trip_model.id, pricing_model=pricing_data.get("pricing_model"), data=pricing_json))

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
    """
    Safely parse pricing JSON and guarantee valid structure.
    """
    try:
        parsed = json.loads(data)
        # Ensure fixed_departure list exists
        if not isinstance(parsed.get("fixed_departure"), list):
            parsed["fixed_departure"] = []
        else:
            # Ensure costingPackages exists for each
            for fd in parsed["fixed_departure"]:
                if "costingPackages" not in fd:
                    fd["costingPackages"] = []
        # Ensure customized block exists
        if not isinstance(parsed.get("customized"), dict):
            parsed["customized"] = {
                "pricing_type": "",
                "base_price": 0,
                "discount": 0,
                "final_price": 0
            }
        return parsed
    except Exception:
        return {
            "pricing_model": "fixed_departure",
            "fixed_departure": [],
            "customized": {
                "pricing_type": "",
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
        "category_id": trip.category_id.split(",") if trip.category_id else [],
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
        "pricing": normalize_fixed_departure(trip.pricing.data) if trip.pricing else None,
        "policies": [{"title": p.title, "content": p.content} for p in trip.policies] if trip.policies else [],
        "itinerary": [
            {
                "day_number": i.day_number,
                "title": i.title,
                "description": i.description,
                "image_urls": i.image_urls.split(",") if i.image_urls else [],
                "activities": i.activities.split(",") if i.activities else [],
                "hotel_name": i.hotel_name,
                "meal_plan": i.meal_plan.split(",") if i.meal_plan else []
            }
            for i in trip.itinerary
        ] if trip.itinerary else []
    }
