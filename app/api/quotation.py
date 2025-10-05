from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
        db.commit()
        db.refresh(quotation)

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

        return api_json_response_format(True, "Quotation created successfully.", 201, {"quotation_id": quotation.id})

    except Exception as e:
        return api_json_response_format(False, f"Error creating quotation: {e}", 500, {})


@router.get("/lead/{lead_id}")
def get_quotations_for_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        quotations = db.query(Quotation).filter(Quotation.lead_id == lead_id).order_by(Quotation.date.desc()).all()
        data = [QuotationOut.model_validate(q).model_dump() for q in quotations]
        return api_json_response_format(True, "Quotations for lead retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving quotations for lead: {e}", 500, {})


@router.get("/")
def get_all_quotations(db: Session = Depends(get_db)):
    try:
        quotations = db.query(Quotation).order_by(Quotation.date.desc()).all()
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
                } if q.agent else None,
                "company": {
                    "name": q.company.name,
                    "email": q.company.email,
                    "mobile": q.company.mobile,
                    "website": q.company.website,
                    "licence": q.company.licence,
                    "logo_url": q.company.logo_url
                } if q.company else None,
                "trip": {
                    "display_title": q.trip.display_title,
                    "overview": q.trip.overview,
                    "hero_image": q.trip.hero_image,
                    "gallery_images": q.trip.gallery_images.split(",") if q.trip.gallery_images else [],
                    "sections": [
                        {
                            "title": s.title,
                            "content": s.content
                        }
                        for s in db.query(QuotationTripSection).filter_by(quotation_id=q.id).all()
                    ]
                } if q.trip else None,
                "itinerary": [
                    {
                        "day": i.day,
                        "title": i.title,
                        "description": i.description
                    }
                    for i in q.itinerary
                ],
                "costing": {
                    "type": q.costing.type,
                    "price_per_person": q.costing.price_per_person,
                    "price_per_package": q.costing.price_per_package,
                    "selected_slot": q.costing.selected_slot,
                    "selected_package": q.costing.selected_package
                } if q.costing else None,
                "policies": {
                    "payment_terms": q.policies.payment_terms,
                    "cancellation_policy": q.policies.cancellation_policy,
                    "terms_and_conditions": q.policies.terms_and_conditions,
                    "custom_policy": q.policies.custom_policy
                } if q.policies else None,
                "payment": {
                    "bank_name": q.payment.bank_name,
                    "account_number": q.payment.account_number,
                    "ifsc_code": q.payment.ifsc_code,
                    "branch_name": q.payment.branch_name,
                    "gst_number": q.payment.gst_number,
                    "address": q.payment.address,
                    "upi_ids": q.payment.upi_ids.split(",") if q.payment.upi_ids else [],
                    "qr_code_url": q.payment.qr_code_url
                } if q.payment else None
            }
            data.append(item)

        return api_json_response_format(True, "All quotations retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving quotations: {e}", 500, {})

@router.get("/{quotation_id}")
def get_full_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
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
                "display_title": quotation.trip.display_title,
                "overview": quotation.trip.overview,
                "hero_image": quotation.trip.hero_image,
                "gallery_images": quotation.trip.gallery_images.split(",") if quotation.trip.gallery_images else [],
                "sections": [
                    {
                        "title": section.title,
                        "content": section.content
                    }
                    for section in db.query(QuotationTripSection).filter_by(quotation_id=quotation.id).all()
                ]
            } if quotation.trip else None,
            "itinerary": [
                {
                    "day": item.day,
                    "title": item.title,
                    "description": item.description
                }
                for item in quotation.itinerary
            ],
            "costing": {
                "type": quotation.costing.type,
                "price_per_person": quotation.costing.price_per_person,
                "price_per_package": quotation.costing.price_per_package,
                "selected_slot": quotation.costing.selected_slot,
                "selected_package": quotation.costing.selected_package
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

        return api_json_response_format(True, "Full quotation retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving full quotation: {e}", 500, {})


@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
        if not quotation:
            return api_json_response_format(False, "Quotation not found", 404, {})

        # Manually delete nested records if cascade is not set
        db.query(QuotationAgent).filter(QuotationAgent.quotation_id == quotation.id).delete()
        db.query(QuotationCompany).filter(QuotationCompany.quotation_id == quotation.id).delete()
        db.query(QuotationTrip).filter(QuotationTrip.quotation_id == quotation.id).delete()
        db.query(QuotationTripSection).filter(QuotationTripSection.quotation_id == quotation.id).delete()
        db.query(QuotationItinerary).filter(QuotationItinerary.quotation_id == quotation.id).delete()
        db.query(QuotationCosting).filter(QuotationCosting.quotation_id == quotation.id).delete()
        db.query(QuotationPolicies).filter(QuotationPolicies.quotation_id == quotation.id).delete()
        db.query(QuotationPayment).filter(QuotationPayment.quotation_id == quotation.id).delete()

        db.delete(quotation)
        db.commit()

        return api_json_response_format(True, "Quotation deleted successfully.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Error deleting quotation: {e}", 500, {})