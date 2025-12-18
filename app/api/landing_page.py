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
    
    # Extract domain from headers or use a default
    domain_name = request.headers.get("x-domain-name", "default")
    
    return user_id, domain_name


# ============================
# CREATE LANDING PAGE
# ============================
@router.post("/")
def create_landing_page(
    landing_page: LandingPageCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Create a new landing page"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    # Check if slug already exists for this user
    existing = db.query(LandingPage).filter(
        LandingPage.slug == landing_page.slug,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    # Create new landing page
    db_landing_page = LandingPage(
        user_id=user_id,
        domain_name=domain_name,
        page_name=landing_page.page_name,
        slug=landing_page.slug,
        template=landing_page.template,
        is_active=landing_page.is_active,
        company=landing_page.company.dict() if landing_page.company else None,
        seo=landing_page.seo.dict() if landing_page.seo else None,
        hero=landing_page.hero.dict() if landing_page.hero else None,
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
    
    # Return direct data (not wrapped) - Frontend expects this
    return db_landing_page


# ============================
# LIST LANDING PAGES
# ============================
@router.get("/", response_model=PaginatedLandingPages)
def get_all_landing_pages(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all landing pages for the authenticated user with pagination"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    # Base query
    query = db.query(LandingPage).filter(
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    )
    
    # Apply filters
    if search:
        query = query.filter(LandingPage.page_name.ilike(f"%{search}%"))
    
    if is_active is not None:
        query = query.filter(LandingPage.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    pages = query.order_by(LandingPage.created_at.desc()).offset(offset).limit(per_page).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return PaginatedLandingPages(
        pages=pages,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


# ============================
# GET SINGLE LANDING PAGE
# ============================
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
    
    # Return direct data (not wrapped) - Frontend expects this
    return landing_page


# ============================
# GET LANDING PAGE BY SLUG (PUBLIC)
# ============================
@router.get("/slug/{slug}")
def get_landing_page_by_slug(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get landing page by slug (Public endpoint for frontend display)"""
    # For public access, we might not require user_id
    # But we need domain_name to filter correctly
    domain_name = request.headers.get("x-domain-name", "default")
    
    landing_page = db.query(LandingPage).filter(
        LandingPage.slug == slug,
        LandingPage.domain_name == domain_name,
        LandingPage.is_active == True,
        LandingPage.is_deleted == False
    ).first()
    
    if not landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    # Increment view count
    landing_page.views += 1
    db.commit()
    
    return landing_page


# ============================
# UPDATE LANDING PAGE
# ============================
@router.put("/{landing_page_id}")
def update_landing_page(
    landing_page_id: int,
    landing_page_update: LandingPageUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update an existing landing page"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    # Update fields
    update_data = landing_page_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(db_landing_page, field):
            # Convert Pydantic models to dict for JSON fields
            if field in ['company', 'seo', 'hero', 'packages', 'attractions', 
                        'gallery', 'testimonials', 'faqs', 'travel_guidelines', 'offers']:
                if value is not None:
                    value = value.dict() if hasattr(value, 'dict') else value
            setattr(db_landing_page, field, value)
    
    db.commit()
    db.refresh(db_landing_page)
    
    # Return direct data (not wrapped) - Frontend expects this
    return db_landing_page


# ============================
# DELETE LANDING PAGE (SOFT DELETE)
# ============================
@router.delete("/{landing_page_id}")
def delete_landing_page(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Soft delete a landing page"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    # Soft delete
    db_landing_page.is_deleted = True
    db.commit()
    
    return {
        "success": True,
        "message": "Landing page deleted successfully"
    }


# ============================
# TOGGLE ACTIVE STATUS
# ============================
@router.patch("/{landing_page_id}/toggle-active")
def toggle_active_status(
    landing_page_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Toggle the active status of a landing page"""
    user_id, domain_name = get_user_id_and_domain(request)
    
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.user_id == user_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    # Toggle the status
    db_landing_page.is_active = not db_landing_page.is_active
    db.commit()
    db.refresh(db_landing_page)
    
    return {
        "success": True,
        "message": f"Landing page {'activated' if db_landing_page.is_active else 'deactivated'} successfully",
        "is_active": db_landing_page.is_active
    }


# ============================
# TRACK VIEW (PUBLIC)
# ============================
@router.post("/{landing_page_id}/track-view")
def track_view(
    landing_page_id: int,
    db: Session = Depends(get_db)
):
    """Increment view count for a landing page (Public endpoint)"""
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    db_landing_page.views += 1
    db.commit()
    
    return {
        "success": True,
        "views": db_landing_page.views
    }


# ============================
# TRACK LEAD (PUBLIC)
# ============================
@router.post("/{landing_page_id}/track-lead")
def track_lead(
    landing_page_id: int,
    db: Session = Depends(get_db)
):
    """Increment lead count for a landing page (Public endpoint)"""
    db_landing_page = db.query(LandingPage).filter(
        LandingPage.id == landing_page_id,
        LandingPage.is_deleted == False
    ).first()
    
    if not db_landing_page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    db_landing_page.leads += 1
    db.commit()
    
    return {
        "success": True,
        "leads": db_landing_page.leads
    }