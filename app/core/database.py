from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from urllib.parse import quote_plus
import os
import pymysql

pymysql.install_as_MySQLdb()

# ✅ Safe environment loading and engine creation
try:
    password = quote_plus("utsWPdbeqUHFGnFVlZohvRXDdmePdeMG")  # becomes 'PixelAdvant%40123'

    # DATABASE_URL = f"mysql://root:utsWPdbeqUHFGnFVlZohvRXDdmePdeMG@turntable.proxy.rlwy.net:31471/railway"

    DATABASE_URL = f"mysql://root:PixelAdvant%40123@localhost:3306/travel_crm"


    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing or empty")

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    print(f"✅ Database engine initialized with URL: {DATABASE_URL}")

except Exception as e:
    print(f"❌ Failed to initialize database engine: {e}")
    engine = None
    SessionLocal = None
    Base = declarative_base()  # Still define Base to avoid model import errors

# ✅ Dependency for DB session
def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database session is not initialized")
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()