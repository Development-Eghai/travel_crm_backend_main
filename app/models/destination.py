from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from models.trip import Trip  # ✅ Import Trip model

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer) 
    title = Column(String(100), nullable=False)
    subtitle = Column(String(255))
    destination_type = Column(String(50))  # Domestic / International
    primary_destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=True)
    slug = Column(String(255), unique=True, index=True)
    overview = Column(Text)
    travel_guidelines = Column(Text)
    hero_banner_images = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    primary = relationship("Destination", remote_side=[id])
    trips = relationship("DestinationTrip", cascade="all, delete-orphan", back_populates="destination")
    custom_packages = relationship("CustomPackage", cascade="all, delete-orphan", back_populates="destination")
    blogs = relationship("DestinationBlog", cascade="all, delete-orphan", back_populates="destination")
    activities = relationship("DestinationActivity", cascade="all, delete-orphan", back_populates="destination")
    testimonials = relationship("DestinationTestimonial", cascade="all, delete-orphan", back_populates="destination")
    blog_categories = relationship("DestinationBlogCategory", cascade="all, delete-orphan", back_populates="destination")


class DestinationTrip(Base):
    __tablename__ = "destination_trips"

    id = Column(Integer, primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))  # ✅ FK to Trip

    destination = relationship("Destination", back_populates="trips")
    trip = relationship("Trip")  # ✅ Enables .trip access


class CustomPackage(Base):
    __tablename__ = "custom_packages"

    id = Column(Integer, primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    title = Column(String(255))
    description = Column(Text)

    destination = relationship("Destination", back_populates="custom_packages")
    trips = relationship("CustomPackageTrip", cascade="all, delete-orphan", back_populates="package")


class CustomPackageTrip(Base):
    __tablename__ = "custom_package_trips"

    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("custom_packages.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))  # ✅ FK to Trip

    package = relationship("CustomPackage", back_populates="trips")
    trip = relationship("Trip")  # ✅ Enables .trip access


class DestinationBlog(Base):
    __tablename__ = "destination_blogs"

    id = Column(Integer, primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    blog_id = Column(Integer)
    featured = Column(Boolean, default=False)

    destination = relationship("Destination", back_populates="blogs")


class DestinationActivity(Base):
    __tablename__ = "destination_activities"

    id = Column(Integer, primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    activity_id = Column(Integer)

    destination = relationship("Destination", back_populates="activities")


class DestinationTestimonial(Base):
    __tablename__ = "destination_testimonials"

    id = Column(Integer, primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    testimonial_id = Column(Integer)

    destination = relationship("Destination", back_populates="testimonials")


class DestinationBlogCategory(Base):
    __tablename__ = "destination_blog_categories"

    id = Column(Integer, primary_key=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    category_id = Column(Integer)

    destination = relationship("Destination", back_populates="blog_categories")