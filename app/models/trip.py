from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

# -------------------- Trip Core --------------------

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    overview = Column(Text)
    destination_id = Column(Integer, nullable=False)
    destination_type = Column(String(50), nullable=False)
    categories = Column(Text)  # comma-separated
    themes = Column(Text)      # comma-separated
    hotel_category = Column(Integer)
    pickup_location = Column(String(100))
    drop_location = Column(String(100))
    days = Column(Integer)
    nights = Column(Integer)
    meta_tags = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    pricing_model = Column(String(50))  # "fixed" or "custom"
    highlights = Column(Text)
    inclusions = Column(Text)
    exclusions = Column(Text)
    faqs = Column(Text)
    terms = Column(Text)
    privacy_policy = Column(Text)
    payment_terms = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="trip", cascade="all, delete-orphan")
    media = relationship("TripMedia", uselist=False, back_populates="trip", cascade="all, delete-orphan")
    pricing = relationship("TripPricing", uselist=False, back_populates="trip", cascade="all, delete-orphan")
    policies = relationship("TripPolicy", back_populates="trip", cascade="all, delete-orphan")

# -------------------- Itinerary --------------------

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    day_number = Column(Integer)
    title = Column(String(255))
    description = Column(Text)
    image_urls = Column(Text)  # comma-separated
    activities = Column(Text)  # comma-separated
    hotel_name = Column(String(255))
    meal_plan = Column(Text)   # comma-separated
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    trip = relationship("Trip", back_populates="itinerary")

# -------------------- Media --------------------

class TripMedia(Base):
    __tablename__ = "trip_media"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    hero_image_url = Column(String(255))
    thumbnail_url = Column(String(255))
    gallery_urls = Column(Text)  # comma-separated
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    trip = relationship("Trip", back_populates="media")

# -------------------- Pricing --------------------

class TripPricing(Base):
    __tablename__ = "trip_pricing"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    pricing_model = Column(String(50))  # "fixed" or "custom"
    data = Column(Text)  # JSON string for slots or custom pricing
    created_at = Column(DateTime, default=datetime.now)

    trip = relationship("Trip", back_populates="pricing")

# -------------------- Policies --------------------

class TripPolicy(Base):
    __tablename__ = "trip_policies"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    title = Column(String(255))
    content = Column(Text)

    trip = relationship("Trip", back_populates="policies")