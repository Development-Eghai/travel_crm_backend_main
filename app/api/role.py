from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.role import RoleCreate, RoleOut
from models.role import Role
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    try:
        role = Role(**role_in.model_dump())
        db.add(role)
        db.commit()
        db.refresh(role)
        return api_json_response_format(True, "Role created successfully.", 201, RoleOut.model_validate(role).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating role: {e}", 500, {})

@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    try:
        roles = db.query(Role).all()
        data = [RoleOut.model_validate(r).model_dump() for r in roles]
        return api_json_response_format(True, "Roles retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving roles: {e}", 500, {})

@router.get("/{role_id}")
def get_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return api_json_response_format(False, "Role not found", 404, {})
        return api_json_response_format(True, "Role retrieved successfully.", 200, RoleOut.model_validate(role).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving role: {e}", 500, {})

@router.put("/{role_id}")
def update_role(role_id: int, role_in: RoleCreate, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return api_json_response_format(False, "Role not found", 404, {})
        for key, value in role_in.model_dump().items():
            setattr(role, key, value)
        db.commit()
        db.refresh(role)
        return api_json_response_format(True, "Role updated successfully.", 200, RoleOut.model_validate(role).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating role: {e}", 500, {})

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return api_json_response_format(False, "Role not found", 404, {})
        db.delete(role)
        db.commit()
        return api_json_response_format(True, "Role deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting role: {e}", 500, {})