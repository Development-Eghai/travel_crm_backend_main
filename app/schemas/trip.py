from pydantic import BaseModel, model_validator, field_validator
from typing import List, Optional, Literal
from datetime import datetime

# -------------------- Itinerary --------------------

class ItineraryItem(BaseModel):
    day_number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_urls: Optional[List[str]] = []
    activities: Optional[List[str]] = []
    hotel_name: Optional[str] = None
    meal_plan: Optional[List[str]] = []

class ItineraryOut(ItineraryItem):
    pass


# -------------------- Pricing --------------------

class CostingPackage(BaseModel):
    title: str
    base_price: float
    discount: float
    final_price: float
    booking_amount: float
    gst_percentage: float


class FixedDeparture(BaseModel):
    from_date: datetime
    to_date: datetime
    available_slots: int
    title: Optional[str] = None
    description: Optional[str] = None
    costingPackages: List[CostingPackage]

    # ✅ Validator to ensure non-empty costingPackages
    @field_validator("costingPackages")
    def costing_packages_not_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError("costingPackages cannot be empty")
        return v


class FixedDepartureOut(FixedDeparture):
    pass


class CustomizedPricing(BaseModel):
    pricing_type: Optional[str] = None
    base_price: Optional[float] = None
    discount: Optional[float] = None
    final_price: Optional[float] = None


class CustomizedOut(CustomizedPricing):
    pass


class TripPricingSchema(BaseModel):
    pricing_model: Optional[Literal["fixed_departure", "customized"]] = None
    fixed_departure: Optional[List[FixedDeparture]] = None
    customized: Optional[CustomizedPricing] = None

    @model_validator(mode="after")
    def check_pricing_fields(cls, model_instance: "TripPricingSchema") -> "TripPricingSchema":
        if model_instance.pricing_model == "fixed_departure":
            if not model_instance.fixed_departure:
                raise ValueError("fixed_departure is required when pricing_model='fixed_departure'")
            model_instance.customized = None
        elif model_instance.pricing_model == "customized":
            if not model_instance.customized:
                raise ValueError("customized is required when pricing_model='customized'")
            model_instance.fixed_departure = None
        return model_instance


class TripPricingOut(BaseModel):
    pricing_model: Optional[str] = None
    fixed_departure: Optional[List[FixedDepartureOut]] = []
    customized: Optional[CustomizedOut] = None


# -------------------- Policies --------------------

class TripPolicySchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class TripPolicyOut(TripPolicySchema):
    pass


# -------------------- TripCreate --------------------

class TripCreate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    destination_id: Optional[int] = None
    destination_type: Optional[str] = None
    category_id: Optional[List[str]] = []
    themes: Optional[List[str]] = []
    hotel_category: Optional[int] = None
    pickup_location: Optional[str] = None
    drop_location: Optional[str] = None
    days: Optional[int] = None
    nights: Optional[int] = None
    meta_tags: Optional[str] = None
    hero_image: Optional[str] = None
    gallery_images: Optional[List[str]] = []
    slug: Optional[str] = None
    pricing_model: Optional[str] = None
    highlights: Optional[str] = None
    inclusions: Optional[str] = None
    exclusions: Optional[str] = None
    faqs: Optional[List[dict]] = []
    terms: Optional[str] = None
    privacy_policy: Optional[str] = None
    payment_terms: Optional[str] = None
    itinerary: Optional[List[ItineraryItem]] = []
    pricing: Optional[TripPricingSchema] = None
    policies: Optional[List[TripPolicySchema]] = []
    feature_trip_flag: Optional[bool] = False
    feature_trip_type: Optional[str] = None  # ✅ Already optional with default None
    meta_title: Optional[str] = None  # ✅ Already optional with default None
    meta_description: Optional[str] = None  # ✅ Already optional with default None
    display_order: Optional[int] = None  # ✅ Already optional with default None


# -------------------- TripOut --------------------

class TripOut(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    overview: Optional[str] = None
    destination_id: Optional[int] = None
    destination_type: Optional[str] = None
    category_id: Optional[List[str]] = []
    themes: Optional[List[str]] = []
    hotel_category: Optional[int] = None
    pickup_location: Optional[str] = None
    drop_location: Optional[str] = None
    days: Optional[int] = None
    nights: Optional[int] = None
    meta_tags: Optional[str] = None
    hero_image: Optional[str] = None
    gallery_images: Optional[List[str]] = []
    slug: Optional[str] = None
    pricing_model: Optional[str] = None
    highlights: Optional[str] = None
    inclusions: Optional[str] = None
    exclusions: Optional[str] = None
    faqs: Optional[dict] = {}
    terms: Optional[str] = None
    privacy_policy: Optional[str] = None
    payment_terms: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    itinerary: Optional[List[ItineraryOut]] = []
    pricing: Optional[TripPricingOut] = None
    policies: Optional[List[TripPolicyOut]] = []

    class Config:
        from_attributes = True