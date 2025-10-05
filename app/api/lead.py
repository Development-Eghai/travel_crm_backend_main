from datetime import datetime
import os
from fastapi import APIRouter, Depends, UploadFile,File,Form
from sqlalchemy.orm import Session
from models.quotation import Quotation
from schemas.lead_document import LeadDocumentOut
from models.lead_comments import LeadComment
from models.lead_documents import LeadDocument
from core.database import get_db
from models.lead import Lead
from schemas.lead import LeadCreate, LeadOut
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

UPLOAD_DIR = "uploads/leads"

@router.post("/{lead_id}/documents")
def upload_lead_document(
    lead_id: int,
    file: UploadFile = File(...),
    uploaded_by: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Save file to disk
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{lead_id}_{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(file.file.read())

        # Save metadata to DB
        doc = LeadDocument(
            lead_id=lead_id,
            file_name=file.filename,
            file_path=filepath,
            uploaded_by=uploaded_by
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return api_json_response_format(True, "Document uploaded successfully.", 201, LeadDocumentOut.from_attributes(doc).model_dump())

    except Exception as e:
        return api_json_response_format(False, f"Error uploading document: {e}", 500, {})


@router.post("/")
def create_lead(lead_in: LeadCreate, db: Session = Depends(get_db)):
    try:
        # Create base lead
        lead_data = lead_in.model_dump(exclude={"comments", "linked_documents"})
        lead = Lead(**lead_data)
        db.add(lead)
        db.commit()
        db.refresh(lead)

        # Comments
        for comment in lead_in.comments:
            db.add(LeadComment(
                lead_id=lead.id,
                user_name=comment.user_name,
                comment=comment.comment
            ))

        # Documents
        for doc in lead_in.linked_documents:
            db.add(LeadDocument(
                lead_id=lead.id,
                file_name=doc.file_name,
                file_path=doc.file_path,
                uploaded_by=doc.uploaded_by,
                uploaded_at=doc.uploaded_at
            ))

        db.commit()

        return api_json_response_format(True, "Lead created successfully.", 201, {"lead_id": lead.id})

    except Exception as e:
        return api_json_response_format(False, f"Error creating lead: {e}", 500, {})

@router.get("/")
def get_all_leads(db: Session = Depends(get_db)):
    try:
        leads = db.query(Lead).all()
        data = [LeadOut.model_validate(l).model_dump() for l in leads]
        return api_json_response_format(True, "Leads retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving leads: {e}", 500, {})

@router.get("/{lead_id}")
def get_lead_by_id(lead_id: int, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return api_json_response_format(False, "Lead not found", 404, {})
        return api_json_response_format(True, "Lead retrieved successfully.", 200, LeadOut.model_validate(lead).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving lead: {e}", 500, {})

@router.put("/{lead_id}")
def update_lead(lead_id: int, lead_in: LeadCreate, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return api_json_response_format(False, "Lead not found", 404, {})

        # Update base fields
        base_data = lead_in.model_dump(exclude={"comments", "linked_documents"})
        for key, value in base_data.items():
            setattr(lead, key, value)

        # Clear and re-add comments
        db.query(LeadComment).filter(LeadComment.lead_id == lead.id).delete()
        for comment in lead_in.comments or []:
            db.add(LeadComment(
                lead_id=lead.id,
                user_name=comment.user_name,
                comment=comment.comment
            ))

        # Clear and re-add documents
        db.query(LeadDocument).filter(LeadDocument.lead_id == lead.id).delete()
        for doc in lead_in.linked_documents or []:
            db.add(LeadDocument(
                lead_id=lead.id,
                file_name=doc.file_name,
                file_path=doc.file_path,
                uploaded_by=doc.uploaded_by,
                uploaded_at=doc.uploaded_at
            ))

        db.commit()
        db.refresh(lead)

        return api_json_response_format(True, "Lead updated successfully.", 200, LeadOut.model_validate(lead).model_dump())

    except Exception as e:
        return api_json_response_format(False, f"Error updating lead: {e}", 500, {})

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return api_json_response_format(False, "Lead not found", 404, {})
        db.delete(lead)
        db.commit()
        return api_json_response_format(True, "Lead deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting lead: {e}", 500, {})
    
@router.get("/{lead_id}/full-view")
def get_detailed_lead_view(lead_id: int, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return api_json_response_format(False, "Lead not found", 404, {})

        # Contact & Trip Details
        details = {
            "name": lead.name,
            "email": lead.email,
            # "phone": lead.phone,
            # "trip_title": lead.trip_title,
            # "trip_overview": lead.trip_overview,
            # "special_requirements": lead.special_requirements
        }

        # Activity: Comments History
        comments = db.query(LeadComment).filter_by(lead_id=lead.id).order_by(LeadComment.created_at.desc()).all()
        activity = [
            {
                "user_name": c.user_name,
                "comment": c.comment,
                "created_at": c.created_at
            }
            for c in comments
        ]

        # Quotations
        quotations = db.query(Quotation).filter_by(lead_id=lead.id).order_by(Quotation.date.desc()).all()
        quotation_data = []
        for q in quotations:
            quotation_data.append({
                "id": q.id,
                "design": q.design,
                "status": q.status,
                "amount": q.amount,
                "date": q.date,
                # "template": q.template,
                "trip": {
                    "title": q.trip if q.trip else None,
                    # "overview": q.trip.overview if q.trip else None,
                    # "hero_image": q.trip.hero_image if q.trip else None
                },
                "itinerary": [
                    {
                        "day": i.day,
                        "title": i.title,
                        "description": i.description
                    }
                    for i in q.itinerary
                ],
                # "hotel": [
                #     {
                #         "hotel_name": h.hotel_name,
                #         "city": h.city,
                #         "room_type": h.room_type,
                #         "category": h.category,
                #         "nights": h.nights,
                #         "cost_per_night": h.cost_per_night,
                #         "gallery": h.gallery.split(",") if h.gallery else []
                #     }
                #     for h in db.query(QuotationHotel).filter_by(quotation_id=q.id).all()
                # ],
                # "transport": [
                #     {
                #         "type": t.transport_type,
                #         "cost": t.cost,
                #         "from": t.from_location,
                #         "to": t.to_location,
                #         "details": t.details
                #     }
                #     for t in db.query(QuotationTransport).filter_by(quotation_id=q.id).all()
                # ],
                "cost_breakdown": {
                    # "accommodation": q.costing.accommodation if q.costing else None,
                    # "transport": q.costing.transport if q.costing else None,
                    # "activities": q.costing.activities if q.costing else None,
                    # "meals": q.costing.meals if q.costing else None,
                    # "taxes": q.costing.taxes if q.costing else None,
                    # "service_charge": q.costing.service_charge if q.costing else None,
                    # "discount": q.costing.discount if q.costing else None,
                    "subtotal": q.costing.price_per_person if q.costing else q.amount,
                    "quantity": q.costing.selected_slot if q.costing else 1,
                    "seleted_package": q.costing.selected_package if q.costing else None,
                    "total_price": q.costing.price_per_package if q.costing else q.amount
                },
                "policies": {
                    "terms": q.policies.terms_and_conditions if q.policies else None,
                    "payment": q.policies.payment_terms if q.policies else None,
                    "cancellation": q.policies.cancellation_policy if q.policies else None
                }
            })

        return api_json_response_format(True, "Detailed lead view retrieved successfully.", 200, {
            "details": details,
            "activity": activity,
            "quotations": quotation_data
        })

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving lead view: {e}", 500, {})
