import json
from typing import List

from crud.trip import serialize_trip
from fastapi import APIRouter, Depends, HTTPException, Query,Header
from sqlalchemy.orm import Session
from schemas.destination import DestinationCreate, DestinationOut
from models.destination import (
    Destination, DestinationTrip, CustomPackage, CustomPackageTrip,
    DestinationBlog, DestinationActivity, DestinationTestimonial, DestinationBlogCategory
)
from core.database import get_db
from utils.response import api_json_response_format

from models.trip import Trip
from models.api_key import APIKey

router = APIRouter()

@router.post("/")
def create_destination(destination_in: DestinationCreate, db: Session = Depends(get_db),x_api_key: str = Header(None)):
    try:

        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")

        # 🔍 Get user_id from api_keys table
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        user_id = int(api_key_entry.user_id)
        
        slug = destination_in.slug or destination_in.title.lower().replace(" ", "-")

        destination = Destination(
            title=destination_in.title,
            subtitle=destination_in.subtitle,
            destination_type=destination_in.destination_type,
            primary_destination_id=destination_in.primary_destination_id,
            slug=slug,
            overview=destination_in.overview,
            travel_guidelines=destination_in.travel_guidelines,
            hero_banner_images=json.dumps(destination_in.hero_banner_images or []),
            user_id=user_id

        )

        db.add(destination)
        db.commit()
        db.refresh(destination)

        for trip_id in destination_in.popular_trip_ids:
            db.add(DestinationTrip(destination_id=destination.id, trip_id=trip_id))

        for package in destination_in.custom_packages:
            custom = CustomPackage(destination_id=destination.id, title=package.title, description=package.description)
            db.add(custom)
            db.commit()
            db.refresh(custom)
            for trip_id in package.trip_ids:
                db.add(CustomPackageTrip(package_id=custom.id, trip_id=trip_id))

        for blog_id in destination_in.featured_blog_ids:
            db.add(DestinationBlog(destination_id=destination.id, blog_id=blog_id, featured=True))
        for blog_id in destination_in.related_blog_ids:
            db.add(DestinationBlog(destination_id=destination.id, blog_id=blog_id, featured=False))
        for activity_id in destination_in.activity_ids:
            db.add(DestinationActivity(destination_id=destination.id, activity_id=activity_id))
        for testimonial_id in destination_in.testimonial_ids:
            db.add(DestinationTestimonial(destination_id=destination.id, testimonial_id=testimonial_id))
        for category_id in destination_in.blog_category_ids:
            db.add(DestinationBlogCategory(destination_id=destination.id, category_id=category_id))

        db.commit()

        # ✅ Manual serialization of nested relationships
        data = {
            "id": destination.id,
            "title": destination.title,
            "subtitle": destination.subtitle,
            "destination_type": destination.destination_type,
            "primary_destination_id": destination.primary_destination_id,
            "slug": destination.slug,
            "overview": destination.overview,
            "travel_guidelines": destination.travel_guidelines,
            "hero_banner_images": json.loads(destination.hero_banner_images or "[]"),

            # "hero_banner_images": destination.hero_banner_images,
            "created_at": destination.created_at,
            "updated_at": destination.updated_at,
            "popular_trip_ids": [t.trip_id for t in destination.trips],
            "custom_packages": [
                {
                    "title": p.title,
                    "description": p.description,
                    "trip_ids": [ct.trip_id for ct in db.query(CustomPackageTrip).filter(CustomPackageTrip.package_id == p.id).all()]
                }
                for p in db.query(CustomPackage).filter(CustomPackage.destination_id == destination.id).all()
            ],
            "featured_blog_ids": [b.blog_id for b in destination.blogs if b.featured],
            "related_blog_ids": [b.blog_id for b in destination.blogs if not b.featured],
            "activity_ids": [a.activity_id for a in destination.activities],
            "testimonial_ids": [t.testimonial_id for t in destination.testimonials],
            "blog_category_ids": [c.category_id for c in destination.blog_categories]
        }


        return api_json_response_format(True, "Destination created successfully.", 201, data)

    except Exception as e:
        return api_json_response_format(False, f"Error creating destination: {e}", 500, {})
    
@router.get("/get_trips")
def get_trips(trip_ids: List[int] = Query(...), db: Session = Depends(get_db)):
    if not trip_ids:
        raise HTTPException(status_code=400, detail="trip_ids list cannot be empty")

    trips = db.query(Trip).filter(Trip.id.in_(trip_ids)).all()

    if not trips:
        raise HTTPException(status_code=404, detail="No trips found for the given IDs")

    return trips


@router.get("/{destination_id}")
def get_destination_by_id(destination_id: int, db: Session = Depends(get_db)):
    try:
        destination = db.query(Destination).filter(Destination.id == destination_id).first()
        if not destination:
            return api_json_response_format(False, "Destination not found", 404, {})

        # ✅ Hydrate popular trips via relationship
        popular_trips = [
            serialize_trip(dt.trip)
            for dt in destination.trips
            if dt.trip is not None
        ]

        # ✅ Hydrate custom packages and their trips
        custom_packages = []
        for package in destination.custom_packages:
            trips = [
                serialize_trip(ct.trip)
                for ct in package.trips
                if ct.trip is not None
            ]
            custom_packages.append({
                "title": package.title,
                "description": package.description,
                "trips": trips
            })

        # ✅ Build response
        data = {
            "id": destination.id,
            "title": destination.title,
            "subtitle": destination.subtitle,
            "destination_type": destination.destination_type,
            "primary_destination_id": destination.primary_destination_id,
            "slug": destination.slug,
            "overview": destination.overview,
            "travel_guidelines": destination.travel_guidelines,
            "hero_banner_images": json.loads(destination.hero_banner_images or "[]"),

            "created_at": destination.created_at,
            "updated_at": destination.updated_at,
            "popular_trips": popular_trips,
            "custom_packages": custom_packages,
            "featured_blog_ids": [b.blog_id for b in destination.blogs if b.featured],
            "related_blog_ids": [b.blog_id for b in destination.blogs if not b.featured],
            "activity_ids": [a.activity_id for a in destination.activities],
            "testimonial_ids": [t.testimonial_id for t in destination.testimonials],
            "blog_category_ids": [c.category_id for c in destination.blog_categories]
        }

        return api_json_response_format(True, "Destination retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving destination: {e}", 500, {})

@router.get("/")
def get_all_destinations(db: Session = Depends(get_db), x_api_key: str = Header(None)):
    try:

        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")

        # 🔍 Get user_id from api_keys table
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        user_id = api_key_entry.user_id
        print("DDDDDDDDDDDDDDDDd ",user_id)

        # destinations = db.query(Destination).all()
        destinations = db.query(Destination).filter(Destination.user_id == user_id).all()


        data = []
        for destination in destinations:
            item = {
                "id": destination.id,
                "title": destination.title,
                "subtitle": destination.subtitle,
                "destination_type": destination.destination_type,
                "primary_destination_id": destination.primary_destination_id,
                "slug": destination.slug,
                "overview": destination.overview,
                "travel_guidelines": destination.travel_guidelines,
                "hero_banner_images": json.loads(destination.hero_banner_images or "[]"),

                "created_at": destination.created_at,
                "updated_at": destination.updated_at,
                "popular_trip_ids": [t.trip_id for t in destination.trips],
                "custom_packages": [
                    {
                        "title": p.title,
                        "description": p.description,
                        "trip_ids": [ct.trip_id for ct in db.query(CustomPackageTrip).filter(CustomPackageTrip.package_id == p.id).all()]
                    }
                    for p in db.query(CustomPackage).filter(CustomPackage.destination_id == destination.id).all()
                ],
                "featured_blog_ids": [b.blog_id for b in destination.blogs if b.featured],
                "related_blog_ids": [b.blog_id for b in destination.blogs if not b.featured],
                "activity_ids": [a.activity_id for a in destination.activities],
                "testimonial_ids": [t.testimonial_id for t in destination.testimonials],
                "blog_category_ids": [c.category_id for c in destination.blog_categories]
            }
            data.append(item)

        return api_json_response_format(True, "Destinations retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving destinations: {e}", 500, {})

@router.put("/{destination_id}")
def update_destination(destination_id: int, destination_in: DestinationCreate, db: Session = Depends(get_db)):
    try:
        destination = db.query(Destination).filter(Destination.id == destination_id).first()
        if not destination:
            return api_json_response_format(False, "Destination not found", 404, {})

        # Update base fields (excluding nested relationships)
        for key, value in destination_in.model_dump(exclude={
            "custom_packages", "popular_trip_ids", "featured_blog_ids",
            "related_blog_ids", "activity_ids", "testimonial_ids", "blog_category_ids"
        }).items():
            if key == "hero_banner_images":
                setattr(destination, key, json.dumps(value or []))
            else:
                setattr(destination, key, value)


        # Clear and re-add popular trips
        db.query(DestinationTrip).filter(DestinationTrip.destination_id == destination.id).delete()
        for trip_id in destination_in.popular_trip_ids:
            db.add(DestinationTrip(destination_id=destination.id, trip_id=trip_id))

        # Clear and re-add custom packages and their trips
        db.query(CustomPackageTrip).filter(CustomPackageTrip.package_id.in_(
            db.query(CustomPackage.id).filter(CustomPackage.destination_id == destination.id)
        )).delete()
        db.query(CustomPackage).filter(CustomPackage.destination_id == destination.id).delete()
        for package in destination_in.custom_packages:
            custom = CustomPackage(destination_id=destination.id, title=package.title, description=package.description)
            db.add(custom)
            db.commit()
            db.refresh(custom)
            for trip_id in package.trip_ids:
                db.add(CustomPackageTrip(package_id=custom.id, trip_id=trip_id))

        # Clear and re-add blogs
        db.query(DestinationBlog).filter(DestinationBlog.destination_id == destination.id).delete()
        for blog_id in destination_in.featured_blog_ids:
            db.add(DestinationBlog(destination_id=destination.id, blog_id=blog_id, featured=True))
        for blog_id in destination_in.related_blog_ids:
            db.add(DestinationBlog(destination_id=destination.id, blog_id=blog_id, featured=False))

        # Clear and re-add activities
        db.query(DestinationActivity).filter(DestinationActivity.destination_id == destination.id).delete()
        for activity_id in destination_in.activity_ids:
            db.add(DestinationActivity(destination_id=destination.id, activity_id=activity_id))

        # Clear and re-add testimonials
        db.query(DestinationTestimonial).filter(DestinationTestimonial.destination_id == destination.id).delete()
        for testimonial_id in destination_in.testimonial_ids:
            db.add(DestinationTestimonial(destination_id=destination.id, testimonial_id=testimonial_id))

        # Clear and re-add blog categories
        db.query(DestinationBlogCategory).filter(DestinationBlogCategory.destination_id == destination.id).delete()
        for category_id in destination_in.blog_category_ids:
            db.add(DestinationBlogCategory(destination_id=destination.id, category_id=category_id))

        db.commit()
        db.refresh(destination)

        # ✅ Manual serialization of updated destination
        data = {
            "id": destination.id,
            "title": destination.title,
            "subtitle": destination.subtitle,
            "destination_type": destination.destination_type,
            "primary_destination_id": destination.primary_destination_id,
            "slug": destination.slug,
            "overview": destination.overview,
            "travel_guidelines": destination.travel_guidelines,
            "created_at": destination.created_at,
            "updated_at": destination.updated_at,
            "popular_trip_ids": [t.trip_id for t in destination.trips],
            "hero_banner_images": json.loads(destination.hero_banner_images or "[]"),

            "custom_packages": [
                {
                    "title": p.title,
                    "description": p.description,
                    "trip_ids": [ct.trip_id for ct in db.query(CustomPackageTrip).filter(CustomPackageTrip.package_id == p.id).all()]
                }
                for p in db.query(CustomPackage).filter(CustomPackage.destination_id == destination.id).all()
            ],
            "featured_blog_ids": [b.blog_id for b in destination.blogs if b.featured],
            "related_blog_ids": [b.blog_id for b in destination.blogs if not b.featured],
            "activity_ids": [a.activity_id for a in destination.activities],
            "testimonial_ids": [t.testimonial_id for t in destination.testimonials],
            "blog_category_ids": [c.category_id for c in destination.blog_categories]
        }

        return api_json_response_format(True, "Destination updated successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error updating destination: {e}", 500, {})
    
@router.delete("/{destination_id}")
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    try:
        destination = db.query(Destination).filter(Destination.id == destination_id).first()
        if not destination:
            return api_json_response_format(False, "Destination not found", 404, {})

        # Manually delete child records
        db.query(CustomPackageTrip).filter(CustomPackageTrip.package_id.in_(
            db.query(CustomPackage.id).filter(CustomPackage.destination_id == destination.id)
        )).delete()

        db.query(CustomPackage).filter(CustomPackage.destination_id == destination.id).delete()
        db.query(DestinationTrip).filter(DestinationTrip.destination_id == destination.id).delete()
        db.query(DestinationBlog).filter(DestinationBlog.destination_id == destination.id).delete()
        db.query(DestinationActivity).filter(DestinationActivity.destination_id == destination.id).delete()
        db.query(DestinationTestimonial).filter(DestinationTestimonial.destination_id == destination.id).delete()
        db.query(DestinationBlogCategory).filter(DestinationBlogCategory.destination_id == destination.id).delete()

        db.delete(destination)
        db.commit()

        return api_json_response_format(True, "Destination deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting destination: {e}", 500, {})
