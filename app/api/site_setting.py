from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.site_setting import GlobalSettingsSchema
from models.site_setting import GlobalSettings
from core.database import get_db
from utils.response import api_json_response_format

router = APIRouter()


@router.post("/")
def create_global_settings(payload: GlobalSettingsSchema, db: Session = Depends(get_db)):
    existing = db.query(GlobalSettings).first()
    if existing:
        return api_json_response_format(False, "Settings already exist. Use PUT to update.", 400, {})

    def join(val): return ",".join(val) if isinstance(val, list) else val

    settings = GlobalSettings()
    for key, value in payload.model_dump().items():
        if key in ["homepage_slider", "contact_phones", "social_links", "upi_ids", "qr_code_images", "meta_tags"]:
            setattr(settings, key, join(value))
        else:
            setattr(settings, key, value)

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return api_json_response_format(True, "Global settings created successfully.", 201, {"id": settings.id})

@router.get("/")
def get_global_settings(db: Session = Depends(get_db)):
    settings = db.query(GlobalSettings).first()
    if not settings:
        return api_json_response_format(False, "Settings not found", 404, {})

    def split(val): return val.split(",") if val else []

    data = {
        "site_title": settings.site_title,
        "tagline": settings.tagline,
        "company_name": settings.company_name,
        "site_description": settings.site_description,
        "logo_url": settings.logo_url,
        "favicon_url": settings.favicon_url,
        "homepage_slider": split(settings.homepage_slider),
        "contact_email": settings.contact_email,
        "contact_phones": split(settings.contact_phones),
        "business_address": settings.business_address,
        "social_links": split(settings.social_links),
        "google_map_link": settings.google_map_link,
        "bank_name": settings.bank_name,
        "account_number": settings.account_number,
        "ifsc_code": settings.ifsc_code,
        "branch_name": settings.branch_name,
        "upi_ids": split(settings.upi_ids),
        "qr_code_images": split(settings.qr_code_images),
        "quotation_format": settings.quotation_format,
        "invoice_format": settings.invoice_format,
        "header_menu": settings.header_menu,
        "footer_menu": settings.footer_menu,
        "meta_title": settings.meta_title,
        "meta_description": settings.meta_description,
        "meta_tags": split(settings.meta_tags),
        "og_title": settings.og_title,
        "og_description": settings.og_description,
        "og_image": settings.og_image,
        "terms_conditions": settings.terms_conditions,
        "privacy_policy": settings.privacy_policy,
        "payment_terms": settings.payment_terms,
        "cancellation_policy": settings.cancellation_policy,
        "refund_policy": settings.refund_policy,
        "email_incoming": settings.email_incoming,
        "email_form_submitted": settings.email_form_submitted,
        "email_quotation_sent": settings.email_quotation_sent,
        "email_invoice_sent": settings.email_invoice_sent,
        "email_lead_assigned": settings.email_lead_assigned,
        "email_payment_confirmation": settings.email_payment_confirmation,
        "email_invoice_due": settings.email_invoice_due,
        "email_trip_updates": settings.email_trip_updates,
        "email_follow_up": settings.email_follow_up
    }

    return api_json_response_format(True, "Global settings retrieved successfully.", 200, data)


@router.put("/")
def update_global_settings(payload: GlobalSettingsSchema, db: Session = Depends(get_db)):
    settings = db.query(GlobalSettings).first()
    if not settings:
        settings = GlobalSettings()

    def join(val): return ",".join(val) if isinstance(val, list) else val

    for key, value in payload.model_dump().items():
        if key in ["homepage_slider", "contact_phones", "social_links", "upi_ids", "qr_code_images", "meta_tags"]:
            setattr(settings, key, join(value))
        else:
            setattr(settings, key, value)

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return api_json_response_format(True, "Global settings updated successfully.", 200, {})

@router.delete("/")
def delete_global_settings(db: Session = Depends(get_db)):
    settings = db.query(GlobalSettings).first()
    if not settings:
        return api_json_response_format(False, "No settings found to delete.", 404, {})

    db.delete(settings)
    db.commit()

    return api_json_response_format(True, "Global settings deleted successfully.", 200, {})