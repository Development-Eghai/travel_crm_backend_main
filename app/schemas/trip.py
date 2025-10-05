from pydantic import BaseModel
from typing import List, Optional
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

class TripMediaSchema(BaseModel):
    hero_image_url: str
    thumbnail_url: str
    gallery_urls: List[str]

class TripMediaOut(TripMediaSchema):
    pass

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

class FixedDepartureOut(FixedDeparture):
    pass

class TripPricingSchema(BaseModel):
    pricing_model: str
    fixed_departure: List[FixedDeparture]

class TripPricingOut(TripPricingSchema):
    fixed_departure: List[FixedDepartureOut]

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
    categories: List[str]
    themes: List[str]
    hotel_category: Optional[int]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    days: int
    nights: int
    meta_tags: Optional[str]
    slug: str
    pricing_model: str
    highlights: Optional[str]
    inclusions: Optional[str]
    exclusions: Optional[str]
    faqs: Optional[str]
    terms: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    itinerary: Optional[List[ItineraryItem]]
    media: Optional[TripMediaSchema]
    pricing: Optional[TripPricingSchema]
    policies: Optional[List[TripPolicySchema]]

# -------------------- TripOut --------------------

class TripOut(BaseModel):
    id: int
    title: str
    overview: Optional[str]
    destination_id: int
    destination_type: str
    categories: List[str]
    themes: List[str]
    hotel_category: Optional[int]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    days: int
    nights: int
    meta_tags: Optional[str]
    slug: str
    pricing_model: str
    highlights: Optional[str]
    inclusions: Optional[str]
    exclusions: Optional[str]
    faqs: Optional[str]
    terms: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    created_at: datetime
    updated_at: datetime
    itinerary: Optional[List[ItineraryOut]]
    media: Optional[TripMediaOut]
    pricing: Optional[TripPricingOut]
    policies: Optional[List[TripPolicyOut]]

    class Config:
        from_attributes = True