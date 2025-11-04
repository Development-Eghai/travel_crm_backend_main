from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from urllib.parse import quote_plus
import os
import pymysql

pymysql.install_as_MySQLdb()

# --- Database Configuration ---
# ⚠️ NOTE: These credentials MUST match those defined in your docker-compose.yml 'db' service
DB_USER = "root"
DB_PASS = "examplepassword" 
DB_PORT = "3306"
DB_NAME = "travelcrm"

try:
    # Check if running inside a Docker container
    # The /.dockerenv file is a reliable indicator of Docker execution
    is_docker = os.path.exists('/.dockerenv')
    
    if is_docker:
        # Running in Docker container (Deployment) - use the Docker service name
        # The 'db' service is resolvable within the internal Docker network.
        DB_HOST = "db"
    else:
        # Running locally (uvicorn --reload) - use localhost
        # This connects to the 'db' container via the port 3306 mapped to the host machine.
        DB_HOST = "72.60.202.179"

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing or empty")

    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True, 
        connect_args={'connect_timeout': 10}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    print(f"✅ Database engine initialized for host: {DB_HOST}")

except Exception as e:
    print(f"❌ Failed to initialize database engine: {e}")
    engine = None
    SessionLocal = None
    Base = declarative_base()

# ✅ Dependency for DB session
def get_db():
    if SessionLocal is None:
        # This occurs if the connection failed in the try/except block
        raise RuntimeError("Database session is not initialized")
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()