from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.destination import DestinationCreate, DestinationOut
from models.destination import (
    Destination, DestinationTrip, CustomPackage, CustomPackageTrip,
    DestinationBlog, DestinationActivity, DestinationTestimonial, DestinationBlogCategory
)
from core.database import get_db
from utils.response import api_json_response_format

router = APIRouter()

@router.post("/")
def create_destination(destination_in: DestinationCreate, db: Session = Depends(get_db)):
    try:
        slug = destination_in.slug or destination_in.title.lower().replace(" ", "-")

        destination = Destination(
            title=destination_in.title,
            subtitle=destination_in.subtitle,
            destination_type=destination_in.destination_type,
            primary_destination_id=destination_in.primary_destination_id,
            slug=slug,
            overview=destination_in.overview,
            travel_guidelines=destination_in.travel_guidelines
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
    

@router.get("/{destination_id}")
def get_destination_by_id(destination_id: int, db: Session = Depends(get_db)):
    try:
        destination = db.query(Destination).filter(Destination.id == destination_id).first()
        if not destination:
            return api_json_response_format(False, "Destination not found", 404, {})

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

        return api_json_response_format(True, "Destination retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving destination: {e}", 500, {})

@router.get("/")
def get_all_destinations(db: Session = Depends(get_db)):
    try:
        destinations = db.query(Destination).all()

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