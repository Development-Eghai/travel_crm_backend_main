from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.landing_page import LandingPage
from schemas.landing_page import (
    LandingPageCreate,
    LandingPageUpdate,
    LandingPageResponse,
    LandingPageList,
    PaginatedLandingPages
)
import math

router = APIRouter()

def get_user_id_and_domain(request: Request):
    """Extract user_id and domain_name from request"""
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API key")
    
    domain_name = request.headers.get("x-domain-name", "default")
    return user_id, domain_name


@router.post("/")
def create_landing_page(
    landing_page: LandingPageCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Create a new landing page with all new features"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    # Check slug uniqueness
    existing = db.query(LandingPage).filter(
        LandingPage.slug == landing_page.slug,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    # Create new landing page with all fields (theme_colors excluded)
    db_landing_page = LandingPage(
        user_id=user_id,
        domain_name=domain_name,
        page_name=landing_page.page_name,
        slug=landing_page.slug,
        template=landing_page.template,
        is_active=landing_page.is_active,
        
        # theme_colors REMOVED - field hidden
        
        # UPDATED: Enhanced company info
        company=landing_page.company.dict() if landing_page.company else None,
        
        # NEW: Company about
        company_about=landing_page.company_about.dict() if landing_page.company_about else None,
        
        # NEW: Live notifications
        live_notifications=landing_page.live_notifications.dict() if landing_page.live_notifications else None,
        
        seo=landing_page.seo.dict() if landing_page.seo else None,
        hero=landing_page.hero.dict() if landing_page.hero else None,
        
        # UPDATED: Packages with custom packages
        packages=landing_page.packages.dict() if landing_page.packages else None,
        
        attractions=landing_page.attractions.dict() if landing_page.attractions else None,
        gallery=landing_page.gallery.dict() if landing_page.gallery else None,
        testimonials=landing_page.testimonials.dict() if landing_page.testimonials else None,
        faqs=landing_page.faqs.dict() if landing_page.faqs else None,
        travel_guidelines=landing_page.travel_guidelines.dict() if landing_page.travel_guidelines else None,
        offers=landing_page.offers.dict() if landing_page.offers else None
    )
    
    db.add(db_landing_page)
    db.commit()
    db.refresh(db_landing_page)
    
    return {
        "success": True,
        "message": "Landing Page Created Successfully",
        "data": db_landing_page
    }


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
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return {
        "pages": pages,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }


@router.get("/all")
def get_all_no_pagination(
    request: Request,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get ALL landing pages without pagination"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    query = db.query(LandingPage).filter(
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    )
    
    if search:
        query = query.filter(LandingPage.page_name.ilike(f"%{search}%"))
    
    if is_active is not None:
        query = query.filter(LandingPage.is_active == is_active)
    
    return query.order_by(LandingPage.created_at.desc()).all()


@router.get("/{landing_page_id}")
def get_landing_page(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get a specific landing page by ID"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    return landing_page


@router.get("/slug/{slug}")
def get_landing_page_by_slug(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get landing page by slug (Public)"""
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
    
    return landing_page


@router.put("/{landing_page_id}")
def update_landing_page(
    landing_page_id: int,
    landing_page_update: LandingPageUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update landing page - supports all fields except theme_colors (hidden)"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    # Update all fields (theme_colors excluded)
    update_data = landing_page_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(db_landing_page, field):
            # Convert Pydantic models to dict for JSON fields
            if field in ['company', 'company_about', 'live_notifications',
                        'seo', 'hero', 'packages', 'attractions', 'gallery', 
                        'testimonials', 'faqs', 'travel_guidelines', 'offers']:
                if value is not None:
                    value = value.dict() if hasattr(value, 'dict') else value
            setattr(db_landing_page, field, value)
    
    db.commit()
    db.refresh(db_landing_page)
    
    return {
        "success": True,
        "message": "Landing Page Updated Successfully",
        "data": db_landing_page
    }


@router.delete("/{landing_page_id}")
def delete_landing_page(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Soft delete"""
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
    
    return {"success": True, "message": "Deleted successfully"}


@router.patch("/{landing_page_id}/toggle-active")
def toggle_active_status(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Toggle active status"""
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
    
    return {
        "success": True,
        "message": f"{'Activated' if db_landing_page.is_active else 'Deactivated'}",
        "is_active": db_landing_page.is_active
    }


@router.post("/{landing_page_id}/track-view")
def track_view(landing_page_id: int, db: Session = Depends(get_db)):
    """Public: Track page view"""
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Not found")
    
    db_landing_page.views += 1
    db.commit()
    
    return {"success": True, "views": db_landing_page.views}


@router.post("/{landing_page_id}/track-lead")
def track_lead(landing_page_id: int, db: Session = Depends(get_db)):
    """Public: Track lead conversion"""
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Not found")
    
    db_landing_page.leads += 1
    db.commit()
    
    return {"success": True, "leads": db_landing_page.leads}