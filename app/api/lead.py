from datetime import datetime
import os
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from models.quotation import Quotation
from schemas.lead_document import LeadDocumentOut
from models.lead_comments import LeadComment
from models.lead_documents import LeadDocument
from core.database import get_db
from models.lead import Lead
from schemas.lead import LeadCreate, LeadOut
from utils.response import api_json_response_format

from core.auth import get_current_user_id

router = APIRouter()
UPLOAD_DIR = "uploads/leads"


# -------------------------
# Upload Document
# -------------------------
@router.post("/{lead_id}/documents")
def upload_lead_document(
    lead_id: int,
    file: UploadFile = File(...),
    uploaded_by: int = Form(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id) 
):
    try:
        lead = db.query(Lead).filter(
            Lead.id == lead_id,
            Lead.user_id == user_id
        ).first()

        if not lead:
            return api_json_response_format(False, "Unauthorized or lead not found", 403, {})

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{lead_id}_{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(file.file.read())

        doc = LeadDocument(
            lead_id=lead_id,
            file_name=file.filename,
            file_path=filepath,
            uploaded_by=uploaded_by
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return api_json_response_format(
            True, 
            "Document uploaded successfully.", 
            201, 
            LeadDocumentOut.from_attributes(doc).model_dump()
        )

    except Exception as e:
        return api_json_response_format(False, f"Error uploading document: {e}", 500, {})


# -------------------------
# Create Lead
# -------------------------
@router.post("/")
def create_lead(
    lead_in: LeadCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        lead_data = lead_in.model_dump(exclude_unset=True)
        lead = Lead(user_id=user_id, **lead_data)

        db.add(lead)
        db.flush()  # ensures lead.id is created

        # SAFE MIGRATION FIELD
        lead.lead_id = lead.id

        db.commit()
        db.refresh(lead)

        return api_json_response_format(
            True, 
            "Lead created successfully.", 
            201, 
            {"lead_id": lead.lead_id}
        )

    except Exception as e:
        return api_json_response_format(False, f"Error creating lead: {e}", 500, {})


# -------------------------
# List All Leads
# -------------------------
@router.get("/")
def get_all_leads(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        leads = db.query(Lead).filter(
            Lead.user_id == user_id,
            Lead.is_deleted == False
        ).all()

        data = [LeadOut.model_validate(l).model_dump() for l in leads]

        return api_json_response_format(True, "Leads retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving leads: {e}", 500, {})


# -------------------------
# Get Lead By ID
# -------------------------
@router.get("/{lead_id}")
def get_lead_by_id(
    lead_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        lead = db.query(Lead).filter(
            Lead.id == lead_id,
            Lead.user_id == user_id
        ).first()

        if not lead:
            return api_json_response_format(False, "Lead not found or unauthorized", 404, {})

        return api_json_response_format(
            True, 
            "Lead retrieved successfully.", 
            200, 
            LeadOut.model_validate(lead).model_dump()
        )

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving lead: {e}", 500, {})


# -------------------------
# Update Lead
# -------------------------
@router.put("/{lead_id}")
def update_lead(
    lead_id: int,
    lead_in: LeadCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        lead = db.query(Lead).filter(
            Lead.id == lead_id,
            Lead.user_id == user_id
        ).first()

        if not lead:
            return api_json_response_format(False, "Lead not found or unauthorized", 404, {})

        for key, value in lead_in.model_dump().items():
            setattr(lead, key, value)

        db.commit()
        db.refresh(lead)

        return api_json_response_format(True, "Lead updated successfully.", 200, LeadOut.model_validate(lead).model_dump())

    except Exception as e:
        return api_json_response_format(False, f"Error updating lead: {e}", 500, {})


# -------------------------
# Delete Lead (Hard Delete)
# -------------------------
@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        lead = db.query(Lead).filter(
            Lead.id == lead_id,
            Lead.user_id == user_id
        ).first()

        if not lead:
            return api_json_response_format(False, "Lead not found or unauthorized", 404, {})

        db.delete(lead)
        db.commit()

        return api_json_response_format(True, "Lead deleted successfully.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Error deleting lead: {e}", 500, {})
