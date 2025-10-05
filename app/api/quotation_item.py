from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.quotation_item import QuotationItemCreate, QuotationItemOut
from models.quotation_item import QuotationItem
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_item(item_in: QuotationItemCreate, db: Session = Depends(get_db)):
    try:
        item = QuotationItem(**item_in.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return api_json_response_format(True, "Quotation item created successfully.", 201, QuotationItemOut.model_validate(item).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating quotation item: {e}", 500, {})

@router.get("/")
def get_all_items(db: Session = Depends(get_db)):
    try:
        items = db.query(QuotationItem).order_by(QuotationItem.created_at.desc()).all()
        data = [QuotationItemOut.model_validate(i).model_dump() for i in items]
        return api_json_response_format(True, "Quotation items retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving quotation items: {e}", 500, {})

@router.get("/{quotation_id}")
def get_items_for_quotation(quotation_id: int, db: Session = Depends(get_db)):
    try:
        items = db.query(QuotationItem).filter(QuotationItem.quotation_id == quotation_id).order_by(QuotationItem.sort_order).all()
        data = [QuotationItemOut.model_validate(i).model_dump() for i in items]
        return api_json_response_format(True, "Items for quotation retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving items for quotation: {e}", 500, {})

@router.put("/{item_id}")
def update_item(item_id: int, item_in: QuotationItemCreate, db: Session = Depends(get_db)):
    try:
        item = db.query(QuotationItem).filter(QuotationItem.id == item_id).first()
        if not item:
            return api_json_response_format(False, "Item not found", 404, {})
        for key, value in item_in.model_dump().items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return api_json_response_format(True, "Quotation item updated successfully.", 200, QuotationItemOut.model_validate(item).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating quotation item: {e}", 500, {})

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(QuotationItem).filter(QuotationItem.id == item_id).first()
        if not item:
            return api_json_response_format(False, "Item not found", 404, {})
        db.delete(item)
        db.commit()
        return api_json_response_format(True, "Quotation item deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting quotation item: {e}", 500, {})