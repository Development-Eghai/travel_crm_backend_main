from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.tag import TagCreate, TagOut
from models.tag import Tag
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_tag(tag_in: TagCreate, db: Session = Depends(get_db)):
    try:
        tag = Tag(**tag_in.model_dump())
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return api_json_response_format(True, "Tag created successfully.", 201, TagOut.model_validate(tag).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating tag: {e}", 500, {})

@router.get("/")
def get_tags(db: Session = Depends(get_db)):
    try:
        tags = db.query(Tag).all()
        data = [TagOut.model_validate(t).model_dump() for t in tags]
        return api_json_response_format(True, "Tags retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving tags: {e}", 500, {})

@router.get("/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return api_json_response_format(False, "Tag not found", 404, {})
        return api_json_response_format(True, "Tag retrieved successfully.", 200, TagOut.model_validate(tag).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving tag: {e}", 500, {})

@router.put("/{tag_id}")
def update_tag(tag_id: int, tag_in: TagCreate, db: Session = Depends(get_db)):
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return api_json_response_format(False, "Tag not found", 404, {})
        for key, value in tag_in.model_dump().items():
            setattr(tag, key, value)
        db.commit()
        db.refresh(tag)
        return api_json_response_format(True, "Tag updated successfully.", 200, TagOut.model_validate(tag).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating tag: {e}", 500, {})

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return api_json_response_format(False, "Tag not found", 404, {})
        db.delete(tag)
        db.commit()
        return api_json_response_format(True, "Tag deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting tag: {e}", 500, {})