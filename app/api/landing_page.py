from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import Optional
import math
import traceback
import logging

from core.database import get_db
from models.landing_page import LandingPage
from schemas.landing_page import (
    LandingPageCreate,
    LandingPageUpdate,
    LandingPageResponse,
    LandingPageList,
    PaginatedLandingPages,
)

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter()


def get_user_id_and_domain(request: Request) -> tuple:
    """Extract user_id and domain_name from request headers"""
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API key")
    
    domain_name = request.headers.get("x-domain-name", "default")
    return user_id, domain_name


def convert_to_dict(value):
    """Helper to convert Pydantic models to dict for JSON storage"""
    if value is None:
        return None
    return value.dict() if hasattr(value, 'dict') else value


def sanitize_landing_page(page):
    """
    Sanitize landing page data to ensure all fields are properly typed
    Prevents serialization errors
    """
    if not page:
        return page
    
    # Convert SQLAlchemy object to dict
    data = {
        'id': page.id,
        'page_name': page.page_name or '',
        'slug': page.slug or '',
        'template': page.template or 'template-one',
        'is_active': bool(page.is_active),
        'user_id': page.user_id,
        'domain_name': page.domain_name or 'default',
        'views': page.views or 0,
        'leads': page.leads or 0,
        'created_at': page.created_at,
        'updated_at': page.updated_at,
    }
    
    # Add JSON fields with defaults if they're None or malformed
    json_fields = [
        'custom_scripts', 'theme_colors', 'company', 'company_about', 
        'live_notifications', 'footer', 'seo', 'hero', 'packages', 
        'why_choose_us', 'attractions', 'gallery', 'testimonials', 
        'faqs', 'travel_guidelines', 'custom_sections', 'offers', 
        'section_order'
    ]
    
    for field in json_fields:
        try:
            value = getattr(page, field, None)
            # Ensure it's a dict or None
            if value is None:
                data[field] = None
            elif isinstance(value, dict):
                data[field] = value
            else:
                # Try to convert
                data[field] = value if value else None
        except Exception as e:
            logger.warning(f"Error processing field {field}: {str(e)}")
            data[field] = None
    
    return data


@router.get("/")
def get_all_landing_pages(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all landing pages with pagination"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        query = db.query(LandingPage).filter(
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        )
        
        if search:
            query = query.filter(LandingPage.page_name.ilike(f"%{search}%"))
        
        if is_active is not None:
            query = query.filter(LandingPage.is_active == is_active)
        
        total = query.count()
        offset = (page - 1) * per_page
        pages = query.order_by(LandingPage.created_at.desc()).offset(offset).limit(per_page).all()
        
        sanitized_pages = [sanitize_landing_page(p) for p in pages]
        total_pages = math.ceil(total / per_page) if total > 0 else 1
        
        return {
            "pages": sanitized_pages,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_landing_pages: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/all")
def get_all_landing_pages_no_pagination(
    request: Request,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get ALL landing pages without pagination"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        query = db.query(LandingPage).filter(
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        )
        
        if search:
            query = query.filter(LandingPage.page_name.ilike(f"%{search}%"))
        
        if is_active is not None:
            query = query.filter(LandingPage.is_active == is_active)
        
        pages = query.order_by(LandingPage.created_at.desc()).all()
        sanitized_pages = [sanitize_landing_page(p) for p in pages]
        
        return {"pages": sanitized_pages}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_landing_pages_no_pagination: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{landing_page_id}")
def get_landing_page(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get a specific landing page by ID with all sections"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        landing_page = db.query(LandingPage).filter(
            LandingPage.id == landing_page_id,
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        ).first()
        
        if not landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        return sanitize_landing_page(landing_page)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_landing_page: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/slug/{slug}")
def get_landing_page_by_slug(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get landing page by slug (Public endpoint for frontend display)"""
    try:
        domain_name = request.headers.get("x-domain-name", "default")
        
        landing_page = db.query(LandingPage).filter(
            LandingPage.slug == slug,
            LandingPage.domain_name == domain_name,
            LandingPage.is_active == True,
            LandingPage.is_deleted == False
        ).first()
        
        if not landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        # Auto-increment view count
        landing_page.views += 1
        db.commit()
        
        return sanitize_landing_page(landing_page)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_landing_page_by_slug: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/")
def create_landing_page(
    landing_page: LandingPageCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Create a new landing page with all features including custom scripts"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        # Check slug uniqueness
        existing = db.query(LandingPage).filter(
            LandingPage.slug == landing_page.slug,
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists for this user")
        
        # Create new landing page
        db_landing_page = LandingPage(
            user_id=user_id,
            domain_name=domain_name,
            page_name=landing_page.page_name,
            slug=landing_page.slug,
            template=landing_page.template,
            is_active=landing_page.is_active,
            custom_scripts=convert_to_dict(landing_page.custom_scripts),
            theme_colors=convert_to_dict(landing_page.theme_colors),
            company=convert_to_dict(landing_page.company),
            company_about=convert_to_dict(landing_page.company_about),
            live_notifications=convert_to_dict(landing_page.live_notifications),
            footer=convert_to_dict(landing_page.footer),
            seo=convert_to_dict(landing_page.seo),
            hero=convert_to_dict(landing_page.hero),
            packages=convert_to_dict(landing_page.packages),
            why_choose_us=convert_to_dict(landing_page.why_choose_us),
            attractions=convert_to_dict(landing_page.attractions),
            gallery=convert_to_dict(landing_page.gallery),
            testimonials=convert_to_dict(landing_page.testimonials),
            faqs=convert_to_dict(landing_page.faqs),
            travel_guidelines=convert_to_dict(landing_page.travel_guidelines),
            custom_sections=convert_to_dict(landing_page.custom_sections),
            offers=convert_to_dict(landing_page.offers),
            section_order=convert_to_dict(landing_page.section_order),
        )
        
        db.add(db_landing_page)
        db.commit()
        db.refresh(db_landing_page)
        
        return {
            "success": True,
            "message": "Landing Page Created Successfully",
            "data": sanitize_landing_page(db_landing_page)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in create_landing_page: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{landing_page_id}")
def update_landing_page(
    landing_page_id: int,
    landing_page_update: LandingPageUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update landing page - supports all fields including custom scripts"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        db_landing_page = db.query(LandingPage).filter(
            LandingPage.id == landing_page_id,
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        ).first()
        
        if not db_landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        # Update fields that were provided
        update_data = landing_page_update.dict(exclude_unset=True)
        
        json_fields = {
            'custom_scripts', 'theme_colors', 'company', 'company_about', 
            'live_notifications', 'footer', 'seo', 'hero', 'packages', 
            'why_choose_us', 'attractions', 'gallery', 'testimonials', 
            'faqs', 'travel_guidelines', 'custom_sections', 'offers', 
            'section_order'
        }
        
        for field, value in update_data.items():
            if hasattr(db_landing_page, field):
                if field in json_fields and value is not None:
                    value = convert_to_dict(value)
                setattr(db_landing_page, field, value)
        
        db.commit()
        db.refresh(db_landing_page)
        
        return {
            "success": True,
            "message": "Landing Page Updated Successfully",
            "data": sanitize_landing_page(db_landing_page)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in update_landing_page: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{landing_page_id}")
def delete_landing_page(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Soft delete landing page"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        db_landing_page = db.query(LandingPage).filter(
            LandingPage.id == landing_page_id,
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        ).first()
        
        if not db_landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        db_landing_page.is_deleted = True
        db.commit()
        
        return {"success": True, "message": "Landing page deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in delete_landing_page: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{landing_page_id}/toggle-active")
def toggle_active_status(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Toggle active/inactive status of a landing page"""
    try:
        user_id, domain_name = get_user_id_and_domain(request)
        
        db_landing_page = db.query(LandingPage).filter(
            LandingPage.id == landing_page_id,
            LandingPage.user_id == user_id,
            LandingPage.is_deleted == False
        ).first()
        
        if not db_landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        db_landing_page.is_active = not db_landing_page.is_active
        db.commit()
        
        status = "activated" if db_landing_page.is_active else "deactivated"
        
        return {
            "success": True,
            "message": f"Landing page {status}",
            "is_active": db_landing_page.is_active
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in toggle_active_status: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{landing_page_id}/track-view")
def track_view(landing_page_id: int, db: Session = Depends(get_db)):
    """Track page view (Public endpoint)"""
    try:
        db_landing_page = db.query(LandingPage).filter(
            LandingPage.id == landing_page_id,
            LandingPage.is_deleted == False
        ).first()
        
        if not db_landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        db_landing_page.views += 1
        db.commit()
        
        return {"success": True, "views": db_landing_page.views}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in track_view: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{landing_page_id}/track-lead")
def track_lead(landing_page_id: int, db: Session = Depends(get_db)):
    """Track lead conversion (Public endpoint)"""
    try:
        db_landing_page = db.query(LandingPage).filter(
            LandingPage.id == landing_page_id,
            LandingPage.is_deleted == False
        ).first()
        
        if not db_landing_page:
            raise HTTPException(status_code=404, detail="Landing page not found")
        
        db_landing_page.leads += 1
        db.commit()
        
        return {"success": True, "leads": db_landing_page.leads}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in track_lead: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")