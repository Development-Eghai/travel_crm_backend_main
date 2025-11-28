from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List

from schemas.quotation import QuotationCreate, QuotationOut, QuotationUpdate
from models.quotation import (
    Quotation, QuotationAgent, QuotationCompany, QuotationTrip, 
    QuotationTripSection, QuotationItinerary, QuotationCosting,
    QuotationPolicies, QuotationPayment
)
from core.database import get_db


def api_json_response_format(success, message, status_code, data):
    """Standard API response format"""
    response = {"success": success, "message": message}
    if data is not None:
        if isinstance(data, list):
            response["data"] = data
        elif isinstance(data, dict):
            response.update(data)
    return response


router = APIRouter()


def clean_gallery_images(images: List[str]) -> str:
    """Remove empty strings and return comma-separated string"""
    if not images:
        return ""
    cleaned = [url.strip() for url in images if url and url.strip()]
    return ",".join(cleaned)


# ------------------------------------------------------
# CREATE QUOTATION
# ------------------------------------------------------
@router.post("/")
def create_quotation(quotation_in: QuotationCreate, db: Session = Depends(get_db)):
    try:
        # Extract images from trip object (single source of truth)
        hero_image = quotation_in.trip.hero_image or ""
        gallery_images_str = clean_gallery_images(quotation_in.trip.gallery_images)
        
        # BASE QUOTATION FIELDS
        quotation = Quotation(
            lead_id=quotation_in.lead_id,
            design=quotation_in.design,
            status=quotation_in.status,
            amount=quotation_in.amount,
            date=quotation_in.date or date.today(),
            
            client_name=quotation_in.client_name or "",
            client_email=quotation_in.client_email or "",
            client_mobile=quotation_in.client_mobile or "",
            
            # Store images on main table for list performance
            hero_image=hero_image,
            gallery_images=gallery_images_str
        )
        db.add(quotation)
        db.flush()

        # AGENT
        db.add(QuotationAgent(quotation_id=quotation.id, **quotation_in.agent.model_dump()))

        # COMPANY
        db.add(QuotationCompany(quotation_id=quotation.id, **quotation_in.company.model_dump()))

        # TRIP 
        db.add(QuotationTrip(
            quotation_id=quotation.id,
            trip_id=quotation_in.trip.trip_id, 
            display_title=quotation_in.trip.display_title,
            overview=quotation_in.trip.overview,
            hero_image=hero_image,
            gallery_images=gallery_images_str
        ))

        for section in quotation_in.trip.sections:
            db.add(QuotationTripSection(quotation_id=quotation.id, **section.model_dump()))

        # ITINERARY
        for item in quotation_in.itinerary:
            db.add(QuotationItinerary(quotation_id=quotation.id, **item.model_dump()))

        # COSTING - SUPPORT BOTH PACKAGE AND ITEMS (WITH IMAGES)
        costing_data = {
            "quotation_id": quotation.id,
            "type": quotation_in.costing.type,
            "currency": quotation_in.costing.currency,
            "total_amount": quotation_in.costing.total_amount,
            "selected_package_id": quotation_in.costing.selected_package_id,
            "packages": [pkg.model_dump() for pkg in quotation_in.costing.packages] if quotation_in.costing.packages else [],
            "items": [item.model_dump() for item in quotation_in.costing.items] if quotation_in.costing.items else []
        }
        db.add(QuotationCosting(**costing_data))

        # POLICIES
        db.add(QuotationPolicies(quotation_id=quotation.id, **quotation_in.policies.model_dump()))

        # PAYMENT
        payment_data = quotation_in.payment.model_dump()
        payment_data["upi_ids"] = ",".join(payment_data.get("upi_ids", []))
        db.add(QuotationPayment(quotation_id=quotation.id, **payment_data))

        db.commit()
        db.refresh(quotation)

        return api_json_response_format(True, "Quotation created successfully.", 201, {"quotation_id": quotation.id})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating quotation: {str(e)}")


# ------------------------------------------------------
# GET QUOTATIONS BY LEAD
# ------------------------------------------------------
@router.get("/lead/{lead_id}")
def get_quotations_for_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        quotations = (
            db.query(Quotation)
            .filter(Quotation.lead_id == lead_id, Quotation.is_deleted == False)
            .order_by(Quotation.date.desc())
            .all()
        )
        data = [QuotationOut.model_validate(q).model_dump() for q in quotations]
        return api_json_response_format(True, "Quotations retrieved successfully.", 200, data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quotations: {str(e)}")


# ------------------------------------------------------
# GET ALL QUOTATIONS (SUMMARY LIST)
# ------------------------------------------------------
@router.get("/")
def get_all_quotations(db: Session = Depends(get_db)):
    try:
        quotations = db.query(Quotation).filter(
            Quotation.is_deleted == False
        ).order_by(Quotation.date.desc()).all()

        data = []

        for q in quotations:
            item = {
                "id": q.id,
                "lead_id": q.lead_id,
                "design": q.design,
                "status": q.status,
                "amount": q.amount,
                "date": q.date.isoformat() if q.date else None,
                "client_name": q.client_name,
                "client_email": q.client_email,
                "client_mobile": q.client_mobile,
                "hero_image": q.hero_image,
                "gallery_images": q.gallery_images.split(",") if q.gallery_images else [],
                
                "agent": {
                    "name": q.agent.name,
                    "email": q.agent.email,
                    "contact": q.agent.contact
                } if q.agent else None,
                "company": {
                    "name": q.company.name,
                    "email": q.company.email,
                    "mobile": q.company.mobile,
                    "website": q.company.website,
                    "licence": q.company.licence,
                    "logo_url": q.company.logo_url
                } if q.company else None,
            }
            data.append(item)

        return api_json_response_format(True, "All quotations retrieved.", 200, data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quotations: {str(e)}")


# ------------------------------------------------------
# GET FULL QUOTATION
# ------------------------------------------------------
@router.get("/{quotation_id}")
def get_full_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        quotation = db.query(Quotation).filter(
            Quotation.id == quotation_id, Quotation.is_deleted == False
        ).first()

        if not quotation:
            raise HTTPException(status_code=404, detail="Quotation not found")

        data = {
            "id": quotation.id,
            "lead_id": quotation.lead_id,
            "design": quotation.design,
            "status": quotation.status,
            "amount": quotation.amount,
            "date": quotation.date.isoformat() if quotation.date else None, 
            
            "client_name": quotation.client_name,
            "client_email": quotation.client_email,
            "client_mobile": quotation.client_mobile,
            
            # Images from main table
            "hero_image": quotation.hero_image,
            "gallery_images": quotation.gallery_images.split(",") if quotation.gallery_images else [],
            
            "agent": {
                "name": quotation.agent.name,
                "email": quotation.agent.email,
                "contact": quotation.agent.contact
            } if quotation.agent else None,
            
            "company": {
                "name": quotation.company.name,
                "email": quotation.company.email,
                "mobile": quotation.company.mobile,
                "website": quotation.company.website,
                "licence": quotation.company.licence,
                "logo_url": quotation.company.logo_url
            } if quotation.company else None,
            
            "trip": {
                "trip_id": quotation.trip.trip_id,
                "display_title": quotation.trip.display_title,
                "overview": quotation.trip.overview,
                "hero_image": quotation.trip.hero_image,
                "gallery_images": quotation.trip.gallery_images.split(",") if quotation.trip.gallery_images else [],
                "sections": [
                    {"title": s.title, "content": s.content}
                    for s in db.query(QuotationTripSection)
                    .filter_by(quotation_id=quotation_id, is_deleted=False)
                    .all()
                ]
            } if quotation.trip else None,
            
            "itinerary": [
                {"day": i.day, "title": i.title, "description": i.description}
                for i in quotation.itinerary if not i.is_deleted
            ],
            
            # COSTING - RETURN BOTH PACKAGES AND ITEMS (WITH IMAGES)
            "costing": {
                "type": quotation.costing.type,
                "currency": quotation.costing.currency,
                "total_amount": quotation.costing.total_amount,
                "selected_package_id": quotation.costing.selected_package_id,
                "packages": quotation.costing.packages or [],
                "items": quotation.costing.items or []
            } if quotation.costing else None,
            
            "policies": {
                "payment_terms": quotation.policies.payment_terms,
                "cancellation_policy": quotation.policies.cancellation_policy,
                "terms_and_conditions": quotation.policies.terms_and_conditions,
                "custom_policy": quotation.policies.custom_policy
            } if quotation.policies else None,
            
            "payment": {
                "bank_name": quotation.payment.bank_name,
                "account_number": quotation.payment.account_number,
                "ifsc_code": quotation.payment.ifsc_code,
                "branch_name": quotation.payment.branch_name,
                "gst_number": quotation.payment.gst_number,
                "address": quotation.payment.address,
                "upi_ids": quotation.payment.upi_ids.split(",") if quotation.payment.upi_ids else [],
                "qr_code_url": quotation.payment.qr_code_url
            } if quotation.payment else None
        }

        return api_json_response_format(True, "Full quotation retrieved.", 200, data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quotation: {str(e)}")


# ------------------------------------------------------
# UPDATE QUOTATION
# ------------------------------------------------------
@router.put("/{quotation_id}")
def update_quotation(quotation_id: int, quotation_in: QuotationUpdate, db: Session = Depends(get_db)):
    try:
        quotation = db.query(Quotation).filter(
            Quotation.id == quotation_id,
            Quotation.is_deleted == False
        ).first()

        if not quotation:
            raise HTTPException(status_code=404, detail="Quotation not found")

        # BASE FIELDS
        if quotation_in.design is not None:
            quotation.design = quotation_in.design
        if quotation_in.status is not None:
            quotation.status = quotation_in.status
        if quotation_in.amount is not None:
            quotation.amount = quotation_in.amount
        if quotation_in.date is not None:
            quotation.date = quotation_in.date
            
        if quotation_in.client_name is not None:
            quotation.client_name = quotation_in.client_name
        if quotation_in.client_email is not None:
            quotation.client_email = quotation_in.client_email
        if quotation_in.client_mobile is not None:
            quotation.client_mobile = quotation_in.client_mobile
        
        # Update images from trip object
        if quotation_in.trip:
            hero_image = quotation_in.trip.hero_image or ""
            gallery_images_str = clean_gallery_images(quotation_in.trip.gallery_images)
            
            quotation.hero_image = hero_image
            quotation.gallery_images = gallery_images_str

        # DELETE OLD RELATED DATA (for atomic update)
        db.query(QuotationAgent).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationCompany).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationTripSection).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationTrip).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationItinerary).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationCosting).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationPolicies).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationPayment).filter_by(quotation_id=quotation_id).delete()

        # RE-INSERT UPDATED DATA
        if quotation_in.agent:
            db.add(QuotationAgent(quotation_id=quotation_id, **quotation_in.agent.model_dump()))

        if quotation_in.company:
            db.add(QuotationCompany(quotation_id=quotation_id, **quotation_in.company.model_dump()))

        if quotation_in.trip:
            trip = quotation_in.trip
            hero_image = trip.hero_image or ""
            gallery_images_str = clean_gallery_images(trip.gallery_images)
            
            db.add(QuotationTrip(
                quotation_id=quotation_id,
                trip_id=trip.trip_id,
                display_title=trip.display_title,
                overview=trip.overview,
                hero_image=hero_image,
                gallery_images=gallery_images_str
            ))

            for section in trip.sections:
                db.add(QuotationTripSection(quotation_id=quotation_id, **section.model_dump()))

        if quotation_in.itinerary:
            for item in quotation_in.itinerary:
                db.add(QuotationItinerary(quotation_id=quotation_id, **item.model_dump()))

        # COSTING - SUPPORT BOTH PACKAGES AND ITEMS (WITH IMAGES)
        if quotation_in.costing:
            costing_data = {
                "quotation_id": quotation_id,
                "type": quotation_in.costing.type,
                "currency": quotation_in.costing.currency,
                "total_amount": quotation_in.costing.total_amount,
                "selected_package_id": quotation_in.costing.selected_package_id,
                "packages": [pkg.model_dump() for pkg in quotation_in.costing.packages] if quotation_in.costing.packages else [],
                "items": [item.model_dump() for item in quotation_in.costing.items] if quotation_in.costing.items else []
            }
            db.add(QuotationCosting(**costing_data))

        if quotation_in.policies:
            db.add(QuotationPolicies(quotation_id=quotation_id, **quotation_in.policies.model_dump()))

        if quotation_in.payment:
            pay = quotation_in.payment.model_dump()
            pay["upi_ids"] = ",".join(pay.get("upi_ids", []))
            db.add(QuotationPayment(quotation_id=quotation_id, **pay))

        db.commit()

        return api_json_response_format(True, "Quotation updated successfully.", 200, {})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating quotation: {str(e)}")


# ------------------------------------------------------
# SOFT DELETE (MOVE TO TRASH)
# ------------------------------------------------------
@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        q = db.query(Quotation).filter(Quotation.id == quotation_id).first()

        if not q:
            raise HTTPException(status_code=404, detail="Quotation not found")

        q.is_deleted = True

        db.query(QuotationAgent).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationCompany).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationTrip).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationTripSection).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationItinerary).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationCosting).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationPolicies).filter_by(quotation_id=quotation_id).update({"is_deleted": True})
        db.query(QuotationPayment).filter_by(quotation_id=quotation_id).update({"is_deleted": True})

        db.commit()
        return api_json_response_format(True, "Quotation moved to trash.", 200, {})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting quotation: {str(e)}")


# ------------------------------------------------------
# HARD DELETE (PERMANENT)
# ------------------------------------------------------
@router.delete("/hard/{quotation_id}")
def hard_delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        db.query(QuotationAgent).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationCompany).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationTrip).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationTripSection).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationItinerary).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationCosting).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationPolicies).filter_by(quotation_id=quotation_id).delete()
        db.query(QuotationPayment).filter_by(quotation_id=quotation_id).delete()

        db.query(Quotation).filter_by(id=quotation_id).delete()

        db.commit()
        return api_json_response_format(True, "Quotation permanently deleted.", 200, {})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error permanently deleting quotation: {str(e)}")