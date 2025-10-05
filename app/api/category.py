from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.category import CategoryCreate, CategoryOut
from models.category import Category
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    try:
        category = Category(**category_in.model_dump())
        db.add(category)
        db.commit()
        db.refresh(category)
        return api_json_response_format(True, "Category created successfully.", 201, CategoryOut.model_validate(category).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating category: {e}", 500, {})

@router.get("/{category_id}")
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return api_json_response_format(False, "Category not found", 404, {})
        return api_json_response_format(True, "Category retrieved successfully.", 200, CategoryOut.model_validate(category).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving category: {e}", 500, {})

@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Category).all()
        data = [CategoryOut.model_validate(c).model_dump() for c in categories]
        return api_json_response_format(True, "Categories retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving categories: {e}", 500, {})

@router.put("/{category_id}")
def update_category(category_id: int, category_in: CategoryCreate, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return api_json_response_format(False, "Category not found", 404, {})
        for key, value in category_in.model_dump().items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return api_json_response_format(True, "Category updated successfully.", 200, CategoryOut.model_validate(category).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating category: {e}", 500, {})

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return api_json_response_format(False, "Category not found", 404, {})
        db.delete(category)
        db.commit()
        return api_json_response_format(True, "Category deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting category: {e}", 500, {})