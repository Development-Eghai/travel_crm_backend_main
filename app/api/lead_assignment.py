from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.lead_assignment import LeadAssignmentCreate, LeadAssignmentOut
from models.lead_assignment import LeadAssignment
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_assignment(assignment_in: LeadAssignmentCreate, db: Session = Depends(get_db)):
    try:
        assignment = LeadAssignment(**assignment_in.model_dump())
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return api_json_response_format(True, "Assignment created successfully.", 201, LeadAssignmentOut.model_validate(assignment).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating assignment: {e}", 500, {})

@router.get("/")
def get_all_assignments(db: Session = Depends(get_db)):
    try:
        assignments = db.query(LeadAssignment).all()
        data = [LeadAssignmentOut.model_validate(a).model_dump() for a in assignments]
        return api_json_response_format(True, "Assignments retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving assignments: {e}", 500, {})

@router.get("/lead/{lead_id}")
def get_assignments_by_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        assignments = db.query(LeadAssignment).filter(LeadAssignment.lead_id == lead_id).all()
        data = [LeadAssignmentOut.model_validate(a).model_dump() for a in assignments]
        return api_json_response_format(True, "Assignments for lead retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving assignments for lead: {e}", 500, {})

@router.get("/{assignment_id}")
def get_assignment_by_id(assignment_id: int, db: Session = Depends(get_db)):
    try:
        assignment = db.query(LeadAssignment).filter(LeadAssignment.id == assignment_id).first()
        if not assignment:
            return api_json_response_format(False, "Assignment not found", 404, {})
        return api_json_response_format(True, "Assignment retrieved successfully.", 200, LeadAssignmentOut.model_validate(assignment).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving assignment: {e}", 500, {})

@router.put("/{assignment_id}")
def update_assignment(assignment_id: int, assignment_in: LeadAssignmentCreate, db: Session = Depends(get_db)):
    try:
        assignment = db.query(LeadAssignment).filter(LeadAssignment.id == assignment_id).first()
        if not assignment:
            return api_json_response_format(False, "Assignment not found", 404, {})
        for key, value in assignment_in.model_dump().items():
            setattr(assignment, key, value)
        db.commit()
        db.refresh(assignment)
        return api_json_response_format(True, "Assignment updated successfully.", 200, LeadAssignmentOut.model_validate(assignment).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating assignment: {e}", 500, {})

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    try:
        assignment = db.query(LeadAssignment).filter(LeadAssignment.id == assignment_id).first()
        if not assignment:
            return api_json_response_format(False, "Assignment not found", 404, {})
        db.delete(assignment)
        db.commit()
        return api_json_response_format(True, "Assignment deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting assignment: {e}", 500, {})