# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as _Session, declarative_base
from fastapi import Request
from contextvars import ContextVar
import pymysql
import os

pymysql.install_as_MySQLdb()

# --- Database Configuration (same as your current logic) ---
DB_USER = "root"
DB_PASS = "examplepassword"
DB_PORT = "3306"
DB_NAME = "travelcrm"

try:
    # Detect Docker
    is_docker = os.path.exists('/.dockerenv')

    if is_docker:
        DB_HOST = "db"
    else:
        DB_HOST = "72.60.202.179"

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing or empty")

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={'connect_timeout': 10}
    )

except Exception as e:
    print(f"❌ Failed to initialize database engine: {e}")
    engine = None

Base = declarative_base()

# Store tenant user_id for current request
current_request_user_id: ContextVar[int | None] = ContextVar("current_request_user_id", default=None)


# ---------------------------
# 🚀 Custom TenantSession
# ---------------------------
class TenantSession(_Session):
    """
    Custom SQLAlchemy Session that:
      - Auto-fills instance.user_id on add()
      - Auto-filters queries by user_id for single-model queries
    """
    def add(self, instance, _warn=True):
        try:
            uid = self.info.get("user_id")

            if uid is None:
                uid = current_request_user_id.get(None)

            if uid is not None and hasattr(instance, "user_id"):
                if getattr(instance, "user_id", None) in (None, 0):
                    setattr(instance, "user_id", uid)

        except Exception:
            pass

        return super().add(instance, _warn=_warn)

    def query(self, *entities, **kwargs):
        q = super().query(*entities, **kwargs)

        try:
            if len(entities) == 1:
                try:
                    model_class = q._entity_zero().class_
                except Exception:
                    model_class = None

                if model_class is not None and hasattr(model_class, "user_id"):
                    uid = self.info.get("user_id") or current_request_user_id.get(None)

                    if uid is not None:
                        q = q.filter(model_class.user_id == uid)

        except Exception:
            pass

        return q


# ---------------------------
# Session Factory
# ---------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=TenantSession
)


# ---------------------------
# 🚀 Main DB Dependency
# ---------------------------
def get_db(request: Request):
    if SessionLocal is None:
        raise RuntimeError("Database session is not initialized")

    db = SessionLocal()
    try:
        uid = getattr(request.state, "user_id", None)

        db.info["user_id"] = uid
        current_request_user_id.set(uid)

        yield db

    finally:
        current_request_user_id.set(None)
        db.close()
