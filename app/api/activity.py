from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.activity import ActivityCreate, ActivityOut
from models.activity import Activity
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_activity(activity_in: ActivityCreate, db: Session = Depends(get_db)):
    try:
        activity = Activity(**activity_in.model_dump())
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return api_json_response_format(True, "Activity created successfully.", 201, ActivityOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating activity: {e}", 500, {})

@router.get("/")
def get_all_activities(db: Session = Depends(get_db)):
    try:
        activities = db.query(Activity).all()
        data = [ActivityOut.model_validate(a).model_dump() for a in activities]
        return api_json_response_format(True, "Activities retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving activities: {e}", 500, {})

@router.get("/{activity_id}")
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return api_json_response_format(False, "Activity not found", 404, {})
        return api_json_response_format(True, "Activity retrieved successfully.", 200, ActivityOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving activity: {e}", 500, {})

@router.put("/{activity_id}")
def update_activity(activity_id: int, activity_in: ActivityCreate, db: Session = Depends(get_db)):
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return api_json_response_format(False, "Activity not found", 404, {})
        for key, value in activity_in.model_dump().items():
            setattr(activity, key, value)
        db.commit()
        db.refresh(activity)
        return api_json_response_format(True, "Activity updated successfully.", 200, ActivityOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating activity: {e}", 500, {})

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return api_json_response_format(False, "Activity not found", 404, {})
        db.delete(activity)
        db.commit()
        return api_json_response_format(True, "Activity deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting activity: {e}", 500, {})