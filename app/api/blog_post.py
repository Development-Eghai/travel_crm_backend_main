from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.blog_post import BlogPostCreate, BlogPostOut
from models.blog_post import BlogPost
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_blog(blog_in: BlogPostCreate, db: Session = Depends(get_db)):
    try:
        blog = BlogPost(**blog_in.model_dump())
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return api_json_response_format(True, "Blog post created successfully.", 201, BlogPostOut.model_validate(blog).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating blog post: {e}", 500, {})

@router.get("/")
def get_blogs(db: Session = Depends(get_db)):
    try:
        blogs = db.query(BlogPost).all()
        data = [BlogPostOut.model_validate(b).model_dump() for b in blogs]
        return api_json_response_format(True, "Blog posts retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving blog posts: {e}", 500, {})

@router.get("/{blog_id}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    try:
        blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
        if not blog:
            return api_json_response_format(False, "Blog post not found", 404, {})
        return api_json_response_format(True, "Blog post retrieved successfully.", 200, BlogPostOut.model_validate(blog).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving blog post: {e}", 500, {})

@router.put("/{blog_id}")
def update_blog(blog_id: int, blog_in: BlogPostCreate, db: Session = Depends(get_db)):
    try:
        blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
        if not blog:
            return api_json_response_format(False, "Blog post not found", 404, {})
        for key, value in blog_in.model_dump().items():
            setattr(blog, key, value)
        db.commit()
        db.refresh(blog)
        return api_json_response_format(True, "Blog post updated successfully.", 200, BlogPostOut.model_validate(blog).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating blog post: {e}", 500, {})

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    try:
        blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
        if not blog:
            return api_json_response_format(False, "Blog post not found", 404, {})
        db.delete(blog)
        db.commit()
        return api_json_response_format(True, "Blog post deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting blog post: {e}", 500, {})