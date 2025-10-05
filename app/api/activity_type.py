from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.activity_type import ActivityTypeCreate, ActivityTypeOut
from models.activity_type import ActivityType
from core.database import get_db
from utils.response import api_json_response_format  # Adjust import if needed

router = APIRouter()

@router.post("/")
def create_activity_type(activity_in: ActivityTypeCreate, db: Session = Depends(get_db)):
    try:
        activity = ActivityType(**activity_in.model_dump())
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return api_json_response_format(True, "Activity type created successfully.", 201, ActivityTypeOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating activity type: {e}", 500, {})

@router.get("/")
def get_activity_types(db: Session = Depends(get_db)):
    try:
        activities = db.query(ActivityType).all()
        data = [ActivityTypeOut.model_validate(a).model_dump() for a in activities]
        return api_json_response_format(True, "Activity types retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving activity types: {e}", 500, {})

@router.get("/{activity_id}")
def get_activity_type(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity = db.query(ActivityType).filter(ActivityType.id == activity_id).first()
        if not activity:
            return api_json_response_format(False, "Activity type not found", 404, {})
        return api_json_response_format(True, "Activity type retrieved successfully.", 200, ActivityTypeOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving activity type: {e}", 500, {})

@router.put("/{activity_id}")
def update_activity_type(activity_id: int, activity_in: ActivityTypeCreate, db: Session = Depends(get_db)):
    try:
        activity = db.query(ActivityType).filter(ActivityType.id == activity_id).first()
        if not activity:
            return api_json_response_format(False, "Activity type not found", 404, {})
        for key, value in activity_in.model_dump().items():
            setattr(activity, key, value)
        db.commit()
        db.refresh(activity)
        return api_json_response_format(True, "Activity type updated successfully.", 200, ActivityTypeOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating activity type: {e}", 500, {})

@router.delete("/{activity_id}")
def delete_activity_type(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity = db.query(ActivityType).filter(ActivityType.id == activity_id).first()
        if not activity:
            return api_json_response_format(False, "Activity type not found", 404, {})
        db.delete(activity)
        db.commit()
        return api_json_response_format(True, "Activity type deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting activity type: {e}", 500, {})