from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.model_enquireform import EnquireForm
from schemas.schema_enquireform import EnquireFormCreate, EnquireFormOut
from core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[EnquireFormOut])
async def get_enquiries(db: Session = Depends(get_db)):
    enquiries = db.query(EnquireForm).order_by(EnquireForm.created_at.desc()).all()
    return enquiries

@router.get("/{enquire_id}", response_model=EnquireFormOut)
async def get_enquiry(enquire_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(EnquireForm).filter(EnquireForm.id == enquire_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return enquiry

@router.post("/", response_model=EnquireFormOut, status_code=status.HTTP_201_CREATED)
async def create_enquiry(data: EnquireFormCreate, db: Session = Depends(get_db)):
    new_enquiry = EnquireForm(**data.dict())
    db.add(new_enquiry)
    db.commit()
    db.refresh(new_enquiry)
    return new_enquiry

enquire_router = router
