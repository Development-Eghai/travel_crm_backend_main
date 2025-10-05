from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

class Settings:
    try:
        APP_NAME = os.getenv("APP_NAME", "TravelCRM")
        APP_ENV = os.getenv("APP_ENV", "development")
        APP_PORT = int(os.getenv("APP_PORT", 8000))

        MYSQL_USER = os.getenv("MYSQL_USER")
        MYSQL_PASSWORD_RAW = os.getenv("MYSQL_PASSWORD")
        MYSQL_PASSWORD = quote_plus(MYSQL_PASSWORD_RAW) if MYSQL_PASSWORD_RAW else ""
        MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
        MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
        MYSQL_DB = os.getenv("MYSQL_DB")

        if not all([MYSQL_USER, MYSQL_PASSWORD_RAW, MYSQL_DB]):
            raise ValueError("Missing required MySQL environment variables")

        SQLALCHEMY_DATABASE_URL = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        )

        print(f"✅ Database URL: {SQLALCHEMY_DATABASE_URL}")  # Debugging line

    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        SQLALCHEMY_DATABASE_URL = None  # Fallback to avoid breaking imports

settings = Settings()
