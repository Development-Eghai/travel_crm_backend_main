from pydantic import BaseModel, model_validator, field_validator
from typing import List, Optional, Literal
from datetime import datetime

# -------------------- Itinerary --------------------

class ItineraryItem(BaseModel):
    day_number: Optional[int]
    title: Optional[str]
    description: Optional[str]
    image_urls: Optional[List[str]] = []
    activities: Optional[List[str]] = []
    hotel_name: Optional[str]
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
    pricing_type: Optional[str]
    base_price: Optional[float]
    discount: Optional[float]
    final_price: Optional[float]


class CustomizedOut(CustomizedPricing):
    pass


class TripPricingSchema(BaseModel):
    pricing_model: Optional[Literal["fixed_departure", "customized"]]
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
    pricing_model: Optional[str]
    fixed_departure: Optional[List[FixedDepartureOut]] = []
    customized: Optional[CustomizedOut] = None


# -------------------- Policies --------------------

class TripPolicySchema(BaseModel):
    title: Optional[str]
    content: Optional[str]


class TripPolicyOut(TripPolicySchema):
    pass


# -------------------- TripCreate --------------------

class TripCreate(BaseModel):
    title: Optional[str]
    overview: Optional[str]
    destination_id: Optional[int]
    destination_type: Optional[str]
    category_id: Optional[List[str]] = []
    themes: Optional[List[str]] = []
    hotel_category: Optional[int]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    days: Optional[int]
    nights: Optional[int]
    meta_tags: Optional[str]
    hero_image: Optional[str]
    gallery_images: Optional[List[str]] = []
    slug: Optional[str]
    pricing_model: Optional[str]
    highlights: Optional[str]
    inclusions: Optional[str]
    exclusions: Optional[str]
    faqs: Optional[List[dict]] = []
    terms: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    itinerary: Optional[List[ItineraryItem]] = []
    pricing: Optional[TripPricingSchema]
    policies: Optional[List[TripPolicySchema]] = []


# -------------------- TripOut --------------------

class TripOut(BaseModel):
    id: Optional[int]
    title: Optional[str]
    overview: Optional[str]
    destination_id: Optional[int]
    destination_type: Optional[str]
    category_id: Optional[List[str]] = []
    themes: Optional[List[str]] = []
    hotel_category: Optional[int]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    days: Optional[int]
    nights: Optional[int]
    meta_tags: Optional[str]
    hero_image: Optional[str]
    gallery_images: Optional[List[str]] = []
    slug: Optional[str]
    pricing_model: Optional[str]
    highlights: Optional[str]
    inclusions: Optional[str]
    exclusions: Optional[str]
    faqs: Optional[dict] = {}
    terms: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    itinerary: Optional[List[ItineraryOut]] = []
    pricing: Optional[TripPricingOut]
    policies: Optional[List[TripPolicyOut]] = []

    class Config:
        from_attributes = True
