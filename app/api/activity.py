from fastapi import APIRouter, Depends,Header,HTTPException
from sqlalchemy.orm import Session
from schemas.activity import ActivityCreate, ActivityOut
from models.activity import Activity
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed
from models.api_key import APIKey

router = APIRouter()

@router.post("/")
def create_activity(activity_in: ActivityCreate, db: Session = Depends(get_db),x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")

        # 🔍 Get user_id from api_keys table
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        user_id = api_key_entry.user_id

        # activity = Activity(**activity_in.model_dump())
        # activity["user_id"] = user_id
        activity_data = activity_in.model_dump()
        activity_data["user_id"] = user_id

        activity = Activity(**activity_data)

        db.add(activity)
        db.commit()
        db.refresh(activity)
        return api_json_response_format(True, "Activity created successfully.", 201, ActivityOut.model_validate(activity).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating activity: {e}", 500, {})

@router.get("/")
def get_all_activities(db: Session = Depends(get_db),x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="x-api-key header missing")

        # 🔍 Get user_id from api_keys table
        api_key_entry = db.query(APIKey).filter(APIKey.key_value == x_api_key).first()
        if not api_key_entry:
            raise HTTPException(status_code=401, detail="Invalid API key")

        user_id = api_key_entry.user_id
        # activities = db.query(Activity).all()
        activities = db.query(Activity).filter(Activity.user_id == user_id).all()
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