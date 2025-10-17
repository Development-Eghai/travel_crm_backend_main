from pydantic import BaseModel, model_validator
from typing import List, Optional, Literal
from datetime import datetime

# -------------------- Itinerary --------------------

class ItineraryItem(BaseModel):
    day_number: int
    title: str
    description: str
    image_urls: List[str]
    activities: List[str]
    hotel_name: str
    meal_plan: List[str]

class ItineraryOut(ItineraryItem):
    pass

# -------------------- Media --------------------

# class TripMediaSchema(BaseModel):
#     hero_image_url: str
#     thumbnail_url: str
#     gallery_urls: List[str]

# class TripMediaOut(TripMediaSchema):
#     pass

# -------------------- Pricing --------------------

class FixedDeparture(BaseModel):
    from_date: datetime
    to_date: datetime
    available_slots: int
    title: str
    description: str
    base_price: float
    discount: float
    final_price: float
    booking_amount: float
    gst_percentage: float

class CustomizedPricing(BaseModel):
    pricing_type: str
    base_price: float
    discount: float
    final_price: float

class customizedOut(BaseModel):
    pass

class FixedDepartureOut(FixedDeparture):
    pass

class TripPricingSchema(BaseModel):
    pricing_model: Literal["fixed_departure", "customized"]
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

class TripPricingOut(TripPricingSchema):
    fixed_departure: List[FixedDepartureOut]
    customized: List[customizedOut]

# -------------------- Policies --------------------

class TripPolicySchema(BaseModel):
    title: str
    content: str

class TripPolicyOut(TripPolicySchema):
    pass

# -------------------- TripCreate --------------------

class TripCreate(BaseModel):
    title: str
    overview: Optional[str]
    destination_id: int
    destination_type: str
    category_id: Optional[int]
    themes: Optional[List[str]] = []
    hotel_category: Optional[int]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    days: int
    nights: int
    meta_tags: Optional[str]
    hero_image: Optional[str]
    gallery_images : Optional[List[str]] = []
    slug: str
    pricing_model: str
    highlights: Optional[str]
    inclusions: Optional[str]
    exclusions: Optional[str]
    faqs: Optional[list[dict]] = None
    terms: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    itinerary: Optional[List[ItineraryItem]]
    # media: Optional[TripMediaSchema]
    pricing: Optional[TripPricingSchema]
    policies: Optional[List[TripPolicySchema]]

# -------------------- TripOut --------------------

class TripOut(BaseModel):
    id: int
    title: str
    overview: Optional[str]
    destination_id: int
    destination_type: str
    category_id: Optional[int]
    # category: Optional[str] = None
    themes: Optional[List[str]] = []
    hotel_category: Optional[int]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    days: int
    nights: int
    meta_tags: Optional[str]
    hero_image: Optional[str]
    gallery_images : Optional[List[str]] = []
    slug: str
    pricing_model: str
    highlights: Optional[str]
    inclusions: Optional[str]
    exclusions: Optional[str]
    faqs: Optional[dict] = None
    terms: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    created_at: datetime
    updated_at: datetime
    itinerary: Optional[List[ItineraryOut]]
    # media: Optional[TripMediaOut]
    pricing: Optional[TripPricingOut]
    policies: Optional[List[TripPolicyOut]]

    class Config:
        from_attributes = True