from sqlalchemy.orm import Session
from models.lead import Lead
from schemas.lead import LeadCreate

def create_lead(db: Session, lead_in: LeadCreate) -> Lead:
    lead = Lead(**lead_in.dict())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

def get_leads(db: Session, tenant_id: int):
    return db.query(Lead).filter(Lead.tenant_id == tenant_id).all()