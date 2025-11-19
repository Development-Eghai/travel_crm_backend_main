# api/quotation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from schemas.quotation import QuotationCreate, QuotationOut
from models.quotation import *
from core.database import get_db
from utils.response import api_json_response_format
from datetime import date

router = APIRouter()


@router.post("/")
def create_quotation(quotation_in: QuotationCreate, db: Session = Depends(get_db)):
    try:
        quotation = Quotation(
            lead_id=quotation_in.lead_id,
            design=quotation_in.design,
            status=quotation_in.status,
            amount=quotation_in.amount,
            date=quotation_in.date or date.today()
        )
        db.add(quotation)
        db.flush()  # ensure id available if you want to set quotation_id in nested rows

        # Optionally, ensure a stable "quotation_id" field exists if you use it elsewhere.
        # If you added a 'quotation_id' to the quotations table (pattern used earlier),
        # you could set quotation.quotation_id = quotation.id here. Otherwise omit.

        # Agent
        db.add(QuotationAgent(quotation_id=quotation.id, **quotation_in.agent.model_dump()))

        # Company
        db.add(QuotationCompany(quotation_id=quotation.id, **quotation_in.company.model_dump()))

        # Trip
        db.add(QuotationTrip(
            quotation_id=quotation.id,
            display_title=quotation_in.trip.display_title,
            overview=quotation_in.trip.overview,
            hero_image=quotation_in.trip.hero_image,
            gallery_images=",".join(quotation_in.trip.gallery_images)
        ))

        # Trip Sections
        for section in quotation_in.trip.sections:
            db.add(QuotationTripSection(quotation_id=quotation.id, **section.model_dump()))

        # Itinerary
        for item in quotation_in.itinerary:
            db.add(QuotationItinerary(quotation_id=quotation.id, **item.model_dump()))

        # Costing
        db.add(QuotationCosting(quotation_id=quotation.id, **quotation_in.costing.model_dump()))

        # Policies
        db.add(QuotationPolicies(quotation_id=quotation.id, **quotation_in.policies.model_dump()))

        # Payment
        payment_data = quotation_in.payment.model_dump()
        payment_data["upi_ids"] = ",".join(payment_data.get("upi_ids", []))
        db.add(QuotationPayment(quotation_id=quotation.id, **payment_data))

        db.commit()
        db.refresh(quotation)

        return api_json_response_format(True, "Quotation created successfully.", 201, {"quotation_id": quotation.id})

    except Exception as e:
        db.rollback()
        return api_json_response_format(False, f"Error creating quotation: {e}", 500, {})


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
        return api_json_response_format(True, "Quotations for lead retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving quotations for lead: {e}", 500, {})


@router.get("/")
def get_all_quotations(db: Session = Depends(get_db)):
    try:
        quotations = db.query(Quotation).filter(Quotation.is_deleted == False).order_by(Quotation.date.desc()).all()
        data = []

        for q in quotations:
            item = {
                "id": q.id,
                "lead_id": q.lead_id,
                "design": q.design,
                "status": q.status,
                "amount": q.amount,
                "date": q.date,
                "agent": {
                    "name": q.agent.name,
                    "email": q.agent.email,
                    "contact": q.agent.contact
                } if q.agent and not getattr(q.agent, "is_deleted", False) else None,
                "company": {
                    "name": q.company.name,
                    "email": q.company.email,
                    "mobile": q.company.mobile,
                    "website": q.company.website,
                    "licence": q.company.licence,
                    "logo_url": q.company.logo_url
                } if q.company and not getattr(q.company, "is_deleted", False) else None,
                "trip": {
                    "display_title": q.trip.display_title,
                    "overview": q.trip.overview,
                    "hero_image": q.trip.hero_image,
                    "gallery_images": q.trip.gallery_images.split(",") if q.trip and q.trip.gallery_images else [],
                    "sections": [
                        {
                            "title": s.title,
                            "content": s.content
                        }
                        for s in db.query(QuotationTripSection).filter_by(quotation_id=q.id, is_deleted=False).all()
                    ]
                } if q.trip and not getattr(q.trip, "is_deleted", False) else None,
                "itinerary": [
                    {
                        "day": i.day,
                        "title": i.title,
                        "description": i.description
                    }
                    for i in q.itinerary if not getattr(i, "is_deleted", False)
                ],
                "costing": {
                    "type": q.costing.type,
                    "price_per_person": q.costing.price_per_person,
                    "price_per_package": q.costing.price_per_package,
                    "selected_slot": q.costing.selected_slot,
                    "selected_package": q.costing.selected_package
                } if q.costing and not getattr(q.costing, "is_deleted", False) else None,
                "policies": {
                    "payment_terms": q.policies.payment_terms,
                    "cancellation_policy": q.policies.cancellation_policy,
                    "terms_and_conditions": q.policies.terms_and_conditions,
                    "custom_policy": q.policies.custom_policy
                } if q.policies and not getattr(q.policies, "is_deleted", False) else None,
                "payment": {
                    "bank_name": q.payment.bank_name,
                    "account_number": q.payment.account_number,
                    "ifsc_code": q.payment.ifsc_code,
                    "branch_name": q.payment.branch_name,
                    "gst_number": q.payment.gst_number,
                    "address": q.payment.address,
                    "upi_ids": q.payment.upi_ids.split(",") if q.payment and q.payment.upi_ids else [],
                    "qr_code_url": q.payment.qr_code_url
                } if q.payment and not getattr(q.payment, "is_deleted", False) else None
            }
            data.append(item)

        return api_json_response_format(True, "All quotations retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving quotations: {e}", 500, {})


@router.get("/{quotation_id}")
def get_full_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        quotation = db.query(Quotation).filter(Quotation.id == quotation_id, Quotation.is_deleted == False).first()
        if not quotation:
            return api_json_response_format(False, "Quotation not found", 404, {})

        data = {
            "id": quotation.id,
            "lead_id": quotation.lead_id,
            "design": quotation.design,
            "status": quotation.status,
            "amount": quotation.amount,
            "date": quotation.date,
            "agent": {
                "name": quotation.agent.name,
                "email": quotation.agent.email,
                "contact": quotation.agent.contact
            } if quotation.agent and not getattr(quotation.agent, "is_deleted", False) else None,
            "company": {
                "name": quotation.company.name,
                "email": quotation.company.email,
                "mobile": quotation.company.mobile,
                "website": quotation.company.website,
                "licence": quotation.company.licence,
                "logo_url": quotation.company.logo_url
            } if quotation.company and not getattr(quotation.company, "is_deleted", False) else None,
            "trip": {
                "display_title": quotation.trip.display_title,
                "overview": quotation.trip.overview,
                "hero_image": quotation.trip.hero_image,
                "gallery_images": quotation.trip.gallery_images.split(",") if quotation.trip and quotation.trip.gallery_images else [],
                "sections": [
                    {
                        "title": section.title,
                        "content": section.content
                    }
                    for section in db.query(QuotationTripSection).filter_by(quotation_id=quotation.id, is_deleted=False).all()
                ]
            } if quotation.trip and not getattr(quotation.trip, "is_deleted", False) else None,
            "itinerary": [
                {
                    "day": item.day,
                    "title": item.title,
                    "description": item.description
                }
                for item in quotation.itinerary if not getattr(item, "is_deleted", False)
            ],
            "costing": {
                "type": quotation.costing.type,
                "price_per_person": quotation.costing.price_per_person,
                "price_per_package": quotation.costing.price_per_package,
                "selected_slot": quotation.costing.selected_slot,
                "selected_package": quotation.costing.selected_package
            } if quotation.costing and not getattr(quotation.costing, "is_deleted", False) else None,
            "policies": {
                "payment_terms": quotation.policies.payment_terms,
                "cancellation_policy": quotation.policies.cancellation_policy,
                "terms_and_conditions": quotation.policies.terms_and_conditions,
                "custom_policy": quotation.policies.custom_policy
            } if quotation.policies and not getattr(quotation.policies, "is_deleted", False) else None,
            "payment": {
                "bank_name": quotation.payment.bank_name,
                "account_number": quotation.payment.account_number,
                "ifsc_code": quotation.payment.ifsc_code,
                "branch_name": quotation.payment.branch_name,
                "gst_number": quotation.payment.gst_number,
                "address": quotation.payment.address,
                "upi_ids": quotation.payment.upi_ids.split(",") if quotation.payment and quotation.payment.upi_ids else [],
                "qr_code_url": quotation.payment.qr_code_url
            } if quotation.payment and not getattr(quotation.payment, "is_deleted", False) else None
        }

        return api_json_response_format(True, "Full quotation retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving full quotation: {e}", 500, {})


@router.delete("/{quotation_id}", summary="Soft delete quotation (move to trash)")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        q = db.query(Quotation).filter(Quotation.id == quotation_id).first()
        if not q:
            return api_json_response_format(False, "Quotation not found", 404, {})

        # Soft delete base row
        q.is_deleted = True

        # Soft delete nested items for consistency (child tables)
        db.query(QuotationAgent).filter(QuotationAgent.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationCompany).filter(QuotationCompany.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationTrip).filter(QuotationTrip.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationTripSection).filter(QuotationTripSection.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationItinerary).filter(QuotationItinerary.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationCosting).filter(QuotationCosting.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationPolicies).filter(QuotationPolicies.quotation_id == quotation_id).update({"is_deleted": True})
        db.query(QuotationPayment).filter(QuotationPayment.quotation_id == quotation_id).update({"is_deleted": True})

        db.commit()
        return api_json_response_format(True, "Quotation moved to trash.", 200, {})
    except Exception as e:
        db.rollback()
        return api_json_response_format(False, f"Error deleting quotation: {e}", 500, {})


@router.delete("/hard/{quotation_id}", summary="Hard delete quotation and all nested rows")
def hard_delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        # delete children first
        db.query(QuotationAgent).filter(QuotationAgent.quotation_id == quotation_id).delete()
        db.query(QuotationCompany).filter(QuotationCompany.quotation_id == quotation_id).delete()
        db.query(QuotationTrip).filter(QuotationTrip.quotation_id == quotation_id).delete()
        db.query(QuotationTripSection).filter(QuotationTripSection.quotation_id == quotation_id).delete()
        db.query(QuotationItinerary).filter(QuotationItinerary.quotation_id == quotation_id).delete()
        db.query(QuotationCosting).filter(QuotationCosting.quotation_id == quotation_id).delete()
        db.query(QuotationPolicies).filter(QuotationPolicies.quotation_id == quotation_id).delete()
        db.query(QuotationPayment).filter(QuotationPayment.quotation_id == quotation_id).delete()

        # then base
        db.query(Quotation).filter(Quotation.id == quotation_id).delete()

        db.commit()
        return api_json_response_format(True, "Quotation permanently deleted.", 200, {})
    except Exception as e:
        db.rollback()
        return api_json_response_format(False, f"Error permanently deleting quotation: {e}", 500, {})
