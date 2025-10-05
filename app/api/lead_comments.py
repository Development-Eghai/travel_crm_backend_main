from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.lead_comments import LeadComment
from schemas.lead_comments import LeadCommentCreate, LeadCommentOut
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_comment(comment_in: LeadCommentCreate, db: Session = Depends(get_db)):
    try:
        comment = LeadComment(**comment_in.model_dump())
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return api_json_response_format(True, "Comment added successfully.", 201, LeadCommentOut.model_validate(comment).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error adding comment: {e}", 500, {})

@router.get("/{lead_id}")
def get_comments_for_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        comments = db.query(LeadComment).filter(LeadComment.lead_id == lead_id).order_by(LeadComment.created_at.desc()).all()
        data = [LeadCommentOut.model_validate(c).model_dump() for c in comments]
        return api_json_response_format(True, "Comments retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving comments: {e}", 500, {})

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    try:
        comment = db.query(LeadComment).filter(LeadComment.id == comment_id).first()
        if not comment:
            return api_json_response_format(False, "Comment not found", 404, {})
        db.delete(comment)
        db.commit()
        return api_json_response_format(True, "Comment deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting comment: {e}", 500, {})