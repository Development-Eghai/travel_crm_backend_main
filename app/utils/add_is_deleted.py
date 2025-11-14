from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import Column, Boolean
from core.database import Base

def add_is_deleted_to_all_models():
    """
    Auto-add is_deleted column to all SQLAlchemy models (SQLAlchemy 2.0 compatible).
    """
    for mapper in Base.registry.mappers:
        cls = mapper.class_

        if isinstance(cls, type) and issubclass(cls, Base):
            # If the model does NOT have is_deleted -> add it
            if not hasattr(cls, "is_deleted"):
                setattr(cls, "is_deleted", Column(Boolean, default=False))

    print("✔ Global soft-delete column patched into all models.")
